from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QLabel, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("TP21 : tp_interface_complete")
        self.setGeometry(100, 100, 800, 600)

        label = QLabel("Hello, World!")
        self.setCentralWidget(label)
        self.setup_menu_bar()
        self.setup_toolbar()

        # Barre de statut
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Application prête")

    def setup_menu_bar(self) -> None:
        if (menu_bar := self.menuBar()) is None:
            return

        action_nouveau = QAction("&Nouveau", self)
        action_nouveau.setShortcut("Ctrl+N")
        action_nouveau.triggered.connect(self.action_nouveau)
        menu_bar.addAction(action_nouveau)

        action_ouvrir = QAction("&Ouvrir", self)
        action_ouvrir.setShortcut("Ctrl+O")
        action_ouvrir.triggered.connect(self.action_ouvrir)
        menu_bar.addAction(action_ouvrir)

        action_sauvegarder = QAction("&Sauvegarder", self)
        action_sauvegarder.setShortcut("Ctrl+S")
        action_sauvegarder.triggered.connect(self.action_sauvegarder)
        menu_bar.addAction(action_sauvegarder)

        action_quitter = QAction("&Quitter", self)
        action_quitter.setShortcut("Ctrl+Q")
        action_quitter.triggered.connect(self.action_quitter)
        menu_bar.addAction(action_quitter)

    def action_nouveau(self) -> None:
        # Barre de statut
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Nouvelle fenêtre ouverte", 1000)

    def action_ouvrir(self) -> None:
        # Barre de statut
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Fenêtre ouverte", 1000)

    def action_sauvegarder(self) -> None:
        # Barre de statut
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Fenêtre sauvegardée", 1000)

    def action_quitter(self) -> None:
        # Barre de statut
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Application quittée", 1000)

    def setup_toolbar(self) -> None:
        if (toolbar := self.addToolBar("Principal")) is None:
            return

        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        action_nouveau = QAction("&Nouveau", self)
        action_nouveau.setIcon(QIcon("icons/new.png"))
        action_nouveau.triggered.connect(self.action_nouveau)
        toolbar.addAction(action_nouveau)

        toolbar.addSeparator()

        action_ouvrir = QAction("&Ouvrir", self)
        action_ouvrir.setIcon(QIcon("icons/open.png"))
        action_ouvrir.triggered.connect(self.action_ouvrir)
        toolbar.addAction(action_ouvrir)

        toolbar.addSeparator()

        action_sauvegarder = QAction("&Sauvegarder", self)
        action_sauvegarder.setIcon(QIcon("icons/save.png"))
        action_sauvegarder.triggered.connect(self.action_sauvegarder)
        toolbar.addAction(action_sauvegarder)

        toolbar.addSeparator()

        action_quitter = QAction("&Quitter", self)
        action_quitter.setIcon(QIcon("icons/open.png"))
        action_quitter.triggered.connect(self.action_quitter)
        toolbar.addAction(action_quitter)
