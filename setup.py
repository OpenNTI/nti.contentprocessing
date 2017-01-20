import codecs
from setuptools import setup, find_packages

VERSION = '0.0.0'

entry_points = {
    'console_scripts': [
    ],
}

TESTS_REQUIRE = [
    'nose',
    'nose-timer',
    'nose-pudb',
    'nose-progressive',
    'nose2[coverage_plugin]',
    'pyhamcrest',
    'nti.nose_traceback_info',
    'nti.testing'
]

setup(
    name='nti.contentprocessing',
    version=VERSION,
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="NTI Content Processing",
    long_description=codecs.open('README.rst', encoding='utf-8').read(),
    license='Proprietary',
    keywords='Content Processing',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['nti'],
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'setuptools',
        'nltk',
        'numpy',
        'pyquery',
        'PyPDF2',
        'rdflib',
        'repoze.lru',
        'requests',
        'simplejson',
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
        'nti.contentfragments',
        'nti.property',
        'nti.schema'
    ],
    extras_require={
        'test': TESTS_REQUIRE,
    },
    dependency_links=[],
    entry_points=entry_points
)
