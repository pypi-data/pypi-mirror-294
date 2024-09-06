from setuptools import setup, find_packages

setup(
    name='PradyumnaCustomeDatabse',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[],  # Add any external dependencies here
    description='A simple package for managing notes using a custom database with Python.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Pradyumna Aher',
    author_email='pradyumnaaher05@gmail.com',
    url='https://github.com/yourusername/notes_database',  # Your project repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
