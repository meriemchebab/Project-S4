import sys
import time
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QLabel, QProgressBar, QPushButton)
from PySide6.QtCore import Qt, QSize, QTimer, Signal, Slot, QSettings, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon, QFont, QPainter, QPen, QColor, QBrush, QPainterPath, QPixmap
from urllib.request import urlopen  # Replace requests with urllib
from io import BytesIO

class ThemeManager:
    """Manages application theme (dark/light mode)"""
    def __init__(self):
        self.settings = QSettings("AntennaRay", "AntennaRay")  # Updated name
        self.dark_mode = self.settings.value("dark_mode", False, type=bool)
        
        # Define color palettes
        self.light_palette = {
            "background": "#FFFFFF",
            "text_primary": "#333333",
            "text_secondary": "#666666",
            "accent": "#135CF8",  # Updated to new blue color
            "progress_bg": "#E0E0E0",
            "progress_fill": "#4169E1",
            "logo_color": "#4169E1"
        }
        
        self.dark_palette = {
            "background": "#1A1A1A",
            "text_primary": "#FFFFFF",
            "text_secondary": "#AAAAAA",
            "accent": "#135CF8",  # Updated to new blue color
            "progress_bg": "#333333",
            "progress_fill": "#6495ED",
            "logo_color": "#6495ED"
        }
    
    def get_color(self, key):
        """Get color for the current theme"""
        palette = self.dark_palette if self.dark_mode else self.light_palette
        return palette.get(key, "#FFFFFF")
    
    def toggle_theme(self):
        """Toggle between light and dark mode"""
        self.dark_mode = not self.dark_mode
        self.settings.setValue("dark_mode", self.dark_mode)
        return self.dark_mode

class ThemeToggleButton(QPushButton):
    """Button to toggle between light and dark mode"""
    def __init__(self, theme_manager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.setFixedSize(48, 48)  # Increased button size
        self.setCursor(Qt.PointingHandCursor)
        
        # Load icons
        self.sun_icon = self.load_icon("https://hebbkx1anhila5yf.public.blob.vercel-storage.com/sun-spxpyHqsOu5QFIvjTI7NoIrzwZPKTy.png")
        self.moon_icon = self.load_icon("https://hebbkx1anhila5yf.public.blob.vercel-storage.com/moon-AWn88A7paB2J3jXpQHtxyb6oUKin3l.png")
        
        self.update_icon()
        
        # Connect the clicked signal
        self.clicked.connect(self.toggle_theme)
    
    def load_icon(self, url):
        """Load icon from URL using urllib"""
        try:
            response = urlopen(url)
            pixmap = QPixmap()
            pixmap.loadFromData(response.read())
            return QIcon(pixmap)
        except Exception as e:
            print(f"Error loading icon: {e}")
            return QIcon()
    
    def toggle_theme(self):
        """Toggle the theme and update the icon"""
        self.theme_manager.toggle_theme()
        self.update_icon()
    
    def update_icon(self):
        """Update the icon based on the current theme"""
        if self.theme_manager.dark_mode:
            self.setIcon(self.sun_icon)
            self.setToolTip("Switch to Light Mode")
        else:
            self.setIcon(self.moon_icon)
            self.setToolTip("Switch to Dark Mode")
        self.setIconSize(QSize(36, 36))  # Increased icon size

class LogoWidget(QWidget):
    """Custom widget to draw the AntennaRay logo"""
    def __init__(self, theme_manager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.setFixedSize(120, 120)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Get logo color based on theme
        logo_color = QColor(self.theme_manager.get_color("logo_color"))
        
        # Draw circle
        painter.setPen(QPen(logo_color, 4))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(10, 10, 100, 100)
        
        # Draw wave inside circle
        path = QPainterPath()
        path.moveTo(35, 40)
        path.cubicTo(45, 80, 60, 20, 85, 60)
        
        painter.setPen(QPen(logo_color, 4))
        painter.drawPath(path)

class SplashScreen(QWidget):
    """Splash screen with progress bar and theme toggle"""
    def __init__(self, on_finish=None):
        super().__init__()
        self.on_finish = on_finish
        self.setWindowTitle("AntennaRay")  # Updated name
        self.setFixedSize(800, 500)
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        # Theme manager
        self.theme_manager = ThemeManager()
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Header with theme toggle
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.addStretch()
        
        self.theme_toggle = ThemeToggleButton(self.theme_manager)
        header_layout.addWidget(self.theme_toggle)
        
        main_layout.addLayout(header_layout)
        
        # Logo from SVG
        logo_label = QLabel()
        pixmap = QPixmap("logo vertical.svg")  # Ensure this file exists in the same directory or provide the full path
        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)
        
        
        # Welcome message
        self.welcome_label = QLabel("Welcome to PlotMaster, your advanced tool for 2D\nand 3D data visualization")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setFont(QFont("Arial", 14))
        main_layout.addWidget(self.welcome_label)

        # Spacer
        main_layout.addSpacing(40)
        
        # Loading status
        loading_layout = QHBoxLayout()
        
        self.loading_label = QLabel("Loading application...")
        self.loading_label.setFont(QFont("Arial", 12))
        loading_layout.addWidget(self.loading_label)
        
        loading_layout.addStretch()
        
        self.progress_label = QLabel("0%")
        self.progress_label.setFont(QFont("Arial", 12))
        loading_layout.addWidget(self.progress_label)
        
        main_layout.addLayout(loading_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(10)
        main_layout.addWidget(self.progress_bar)
        
        self.setLayout(main_layout)
        
        # Apply theme
        self.apply_theme()
        
        # Connect theme toggle
        self.theme_toggle.clicked.connect(self.apply_theme)
        
        # Timer for progress simulation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50)
        
        # Center on screen
        self.center_on_screen()
    
    def apply_theme(self):
        """Apply the current theme to all widgets"""
        bg_color = self.theme_manager.get_color("background")
        text_primary = self.theme_manager.get_color("text_primary")
        text_secondary = self.theme_manager.get_color("text_secondary")
        progress_bg = self.theme_manager.get_color("progress_bg")
        progress_fill = self.theme_manager.get_color("progress_fill")
        
        # Set background color
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
            }}
            QLabel {{
                color: {text_primary};
                background-color: transparent;
            }}
            QPushButton {{
                background-color: transparent;
                border: none;
            }}
            QProgressBar {{
                background-color: {progress_bg};
                border: none;
                border-radius: 5px;
            }}
            QProgressBar::chunk {{
                background-color: {progress_fill};
                border-radius: 5px;
            }}
        """)
        
        # Update specific widgets
        self.loading_label.setStyleSheet(f"color: {text_secondary};")
        self.progress_label.setStyleSheet(f"color: {text_secondary};")
    
    def update_progress(self):
        """Update progress bar value"""
        current_value = self.progress_bar.value()
        
        if current_value < 100:
            new_value = current_value + 1
            self.progress_bar.setValue(new_value)
            self.progress_label.setText(f"{new_value}%")
        else:
            self.timer.stop()
            if self.on_finish:
                # Start fade-out animation before closing
                self.start_fade_out()

    def start_fade_out(self):
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(700)
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_anim.finished.connect(self.finish_and_close)
        self.fade_anim.start()

    def finish_and_close(self):
        if self.on_finish:
            self.on_finish()
        self.close()
    
    def center_on_screen(self):
        """Center the window on the screen"""
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
    
    def mousePressEvent(self, event):
        """Enable dragging the window"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Move the window when dragged"""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec())