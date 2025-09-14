from typing import Literal

from PyQt6.QtCore import QPoint, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QLabel, QMainWindow, QMenu, QPushButton

from src.domain.constants import CSS_DARK_FILE_PATH, CSS_LIGHT_FILE_PATH
from src.utils import load_css


class MainWindow(QMainWindow):
    # Signal pour le système de notifications
    show_notification = pyqtSignal(str, str)  # (message, type)

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

        # Initialiser le système de notifications
        self.notification_widgets: list[QLabel] = []  # Liste des widgets de notification actifs
        self.notification_timers: list[QTimer] = []  # Liste des timers associés

        # Créer les actions partagées
        self.create_actions()

        # Connecter le signal de notification
        self.show_notification.connect(self.display_notification)

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
        self.show_notification.emit("Thème clair appliqué", "info")
        self.setStyleSheet(load_css(CSS_LIGHT_FILE_PATH))

    def apply_dark_theme(self) -> None:
        self.increment_action_counter("Thème sombre")
        self.show_notification.emit("Thème sombre appliqué", "info")
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

        # Notification d'information
        message = "Barre d'outils affichée" if is_visible else "Barre d'outils masquée"
        self.show_notification.emit(message, "info")

        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage(message, 2000)

    def toggle_statusbar_visibility(self) -> None:
        """Bascule la visibilité de la barre de statut"""
        if (status_bar := self.statusBar()) is None:
            return

        is_visible = not status_bar.isVisible()
        action_name = "Afficher barre de statut" if is_visible else "Masquer barre de statut"
        self.increment_action_counter(action_name)

        # Notification d'information (avant de masquer la barre de statut)
        message = "Barre de statut affichée" if is_visible else "Barre de statut masquée"
        if not is_visible:
            # Si on va masquer la barre, montrer la notification avant
            self.show_notification.emit(message, "warning")

        status_bar.setVisible(is_visible)
        # Synchroniser l'état de l'action avec la visibilité réelle
        self.statusbar_view_action.setChecked(is_visible)

        # Si la barre est visible, afficher un message et notification
        if is_visible:
            status_bar.showMessage("Barre de statut affichée", 2000)
            self.show_notification.emit(message, "info")

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
        self.show_notification.emit("Nouveau document créé avec succès", "success")
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Nouvelle fenêtre ouverte", 1000)
        self.save_action.setEnabled(True)

    def action_ouvrir(self) -> None:
        self.increment_action_counter("Ouvrir document")
        self.show_notification.emit("Document ouvert avec succès", "success")
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Fenêtre ouverte", 1000)
        self.save_action.setEnabled(True)

    def action_sauvegarder(self) -> None:
        self.increment_action_counter("Sauvegarder document")
        self.show_notification.emit("Document sauvegardé avec succès", "success")
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

        # Notification importante pour la remise à zéro
        self.show_notification.emit(f"Compteur remis à zéro ({previous_count} actions effacées)", "warning")

        # Feedback dans la barre de statut
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage(f"Compteur remis à zéro (était: {previous_count})", 2000)

        # Communication bidirectionnelle : affecter le comportement de l'application
        # Par exemple, remettre à zéro certains états
        self.content_to_copy = False
        self.content_to_cut = False

        # Mettre à jour l'état permanent
        self.status_label_permanent.setText("État: Compteur remis à zéro")

    def display_notification(
        self,
        message: str,
        notification_type: Literal["info", "success", "warning", "error"],
    ) -> None:
        """Affiche une notification colorée dans la barre de statut"""
        if (status_bar := self.statusBar()) is None:
            return

        # Définir les styles pour chaque type de notification avec !important pour écraser le CSS global
        styles: dict[Literal["info", "success", "warning", "error"], str] = {
            "info": """
                QLabel {
                    background-color: #e3f2fd !important;
                    color: #1565c0 !important;
                    border: 2px solid #90caf9 !important;
                    padding: 8px 12px !important;
                    border-radius: 4px !important;
                    font-weight: bold !important;
                    margin: 2px !important;
                }
            """,
            "success": """
                QLabel {
                    background-color: #e8f5e8 !important;
                    color: #2e7d32 !important;
                    border: 2px solid #81c784 !important;
                    padding: 8px 12px !important;
                    border-radius: 4px !important;
                    font-weight: bold !important;
                    margin: 2px !important;
                }
            """,
            "warning": """
                QLabel {
                    background-color: #fff8e1 !important;
                    color: #f57c00 !important;
                    border: 2px solid #ffb74d !important;
                    padding: 8px 12px !important;
                    border-radius: 4px !important;
                    font-weight: bold !important;
                    margin: 2px !important;
                }
            """,
            "error": """
                QLabel {
                    background-color: #ffebee !important;
                    color: #c62828 !important;
                    border: 2px solid #e57373 !important;
                    padding: 8px 12px !important;
                    border-radius: 4px !important;
                    font-weight: bold !important;
                    margin: 2px !important;
                }
            """,
        }

        # Créer le widget de notification
        notification_label = QLabel(message)
        notification_label.setStyleSheet(styles[notification_type])
        notification_label.setMaximumWidth(250)
        notification_label.setMinimumWidth(150)
        notification_label.setWordWrap(True)

        # Propriétés pour forcer la visibilité
        notification_label.setVisible(True)
        notification_label.setAttribute(Qt.WidgetAttribute.WA_ForceUpdatesDisabled, False)
        notification_label.setEnabled(True)

        # Insérer au début de la barre de statut (index 0) pour être sûr qu'elle soit visible
        status_bar.insertWidget(0, notification_label)

        # Forcer l'affichage
        notification_label.show()
        notification_label.repaint()
        status_bar.repaint()

        # Ajouter à la liste des widgets actifs
        self.notification_widgets.append(notification_label)

        # Créer un timer pour l'auto-suppression
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self.remove_notification(notification_label, timer))

        # Durée basée sur le type de notification
        durations: dict[Literal["info", "success", "warning", "error"], int] = {
            "info": 3000,  # 3 secondes
            "success": 2500,  # 2.5 secondes
            "warning": 4000,  # 4 secondes
            "error": 5000,  # 5 secondes
        }

        timer.start(durations[notification_type])
        self.notification_timers.append(timer)

    def remove_notification(self, notification_widget: QLabel, timer: QTimer | None) -> None:
        """Supprime une notification de la barre de statut"""
        try:
            # Cacher d'abord le widget
            notification_widget.hide()

            # Supprimer de la barre de statut
            if (status_bar := self.statusBar()) is not None:
                status_bar.removeWidget(notification_widget)
                status_bar.repaint()

            # Supprimer le widget
            notification_widget.deleteLater()

            # Nettoyer les listes
            if notification_widget in self.notification_widgets:
                self.notification_widgets.remove(notification_widget)
            if timer is not None and timer in self.notification_timers:
                self.notification_timers.remove(timer)

        except Exception as e:
            # Gestion d'erreur silencieuse pour éviter les crashes
            print(f"Erreur lors de la suppression de la notification: {e}")

    def clear_all_notifications(self) -> None:
        """Supprime toutes les notifications actives"""
        # Arrêter tous les timers
        for timer in self.notification_timers.copy():
            timer.stop()

        # Supprimer tous les widgets
        for widget in self.notification_widgets.copy():
            self.remove_notification(widget, None)

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
        self.show_notification.emit("Contenu copié dans le presse-papier", "success")
        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage("Contenu copié", 2000)

    def paste_content(self) -> None:
        """Gestionnaire coller"""
        self.increment_action_counter("Coller")
        if self.content_to_cut is True:
            self.content_to_cut = False

        if self.has_clipboard_content():
            message = "Contenu collé avec succès"
            self.show_notification.emit(message, "success")
        else:
            message = "Aucun contenu à coller"
            self.show_notification.emit(message, "warning")

        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage(message, 2000)

    def cut_content(self) -> None:
        """Gestionnaire couper"""
        self.increment_action_counter("Couper")
        self.content_to_cut = True
        self.content_to_copy = False
        self.show_notification.emit("Contenu coupé et placé dans le presse-papier", "success")
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

        # Notification de formatage
        message = "Formatage gras activé" if self.is_bold else "Formatage gras désactivé"
        self.show_notification.emit(message, "info")

        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage(message, 2000)

    def toggle_italic(self) -> None:
        """Bascule l'état italique du texte"""
        self.is_italic = not self.is_italic

        action_name = "Activer italique" if self.is_italic else "Désactiver italique"
        self.increment_action_counter(action_name)

        # Notification de formatage
        message = "Formatage italique activé" if self.is_italic else "Formatage italique désactivé"
        self.show_notification.emit(message, "info")

        if (status_bar := self.statusBar()) is not None:
            status_bar.showMessage(message, 2000)
