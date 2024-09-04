from setuptools import setup, find_packages

setup(
    name='react-component-generator',
    version='0.1.0',
    description='A CLI tool for generating React components',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Damian Ledesma',
    author_email='DamianLedesma@protonmail.com',
    url='https://github.com/pylds/react-component-generator',
    packages=find_packages(),
    install_requires=[
        'rich>=13.0.0',
        'typer',
    ],
    entry_points={
        'console_scripts': [
            'react-component-generator = react_component_generator.cli:cli',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
