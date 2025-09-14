from PyQt6.QtWidgets import QApplication

from src.main_windows import MainWindow


def main() -> None:
    """Entry point for pyqt_tp_chap2."""

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
