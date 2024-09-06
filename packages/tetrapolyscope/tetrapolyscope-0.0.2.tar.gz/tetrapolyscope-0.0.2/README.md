# polyscope-py
Python bindings for Polyscope - Chromalab Version. https://polyscope.run/py


This library is a python wrapper and deployment system. The core library lives at [this polyscope fork](https://github.com/i-geng/polyscope)

To contribute, check out the [instructions here](https://polyscope.run/about/contributing/).

### Installation (for now before Irene puts it on PyPI)

Uninstall current version of polyscope from current virtual environment:
```
pip uninstall polyscope
```

Local installation. Haven't put this version on PyPI yet, since it seems like uploading a 
new version could take over an hour. 
```
git clone --recurse-submodules git@github.com:i-geng/polyscope-py.git
```

From the root polyscope-py directory, build the C++ source:
```
mkdir build; cd build
cmake ../
make -j4
```
Back in the root polyscope-py directory:
```
pip install .
```

To use polyscope's functions for writing videos, you will also need FFmpeg.
