python3 -m venv ulti
source ulti/bin/activate

python setup.py sdist bdist_wheel

pip install --upgrade setuptools wheel twine
pip install setuptools wheel


deactivate