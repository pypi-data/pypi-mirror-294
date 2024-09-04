from setuptools import setup, find_packages

setup(
    name='nbxmssql',
    version='0.1.1',
    packages=find_packages(),
    install_requires=['pyodbc',],  # List your package's dependencies here
    author='Luuk Laarveld',
    author_email='l.laarveld@nubix.nl',
    description='used to connect to an MSSQL db',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_package',  # project URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
