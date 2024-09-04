# Repository Scan Project

## Overview

The Repository Scan Project is a Python package that is used to scan repositories from a repo list in CSV and a config file in JSON and extract to apis in CSV/XLSX format and api summaries in JSON format. It also provides many useful methods in Helper class.

### Project Structure

The project is organized as follows:

- **build/**: Library dependencies in Deploy phase
- **dist/**: Deploy files in Deploy phase
  - `reposcan-x.y-py3-non-any.whl`
  - `reposcan-x.y.tar.gz`
- **reposcan/**: Source code in Analyse/Design/Develop phase
  - `__init__.py`: Initializes the `calculator` package.
  - `reposcan.py`: Contains the `RepoScan` class with basic
  - **exporters/**
    - `__init__.py`: Initializes the `exporters` subpackage.
    - `FileExporter.py`: Contains the `FileExporter` class with FileExporter.
    - `CSVExporter.py`: Contains the `CSVExporter` class with CSVExporter.
    - `XLSXExporter.py`: Contains the `XLSXExporter` class with XLSXExporter.
  - **helpers/**
    - `__init__.py`: Initializes the `helpers` subpackage.
    - `Helper.py`: Contains the `Helper` class with Helper.
  - **models/**
    - `__init__.py`: Initializes the `models` subpackage.
    - `APIInfo.py`: Contains the `APIInfo` class with APIInfo.
    - `RepoInfo.py`: Contains the `RepoInfo` class with Helper.
  - **scanners/**
    - `__init__.py`: Initializes the `exporters` subpackage.
    - `FileScanner.py`: Contains the `FileScanner` class with FileScanner.
    - `CSharpScanner.py`: Contains the `CSharpScanner` class with CSharpScanner.
    - `JavaScanner.py`: Contains the `JavaScanner` class with JavaScanner.
    - `PythonScanner.py`: Contains the `PythonScanner` class with PythonScanner.
- **tests/**: Test cases in Test phase
  - `__init__.py`: Initializes the `tests` package.
  - `testHelper.py`: Contains unit tests for the `Helper` class.
  - `flask_python.py`: Contains unit tests for the `Flask Python` repository.
- **data/**: Data in Test phase
  - `config.json`: Input the `config` list.
  - `repo.csv`: Input the `repository` list.
  - `api.csv`: Output the `api` list.
  - `apiSummary.json`: Output the `api summary` list.
- **logs/**: Logs in Test phase
  - `140501_03092024_reposcan.log`: Log `Repo Scan` at 14:05:01 03/09/2024.
  - `180808_03092024_reposcan.log`: Log `Repo Scan` at 18:08:08 03/09/2024.

## Process Overview

### 1. Analyze
- **Requirement Gathering**:
  - Read config from the config file `configFilePath`
  - Write app log to the log file `logFilePath`
  - Add api infos from the repo file `repoFilePath`
  - Export api infos to the api file `apiFilePath`
  - Write api summary infos to the api summary file `apiSummaryFilePath`
- **Feasibility Study**: Assess if Python and its libraries can meet the project requirements.

### 2. Design
- **Architecture Design**:
  - A main package `reposcan`
  - Some subpackages `exporters`, `scanners`, `helpers`, `models`, `logs`, `tests`, `data`, `repos`
- **Class Design**:
  - Define the `RepoSan` class for the main operations
  - Define many `exporters` to export to CSV, XLSX files
  - Define many `scanners` to scan from Python, CSharp, Java, ... repositories
  - Define `logs` to keep log infos
  - Define `data` to keep input files, output files
  - Define `repos` to keep repositories locally

### 3. Develop
- **Source Code Server Management**: Ensure the synchronization between local code and remote code
```
git clone https://github.com/SingularityDevOps/api-governance.git
cd api-governance
git pull origin main --rebase
git add .
git push -f
``` 
### 4. Deploy
- **Package Server Configuration ~/.pypirc**: Generate API token by `pypi.org` then add it into `~/.pyirc` like the below
```
[distutils]
index-servers =
    pypi

[pypi]
  username = __token__
  password = pypi-AgEIcHlwaS5vcmcCJGRhODVlMjkyLWE3ZTYtNGRiZi1iN2I3LTU1MGRhOTQ1MGYzNgACKlszLCJkY2M1NmVjZS05MzNiLTRmZWItYmNmOC01MjFjOWZlNzM0M2UiXQAABiCaZaEx8f4l6HHs8SZeaZmMP9_2hT3Ze8rIO0_KvjVSpA
```
- **Packaging and uploading**: Ensure the project is structured correctly for distribution with `__init__.py` files. There will be two files: `reposcan-x.x-py3-non-any.whl`, and `reposcan-x.y.tar.gz` created in ./dist folder
```
py -3 setup.py sdist bdist_wheel
py -3 -m pip install twine
twine upload ./dist/*
```
- **Installation**: Clone the repository and install any required dependencies.
```
py -3 -m pip install ./dist/reposcan-x.x-py3-non-any.whl
py -3 -m pip install ./dist/reposcan-x.y.tar.gz
```
### 5. Test
- **UI Testing**: 
```
py -3 -m reposcan.reposcan
py -3 -m reposcan.reposcan .\\data\\config.json .\\data\\repo.csv .\\data\\api.csv .\\data\\apisummary.json
```
- **Unit Testing**: 
  - Write and run test cases for the `Helper` class in `testHelper.py`.
  - Write and run test cases for the `Flask Python` class in `flask_python.py` if necessary.
```
py -3 -m unittest tests/testHelper.py
py -3 -m unittest discover -s tests
```