
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
