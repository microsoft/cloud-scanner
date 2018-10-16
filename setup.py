from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='cloud_scanner',
      version='0.0.1',
      description='Core package for scanning cloud resources across providers',
      url='https://github.com/Microsoft/cloud-scanner',
      author='Microsoft',
      author_email='tanner.barlow@microsoft.com,wallace.breza@microsoft.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'python-dotenv',
          'pytest',
          'pytest-cov',
          'click'
      ])
