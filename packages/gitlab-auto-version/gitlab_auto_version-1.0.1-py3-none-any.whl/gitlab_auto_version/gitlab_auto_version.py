import subprocess
import re
import os
import argparse
import configparser

def get_current_version():
    """Retrieves the current version from Git tags."""

    try:
        result = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                check=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if "fatal: No names found, cannot describe anything" in e.stderr:
            return '0.0.0'  # If no tags exist
        else:
            raise RuntimeError(f"Error getting current version: {e.stderr}")

def get_branch_name():
    """Retrieves the current branch name from GitLab CI environment variables."""

    branch_name = os.getenv('CI_COMMIT_REF_NAME')
    if not branch_name:
        raise ValueError("Environment variable CI_COMMIT_REF_NAME is not set.")
    return branch_name

def bump_version(version, part):
    """Bumps the specified part of the version number."""

    major, minor, patch = map(int, version.split('.'))
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

    try:
        subprocess.run(['git', 'rev-parse', tag],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def create_tag(version, tag_name=None):
    """Creates and pushes a Git tag."""

    branch_name = get_branch_name()
    if not tag_name:
        tag_name = f"{version}-{branch_name}"

    try:
        subprocess.run(['git', 'tag', tag_name], check=True)

        # Get the Deploy Token from the environment variable
        deploy_token = os.getenv('DEPLOY_TOKEN')
        if not deploy_token:
            raise ValueError("Environment variable DEPLOY_TOKEN is not set.")

        # Configure Git to use the Deploy Token for authentication
        subprocess.run(['git', 'config', 'credential.helper', f'store --file=.git/credentials'], check=True)
        with open('.git/credentials', 'w') as f:
            f.write(f'https://oauth2:{deploy_token}@{os.getenv("CI_SERVER_HOST")}')

        # Push the tag
        subprocess.run(['git', 'push', 'origin', tag_name], check=True)

        print(f"Tag created and pushed: {tag_name}")
        return tag_name
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error creating or pushing tag: {e.stderr}")


def get_commit_message():
    """Retrieves the commit message of the latest commit."""

    try:
        result = subprocess.run(['git', 'log', '-1', '--pretty=%B'],
                                stdout=subprocess.PIPE, check=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error getting commit message: {e.stderr}")

def determine_new_version(current_version, commit_message):
    """Determines the new version based on the commit message."""

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

    os.environ[env_var_name] = created_tag
    print(f"{env_var_name} set to: {created_tag}")

    try:
        with open(env_file_path, 'w') as env_file:
            env_file.write(f"{env_var_name}={created_tag}\n")
    except OSError as e:
        print(f"Warning: Error writing to environment file: {e}")

def load_config(config_file_path='.gitlab-ci.yml'):
    """Loads configuration from GitLab CI YAML file."""

    try:
        with open(config_file_path, 'r') as f:
            config_content = f.read()

        # Extract relevant configuration using regular expressions or YAML parsing library
        tag_name_match = re.search(r'tag_name:\s*([\w.-]+)', config_content)
        env_var_name_match = re.search(r'env_var_name:\s*([\w.-]+)', config_content)
        env_file_path_match = re.search(r'env_file_path:\s*([\w./-]+)', config_content)

        tag_name = tag_name_match.group(1) if tag_name_match else None
        env_var_name = env_var_name_match.group(1) if env_var_name_match else 'BUILD_VERSION'
        env_file_path = env_file_path_match.group(1) if env_file_path_match else 'build_version.env'

        return tag_name, env_var_name, env_file_path

    except FileNotFoundError:
        print(f"Warning: Configuration file '{config_file_path}' not found. Using default values.")
        return None, 'BUILD_VERSION', 'build_version.env'

def main():
    parser = argparse.ArgumentParser(description="Automate version bumping and Git tag creation for GitLab CI.")
    parser.add_argument('--tag-name', help="Custom tag name (optional)")
    parser.add_argument('--env-var-name', help="Environment variable name (default: BUILD_VERSION)")
    parser.add_argument('--env-file-path', help="Environment file path (default: build_version.env)")

    # Remove unrecognized arguments
    known_args, _ = parser.parse_known_args()

    if not any([known_args.tag_name, known_args.env_var_name, known_args.env_file_path]):
        tag_name, env_var_name, env_file_path = load_config()
    else:
        tag_name = known_args.tag_name
        env_var_name = known_args.env_var_name or 'BUILD_VERSION'
        env_file_path = known_args.env_file_path or 'build_version.env'

    current_version = get_current_version()
    commit_message = get_commit_message()

    new_version = determine_new_version(current_version, commit_message)
    created_tag = create_tag(new_version, tag_name)
    set_build_version(created_tag, env_var_name, env_file_path)

if __name__ == "__main__":
    main()