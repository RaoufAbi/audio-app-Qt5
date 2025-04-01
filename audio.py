from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QSlider, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog
from PyQt5.QtMultimedia import QMediaPlaylist,QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl, QFileInfo 
from PyQt5.QtGui import QIcon ,QFont

class AudioPlayer(QWidget):
    def __init__(self):
        super().__init__()

        # Initialisation du lecteur multimédia, des curseurs et d'autres variables
        self.media_player = QMediaPlayer()
        self.speed_slider = QSlider(Qt.Horizontal)
        self.position_slider = QSlider(Qt.Horizontal)
        self.current_index = 0
        self.playlist = []
        self.is_playing = False
        self.is_looping = False  
        self.init_ui()

    def init_ui(self):
        # Configuration des styles de l'interface utilisateur pour les curseurs et les étiquettes

        # Style pour le curseur de position
        self.position_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid rgba(129,149,221,0.5663515406162465);
                height: 10px;
                margin: 0px;
                background: rgba(129,149,221,0.3663515406162465);
            }

            QSlider::handle:horizontal {
                background: #092d69;
                width: 8px;
                margin: -2px 0;
                border-radius: 3px;
            }
        """)

        # Style pour le curseur de vitesse
        self.speed_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid rgba(129,149,221,0.6663515406162465);
                height: 3px;
                margin: 0px;
                background: rgba(129,149,221,0.3663515406162465);
            }

            QSlider::handle:horizontal {
                background: #092d69;
                width: 9px;
                height: 16px;
                margin: -8px 0;
                border-radius: 8px; 
            }
        """)

        # Style pour le curseur de volume (réutilisation du style du curseur de vitesse)
        volume_slider_style = """
            QSlider::groove:horizontal {
                border: 1px solid rgba(129,149,221,0.6663515406162465);
                height: 3px;
                margin: 0px;
                background: rgba(129,149,221,0.3663515406162465);
            }

            QSlider::handle:horizontal {
                background: #092d69;
                width: 9px;
                height: 16px;
                margin: -8px 0;
                border-radius: 8px; 
            }
        """

        # Style pour les étiquettes
        label_style = """
            QLabel {
                color: #000;
                font-size: 16px;
                font-weight: bold;
                margin-left : 20px;
            }
        """

        # Création des widgets pour les étiquettes
        self.filename_label = QLabel("Aucun fichier chargé", self)
        self.vol_name = QLabel("Volume :", self)
        self.speed_name = QLabel("Vitesse :", self)

        # Création des widgets pour les boutons

        # bouton Charger des fichiers audio
        load_button = QPushButton("Sélectionner PLayListe", self)
        load_button.setFixedHeight(50)
        load_button.setStyleSheet("background-color: rgba(71,160,215,0.4663515406162465);border-radius: 25px;")
        load_button.setFont(QFont("Arial", 10))
        load_button.clicked.connect(self.load_audio_files)

        # bouton play et pause
        self.play_button = QPushButton("play",self)
        
        self.play_button.setToolTip("Lire")
        self.play_button.setFixedSize(50, 50)
        self.play_button.setStyleSheet("background-color: rgba(71,70,115,0.5663515406162465);border-radius: 25px;")
        self.play_button.clicked.connect(self.toggle_play_pause)

        #  buttons  skipping 
        forward_10s_button = QPushButton(">10s", self)
        forward_10s_button.setToolTip("Suivant10")
        forward_10s_button.setFixedSize(50, 50)
        forward_10s_button.setStyleSheet("background-color: rgba(71,70,115,0.5663515406162465);border-radius: 25px;")
        forward_10s_button.clicked.connect(self.skip_forward_10s)

        backward_10s_button = QPushButton("10s<", self)
        backward_10s_button.setIcon(QIcon(r"loop.png"))
        backward_10s_button.setToolTip("back10")
        backward_10s_button.setFixedSize(50, 50)
        backward_10s_button.setStyleSheet("background-color: rgba(71,70,115,0.5663515406162465);border-radius: 25px;")
        backward_10s_button.clicked.connect(self.skip_backward_10s)


        # bouton Suivant
        next_button = QPushButton(">",self)
        next_button.setToolTip("Suivant")
        next_button.setFixedSize(50, 50)
        next_button.setStyleSheet("background-color: rgba(71,70,115,0.5663515406162465);border-radius: 25px;")
        next_button.clicked.connect(self.play_next_audio)

        # bouton Suivant Précédent
        prev_button = QPushButton("<",self)
        prev_button.setToolTip("Précédent")
        prev_button.setFixedSize(50, 50)
        prev_button.setStyleSheet("background-color: rgba(71,70,115,0.5663515406162465);border-radius: 25px;")
        prev_button.clicked.connect(self.play_previous_audio)

        # Création du curseur de volume
        volume_slider = QSlider(Qt.Horizontal, self)
        volume_slider.setRange(0, 100)
        volume_slider.setValue(50)
        volume_slider.setStyleSheet(volume_slider_style)
        volume_slider.valueChanged.connect(self.set_volume)

        # Configuration du curseur de vitesse
        self.speed_slider.setRange(50, 200)
        self.speed_slider.setValue(100)
        self.speed_slider.valueChanged.connect(self.set_speed)

        # Configuration du curseur de position
        self.position_slider.setRange(0, 100)
        self.position_slider.setValue(0)
        self.position_slider.sliderReleased.connect(self.set_position)

        # Mise en page des curseurs
        self.position_slider_layout = QHBoxLayout()
        self.position_slider_layout.addWidget(QLabel("0:00"))
        self.position_slider_layout.addWidget(self.position_slider)
        self.position_slider_layout.addWidget(QLabel("0:00"))

        # Mise en page des boutons
        button_layout = QHBoxLayout()
        button_layout.addWidget(prev_button)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(next_button)

        # Mise en page des boutons skipping
        skip_layout = QHBoxLayout()
        button_layout.addWidget(backward_10s_button)
        button_layout.addWidget(forward_10s_button)

        # Mise en page des curseurs de contrôle
        control_layout = QHBoxLayout()
        control_layout.addWidget(volume_slider)
        control_layout.addWidget(self.speed_slider)

        # Mise en page des étiquettes
        aff_layout = QHBoxLayout()
        aff_layout.addWidget(self.vol_name)
        aff_layout.addWidget(self.speed_name)

        # Mise en page principale du widget
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.filename_label)
        main_layout.addLayout(self.position_slider_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(skip_layout)
        main_layout.addLayout(aff_layout)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(load_button)

        # Définition du layout principal du widget
        self.setLayout(main_layout)

        self.playlist = QMediaPlaylist()
        self.media_player.setPlaylist(self.playlist)

        # Connexion des signaux pour mettre à jour l'interface utilisateur en fonction des événements du lecteur multimédia
        self.media_player.durationChanged.connect(self.update_duration)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration_display)

        # Définition de la taille fixe du widget
        self.setFixedSize(500, 250)


    def skip_forward_10s(self):
        # Skip forward by 10 seconds
        position = self.media_player.position() + 10000  # 10 seconds in milliseconds
        self.media_player.setPosition(position)

    def skip_backward_10s(self):
        # Skip backward by 10 seconds
        position = max(0, self.media_player.position() - 10000)  # 10 seconds in milliseconds
        self.media_player.setPosition(position)

    def load_audio_files(self):
        # Ouvrir une boîte de dialogue pour sélectionner des fichiers audio
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Sélectionner PLayListe", "", "Fichiers audio (*.mp3 *.wav)")
        if file_paths:
            # Créer une liste de lecture à partir des fichiers sélectionnés
            self.playlist = [QMediaContent(QUrl.fromLocalFile(file)) for file in file_paths]
            self.current_index = 0
            self.play_current_audio()

    def toggle_play_pause(self):
        # Basculer entre lecture et pause, mettre à jour l'icône du bouton en conséquence
        if self.playlist:
            if self.is_playing:
                self.media_player.pause()
                self.play_button.setText("Play")
            else:
                self.media_player.play()
                self.play_button.setText("Pause")
            self.is_playing = not self.is_playing

    def play_current_audio(self):
        # Lire l'audio actuel de la liste de lecture
        if self.playlist:
            media_content = self.playlist[self.current_index]
            self.media_player.setMedia(media_content)

            # Mettre à jour le nom de fichier affiché
            filename = QFileInfo(self.playlist[self.current_index].canonicalUrl().toLocalFile()).fileName()
            self.filename_label.setText(f"Fichier chargé : {filename}")

            if self.is_playing:
                self.media_player.play()

            # Réinitialiser le curseur de position
            self.position_slider.setValue(0)

    def play_next_audio(self):
        # Lire l'audio suivant de la liste de lecture
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play_current_audio()

    def play_previous_audio(self):
        # Lire l'audio précédent de la liste de lecture
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play_current_audio()

    def set_volume(self, value):
        # Définir le volume du lecteur multimédia
        self.media_player.setVolume(value)

    def set_speed(self, value):
        # Définir la vitesse de lecture du lecteur multimédia
        speed_factor = value / 100.0
        self.media_player.setPlaybackRate(speed_factor)

    def set_position(self):
        # Définir la position de lecture en fonction du curseur de position
        duration = self.media_player.duration()
        if duration > 0:
            position = int((self.position_slider.value() / 100.0) * duration)
            self.media_player.setPosition(position)

    def update_duration(self, duration):
        # Mettre à jour la durée du lecteur multimédia
        if duration > 0:
            self.position_slider.setMaximum(100)

    def update_position(self, position):
        # Mettre à jour la position du lecteur multimédia et du curseur de position
        duration = self.media_player.duration()
        if duration > 0:
            progress = int((position / duration) * 100)
            self.position_slider.setValue(progress)

            # Mettre à jour la position affichée en minutes et secondes
            current_minutes = position // 60000
            current_seconds = (position // 1000) % 60
            self.position_slider_layout.itemAt(0).widget().setText(f"{current_minutes}:{current_seconds:02}")

    def update_duration_display(self, duration):
        # Mettre à jour la durée affichée en minutes et secondes
        if duration > 0:
            total_minutes = duration // 60000
            total_seconds = (duration // 1000) % 60
            self.position_slider_layout.itemAt(0).widget().setText(f"0:00")
            self.position_slider_layout.itemAt(2).widget().setText(f"{total_minutes}:{total_seconds:02}")

# Exécuter l'application
if __name__ == "__main__":
    app = QApplication([])
    player = AudioPlayer()
    player.show()
    app.exec_()
