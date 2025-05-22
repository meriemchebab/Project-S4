import sys
import warnings
import numpy as np
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QPushButton, QTabWidget, QSlider, QLabel, QComboBox, QFileDialog, 
    QStatusBar, QSizePolicy, QMessageBox, QStyle, QCheckBox, QMenu
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPalette, QColor, QIcon, QAction

# Suppress specific warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
matplotlib.pyplot._INSTALL_FIG_OBSERVER = False

# Updated color scheme
PRIMARY_COLOR = "#4169E1"
SECONDARY_COLOR = "#F3F3F3"
ACCENT_COLOR = "#3A5FCD"
TEXT_COLOR = "#333333"
BUTTON_TEXT_COLOR = "#FFFFFF"

# Dark mode colors
DARK_PRIMARY_COLOR = "#4169E1"
DARK_SECONDARY_COLOR = "#2D2D30"
DARK_ACCENT_COLOR = "#3A5FCD"
DARK_TEXT_COLOR = "#E0E0E0"
DARK_BUTTON_TEXT_COLOR = "#FFFFFF"

# Style templates
BUTTON_STYLE_TEMPLATE = """
    QPushButton {{
        background-color: {primary_color};
        color: {button_text_color};
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 10px 15px;
        font-size: 13px;
        min-height: 32px;
    }}
    QPushButton:hover {{
        background-color: {accent_color};
    }}
    QPushButton:pressed {{
        background-color: {darker_accent};
    }}
    QPushButton:disabled {{
        background-color: #BDBDBD;
        color: #757575;
    }}
"""

COMBO_BUTTON_STYLE_TEMPLATE = """
    QPushButton {{
        background-color: {primary_color};
        color: {button_text_color};
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 10px 15px 10px 12px;
        font-size: 13px;
        min-height: 32px;
        text-align: left;
        padding-right: 30px;
    }}
    QPushButton:hover {{
        background-color: {accent_color};
    }}
    QPushButton:pressed {{
        background-color: {darker_accent};
    }}
    QPushButton::menu-indicator {{
        subcontrol-origin: padding;
        subcontrol-position: right center;
        width: 20px;
    }}
"""

NAV_BUTTON_STYLE_TEMPLATE = """
    QPushButton {{
        background-color: {nav_color};
        color: {button_text_color};
        font-weight: normal;
        border: none;
        border-radius: 5px;
        padding: 8px 12px;
        font-size: 13px;
    }}
    QPushButton:hover {{
        background-color: {nav_hover};
    }}
    QPushButton:pressed {{
        background-color: {nav_pressed};
    }}
"""

SLIDER_STYLE_TEMPLATE = """
    QSlider::groove:horizontal {{
        border: 1px solid {border_color};
        height: 6px;
        background: {groove_bg};
        margin: 2px 0;
        border-radius: 3px;
    }}
    QSlider::handle:horizontal {{
        background: {primary_color};
        border: 1px solid {accent_color};
        width: 16px;
        margin: -5px 0;
        border-radius: 8px;
    }}
    QSlider::handle:horizontal:hover {{
        background: {accent_color};
    }}
"""

TAB_STYLE_TEMPLATE = """
    QTabWidget::pane {{
        border: 1px solid {border_color};
        border-top: none;
        border-radius: 0 0 5px 5px;
        padding: 10px;
        background: {bg_color};
    }}
    QTabBar::tab {{
        background: {tab_bg};
        border: 1px solid {border_color};
        border-bottom: none;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        padding: 10px 20px;
        min-width: 120px;
        font-weight: bold;
        color: {tab_text};
    }}
    QTabBar::tab:selected {{
        background: {selected_bg};
        border-color: {border_color};
        color: {primary_color};
    }}
    QTabBar::tab:hover:!selected {{
        background: {tab_hover};
    }}
    QTabBar::tab:!selected {{
        margin-top: 2px;
    }}
"""

