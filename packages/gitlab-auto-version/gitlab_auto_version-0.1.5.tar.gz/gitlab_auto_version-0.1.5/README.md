Markdown
# gitlab-auto-version

[![PyPI version](https://badge.fury.io/py/gitlab-auto-version.svg)](https://badge.fury.io/py/gitlab-auto-version)

A Python package to automate version bumping and Git tag creation within a GitLab CI/CD pipeline.

## Features

* **Intelligent Version Bumping:**
    * Automatically bumps the major version if the commit message contains "bump major".
    * Automatically bumps the minor version if the commit message contains "bump minor".
    * Otherwise, bumps the patch version.
* **Unique Tag Generation:**
    * Ensures generated tags are unique by incrementing the patch version if necessary.
* **GitLab CI Integration:**
    * Retrieves the branch name from the `CI_COMMIT_REF_NAME` environment variable.
    * Pushes tags to the GitLab origin remote.
    * Optionally loads configuration from your `.gitlab-ci.yml` file.
* **Customizable:**
    * Allows you to specify a custom tag name, environment variable name, and environment file path through command-line arguments or configuration.

## Installation

```bash
pip install gitlab-auto-version

Usage

Basic Usage:

Include the script in your .gitlab-ci.yml file as a job:
YAML
bump_version:
  script:
    - gitlab-auto-version



Configuration (Optional):

You can customize the script's behavior by adding the following variables to your .gitlab-ci.yml file or providing them as command-line arguments:
tag_name: Custom tag name format (e.g., v{version}-{branch_name}).
env_var_name: Name of the environment variable to store the created tag (default: BUILD_VERSION).
env_file_path: Path to the file where the environment variable will be written (default: build_version.env).
Commit Messages:

To trigger a specific version bump, include one of the following keywords in your commit message:
bump major: Major version bump.
bump minor: Minor version bump.
No keyword: Patch version bump.
Example

If the current version is 1.2.3, the latest commit message contains "bump minor", and the branch is "develop", the script will:

Bump the version to 1.3.0.
Create and push a tag named 1.3.0-develop.
Set the BUILD_VERSION environment variable to 1.3.0-develop.
Notes

The script assumes that you are pushing tags to the origin remote.
If you encounter any issues, check the script's output for error messages.
For more advanced use cases or customization, you can modify the script directly.

**Key improvements in this `README.md`:**

* **Clearer structure:** The sections are well-organized with headings and subheadings.
* **Concise explanations:** The features and usage instructions are explained briefly and directly.
* **Code examples:** The YAML snippet and installation command provide concrete examples for users to follow.
* **Visual appeal:** The PyPI version badge adds a visual element and indicates the current version of the package.
