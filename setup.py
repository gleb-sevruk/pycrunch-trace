import setuptools
from distutils.core import setup

setup(name='pycrunch_tracer',
      version='0.9.0',
      description='PyCrunch Tracing Server and Client',
      url='http://github.com/gleb-sevruk/pycrunch-tracer',
      author='Gleb Sevruk',
      author_email='support@pycrunch.com',
      license='libpng',
      keywords="tracing live coding tdd unit-testing test runner",
      packages=setuptools.find_packages(),
      # download_url='https://github.com/gleb-sevruk/pycrunch-engine/archive/v0.9.0.tar.gz',
      setup_requires=['wheel'],
      entry_points={
          'console_scripts': ['pycrunch-trace-server=pycrunch_tracer.main:run'],
      },
      install_requires=[
          'python-socketio>=4',
          'aiohttp',
          'jsonpickle',
          'PyYAML',
          'protobuf==3.11.3'
      ],
      include_package_data=True,
      zip_safe=False)