class Ui_Window(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Plot Master Pro")
        MainWindow.setMinimumSize(1000, 800)
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.grid_layout = QGridLayout(self.centralwidget)
        self.grid_layout.setContentsMargins(15, 15, 15, 15)
        self.grid_layout.setSpacing(10)

        self.vertical_layout = QVBoxLayout()
        # Sidebar buttons
        self.import_button = QPushButton("Import Data")
        self.import_button.setIcon(MainWindow.style().standardIcon(getattr(QStyle, "SP_DialogOpenButton", QStyle.SP_DialogOpenButton)))
        self.usb_button = QPushButton("Read from USB")
        self.usb_button.setIcon(MainWindow.style().standardIcon(getattr(QStyle, "SP_DriveHDIcon", QStyle.SP_DriveHDIcon)))
        self.display_mode_button = QPushButton("2D Split Planes")
        
        
        # Create menu for display mode button
        self.display_mode_menu = QMenu()
        self.display_mode_menu.addAction("2D Split Planes")
        self.display_mode_menu.addAction("2D Both Planes")
        self.display_mode_button.setMenu(self.display_mode_menu)
        
        self.plot_3d_button = QPushButton("Plot 3D")
        self.plot_3d_button.setIcon(MainWindow.style().standardIcon(getattr(QStyle, "SP_ToolBarVerticalExtensionButton", QStyle.SP_ToolBarVerticalExtensionButton)))
        self.save_button = QPushButton("Save Plot")
        self.save_button.setIcon(MainWindow.style().standardIcon(getattr(QStyle, "SP_DialogSaveButton", QStyle.SP_DialogSaveButton)))
        self.offset_button = QPushButton("Apply Offset")
        self.offset_button.setCheckable(True)
        self.offset_button.setIcon(MainWindow.style().standardIcon(getattr(QStyle, "SP_ArrowDown", QStyle.SP_ArrowDown)))
        # Theme toggle
        self.theme_layout = QHBoxLayout()
        self.theme_label = QLabel("Dark Mode:")
        self.theme_toggle = QCheckBox()
        self.theme_toggle.setChecked(False)
        self.theme_layout.addWidget(self.theme_label)
        self.theme_layout.addWidget(self.theme_toggle)
        self.vertical_layout.addWidget(self.import_button)
        self.vertical_layout.addWidget(self.usb_button)
        self.vertical_layout.addWidget(self.display_mode_button)
        self.vertical_layout.addWidget(self.plot_3d_button)
        self.vertical_layout.addWidget(self.save_button)
        self.vertical_layout.addWidget(self.offset_button)
        self.vertical_layout.addLayout(self.theme_layout)
        self.vertical_layout.addStretch(1)
        self.grid_layout.addLayout(self.vertical_layout, 0, 0)
        # Create tab widget
        self.tab_widget = QTabWidget()
        # --- Tab 1: 2D Visualization ---
        self.tab1 = QWidget()
        self.tab_widget.addTab(self.tab1, "2D Visualization")
        tab1_layout = QVBoxLayout(self.tab1)
        nav_bar_layout1 = QHBoxLayout()
        self.zoom_in_button1 = QPushButton()
        self.zoom_in_button1.setIcon(QIcon.fromTheme("zoom-in"))
        self.zoom_in_button1.setToolTip("Zoom In")
        self.zoom_out_button1 = QPushButton()
        self.zoom_out_button1.setIcon(QIcon.fromTheme("zoom-out"))
        self.zoom_out_button1.setToolTip("Zoom Out")
        self.color_button1 = QPushButton("Change Plot Color")
        nav_bar_layout1.addStretch(1)
        nav_bar_layout1.addWidget(self.zoom_in_button1)
        nav_bar_layout1.addWidget(self.zoom_out_button1)
        nav_bar_layout1.addWidget(self.color_button1)
        tab1_layout.addLayout(nav_bar_layout1)
        # Placeholder for dynamic canvas and toolbar
        self.tab1_canvas_layout = QVBoxLayout()
        tab1_layout.addLayout(self.tab1_canvas_layout)
        # Smoothing Controls for Tab 1
        smoothing_controls_layout1 = QHBoxLayout()
        self.smooth_label1 = QLabel("Smooth the plot")
        self.smoothness_slider1 = QSlider(Qt.Horizontal)
        
        
        smoothing_controls_layout1.addStretch(1)
        smoothing_controls_layout1.addWidget(self.smooth_label1)
        smoothing_controls_layout1.addWidget(self.smoothness_slider1, 2)
        smoothing_controls_layout1.addStretch(1)
        tab1_layout.addLayout(smoothing_controls_layout1)
        navigation_layout1 = QHBoxLayout()
        self.back_button1 = QPushButton("Back")
        self.next_button1 = QPushButton("Next")
        navigation_layout1.addWidget(self.back_button1)
        navigation_layout1.addStretch(1)
        navigation_layout1.addWidget(self.next_button1)
        tab1_layout.addLayout(navigation_layout1)
        # --- Tab 2: 3D Visualization ---
        self.tab2 = QWidget()
        self.tab_widget.addTab(self.tab2, "3D Visualization")
        tab2_layout = QVBoxLayout(self.tab2)
        nav_bar_layout2 = QHBoxLayout()
        self.zoom_in_button2 = QPushButton()
        self.zoom_in_button2.setIcon(QIcon.fromTheme("zoom-in"))
        self.zoom_in_button2.setToolTip("Zoom In")
        self.zoom_out_button2 = QPushButton()
        self.zoom_out_button2.setIcon(QIcon.fromTheme("zoom-out"))
        self.zoom_out_button2.setToolTip("Zoom Out")
        self.color_button2 = QPushButton("Change Plot Color")
        self.color_button3D = QPushButton("Change 3D Plot Color")
        nav_bar_layout2.addStretch(1)
        nav_bar_layout2.addWidget(self.zoom_in_button2)
        nav_bar_layout2.addWidget(self.zoom_out_button2)
        nav_bar_layout2.addWidget(self.color_button2)
        tab2_layout.addLayout(nav_bar_layout2)
        # Placeholder for dynamic canvas and toolbar
        self.tab2_canvas_layout = QVBoxLayout()
        tab2_layout.addLayout(self.tab2_canvas_layout)
        smoothing_controls_layout2 = QHBoxLayout()
        self.smooth_label2 = QLabel("Smooth the plot")
        self.smoothness_slider2 = QSlider(Qt.Horizontal)
    
        smoothing_controls_layout2.addStretch(1)
        smoothing_controls_layout2.addWidget(self.smooth_label2)
        smoothing_controls_layout2.addWidget(self.smoothness_slider2, 2)
        smoothing_controls_layout2.addStretch(1)
        tab2_layout.addLayout(smoothing_controls_layout2)
        navigation_layout2 = QHBoxLayout()
        self.back_button2 = QPushButton("Back")
        self.next_button2 = QPushButton("Next")
        navigation_layout2.addWidget(self.back_button2)
        navigation_layout2.addStretch(1)
        navigation_layout2.addWidget(self.next_button2)
        tab2_layout.addLayout(navigation_layout2)
        # Add tab widget to grid
        self.grid_layout.addWidget(self.tab_widget, 0, 1)
        self.grid_layout.setColumnStretch(0, 0)
        self.grid_layout.setColumnStretch(1, 1)
        # Status Bar
        self.statusBar = QStatusBar()
        MainWindow.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

        self.theme_toggle.stateChanged.connect(self.toggle_dark_mode)
       
        self.is_dark_mode = False
        self.apply_styles()

    def apply_styles(self):
        if getattr(self, 'is_dark_mode', False):
            primary_color = DARK_PRIMARY_COLOR
            secondary_color = DARK_SECONDARY_COLOR
            accent_color = DARK_ACCENT_COLOR
            text_color = DARK_TEXT_COLOR
            button_text_color = DARK_BUTTON_TEXT_COLOR
            darker_accent = "#2A4FBD"
            border_color = "#555555"
            groove_bg = "#444444"
            tab_bg = "#3D3D40"
            selected_bg = "#2D2D30"
            tab_text = "#E0E0E0"
            tab_hover = "#4D4D50"
            bg_color = "#2D2D30"
            nav_color = "#4D4D50"
            nav_hover = "#5D5D60"
            nav_pressed = "#3D3D40"
        else:
            primary_color = PRIMARY_COLOR
            secondary_color = SECONDARY_COLOR
            accent_color = ACCENT_COLOR
            text_color = TEXT_COLOR
            button_text_color = BUTTON_TEXT_COLOR
            darker_accent = "#2A4FBD"
            border_color = "#D0D0D0"
            groove_bg = "#E0E0E0"
            tab_bg = "#E9ECEF"
            selected_bg = "#FFFFFF"
            tab_text = "#495057"
            tab_hover = "#DEE2E6"
            bg_color = "#FFFFFF"
            nav_color = "#6c757d"
            nav_hover = "#5a6268"
            nav_pressed = "#4e555b"

        button_style = BUTTON_STYLE_TEMPLATE.format(
            primary_color=primary_color,
            button_text_color=button_text_color,
            accent_color=accent_color,
            darker_accent=darker_accent
        )
        nav_button_style = NAV_BUTTON_STYLE_TEMPLATE.format(
            nav_color=nav_color,
            button_text_color=button_text_color,
            nav_hover=nav_hover,
            nav_pressed=nav_pressed
        )
        combo_button_style = COMBO_BUTTON_STYLE_TEMPLATE.format(
            primary_color=primary_color,
            button_text_color=button_text_color,
            accent_color=accent_color,
            darker_accent=darker_accent
        )
        tab_style = TAB_STYLE_TEMPLATE.format(
            border_color=border_color,
            bg_color=bg_color,
            tab_bg=tab_bg,
            tab_text=tab_text,
            selected_bg=selected_bg,
            primary_color=primary_color,
            tab_hover=tab_hover
        )
        self.centralwidget.setStyleSheet(f"background-color: {secondary_color};")
        self.tab_widget.setStyleSheet(tab_style)
        for button in self.centralwidget.findChildren(QPushButton):
            button.setStyleSheet(button_style)
        self.display_mode_button.setStyleSheet(combo_button_style)
        for button in [self.back_button1, self.next_button1, self.back_button2, self.next_button2]:
            button.setStyleSheet(nav_button_style)
        # Optionally style sliders, labels, etc.
        # Style NavigationToolbars if present
        if hasattr(self, 'toolbar1'):
            self.style_navigation_toolbar(self.toolbar1)
        if hasattr(self, 'toolbar2'):
            self.style_navigation_toolbar(self.toolbar2)

    def toggle_dark_mode(self, state):
        self.is_dark_mode = bool(state)
        self.apply_styles()

    def style_navigation_toolbar(self, toolbar):
        """Apply background and label/icon color to NavigationToolbar based on theme."""
        if getattr(self, 'is_dark_mode', False):
            bg_color = "#2D2D30"
            text_color = "#E0E0E0"
            icon_color = "#E0E0E0"
        else:
            bg_color = "#F3F3F3"
            text_color = "#000000"
            icon_color = "#333333"
        # Set background and text color for toolbar and its children
        toolbar.setStyleSheet(f"""
            QToolBar {{
                background: {bg_color};
                color: {text_color};
            }}
            QToolButton {{
                background: transparent;
                color: {icon_color};
            }}
            QLabel {{
                color: {text_color};
            }}
        """)
        # Optionally, update icons to use theme-appropriate QIcons here

