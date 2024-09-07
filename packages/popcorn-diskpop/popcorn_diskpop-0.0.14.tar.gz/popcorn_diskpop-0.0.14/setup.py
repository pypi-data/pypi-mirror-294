from setuptools import find_packages, setup

setup(
    name = 'popcorn_diskpop',
    version = '0.0.14',
    description = 'Popcorn - tool to analyse Diskpop output',
    author = 'Alice Somigliana, Claudia Toci, Giovanni Rosotti',
    author_email= 'alice.somigliana@eso.org',
    url = 'https://bitbucket.org/diskpopteam/diskpop/src/master/',
    license = 'GPL',
    packages = find_packages(),
    install_requires=["numpy==1.21", "pandas"],
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest==4.4.1'],
    test_suite = 'tests',
    long_description = open("README.rst").read(),
)

print("Please make sure you have installed Diskpop (https://bitbucket.org/diskpopteam/diskpop/src/master/): popcorn won't work otherwise!")
