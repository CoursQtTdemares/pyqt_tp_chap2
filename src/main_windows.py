from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QLabel, QMainWindow

from src.domain.constants import CSS_FILE_PATH
from src.utils import load_css


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("TP21 : tp_interface_complete")
        self.setGeometry(100, 100, 800, 600)

        label = QLabel("Hello, World!")
        self.setCentralWidget(label)
        self.setup_menu_bar()
        self.setup_toolbar()
        self.setup_status_bar()
        self.action_sauvegarder_menu.setEnabled(False)
        self.action_sauvegarder_toolbar.setEnabled(False)
        self.setStyleSheet(load_css(CSS_FILE_PATH))

    def setup_menu_bar(self) -> None:
        if (menu_bar := self.menuBar()) is None:
            return

        action_nouveau = QAction("&Nouveau", self)
        action_nouveau.setShortcut("Ctrl+N")
        action_nouveau.setStatusTip("Créer un nouveau document")
        action_nouveau.triggered.connect(self.action_nouveau)
        menu_bar.addAction(action_nouveau)

        action_ouvrir = QAction("&Ouvrir", self)
        action_ouvrir.setShortcut("Ctrl+O")
        action_ouvrir.setStatusTip("Ouvrir un document existant")
        action_ouvrir.triggered.connect(self.action_ouvrir)
        menu_bar.addAction(action_ouvrir)

        self.action_sauvegarder_menu = QAction("&Sauvegarder", self)
        self.action_sauvegarder_menu.setShortcut("Ctrl+S")
        self.action_sauvegarder_menu.setStatusTip("Sauvegarder le document actuel")
        self.action_sauvegarder_menu.triggered.connect(self.action_sauvegarder)
        menu_bar.addAction(self.action_sauvegarder_menu)

        action_quitter = QAction("&Quitter", self)
        action_quitter.setShortcut("Ctrl+Q")
        action_quitter.setStatusTip("Fermer l'application")
        action_quitter.triggered.connect(self.close)
        menu_bar.addAction(action_quitter)

    def action_nouveau(self) -> None:
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Nouvelle fenêtre ouverte", 1000)
        self.action_sauvegarder_menu.setEnabled(True)
        self.action_sauvegarder_toolbar.setEnabled(True)

    def action_ouvrir(self) -> None:
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Fenêtre ouverte", 1000)
        self.action_sauvegarder_menu.setEnabled(True)
        self.action_sauvegarder_toolbar.setEnabled(True)

    def action_sauvegarder(self) -> None:
        # Barre de statut
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Fenêtre sauvegardée", 1000)

        self.action_sauvegarder_menu.setEnabled(False)
        self.action_sauvegarder_toolbar.setEnabled(False)

    def setup_toolbar(self) -> None:
        if (toolbar := self.addToolBar("Principal")) is None:
            return

        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        action_nouveau = QAction("&Nouveau", self)
        action_nouveau.setIcon(QIcon("icons/new.png"))
        action_nouveau.setStatusTip("Créer un nouveau document")
        action_nouveau.triggered.connect(self.action_nouveau)
        toolbar.addAction(action_nouveau)

        toolbar.addSeparator()

        action_ouvrir = QAction("&Ouvrir", self)
        action_ouvrir.setIcon(QIcon("icons/open.png"))
        action_ouvrir.setStatusTip("Ouvrir un document existant")
        action_ouvrir.triggered.connect(self.action_ouvrir)
        toolbar.addAction(action_ouvrir)

        toolbar.addSeparator()

        self.action_sauvegarder_toolbar = QAction("&Sauvegarder", self)
        self.action_sauvegarder_toolbar.setIcon(QIcon("icons/save.png"))
        self.action_sauvegarder_toolbar.setStatusTip("Sauvegarder le document actuel")
        self.action_sauvegarder_toolbar.triggered.connect(self.action_sauvegarder)
        toolbar.addAction(self.action_sauvegarder_toolbar)

    def setup_status_bar(self) -> None:
        if (status_bar := self.statusBar()) is None:
            return

        status_bar.showMessage("Application prête", 2000)

        self.status_label_permanent = QLabel("État: Prêt")
        status_bar.addPermanentWidget(self.status_label_permanent)
