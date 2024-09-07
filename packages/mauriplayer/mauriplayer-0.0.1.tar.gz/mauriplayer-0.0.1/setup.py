import setuptools
from pathlib import Path

readme = Path('README.md').read_text()

setuptools.setup(name="mauriplayer", version="0.0.1", long_description=readme,
                 packages=setuptools.find_packages(exclude=["mocks", "tests"]))


# ahora vamos a publicar el paquete
# 1-primero compilamos
# python setup.py sdist bdist_wheel
# sdist -> source distribution
# bdist_wheel -> build distribution

# 2-subimos con twine
# twine upload dist/*
