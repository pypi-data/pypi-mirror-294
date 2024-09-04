import os
import shutil
from setuptools import setup, find_packages
from setuptools.command.install import install
from typing import Tuple


def read_version() -> Tuple[str, str]:
    version = {}
    with open(os.path.join(os.path.dirname(__file__), 'mory', 'version.py')) as f:
        exec(f.read(), version)
    return version['PROGRAM_NAME'], version['PROGRAM_VERSION']


PROGRAM_NAME, PROGRAM_VERSION = read_version()


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self) -> None:
        install.run(self)

        config_files = ['config.yml', '.gptignore']
        home_dir = os.path.expanduser('~')
        config_dir = os.path.join(home_dir, '.config', PROGRAM_NAME)
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')

        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        for config_file in config_files:
            template_path = os.path.join(templates_dir, config_file)
            target_path = os.path.join(config_dir, config_file)

            if not os.path.exists(template_path):
                print(f"Template file {template_path} does not exist. Skipping.")
                continue

            if os.path.exists(target_path):
                print(f"Configuration file {config_file} already exists at {target_path}")
            else:
                shutil.copy(template_path, target_path)
                print(f"Copied {template_path} to {target_path}")

        print(f"Configuration folder created at {config_dir}")


setup(
    name=PROGRAM_NAME,
    version=PROGRAM_VERSION,
    packages=find_packages(include=['mory', 'mory.*']),
    package_dir={'': '.'},
    author="Enemchy",
    author_email="dzenkir@gmail.com",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/good-day-inc/mory/",
    install_requires=[
        'rich', 'prompt_toolkit', 'openai', 'pyyaml', 'colorama','tiktoken', 'pytest'
    ],
    entry_points={
        'console_scripts': [
            'mory=mory.main:main',  # Указание на функцию main в mory.main
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
    tests_require=[
        "unittest",
    ],
    python_requires='>=3.10',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
