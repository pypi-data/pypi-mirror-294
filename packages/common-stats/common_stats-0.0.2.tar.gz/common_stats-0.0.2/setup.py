from setuptools import setup, find_packages

setup(
    name='common_stats',
    version='0.0.2',
    description='A simple library for basic statistical calculations',
    long_description=open('USAGE.md').read(),
    long_description_content_type='text/markdown',
    author='Paras Arora',
    author_email='parasaroraee@gmail.com',
    packages=find_packages(),
    install_requires=[
        "pytest"
    ],
    license='MIT',
    python_requires='>=3.7',
)