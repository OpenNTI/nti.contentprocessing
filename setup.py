import codecs
from setuptools import setup, find_packages

import platform
py_impl = getattr(platform, 'python_implementation', lambda: None)
IS_PYPY = py_impl() == 'PyPy'

entry_points = {
    'console_scripts': [
    ],
}

TESTS_REQUIRE = [
    'nti.testing',
    'zope.testrunner',
]


def _read(fname):
    with codecs.open(fname, encoding='utf-8') as f:
        return f.read()


setup(
    name='nti.contentprocessing',
    version=_read('version.txt').strip(),
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="NTI content processing",
    long_description=(_read('README.rst')  + '\n\n' + _read('CHANGES.rst')),
    license='Apache',
    keywords='ZODB',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    zip_safe=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    namespace_packages=['nti'],
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'setuptools',
        'nltk' if not IS_PYPY else '',
        'nti.contentfragments',
        'nti.property',
        'nti.schema',
        'numpy' if not IS_PYPY else '',
        'pyquery',
        'PyPDF2',
        'rdflib',
        'repoze.lru',
        'requests',
        'six',
        'watson-developer-cloud',
        'Whoosh',
        'zope.cachedescriptors',
        'zope.component',
        'zope.deprecation',
        'zope.interface',
        'zope.location',
        'zope.mimetype',
        'zope.security',
        'zope.schema',
        'zopyx.txng3.ext',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
    },
    entry_points=entry_points,
    test_suite="nti.contentprocessing.tests",
)
