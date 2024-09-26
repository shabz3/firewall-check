
# If we are running from a wheel, add the wheel to sys.path
# This allows the usage python pip-*.whl/pip install pip-*.whl
if __package__ == "":
    # __file__ is pip-*.whl/pip/__main__.py
    # first dirname call strips of '/__main__.py', second strips off '/pip'
    # Resulting path is the name of the wheel itself
    # Add that to sys.path so we can import pip
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

if __name__ == "__main__":
    import importlib.util
    import sys
    spec = importlib.util.spec_from_file_location(
        "pipenv", location=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "__init__.py"))
    pipenv = importlib.util.module_from_spec(spec)
    sys.modules["pipenv"] = pipenv
    spec.loader.exec_module(pipenv)
    from pipenv.patched.pip._internal.cli.main import main as _main

    sys.exit(_main())
