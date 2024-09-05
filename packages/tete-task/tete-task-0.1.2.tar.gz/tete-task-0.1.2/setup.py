from setuptools import setup, find_packages

setup(
    name='tete-task',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[],
    author='jancey',
    author_email='jancey.email@example.com',
    description='A simple Python module with a test function',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
