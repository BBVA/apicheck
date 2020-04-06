from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

setup(
    name='apicheck-package-manager',
    version="1.0.0",
    packages=find_packages(),
    description='APICheck package manager',
    include_package_data=True,
    zip_safe=True,
    url='https://github.com/bbva/apicheck',
    license='Apache 2.0',
    author='BBVA Labs',
    entry_points={'console_scripts': [
        'acp = package_manager.__main__:main'
    ]},
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.8',
    ],
)

