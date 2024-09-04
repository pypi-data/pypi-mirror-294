# Lyrasense Python SDK

This is the repository for the Python SDK that allows you to interface with the Lyrasense Earth Observation platform.

## Packaging Instructions

Make sure you have access to an API key to push in PyPI, ask <dimkirts@gmail.com> for one.
Make sure you have installed PyPA's build, and Twine:

```bash
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine
```

Then build your library by running in the root of the project directory:

```bash
python3 -m build
```

This should create two files in a `dist` folder that look like:

```txt
lyrasense-0.0.1.tar.gz
lyrasense-0.0.1-py3-none-any.whl
```

Now to push these files to PyPI:

```bash
python3 -m twine upload --repository pypi dist/*
```

You are good to go!

Reference: <https://packaging.python.org/en/latest/tutorials/packaging-projects/>

## Virtual Environment

We assume that you have Python installed on your system.

Create a fresh virtual environment:

```bash
rm -rf .venv
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
# confirm that you are in your venv
which python
```

To exit your venv:

```bash
deactivate
```

## Running locally on editable mode for testing

- Go to the root folder of the project
- Create a virtualenv and activate it
- Install the library in editable mode `pip install -e .`
- Now you can either execute the example, run or write unit tests

## Installing the library and running the example

First create and activate a virtualenv as mentioned above.
Then install the library inside the activated virtualenv like this:

```bash
pip install lyrasense
```

Then run the example like this:

```bash
python3 examples/example.py
```
