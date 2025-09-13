from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QLabel, QMainWindow, QMenu

from src.domain.constants import CSS_DARK_FILE_PATH, CSS_LIGHT_FILE_PATH
from src.utils import load_css


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("TP21 : tp_interface_complete")
        self.setGeometry(100, 100, 800, 600)

        label = QLabel("Hello, World!")
        self.setCentralWidget(label)

        # Initialiser les états de formatage
        self.is_bold = False
        self.is_italic = False

        self.setup_menu_bar()
        self.setup_toolbar()
        self.setup_status_bar()
        self.action_sauvegarder_menu.setEnabled(False)
        self.action_sauvegarder_toolbar.setEnabled(False)
        self.content_to_copy = False
        self.content_to_cut = False
        self.setup_theme()
        self.setup_context_menu()

    def setup_theme(self) -> None:
        self.apply_light_theme()  # default theme

        if (menu := self.menuBar()) is None:
            return

        if (theme_menu := menu.addMenu("&Thème")) is None:
            return

        light_theme = QAction("&Thème clair", self)
        light_theme.triggered.connect(self.apply_light_theme)
        theme_menu.addAction(light_theme)

        dark_theme = QAction("&Thème sombre", self)
        dark_theme.triggered.connect(self.apply_dark_theme)
        theme_menu.addAction(dark_theme)

    def apply_light_theme(self) -> None:
        self.setStyleSheet(load_css(CSS_LIGHT_FILE_PATH))

    def apply_dark_theme(self) -> None:
        self.setStyleSheet(load_css(CSS_DARK_FILE_PATH))

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
        self.toolbar = self.addToolBar("Principal")
        if self.toolbar is None:
            return

        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        action_nouveau = QAction("&Nouveau", self)
        action_nouveau.setIcon(QIcon("icons/new.png"))
        action_nouveau.setStatusTip("Créer un nouveau document")
        action_nouveau.triggered.connect(self.action_nouveau)
        self.toolbar.addAction(action_nouveau)

        self.toolbar.addSeparator()

        action_ouvrir = QAction("&Ouvrir", self)
        action_ouvrir.setIcon(QIcon("icons/open.png"))
        action_ouvrir.setStatusTip("Ouvrir un document existant")
        action_ouvrir.triggered.connect(self.action_ouvrir)
        self.toolbar.addAction(action_ouvrir)

        self.toolbar.addSeparator()

        self.action_sauvegarder_toolbar = QAction("&Sauvegarder", self)
        self.action_sauvegarder_toolbar.setIcon(QIcon("icons/save.png"))
        self.action_sauvegarder_toolbar.setStatusTip("Sauvegarder le document actuel")
        self.action_sauvegarder_toolbar.triggered.connect(self.action_sauvegarder)
        self.toolbar.addAction(self.action_sauvegarder_toolbar)

    def setup_status_bar(self) -> None:
        if (status_bar := self.statusBar()) is None:
            return

        status_bar.showMessage("Application prête", 2000)

        self.status_label_permanent = QLabel("État: Prêt")
        status_bar.addPermanentWidget(self.status_label_permanent)

    def setup_context_menu(self) -> None:
        """Configure les menus contextuels"""
        # Activer les menus contextuels
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position: QPoint) -> None:
        """Affiche le menu contextuel"""
        widget_clicked = self.childAt(position)
        context_menu = QMenu(self)

        if widget_clicked == self.toolbar:
            context_menu.addAction("Personnaliser la barre d'outils")
            context_menu.addAction("Masquer la barre d'outils")
            context_menu.addAction("Réinitialiser la barre d'outils")
        else:
            if (copy_action := context_menu.addAction("Copier")) is None:
                return

            copy_action.triggered.connect(self.copy_content)

            if (paste_action := context_menu.addAction("Coller")) is None:
                return

            paste_action.triggered.connect(self.paste_content)
            paste_action.setEnabled(self.has_clipboard_content())

            context_menu.addSeparator()

            if (properties_action := context_menu.addAction("Couper")) is None:
                return

            properties_action.triggered.connect(self.cut_content)

            # Sous-menu Format avec actions checkable
            if (format_menu := context_menu.addMenu("Format")) is None:
                return

            # Action Gras - checkable
            action_gras = QAction("Gras", self)
            action_gras.setCheckable(True)
            action_gras.setChecked(self.is_bold)
            action_gras.triggered.connect(self.toggle_bold)
            format_menu.addAction(action_gras)

            # Action Italique - checkable
            action_italique = QAction("Italique", self)
            action_italique.setCheckable(True)
            action_italique.setChecked(self.is_italic)
            action_italique.triggered.connect(self.toggle_italic)
            format_menu.addAction(action_italique)

            format_menu.addAction("Couleur du texte")

        # Afficher le menu à la position du clic
        context_menu.exec(self.mapToGlobal(position))

    def copy_content(self) -> None:
        """Gestionnaire copier"""
        self.content_to_copy = True
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Contenu copié", 2000)

    def paste_content(self) -> None:
        """Gestionnaire coller"""
        if self.content_to_cut is True:
            self.content_to_cut = False

        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Contenu collé", 2000)

    def cut_content(self) -> None:
        """Affiche les propriétés"""
        self.content_to_cut = True
        self.content_to_copy = False
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Contenu coupé", 2000)

    def has_text_selected(self) -> bool:
        """Vérifie si du texte est sélectionné"""
        return True

    def has_clipboard_content(self) -> bool:
        """Vérifie si le presse-papier contient du contenu"""
        return self.content_to_copy or self.content_to_cut

    def toggle_bold(self) -> None:
        """Bascule l'état gras du texte"""
        self.is_bold = not self.is_bold

        if (status_bar := self.statusBar()) is not None:
            if self.is_bold:
                status_bar.showMessage("Formatage gras activé", 2000)
            else:
                status_bar.showMessage("Formatage gras désactivé", 2000)

    def toggle_italic(self) -> None:
        """Bascule l'état italique du texte"""
        self.is_italic = not self.is_italic

        if (status_bar := self.statusBar()) is not None:
            if self.is_italic:
                status_bar.showMessage("Formatage italique activé", 2000)
            else:
                status_bar.showMessage("Formatage italique désactivé", 2000)
