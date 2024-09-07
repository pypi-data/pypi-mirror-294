# asm_api_lib

`asm_api_lib` is a Python library serving as a proof of concept to promote greater code reuse across ASM scanners. This library contains a class for interacting with the ASM API. Other code for logging and testing across scanners can be added in the future.


This library was created by following these directions: https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f 

I installed the library to PyPi using instructions here: https://www.turing.com/kb/how-to-create-pypi-packages#pypi:-a-pillar-for-python-projects 

## Publishing to PyPi
Note that right now the library is scoped to only John Cloeter's PyPi api token, but this can be changed in the future.

To upload new library using twine:
1. Setup PyPi api token locally using: 
  `nano ~/.pypirc`
2. Inside of `.pypirc` set this data (keep username as "__token__"):
  [pypi]
  username = __token__
  password = your-pypi-token
3. In `setup.py`, increment the next release value to a new number
4. Run: `python setup.py sdist` 
5. Delete older version of the distribution inside `/dist`
6. Run: `twine upload dist/*`
7. Rebuild any scanner container relying on this library
