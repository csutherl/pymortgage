__author__ = 'coty'

from setuptools import setup, find_packages
import pymortgage
from setuptools.command.test import test as TestCommand
import sys

class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)

setup(
    name='pymortgage',
    version=pymortgage.__version__,
    url='http://github.com/csutherl/pymortgage',
    license='Apache LICENSE Version 2.0',
    description='Application to chart mortgage and other loan data.',
    author='Coty Sutherland',
    packages=find_packages(),
    install_requires=[
        "CherryPy==3.2.4",
        "pip==1.2.1",
        "setuptools==0.6c11",
        "wsgiref==0.1.2",
    ],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta'
        'Natural Language :: English',
    ],
    cmdclass = {'tox': Tox},
    test_suite='pymortgage.test'
)
