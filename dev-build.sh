echo '---> Cleaning up cache'
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
rm -r ./*.egg-info
rm -r ./build

echo '---> Removing the old wheel'
rm dist/*.whl

echo '---> Building the wheel'
python setup.py bdist_wheel dev-build