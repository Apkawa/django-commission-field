# Contributing

## Run example app

```bash
pip install -r requirements-dev.txt
./test/manage.py migrate
./test/manage.py runserver
```

## Run tests

```bash
pip install -r requirements-dev.txt
pytest
tox
```

## Build docs

```bash
python setup.py build_sphinx
```

## Bump version

```bash
python setup.py bumpversion
```

## Publish pypi

```bash
python setup.py publish
```

