import setuptools
from distutils.core import setup

setup(name='pycrunch-trace',
      version='0.1.4',
      description='PyCrunch Time Travel Debugger',
      url='http://github.com/gleb-sevruk/pycrunch-trace',
      author='Gleb Sevruk',
      author_email='gleb@pycrunch.com',
      license='libpng',
      keywords="tracing time travel debugging live coding",
      packages=setuptools.find_packages(),
      download_url='https://github.com/gleb-sevruk/pycrunch-trace/archive/v0.1.0.tar.gz',
      setup_requires=['wheel', 'Cython'],
      install_requires=[
          'Cython',
          'jsonpickle',
          'PyYAML',
          'protobuf==3.11.3'
      ],
      include_package_data=True,
      zip_safe=False)
