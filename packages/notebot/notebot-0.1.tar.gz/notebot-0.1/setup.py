from setuptools import setup, find_packages

# Read the content of README.md for the long description
with open('README.md', 'r', encoding='utf-8') as file:
    mdfile = file.read()

setup(
    name='notebot',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'note=note.note:main',
        ],
    },
    long_description=mdfile,
    long_description_content_type='text/markdown',
    author='Souporno Chakraborty',
    author_email='shrabanichakraborty83@gmail.com',
    description='A command-line tool to open Notepad or create and open files with Notepad.',
    license='MIT',
    keywords='notepad, file, command-line',
    url='https://github.com/Tirthaboss/notebot',  # Replace with your repository URL
)
