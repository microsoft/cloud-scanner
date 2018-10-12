from setuptools import setup, find_packages

setup(name='cloud_scanner',
      version='0.1',
      description='Core package for scanning cloud resources across providers',
      url='',
      author='Tanner Barlow',
      author_email='tanner.barlow12@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'python-dotenv',
          'pytest',
          'pytest-cov',
          'click'
      ])
