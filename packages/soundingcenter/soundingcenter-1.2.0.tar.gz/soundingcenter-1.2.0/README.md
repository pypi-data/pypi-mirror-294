# Sounding Center API

## Release

1. (once) `python -m pip install --upgrade pip build twine`
2. Bump Version in [pyproject.toml](pyproject.toml)
3. `python -m build`
4. `python -m twine upload dist/*`
5. (optional) `rm -r dist`
