from os import path
from os.path import join
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(join(here, 'requirements.txt')) as f:
    required = f.read().splitlines()

setup(
    name='ac-sensitive-data',
    version="1.0.0",
    packages=find_packages(),
    description='Find sensitive data in HTTP Request / Response',
    install_requires=required,
    include_package_data=True,
    zip_safe=True,
    url='https://github.com/bbva/apicheck',
    license='Apache 2.0',
    author='BBVA Labs',
    entry_points={'console_scripts': [
        'ac-sensitive = ac_sensitive_data.__main__:main'
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

