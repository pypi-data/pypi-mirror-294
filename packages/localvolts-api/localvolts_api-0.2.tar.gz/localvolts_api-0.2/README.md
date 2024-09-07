# localvolts

This project is not ready for use yet. It is a work in progress.

## Tagging a new version

First update setup.py with the new version number. Then run the following command:

```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

Also tag the release via a git tag and push it to the repository:

```bash
git tag -a v0.1.0 -m "Release 0.1.0"
git push origin v0.1.0
```