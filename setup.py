from setuptools import setup, find_packages

setup(name='oceanalysis',
      version='0.1',
      description='Tools for analyzing ocean model output',
      url='https://github.com/reykboerner/oceanalysis',
      author='Reyk Börner',
      author_email='r.borner@uu.nl',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'xarray', 'gsw-xarray',
      ],
      zip_safe=False)