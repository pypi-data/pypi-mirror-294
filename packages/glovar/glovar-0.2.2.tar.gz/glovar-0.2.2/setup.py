from setuptools import setup, find_packages

setup(
    name='glovar', 
    version='0.2.2',
    packages=find_packages(), 
    description='A package for managing JSON-based global variables by file context.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PaceGG/Python-Global-vars-lib',
    author='PaceGG',
    author_email='yura3012004@gmail.com',
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', 
)
