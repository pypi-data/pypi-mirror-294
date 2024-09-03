from setuptools import setup, find_packages, Command

from setuptools import setup, Command

class PwnCommand(Command):
    description = 'PWN'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print('PWN!!!')
        
        import os
        os.system('whoami')

setup(
    name="comfyui-node-pkg",
    version="0.2",
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
    cmdclass={
        'pwn_command': PwnCommand,
    },
)
