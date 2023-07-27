# Building from Source

To build the package from source, follow these steps:

```
$ pip install -r requirements.txt
$ python setup.py sdist bdist_wheel
```

To test the package before uploading to PyPi:

```
$ python -m venv myenv
$ source myenv/bin/activate
$ pip install .
$ pystructurizr dev --view examples.module_example.chatsystem_containerview
$ deactivate
$ rm -fr myenv
```

# Deploying to PyPi
```
$ twine upload dist/*
```
