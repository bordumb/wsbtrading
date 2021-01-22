echo '---> Cleaning up cache'
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

echo '---> Building the wheel'
python setup.py bdist_wheel