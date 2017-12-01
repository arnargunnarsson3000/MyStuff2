import importlib
import sys
import os
try:
    try:
        importlib.import_module('sqlite3')
    except ImportError:
        import pip
        pip.main(['install', 'sqlite3'])
    finally:
        globals()['sqlite3'] = importlib.import_module('sqlite3')

    try:
        importlib.import_module('matplotlib')
    except ImportError:
        import pip
        pip.main(['install', 'matplotlib'])
    finally:
        globals()['matplotlib'] = importlib.import_module('matplotlib')

    # below method probably doesn't work, don't think tkinter is a pip package
    try:
        importlib.import_module('tkinter')
    except ImportError:
        try:
            import pip
            pip.main(['install', 'tkinter'])
        except:
            pass
    finally:
        globals()['tkinter'] = importlib.import_module('tkinter')


    if os.path.realpath(__file__.replace("INSTALL.py", "")) not in sys.path:
        sys.path.insert(os.path.realpath(__file__.replace("INSTALL.py", "")))
except:
    print("Read the README.txt")
    print("Read the README.txt")
    print("Read the README.txt")
    exit(0)