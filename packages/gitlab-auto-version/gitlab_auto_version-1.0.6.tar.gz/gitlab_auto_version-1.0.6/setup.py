from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gitlab-auto-version",
    version="1.0.6",
    author="Moshe Eliya",
    author_email="mosiko1234@gmail.com",
    description="A package to automate version bumping and Git tagging in GitLab CI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mosiko1234/gitlab-auto-version",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'configparser',  # For parsing configuration files
        'PyYAML'         # For parsing .gitlab-ci.yml (if you choose to use YAML parsing)
    ],
    entry_points={
        'console_scripts': [
            'gitlab-auto-version = gitlab_auto_version:main',
        ],
    },
)