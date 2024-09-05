# Prerequisites
python -m pip install --upgrade build
python -m pip install  --upgrade twine


# Build
python -m build


python  -m twine upload --repository testpypi dist/*


python  -m twine upload  dist/*

# Notes
You can also `pip install {path to .whl file}` to test the package.

