import subprocess
import re
import os
import argparse
import configparser


import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_tag_creation(tag_name: Optional[str]) -> None:
    """Logs a message indicating that a tag was created and pushed."""
    if tag_name is None:
        logger.warning("Tag name is null")
    else:
        logger.info(f"Tag created and pushed: {tag_name}")



def get_current_version():
    """Retrieves the current version from Git tags."""

    try:
        result = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                check=True,
                                text=True)
        if result is None:
            raise RuntimeError("Error getting current version: Null result.")

        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if e.stderr is None:
            raise RuntimeError("Error getting current version: Null stderr.")
        if "fatal: No names found, cannot describe anything" in e.stderr:
            return '0.0.0'  # If no tags exist
        else:
            raise RuntimeError(f"Error getting current version: {e.stderr}")

def get_branch_name():
    """Retrieves the current branch name from GitLab CI environment variables."""

    commit_ref_name = os.getenv('CI_COMMIT_REF_NAME')
    if commit_ref_name is None:
        raise ValueError("Environment variable CI_COMMIT_REF_NAME is not set.")
    elif not isinstance(commit_ref_name, str):
        raise ValueError("Environment variable CI_COMMIT_REF_NAME is not a string.")
    elif not commit_ref_name.strip():
        raise ValueError("Environment variable CI_COMMIT_REF_NAME is empty.")

    return commit_ref_name

def bump_version(version, part):
    """Bumps the specified part of the version number."""

    if not isinstance(version, str):
        raise TypeError(f"Expected a string for version, got {type(version).__name__} instead.")
    if not isinstance(part, str):
        raise TypeError(f"Expected a string for part, got {type(part).__name__} instead.")
    if part not in ['major', 'minor', 'patch']:
        raise ValueError(f"Expected 'major', 'minor', or 'patch' for part, got '{part}' instead.")

    try:
        major, minor, patch = map(int, version.split('.'))
    except ValueError:
        raise ValueError(f"Expected a version string of the format 'x.y.z', got '{version}' instead.")

    if part == 'major':
        major += 1
        minor = 0
        patch = 0
    elif part == 'minor':
        minor += 1
        patch = 0
    else:
        patch += 1

    return f"{major}.{minor}.{patch}"

def tag_exists(tag):
    """Checks if a Git tag with the given name already exists."""

    if not isinstance(tag, str):
        raise TypeError(f"Expected a string for tag, got {type(tag).__name__} instead.")

    try:
        subprocess.run(['git', 'rev-parse', tag],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       check=True)
        return True
    except subprocess.CalledProcessError as e:
        if e.returncode == 128 and "fatal: Needed a single revision" in e.stderr.decode():
            return False
        else:
            raise RuntimeError(f"Error checking if tag '{tag}' exists: {e.stderr}")

def create_tag(version, tag_name=None):
    gitlab_token = os.environ.get('GITLAB_TOKEN')
    if gitlab_token is None:
        raise ValueError("GitLab token is not set.")

    """Creates and pushes a Git tag."""

    if not version:
        raise ValueError("Version cannot be empty")

    if not tag_name:
        tag_name = f"{version}-{get_branch_name()}"

    try:
        subprocess.run(['git', 'tag', tag_name], check=True)

        deploy_token = os.getenv('DEPLOY_TOKEN')
        if not deploy_token:
            raise ValueError("Environment variable DEPLOY_TOKEN is not set.")

        ci_server_host = os.getenv('CI_SERVER_HOST')
        if not ci_server_host:
            raise ValueError("Environment variable CI_SERVER_HOST is not set.")

        ci_project_path = os.getenv('CI_PROJECT_PATH')
        if not ci_project_path:
            raise ValueError("Environment variable CI_PROJECT_PATH is not set.")

        # Configure Git to use the Deploy Token for authentication
        subprocess.run(['git', 'config', 'credential.helper', f'store --file=.git/credentials'], check=True)
        with open('.git/credentials', 'w') as f:
            f.write(f'https://oauth2:{deploy_token}@{ci_server_host}')
        remote_url = f"https://oauth2:{deploy_token}@{ci_server_host}/{ci_project_path}.git"
        # Push the tag
        subprocess.run(['git', 'push', remote_url, tag_name], env={'GITLAB_TOKEN': gitlab_token}, check=True)

        print(f"Tag created and pushed: {tag_name}")
        return tag_name
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error creating or pushing tag: {e.stderr}")


def get_commit_message():
    """Retrieves the commit message of the latest commit."""

    try:
        result = subprocess.run(['git', 'log', '-1', '--pretty=%B'],
                                stdout=subprocess.PIPE, check=True, text=True)
        if result is None:
            raise RuntimeError("Error getting commit message: Null result.")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if e.stderr is None:
            raise RuntimeError("Error getting commit message: Null stderr.")
        else:
            raise RuntimeError(f"Error getting commit message: {e.stderr}")

