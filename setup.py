from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

exec(open('cloud_scanner/version.py').read())
setup(name='cloud_scanner',
      version=__version__,
      description='Core package for scanning cloud resources across providers',
      url='https://microsoft.github.io/cloud-scanner',
      author='Microsoft',
      author_email='cloudscanner@microsoft.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'python-dotenv',
          'pytest',
          'pytest-cov',
          'click'
      ])
