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

        # Créer les actions partagées
        self.create_actions()

        self.setup_menu_bar()
        self.setup_toolbar()
        self.setup_status_bar()
        self.save_action.setEnabled(False)
        self.content_to_copy = False
        self.content_to_cut = False
        self.setup_theme()
        self.setup_context_menu()
        self.setup_shortcuts()

    def create_actions(self) -> None:
        """Crée toutes les actions partagées entre menus et barres d'outils"""
        # Actions principales
        self.new_action = QAction("&Nouveau", self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.setIcon(QIcon("icons/new.png"))
        self.new_action.setStatusTip("Créer un nouveau document")
        self.new_action.triggered.connect(self.action_nouveau)

        self.open_action = QAction("&Ouvrir", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.setIcon(QIcon("icons/open.png"))
        self.open_action.setStatusTip("Ouvrir un document existant")
        self.open_action.triggered.connect(self.action_ouvrir)

        self.save_action = QAction("&Sauvegarder", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.setIcon(QIcon("icons/save.png"))
        self.save_action.setStatusTip("Sauvegarder le document actuel")
        self.save_action.triggered.connect(self.action_sauvegarder)

        self.quit_action = QAction("&Quitter", self)
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.setStatusTip("Fermer l'application")
        self.quit_action.triggered.connect(self.close)

        # Actions de thème
        self.light_theme_action = QAction("&Thème clair", self)
        self.light_theme_action.triggered.connect(self.apply_light_theme)

        self.dark_theme_action = QAction("&Thème sombre", self)
        self.dark_theme_action.triggered.connect(self.apply_dark_theme)

        # Actions d'édition
        self.copy_action = QAction("&Copier", self)
        self.copy_action.setShortcut("Ctrl+C")
        self.copy_action.setStatusTip("Copier le contenu sélectionné")
        self.copy_action.triggered.connect(self.copy_content)

        self.cut_action = QAction("Co&uper", self)
        self.cut_action.setShortcut("Ctrl+X")
        self.cut_action.setStatusTip("Couper le contenu sélectionné")
        self.cut_action.triggered.connect(self.cut_content)

        self.paste_action = QAction("C&oller", self)
        self.paste_action.setShortcut("Ctrl+V")
        self.paste_action.setStatusTip("Coller le contenu du presse-papier")
        self.paste_action.triggered.connect(self.paste_content)

    def setup_theme(self) -> None:
        self.apply_light_theme()  # default theme

        if (menu := self.menuBar()) is None:
            return

        if (theme_menu := menu.addMenu("&Thème")) is None:
            return

        theme_menu.addAction(self.light_theme_action)
        theme_menu.addAction(self.dark_theme_action)

    def apply_light_theme(self) -> None:
        self.setStyleSheet(load_css(CSS_LIGHT_FILE_PATH))

    def apply_dark_theme(self) -> None:
        self.setStyleSheet(load_css(CSS_DARK_FILE_PATH))

    def setup_menu_bar(self) -> None:
        if (menu_bar := self.menuBar()) is None:
            return

        # Menu Fichier
        if (file_menu := menu_bar.addMenu("&Fichier")) is None:
            return
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addSeparator()
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)

        # Menu Édition
        if (edit_menu := menu_bar.addMenu("&Édition")) is None:
            return
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.paste_action)

    def action_nouveau(self) -> None:
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Nouvelle fenêtre ouverte", 1000)
        self.save_action.setEnabled(True)

    def action_ouvrir(self) -> None:
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Fenêtre ouverte", 1000)
        self.save_action.setEnabled(True)

    def action_sauvegarder(self) -> None:
        # Barre de statut
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Fenêtre sauvegardée", 1000)

        self.save_action.setEnabled(False)

    def setup_toolbar(self) -> None:
        self.toolbar = self.addToolBar("Principal")
        if self.toolbar is None:
            return

        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        # Utiliser les actions partagées
        self.toolbar.addAction(self.new_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.open_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.save_action)

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

    def setup_shortcuts(self) -> None:
        """Configure les raccourcis clavier globaux"""
        # Les raccourcis sont déjà définis dans create_actions()
        # On ajoute les actions à la fenêtre pour qu'elles soient globales
        self.addAction(self.copy_action)
        self.addAction(self.cut_action)
        self.addAction(self.paste_action)
        self.addAction(self.new_action)
        self.addAction(self.open_action)
        self.addAction(self.save_action)
        self.addAction(self.quit_action)

    def show_context_menu(self, position: QPoint) -> None:
        """Affiche le menu contextuel"""
        widget_clicked = self.childAt(position)
        context_menu = QMenu(self)

        if widget_clicked == self.toolbar:
            # === AFFICHAGE === (actions les plus courantes)
            context_menu.addAction("Masquer la barre d'outils")

            context_menu.addSeparator()

            # === PERSONNALISATION ===
            context_menu.addAction("Personnaliser la barre d'outils")
            context_menu.addAction("Réinitialiser la barre d'outils")
        else:
            # === ÉDITION === (actions les plus courantes)
            context_menu.addAction(self.copy_action)
            context_menu.addAction(self.cut_action)
            context_menu.addSeparator()

            # === COLLAGE ===
            # Mettre à jour l'état de paste_action avant de l'afficher
            self.paste_action.setEnabled(self.has_clipboard_content())
            context_menu.addAction(self.paste_action)

            context_menu.addSeparator()

            # === FORMAT ===
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

        message = "Aucun contenu à coller" if self.has_clipboard_content() is False else "Contenu collé"

        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage(message, 2000)

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
