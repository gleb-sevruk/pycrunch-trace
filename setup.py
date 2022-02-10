import setuptools
from distutils.core import setup

setup(name='pycrunch-trace',
      version='0.2',
      description='PyCrunch Time Travel Debugger',
      url='https://pytrace.com/',
      author='Gleb Sevruk',
      author_email='gleb@pycrunch.com',
      license='MIT',
      keywords=[
          'tracing',
          'debugging',
          'time-travel debugging',
          'record-and-replay debugging',
          'live coding',
      ],
      packages=setuptools.find_packages(),
      setup_requires=['wheel', 'Cython'],
      install_requires=[
          'Cython',
          'jsonpickle',
          'PyYAML',
          'protobuf>=3.11.3',
          'jsonpickle',
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Debuggers',
      ],
      project_urls={
          'Source': 'https://github.com/gleb-sevruk/pycrunch-trace/',
          'Funding': 'https://pycrunch.com/donate',
      },
      include_package_data=True,
      zip_safe=False)
