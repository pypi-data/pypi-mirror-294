from setuptools import setup

setup(
    name = 'windcomponents',
    version = '0.2',
    # change this with update of lib
    description = 'A library for calculating aircraft crosswind and tailwind components on a runway',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    author = 'Sebastiaan Menger',
    author_email = 's.menger001@gmail.com',
    py_modules = ['windcomponents'],
    license = 'GPL-3.0',
    classifiers = [
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires = '>=3.6',
)
