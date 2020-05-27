import setuptools
from distutils.core import setup

setup(name='pycrunch-trace',
      version='0.1.0',
      description='PyCrunch Tracing Client',
      url='http://github.com/gleb-sevruk/pycrunch-trace',
      author='Gleb Sevruk',
      author_email='support@pycrunch.com',
      license='libpng',
      keywords="tracing live coding time travel debugging",
      packages=setuptools.find_packages(),
      download_url='https://github.com/gleb-sevruk/pycrunch-trace/archive/v0.1.0.tar.gz',
      setup_requires=['wheel'],
      install_requires=[
          'jsonpickle',
          'PyYAML',
          # 'protobuf==3.11.3'
      ],
      include_package_data=True,
      zip_safe=False)
