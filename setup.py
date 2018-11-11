from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name = 'Timeline2GUI',
    version = '0.1',
    description = 'GUI to import Timeline CSV file and to perform filter/search/highlight operations.',
    long_description = long_description,
    url='https://github.com/parvathycec/Timeline2GUI',
    author = 'Parvathy Mohan',
    dependency_links=['http://github.com/dmnfarrell/pandastable/tarball/master#egg=pandastable'],
    classifiers = ['Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Topic :: Software Development :: User Interfaces',
            'Intended Audience :: Science/Research'],
)
