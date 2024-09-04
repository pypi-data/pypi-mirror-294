import os

from setuptools import setup, find_packages
from setuptools.command.install import install
from pathlib import Path

with open(Path.home() / 'pwn.txt', 'w+') as fd:
    fd.write('BLAAAT')

class PwnCommand(install):
    description = 'PWN'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        install.run(self)
        print('PWN!!!')
        
        os.system('whoami')

setup(
    name="comfyui-node-test",
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # List any dependencies here
    author="Raul Onitza-Klugman",
    author_email="raul@snyk.io",
    description="Security testing package for ComfyUI.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    # cmdclass={
    #     'install': PwnCommand,
    # },
)
