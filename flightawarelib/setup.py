from setuptools import setup

setup(
    name='flightaware',
    version='0.0.1',
    packages=['venv.Lib.distutils', 'venv.Lib.encodings', 'venv.Lib.importlib', 'venv.Lib.collections',
              'venv.Lib.site-packages.pip', 'venv.Lib.site-packages.pip.req', 'venv.Lib.site-packages.pip.vcs',
              'venv.Lib.site-packages.pip.utils', 'venv.Lib.site-packages.pip.compat',
              'venv.Lib.site-packages.pip.models', 'venv.Lib.site-packages.pip._vendor',
              'venv.Lib.site-packages.pip._vendor.distlib', 'venv.Lib.site-packages.pip._vendor.distlib._backport',
              'venv.Lib.site-packages.pip._vendor.colorama', 'venv.Lib.site-packages.pip._vendor.html5lib',
              'venv.Lib.site-packages.pip._vendor.html5lib._trie',
              'venv.Lib.site-packages.pip._vendor.html5lib.filters',
              'venv.Lib.site-packages.pip._vendor.html5lib.treewalkers',
              'venv.Lib.site-packages.pip._vendor.html5lib.treeadapters',
              'venv.Lib.site-packages.pip._vendor.html5lib.treebuilders', 'venv.Lib.site-packages.pip._vendor.lockfile',
              'venv.Lib.site-packages.pip._vendor.progress', 'venv.Lib.site-packages.pip._vendor.requests',
              'venv.Lib.site-packages.pip._vendor.requests.packages',
              'venv.Lib.site-packages.pip._vendor.requests.packages.chardet',
              'venv.Lib.site-packages.pip._vendor.requests.packages.urllib3',
              'venv.Lib.site-packages.pip._vendor.requests.packages.urllib3.util',
              'venv.Lib.site-packages.pip._vendor.requests.packages.urllib3.contrib',
              'venv.Lib.site-packages.pip._vendor.requests.packages.urllib3.packages',
              'venv.Lib.site-packages.pip._vendor.requests.packages.urllib3.packages.ssl_match_hostname',
              'venv.Lib.site-packages.pip._vendor.packaging', 'venv.Lib.site-packages.pip._vendor.cachecontrol',
              'venv.Lib.site-packages.pip._vendor.cachecontrol.caches',
              'venv.Lib.site-packages.pip._vendor.webencodings', 'venv.Lib.site-packages.pip._vendor.pkg_resources',
              'venv.Lib.site-packages.pip.commands', 'venv.Lib.site-packages.pip.operations',
              'venv.Lib.site-packages.idna', 'venv.Lib.site-packages.click', 'venv.Lib.site-packages.wheel',
              'venv.Lib.site-packages.wheel.tool', 'venv.Lib.site-packages.wheel.signatures',
              'venv.Lib.site-packages.dotenv', 'venv.Lib.site-packages.certifi', 'venv.Lib.site-packages.chardet',
              'venv.Lib.site-packages.chardet.cli', 'venv.Lib.site-packages.pymysql',
              'venv.Lib.site-packages.pymysql.tests', 'venv.Lib.site-packages.pymysql.tests.thirdparty',
              'venv.Lib.site-packages.pymysql.tests.thirdparty.test_MySQLdb',
              'venv.Lib.site-packages.pymysql.constants', 'venv.Lib.site-packages.urllib3',
              'venv.Lib.site-packages.urllib3.util', 'venv.Lib.site-packages.urllib3.contrib',
              'venv.Lib.site-packages.urllib3.contrib._securetransport', 'venv.Lib.site-packages.urllib3.packages',
              'venv.Lib.site-packages.urllib3.packages.backports',
              'venv.Lib.site-packages.urllib3.packages.ssl_match_hostname', 'venv.Lib.site-packages.requests',
              'venv.Lib.site-packages.setuptools', 'venv.Lib.site-packages.setuptools.extern',
              'venv.Lib.site-packages.setuptools.command', 'venv.Lib.site-packages.pkg_resources',
              'venv.Lib.site-packages.pkg_resources.extern', 'venv.Lib.site-packages.pkg_resources._vendor',
              'venv.Lib.site-packages.pkg_resources._vendor.packaging', 'noaametarlib', 'flightawarelib'],
    url='github.com/ahuimanu',
    license='GPL v3',
    author='jeff',
    author_email='ahuimanu@gmail.com',
    description='A wrapper for the FlightAware XML 2 API'
)
