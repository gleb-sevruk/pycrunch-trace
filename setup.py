from setuptools import setup, find_packages

setup(name='pycrunch-trace',
      version='0.3',
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
      packages=find_packages(),
      install_requires=[
          "cython",
          "jsonpickle",
          "protobuf>=3.11.3,<4.0.0",
          "pyyaml",
          "setuptools>=80.10.2",
          "wheel>=0.46.3",
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
