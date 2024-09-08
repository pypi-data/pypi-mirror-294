from setuptools import setup, find_packages

setup(
    name='Configify_Wizard',
    version='0.1.1',
    author='Krishna Murthy Srinivasan',
    author_email='harikrishnachn@gmail.com',
    description='A configuration parser for YAML, CFG, and ENV files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/config_parser_module',  # Optional, URL of your project
    packages=find_packages(),  # Automatically find all packages
    install_requires=[
        'python-dotenv',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
