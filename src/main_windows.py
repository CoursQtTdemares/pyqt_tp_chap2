from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QLabel, QMainWindow, QMenu, QPushButton

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

        # Initialiser le compteur d'actions
        self.action_counter = 0

        # Créer les actions partagées
        self.create_actions()

        self.setup_menu_bar()
        self.setup_toolbar()
        self.setup_status_bar()
        self.sync_view_actions_state()
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

        # Actions d'affichage
        self.toolbar_view_action = QAction("&Barre d'outils", self)
        self.toolbar_view_action.setCheckable(True)
        self.toolbar_view_action.setChecked(True)  # Visible par défaut
        self.toolbar_view_action.setStatusTip("Afficher/Masquer la barre d'outils")
        self.toolbar_view_action.triggered.connect(self.toggle_toolbar_visibility)

        self.statusbar_view_action = QAction("Barre de &statut", self)
        self.statusbar_view_action.setCheckable(True)
        self.statusbar_view_action.setChecked(True)  # Visible par défaut
        self.statusbar_view_action.setStatusTip("Afficher/Masquer la barre de statut")
        self.statusbar_view_action.triggered.connect(self.toggle_statusbar_visibility)

    def setup_theme(self) -> None:
        self.apply_light_theme()  # default theme

        if (menu := self.menuBar()) is None:
            return

        if (theme_menu := menu.addMenu("&Thème")) is None:
            return

        theme_menu.addAction(self.light_theme_action)
        theme_menu.addAction(self.dark_theme_action)

    def apply_light_theme(self) -> None:
        self.increment_action_counter("Thème clair")
        self.setStyleSheet(load_css(CSS_LIGHT_FILE_PATH))

    def apply_dark_theme(self) -> None:
        self.increment_action_counter("Thème sombre")
        self.setStyleSheet(load_css(CSS_DARK_FILE_PATH))

    def toggle_toolbar_visibility(self) -> None:
        """Bascule la visibilité de la barre d'outils"""
        if self.toolbar is None:
            return

        is_visible = not self.toolbar.isVisible()
        self.toolbar.setVisible(is_visible)
        # Synchroniser l'état de l'action avec la visibilité réelle
        self.toolbar_view_action.setChecked(is_visible)

        action_name = "Afficher barre d'outils" if is_visible else "Masquer barre d'outils"
        self.increment_action_counter(action_name)

        if (status_bar := self.statusBar()) is not None:
            message = "Barre d'outils affichée" if is_visible else "Barre d'outils masquée"
            status_bar.showMessage(message, 2000)

    def toggle_statusbar_visibility(self) -> None:
        """Bascule la visibilité de la barre de statut"""
        if (status_bar := self.statusBar()) is None:
            return

        is_visible = not status_bar.isVisible()
        status_bar.setVisible(is_visible)
        # Synchroniser l'état de l'action avec la visibilité réelle
        self.statusbar_view_action.setChecked(is_visible)

        action_name = "Afficher barre de statut" if is_visible else "Masquer barre de statut"
        self.increment_action_counter(action_name)

        # Si la barre est visible, afficher un message
        if is_visible:
            status_bar.showMessage("Barre de statut affichée", 2000)

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

        # Menu Affichage
        if (view_menu := menu_bar.addMenu("&Affichage")) is None:
            return
        view_menu.addAction(self.toolbar_view_action)
        view_menu.addAction(self.statusbar_view_action)

        # Menu Quitter
        if (quit_menu := menu_bar.addMenu("&Quitter")) is None:
            return
        quit_menu.addAction(self.quit_action)

    def action_nouveau(self) -> None:
        self.increment_action_counter("Nouveau document")
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Nouvelle fenêtre ouverte", 1000)
        self.save_action.setEnabled(True)

    def action_ouvrir(self) -> None:
        self.increment_action_counter("Ouvrir document")
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Fenêtre ouverte", 1000)
        self.save_action.setEnabled(True)

    def action_sauvegarder(self) -> None:
        self.increment_action_counter("Sauvegarder document")
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
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.quit_action)

    def setup_status_bar(self) -> None:
        if (status_bar := self.statusBar()) is None:
            return

        status_bar.showMessage("Application prête", 2000)

        # Widget d'état permanent (gauche)
        self.status_label_permanent = QLabel("État: Prêt")
        status_bar.addPermanentWidget(self.status_label_permanent)

        # Compteur d'actions (centre-droite)
        self.action_counter_label = QLabel(f"Actions: {self.action_counter}")
        self.action_counter_label.setStyleSheet("QLabel { margin: 0 10px; font-weight: bold; }")
        status_bar.addPermanentWidget(self.action_counter_label)

        # Bouton de remise à zéro (droite)
        self.reset_counter_button = QPushButton("RAZ")
        self.reset_counter_button.setMaximumWidth(50)
        self.reset_counter_button.setToolTip("Remettre le compteur d'actions à zéro")
        self.reset_counter_button.clicked.connect(self.reset_action_counter)
        status_bar.addPermanentWidget(self.reset_counter_button)

    def sync_view_actions_state(self) -> None:
        """Synchronise l'état des actions d'affichage avec la visibilité réelle des barres"""
        # Synchroniser l'action toolbar avec la visibilité de la barre d'outils
        if hasattr(self, "toolbar") and self.toolbar is not None:
            self.toolbar_view_action.setChecked(self.toolbar.isVisible())

        # Synchroniser l'action statusbar avec la visibilité de la barre de statut
        if (status_bar := self.statusBar()) is not None:
            self.statusbar_view_action.setChecked(status_bar.isVisible())

    def increment_action_counter(self, action_name: str = "Action") -> None:
        """Incrémente le compteur d'actions et met à jour l'affichage"""
        self.action_counter += 1
        self.action_counter_label.setText(f"Actions: {self.action_counter}")

        # Feedback optionnel dans la barre de statut
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage(f"{action_name} effectuée (Total: {self.action_counter})", 1500)

    def reset_action_counter(self) -> None:
        """Remet à zéro le compteur d'actions - Communication bidirectionnelle"""
        previous_count = self.action_counter
        self.action_counter = 0
        self.action_counter_label.setText(f"Actions: {self.action_counter}")

        # Feedback dans la barre de statut
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage(f"Compteur remis à zéro (était: {previous_count})", 2000)

        # Communication bidirectionnelle : affecter le comportement de l'application
        # Par exemple, remettre à zéro certains états
        self.content_to_copy = False
        self.content_to_cut = False

        # Mettre à jour l'état permanent
        self.status_label_permanent.setText("État: Compteur remis à zéro")

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
        self.increment_action_counter("Copier")
        self.content_to_copy = True
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Contenu copié", 2000)

    def paste_content(self) -> None:
        """Gestionnaire coller"""
        self.increment_action_counter("Coller")
        if self.content_to_cut is True:
            self.content_to_cut = False

        message = "Aucun contenu à coller" if self.has_clipboard_content() is False else "Contenu collé"

        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage(message, 2000)

    def cut_content(self) -> None:
        """Gestionnaire couper"""
        self.increment_action_counter("Couper")
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

        action_name = "Activer gras" if self.is_bold else "Désactiver gras"
        self.increment_action_counter(action_name)

        if (status_bar := self.statusBar()) is not None:
            if self.is_bold:
                status_bar.showMessage("Formatage gras activé", 2000)
            else:
                status_bar.showMessage("Formatage gras désactivé", 2000)

    def toggle_italic(self) -> None:
        """Bascule l'état italique du texte"""
        self.is_italic = not self.is_italic

        action_name = "Activer italique" if self.is_italic else "Désactiver italique"
        self.increment_action_counter(action_name)

        if (status_bar := self.statusBar()) is not None:
            if self.is_italic:
                status_bar.showMessage("Formatage italique activé", 2000)
            else:
                status_bar.showMessage("Formatage italique désactivé", 2000)
