# Coding Style
Please conform to [Chromium Python Style Guide](https://chromium.googlesource.com/chromium/src/+/master/styleguide/python/python.md)

## yapf
Please use [yapf](https://github.com/google/yapf/) to automatically format your code.

Usage:
```
pip install yapf
(if Python2: pip install futures)
(cd into the root directory containing README.md file)
yapf --in-place --recursive --parallel .
```

## pylint
All python code is required to pass [pylint](https://www.pylint.org/)

Usage:
```
pip install pylint
(cd into the root directory containing README.md file)
pylint {directory of Python files}
```
