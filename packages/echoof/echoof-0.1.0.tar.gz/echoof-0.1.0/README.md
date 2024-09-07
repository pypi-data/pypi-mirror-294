# ECHOOF Development README

## Windows dependencies
### First, run CMD as administrator
```cmd
winget install -e --id=Python.Python.3.12
winget install -e --id=WiXToolset.WiXCLI
```
### Second, run cmd as regular user
```
pip install setuptools pyinstaller Cython
```

## Running ECHOOF from sources
```bash
python -m echoof.cli
```

## Running unit tests
ECHOOF comes with some basic unit tests for validating functionality.

### Run all tests
```bash
python -m unittest discover -s tests
```

## Generating configuration files for version release, i.e. 0.1.0
```bash
python generate_configuration.py 0.1.0
```

## Building for Windows

### Run executable build script
Run `build_exe.cmd`, this will build the executable using cython and pyinstaller. There is a small wrapper script `echoof_launcher.py` used to launch the cli code. Installer will also be built.
