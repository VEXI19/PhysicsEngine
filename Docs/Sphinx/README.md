# Creating documentation with Sphinx

## 1. Build .rst files from docstrings

While in the root directory of the project, run the following command to build .rst files from docstrings in the code.

```bash
sphinx-apidoc -o Docs/Sphinx/source/ PhyscisEngine/
```

## 2. Build html files from .rst files

Go to the `Docs/Sphinx` directory and run the following command to build html files from the .rst files. 

```bash
cd Docs/Sphinx
make html
```
