# python_library

- Mac OS X
  - brew install python-setuptools
- python3 setup.py sdist bdist_wheel
- twine upload --repository testpypi dist/*
- twine upload dist/*

