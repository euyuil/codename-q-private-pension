# Must load_dotenv before everything else.
from dotenv import load_dotenv; load_dotenv()

import os
import sys

def ensure_pythonpath():
    pythonpath = os.environ.get("PYTHONPATH", "")
    paths = pythonpath.split(os.pathsep)
    for path in paths:
        if path and path not in sys.path:
            sys.path.append(path)

ensure_pythonpath()

from app import create_app

app = create_app()

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
