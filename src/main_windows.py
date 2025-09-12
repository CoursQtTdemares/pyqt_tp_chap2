from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QLabel, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("TP21 : tp_interface_complete")
        self.setGeometry(100, 100, 800, 600)

        label = QLabel("Hello, World!")
        self.setCentralWidget(label)
        self.setup_menu_bar()

        # Barre de statut
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Application prête")

    def setup_menu_bar(self) -> None:
        if (menu_bar := self.menuBar()) is None:
            return

        action_nouveau = QAction("&Nouveau", self)
        action_nouveau.setShortcut("Ctrl+N")
        action_nouveau.triggered.connect(self.nouveau)
        menu_bar.addAction(action_nouveau)

        action_ouvrir = QAction("&Ouvrir", self)
        action_ouvrir.setShortcut("Ctrl+O")
        action_ouvrir.triggered.connect(self.ouvrir)
        menu_bar.addAction(action_ouvrir)

        action_sauvegarder = QAction("&Sauvegarder", self)
        action_sauvegarder.setShortcut("Ctrl+S")
        action_sauvegarder.triggered.connect(self.sauvegarder)
        menu_bar.addAction(action_sauvegarder)

        action_quitter = QAction("&Quitter", self)
        action_quitter.setShortcut("Ctrl+Q")
        action_quitter.triggered.connect(self.quitter)
        menu_bar.addAction(action_quitter)

    def nouveau(self) -> None:
        # Barre de statut
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Nouvelle fenêtre ouverte", 1000)

    def ouvrir(self) -> None:
        # Barre de statut
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Fenêtre ouverte", 1000)

    def sauvegarder(self) -> None:
        # Barre de statut
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Fenêtre sauvegardée", 1000)

    def quitter(self) -> None:
        # Barre de statut
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Application quittée", 1000)
