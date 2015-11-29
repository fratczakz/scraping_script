import sys
import setuptools
from setuptools.command.test import test as TestCommand

import optimor


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        retcode = pytest.main(self.test_args)

        sys.exit(retcode)


setuptools.setup(
    name='optimor',
    version=optimor.__version__,
    tests_require=[
        'pytest',
    ],
    install_requires=[
        'setuptools',
        'selenium'
    ],
    cmdclass={
        'test': PyTest
    },
    author_email='fratczakz@gmail.com',
    description='Optimor scraping test',
    include_package_data=True,
    scripts=[
        'scripts/scrape_landline_from_o2.py'
    ],
    packages=setuptools.find_packages()
)
