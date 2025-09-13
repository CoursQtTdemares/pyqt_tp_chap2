from pathlib import Path

# Paths of the application

WORKSPACE_DIR = Path(__file__).parents[2].resolve()

SRC_DIR = WORKSPACE_DIR / "src"

CSS_LIGHT_FILE_PATH = SRC_DIR / "styles_light.css"
CSS_DARK_FILE_PATH = SRC_DIR / "styles_dark.css"
