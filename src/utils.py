from pathlib import Path


def load_css(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Le fichier {path} n'existe pas")

    if path.suffix != ".css":
        raise ValueError(f"Le fichier {path} n'est pas un fichier CSS")

    with open(path, "r") as file:
        return file.read()
