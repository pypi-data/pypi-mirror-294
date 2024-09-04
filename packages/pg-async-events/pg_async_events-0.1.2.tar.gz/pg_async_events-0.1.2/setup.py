from setuptools import setup, find_packages

setup(
    name='pg-async-events',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'asyncpg>=0.24.0',
    ],
    description='A simple async event handling library using PostgreSQL notifications.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/255BITS/pg-async-events',
    author='Martyn Garcia',
    author_email='martyn@255bits.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
