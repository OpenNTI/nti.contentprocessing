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

import platform
py_impl = getattr(platform, 'python_implementation', lambda: None)
IS_PYPY = py_impl() == 'PyPy'

setup(
	name='nti.contentprocessing',
	version=VERSION,
	author='Jason Madden',
	author_email='jason@nextthought.com',
	description="NTI contentprocessing",
	long_description=codecs.open('README.rst', encoding='utf-8').read(),
	license='Proprietary',
	keywords='Content Processing',
	classifiers=[
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython'
	],
	packages=find_packages('src'),
	package_dir={'': 'src'},
	namespace_packages=['nti'],
	tests_require=TESTS_REQUIRE,
	install_requires=[
		'setuptools',
        'nltk',
        'numpy' if not IS_PYPY else '',
        'pyquery',
        'PyPDF2',
        'rdflib',
        'repoze.lru',
		'requests',
        'Whoosh',
        'zope.cachedescriptors',
		'zope.component',
		'zope.interface',
        'zope.location',
        'zope.mimetype',
		'zope.security',
        'zope.schema',
        'zopyx.txng3.ext' if not IS_PYPY else '',
		'nti.common',
		'nti.contentfragments',
		'nti.schema'
	],
	extras_require={
		'test': TESTS_REQUIRE,
	},
	dependency_links=[
		'git+https://github.com/NextThought/nti.schema.git#egg=nti.schema',
		'git+https://github.com/NextThought/nti.nose_traceback_info.git#egg=nti.nose_traceback_info'
	],
	entry_points=entry_points
)