def determine_new_version(current_version, commit_message):
    """Determines the new version based on the commit message."""

    if current_version is None:
        raise ValueError("Current version is null.")

    if not isinstance(current_version, str):
        raise TypeError(f"Expected a string for current_version, got {type(current_version).__name__} instead.")

    if commit_message is None:
        raise ValueError("Commit message is null.")

    if not isinstance(commit_message, str):
        raise TypeError(f"Expected a string for commit_message, got {type(commit_message).__name__} instead.")

    if 'bump major' in commit_message.lower():
        new_version = bump_version(current_version, 'major')
    elif 'bump minor' in commit_message.lower():
        new_version = bump_version(current_version, 'minor')
    else:
        new_version = bump_version(current_version, 'patch')

    while tag_exists(new_version):
        new_version = bump_version(new_version, 'patch')

    return new_version

def set_build_version(created_tag, env_var_name, env_file_path):
    """Sets the build version environment variable and writes it to a file."""

    if created_tag is None:
        raise ValueError("Created tag is null.")

    if not isinstance(created_tag, str):
        raise TypeError(f"Expected a string for created_tag, got {type(created_tag).__name__} instead.")

    if not isinstance(env_var_name, str):
        raise TypeError(f"Expected a string for env_var_name, got {type(env_var_name).__name__} instead.")

    if not isinstance(env_file_path, str):
        raise TypeError(f"Expected a string for env_file_path, got {type(env_file_path).__name__} instead.")

    os.environ[env_var_name] = created_tag
    print(f"{env_var_name} set to: {created_tag}")

    try:
        with open(env_file_path, 'w') as env_file:
            env_file.write(f"{env_var_name}={created_tag}\n")
    except OSError as e:
        if e is None:
            raise RuntimeError("Error writing to environment file: Null exception.")
        else:
            print(f"Warning: Error writing to environment file: {e}")

def load_config(config_file_path='.gitlab-ci.yml'):
    """Loads configuration from GitLab CI YAML file."""

    if not config_file_path:
        raise ValueError("config_file_path is null.")

    if not isinstance(config_file_path, str):
        raise TypeError(f"Expected a string for config_file_path, got {type(config_file_path).__name__} instead.")

    try:
        with open(config_file_path, 'r') as f:
            config_content = f.read()

        # Extract relevant configuration using regular expressions or YAML parsing library
        tag_name_match = re.search(r'tag_name:\s*([\w.-]+)', config_content)
        env_var_name_match = re.search(r'env_var_name:\s*([\w.-]+)', config_content)
        env_file_path_match = re.search(r'env_file_path:\s*([\w./-]+)', config_content)

        if tag_name_match is None:
            tag_name = None
        else:
            tag_name = tag_name_match.group(1)

        if env_var_name_match is None:
            env_var_name = 'BUILD_VERSION'
        else:
            env_var_name = env_var_name_match.group(1)

        if env_file_path_match is None:
            env_file_path = 'build_version.env'
        else:
            env_file_path = env_file_path_match.group(1)

        return tag_name, env_var_name, env_file_path

    except FileNotFoundError:
        print(f"Warning: Configuration file '{config_file_path}' not found. Using default values.")
        return None, 'BUILD_VERSION', 'build_version.env'

def main():
    parser = argparse.ArgumentParser(description="Automate version bumping and Git tag creation for GitLab CI.")
    parser.add_argument('--tag-name', help="Custom tag name (optional)")
    parser.add_argument('--env-var-name', help="Environment variable name (default: BUILD_VERSION)")
    parser.add_argument('--env-file-path', help="Environment file path (default: build_version.env)")

    known_args, _ = parser.parse_known_args()

    if not any([known_args.tag_name, known_args.env_var_name, known_args.env_file_path]):
        tag_name, env_var_name, env_file_path = load_config()
    else:
        tag_name = known_args.tag_name
        env_var_name = known_args.env_var_name or 'BUILD_VERSION'
        env_file_path = known_args.env_file_path or 'build_version.env'

    if tag_name is None:
        raise ValueError("Tag name is null.")
    if env_var_name is None:
        raise ValueError("Environment variable name is null.")
    if env_file_path is None:
        raise ValueError("Environment file path is null.")

    current_version = get_current_version()
    if current_version is None:
        raise ValueError("Current version is null.")

    commit_message = get_commit_message()
    if commit_message is None:
        raise ValueError("Commit message is null.")

    new_version = determine_new_version(current_version, commit_message)
    if new_version is None:
        raise ValueError("New version is null.")

    created_tag = create_tag(new_version, tag_name)
    if created_tag is None:
        raise ValueError("Created tag is null.")

    set_build_version(created_tag, env_var_name, env_file_path)

if __name__ == "__main__":
    main()