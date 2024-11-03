import sys
from pathlib import Path

# Add the root directory (parent of `backend`) to sys.path
# This way, all imports should be done from the root folder perspective.
root_folder = str(Path(__file__).parent.resolve())
sys.path.append(root_folder)

# Now it is possible to import and run backend/main.py
from backend.main import main

if __name__ == "__main__":
    main()