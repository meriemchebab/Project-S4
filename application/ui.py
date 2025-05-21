import sys
import warnings
import numpy as np
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
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

class PlotCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=8, height=8, dpi=100, dark_mode=False):
        self.fig = Figure(figsize=(width, height), dpi=dpi)  # Increased height
        self.ax = None
        super().__init__(self.fig)
        self.setParent(parent)
        
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

        self.current_data_x = None
        self.current_data_y = None
        self.current_plot_type = '2d_line' 
        self.current_cmap = 'viridis' 
        self.current_line_color = 'blue'
        self.dark_mode = dark_mode
        self.update_figure_style()
        
    def update_figure_style(self):
        if self.dark_mode:
            self.fig.patch.set_facecolor('#2D2D30')
            if self.ax:
                self.ax.set_facecolor('#2D2D30')
                self.ax.tick_params(colors='#E0E0E0')
                self.ax.xaxis.label.set_color('#E0E0E0')
                self.ax.yaxis.label.set_color('#E0E0E0')
                self.ax.title.set_color('#E0E0E0')
                for spine in self.ax.spines.values():
                    spine.set_color('#555555')
        else:
            self.fig.patch.set_facecolor('#FFFFFF')
            if self.ax:
                self.ax.set_facecolor('#FFFFFF')
                self.ax.tick_params(colors='#333333')
                self.ax.xaxis.label.set_color('#333333')
                self.ax.yaxis.label.set_color('#333333')
                self.ax.title.set_color('#333333')
                for spine in self.ax.spines.values():
                    spine.set_color('#CCCCCC')
        self.draw()

    def toggle_dark_mode(self, is_dark):
        self.dark_mode = is_dark
        self.update_figure_style()
        if self.current_plot_type == '2d_line' and hasattr(self, 'current_data_y_original_example'):
            self.plot_example_data()
        elif self.current_plot_type == '3d_surface':
            self.plot_3d_example()

    def setup_default_2d_axes(self):
        if self.ax is None or not hasattr(self.ax, 'plot'):
            self.fig.clear()
            self.ax = self.fig.add_subplot(111)
        self.current_plot_type = '2d_line'
        self.update_figure_style()

    def plot_example_data(self, smoothness_factor=None):
        self.setup_default_2d_axes()
        self.ax.clear()
        
        x = np.linspace(0, 2 * np.pi, 150)
        y = np.sin(x)

        self.current_data_x = x 
        self.current_data_y_original_example = y 
        y_to_plot = np.copy(self.current_data_y_original_example)

        if smoothness_factor is not None and smoothness_factor > 0:
            window_size = max(1, int(smoothness_factor / 10)) * 2 + 1 
            if window_size > 1 and len(y_to_plot) > window_size:
                y_to_plot = np.convolve(y_to_plot, np.ones(window_size)/window_size, mode='same')
        
        self.ax.plot(self.current_data_x, y_to_plot, color=self.current_line_color)
        self.ax.set_title('2D Example Plot')
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.ax.grid(True)
        self.update_figure_style()
        self.draw()

    def update_plot_smoothness(self, value):
        if self.current_plot_type == '2d_line' and self.current_data_x is not None and hasattr(self, 'current_data_y_original_example'):
            self.ax.clear()
            
            y_to_smooth = np.copy(self.current_data_y_original_example) 

            if value > 0:
                window_size = max(1, int(value / 10)) * 2 + 1 
                if window_size > 1 and len(y_to_smooth) > window_size:
                    smoothed_y = np.convolve(y_to_smooth, np.ones(window_size)/window_size, mode='same')
                else:
                    smoothed_y = y_to_smooth
            else:
                smoothed_y = y_to_smooth
            
            self.ax.plot(self.current_data_x, smoothed_y, color=self.current_line_color)
            self.ax.set_title(f'2D Smoothed Plot (Factor: {value})')
            self.ax.set_xlabel('X-axis')
            self.ax.set_ylabel('Y-axis')
            self.ax.grid(True)
            self.update_figure_style()
            self.draw()
        elif self.current_plot_type == 'image':
            print(f"Smoothing not implemented for {self.current_plot_type} yet.")
        else:
            print("No active 2D line plot with example data to smooth.")

    def change_colormap(self, cmap_name):
        self.current_cmap = cmap_name 

        if self.ax is None: return

        if self.current_plot_type == '2d_line' and self.current_data_x is not None and hasattr(self, 'current_data_y_original_example'):
            self.ax.clear()
            try:
                cmap_obj = plt.get_cmap(cmap_name)
                self.current_line_color = cmap_obj(0.5) 
            except ValueError:
                print(f"Warning: Colormap '{cmap_name}' not recognized. Using previous line color.")
            
            self.ax.plot(self.current_data_x, self.current_data_y_original_example, color=self.current_line_color)
            self.ax.set_title(f'2D Plot (Colormap: {cmap_name})')
            self.ax.set_xlabel('X-axis')
            self.ax.set_ylabel('Y-axis')
            self.ax.grid(True)
            self.update_figure_style()
            self.draw()
        elif self.current_plot_type == '3d_surface':
            found_surface = False
            if hasattr(self.ax, 'collections'):
                for artist in self.ax.collections:
                    if isinstance(artist, Poly3DCollection):
                        artist.set_cmap(self.current_cmap)
                        found_surface = True
                        break
            if found_surface:
                self.update_figure_style()
                self.draw()
                print(f"3D plot colormap changed to {self.current_cmap}")
            else:
                print(f"Could not directly update 3D colormap. Replotting 3D example with {self.current_cmap}.")
                self.plot_3d_example() 
        
        elif self.current_plot_type == 'image':
            print(f"Colormap change for {self.current_plot_type} (image) placeholder.")
        else:
            print(f"Cannot change colormap for plot type: {self.current_plot_type} or data not present.")

    def plot_3d_example(self):
        self.fig.clear() 
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.current_plot_type = '3d_surface'

        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X**2 + Y**2)
        Z = np.sin(R)
        
        self.current_3d_data = (X,Y,Z) 
        self.ax.plot_surface(X, Y, Z, cmap=self.current_cmap) 
        self.ax.set_title('3D Example Plot')
        self.update_figure_style()
        self.draw()

class PlotMasterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Plot Master Pro")
        self.setMinimumSize(1000, 800)  # Increased height for the window
        
        self.colormaps_tab1 = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'winter', 'autumn', 'spring', 'summer']
        self.current_cmap_index_tab1 = 0
        self.dark_mode = False

        self.setup_ui()
        self.apply_styles()
        self.connect_signals()

        # Load external QSS style for the whole app (including NavigationToolbar)
        self.apply_external_qss()

        if hasattr(self, 'canvas1'):
            self.canvas1.plot_example_data()

    def apply_external_qss(self):
        # Directly apply QToolButton and QToolBox styles (no file reading)
        style = '''
QToolButton 
{
    background-color: transparent;
    color: #ffffff;
    padding: 6px;
    margin-left: 3px;
}
QToolButton:hover
{
    background-color: rgba(70,162,218,50%);
    border: 1px solid #46a2da;
    color: #000000;
}
QToolButton:pressed
{
    background-color: #727272;
    border: 1px solid #46a2da;
}
QToolButton:checked
{
    background-color: #727272;
    border: 1px solid #222;
}
QToolBox {
    background-color: #1e3c72; /* Solid background for toolbox */
    border: 1px solid #1d1d1d;
}
QToolBox::tab {
    background-color: #002b2b; /* Solid tab background */
    border: 1px solid #1d1d1d;
}
QToolBox::tab:hover {
    background-color: #006d6d;
    border: 1px solid #1d1d1d;
}
'''
        self.setStyleSheet(self.styleSheet() + '\n' + style)

    def setup_ui(self):
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.grid_layout = QGridLayout(self.centralwidget)
        self.grid_layout.setContentsMargins(15, 15, 15, 15)
        self.grid_layout.setSpacing(10)
        
        self.vertical_layout = QVBoxLayout()
        
        # Sidebar buttons
        self.import_button = QPushButton("Import Data")
        self.import_button.setIcon(self.style().standardIcon(getattr(QStyle, "SP_DialogOpenButton", QStyle.SP_DialogOpenButton)))
        
        self.usb_button = QPushButton("Read from USB")
        self.usb_button.setIcon(self.style().standardIcon(getattr(QStyle, "SP_DriveHDIcon", QStyle.SP_DriveHDIcon)))
        
        
        
        # Modified display mode button with menu
        self.display_mode_button = QPushButton("2D Split Planes")
        self.display_mode_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowDown))
        self.display_mode_button.setStyleSheet(COMBO_BUTTON_STYLE_TEMPLATE.format(
            primary_color=PRIMARY_COLOR,
            button_text_color=BUTTON_TEXT_COLOR,
            accent_color=ACCENT_COLOR,
            darker_accent="#2A4FBD"
        ))
        
        # Create menu for display mode button
        self.display_mode_menu = QMenu(self)
        self.display_mode_menu.addAction("2D Split Planes")
        self.display_mode_menu.addAction("2D Both Planes")
        self.display_mode_button.setMenu(self.display_mode_menu)
        
        self.plot_3d_button = QPushButton("Plot 3D")
        self.plot_3d_button.setIcon(self.style().standardIcon(getattr(QStyle, "SP_ToolBarVerticalExtensionButton", QStyle.SP_ToolBarVerticalExtensionButton)))
        
       
        self.save_button = QPushButton("Save Plot")
        self.save_button.setIcon(self.style().standardIcon(getattr(QStyle, "SP_DialogSaveButton", QStyle.SP_DialogSaveButton)))
        
        self.offset_button = QPushButton("Apply Offset")
        self.offset_button.setIcon(self.style().standardIcon(getattr(QStyle, "SP_ArrowDown", QStyle.SP_ArrowDown)))

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

        # Top Navigation and Controls for Tab 1
        nav_bar_layout1 = QHBoxLayout()
        
        # Modern zoom buttons
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

        # Plot Canvas and Matplotlib Toolbar for Tab 1
        self.canvas1 = PlotCanvas(self.tab1, width=8, height=6)
        self.nav_toolbar1 = NavigationToolbar(self.canvas1, self.tab1)
        tab1_layout.addWidget(self.nav_toolbar1)
        tab1_layout.addWidget(self.canvas1)

        # Smoothing Controls for Tab 1
        smoothing_controls_layout1 = QHBoxLayout()
        self.smooth_label1 = QLabel("Smooth the plot")
        self.smoothness_slider1 = QSlider(Qt.Horizontal)
        self.smoothness_slider1.setRange(0, 100)
        self.smoothness_slider1.setValue(50)
        
        smoothing_controls_layout1.addStretch(1)
        smoothing_controls_layout1.addWidget(self.smooth_label1)
        smoothing_controls_layout1.addWidget(self.smoothness_slider1, 2)
        smoothing_controls_layout1.addStretch(1)
        tab1_layout.addLayout(smoothing_controls_layout1)

        # Navigation buttons for Tab 1
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

        # Top Navigation and Controls for Tab 2 (same as Tab 1)
        nav_bar_layout2 = QHBoxLayout()
        
        self.zoom_in_button2 = QPushButton()
        self.zoom_in_button2.setIcon(QIcon.fromTheme("zoom-in"))
        self.zoom_in_button2.setToolTip("Zoom In")
        
        self.zoom_out_button2 = QPushButton()
        self.zoom_out_button2.setIcon(QIcon.fromTheme("zoom-out"))
        self.zoom_out_button2.setToolTip("Zoom Out")
        
        self.color_button2 = QPushButton("Change Plot Color")

        nav_bar_layout2.addStretch(1)
        nav_bar_layout2.addWidget(self.zoom_in_button2)
        nav_bar_layout2.addWidget(self.zoom_out_button2)
        nav_bar_layout2.addWidget(self.color_button2)
        tab2_layout.addLayout(nav_bar_layout2)

        # Plot Canvas and Matplotlib Toolbar for Tab 2
        self.canvas2 = PlotCanvas(self.tab2, width=8, height=6)
        self.nav_toolbar2 = NavigationToolbar(self.canvas2, self.tab2)
        tab2_layout.addWidget(self.nav_toolbar2)
        tab2_layout.addWidget(self.canvas2)

        # Smoothing Controls for Tab 2
        smoothing_controls_layout2 = QHBoxLayout()
        self.smooth_label2 = QLabel("Smooth the plot")
        self.smoothness_slider2 = QSlider(Qt.Horizontal)
        self.smoothness_slider2.setRange(0, 100)
        self.smoothness_slider2.setValue(50)
        
        smoothing_controls_layout2.addStretch(1)
        smoothing_controls_layout2.addWidget(self.smooth_label2)
        smoothing_controls_layout2.addWidget(self.smoothness_slider2, 2)
        smoothing_controls_layout2.addStretch(1)
        tab2_layout.addLayout(smoothing_controls_layout2)

        # Navigation buttons for Tab 2
        navigation_layout2 = QHBoxLayout()
        self.back_button2 = QPushButton("Back")
        self.next_button2 = QPushButton("Next")
        navigation_layout2.addWidget(self.back_button2)
        navigation_layout2.addStretch(1)
        navigation_layout2.addWidget(self.next_button2)
        tab2_layout.addLayout(navigation_layout2)

        # Add tab widget to grid
        self.grid_layout.addWidget(self.tab_widget, 0, 1)
        
        # Set column stretch factors
        self.grid_layout.setColumnStretch(0, 0)
        self.grid_layout.setColumnStretch(1, 1)
        
        # Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

    def apply_styles(self):
        self.update_theme_styles()
        if hasattr(self, 'smoothness_slider1'):
            self.smoothness_slider1.setStyleSheet(self.get_slider_style())
        if hasattr(self, 'smoothness_slider2'):
            self.smoothness_slider2.setStyleSheet(self.get_slider_style())

    def update_theme_styles(self):
        if self.dark_mode:
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
            border_hover = "#777777"
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
            border_hover = "#A6B0B8"
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
        
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {secondary_color};
            }}
            QWidget {{
                background-color: {secondary_color};
            }}
            QLabel {{
                color: {text_color};
                font-size: 13px;
                background-color: transparent;
            }}
            QMenuBar {{
                background-color: {tab_bg};
                color: {text_color};
            }}
            QMenuBar::item:selected {{
                background-color: {primary_color};
                color: {button_text_color};
            }}
            QMenu {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                color: {text_color};
            }}
            QMenu::item:selected {{
                background-color: {primary_color};
                color: {button_text_color};
            }}
            QStatusBar {{
                background-color: {tab_bg};
                color: {text_color};
            }}
            QCheckBox {{
                color: {text_color};
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 1px solid {border_color};
                border-radius: 3px;
                background-color: {bg_color};
            }}
            QCheckBox::indicator:checked {{
                background-color: {primary_color};
                border-color: {primary_color};
            }}
        """)
        
        # Apply styles to all buttons
        for button in self.findChildren(QPushButton):
            if button in [self.back_button1, self.next_button1, self.back_button2, self.next_button2]:
                button.setStyleSheet(nav_button_style)
            elif button == self.display_mode_button:
                button.setStyleSheet(combo_button_style)
            else:
                button.setStyleSheet(button_style)
            
            # Ensure icons are visible
            palette = button.palette()
            palette.setColor(QPalette.ButtonText, QColor(button_text_color))
            button.setPalette(palette)
        
        self.tab_widget.setStyleSheet(tab_style)
        
        # Update canvas theme
        if hasattr(self, 'canvas1'):
            self.canvas1.toggle_dark_mode(self.dark_mode)
        if hasattr(self, 'canvas2'):
            self.canvas2.toggle_dark_mode(self.dark_mode)

    def get_slider_style(self):
        if self.dark_mode:
            return SLIDER_STYLE_TEMPLATE.format(
                border_color="#555555",
                groove_bg="#444444",
                primary_color=DARK_PRIMARY_COLOR,
                accent_color=DARK_ACCENT_COLOR
            )
        else:
            return SLIDER_STYLE_TEMPLATE.format(
                border_color="#C0C0C0",
                groove_bg="#E0E0E0",
                primary_color=PRIMARY_COLOR,
                accent_color=ACCENT_COLOR
            )

    def connect_signals(self):
        # Connect main buttons
        self.import_button.clicked.connect(self.import_data_action)
        self.usb_button.clicked.connect(self.read_from_usb_action)
        self.plot_3d_button.clicked.connect(self.plot_3d_on_canvas1)
        self.save_button.clicked.connect(self.save_plot_action)
        self.offset_button.clicked.connect(self.apply_offset_action)
        self.theme_toggle.stateChanged.connect(self.toggle_theme)
        
        # Connect signals for tab1 components
        if hasattr(self, 'smoothness_slider1'):
            self.smoothness_slider1.valueChanged.connect(self.canvas1.update_plot_smoothness)
        if hasattr(self, 'color_button1'):
            self.color_button1.clicked.connect(lambda: self.change_plot_color(self.canvas1))
        if hasattr(self, 'zoom_in_button1'):
            self.zoom_in_button1.clicked.connect(self.zoom_in_action)
        if hasattr(self, 'zoom_out_button1'):
            self.zoom_out_button1.clicked.connect(self.zoom_out_action)
        if hasattr(self, 'back_button1'):
            self.back_button1.clicked.connect(self.go_back_action)
        if hasattr(self, 'next_button1'):
            self.next_button1.clicked.connect(self.go_next_action)

        # Connect signals for tab2 components
        if hasattr(self, 'smoothness_slider2'):
            self.smoothness_slider2.valueChanged.connect(self.canvas2.update_plot_smoothness)
        if hasattr(self, 'color_button2'):
            self.color_button2.clicked.connect(lambda: self.change_plot_color(self.canvas2))
        if hasattr(self, 'zoom_in_button2'):
            self.zoom_in_button2.clicked.connect(self.zoom_in_action)
        if hasattr(self, 'zoom_out_button2'):
            self.zoom_out_button2.clicked.connect(self.zoom_out_action)
        if hasattr(self, 'back_button2'):
            self.back_button2.clicked.connect(self.go_back_action)
        if hasattr(self, 'next_button2'):
            self.next_button2.clicked.connect(self.go_next_action)
        if hasattr(self, 'render_3d_button_tab2'):
            self.render_3d_button_tab2.clicked.connect(self.canvas2.plot_3d_example)

    def toggle_theme(self, state):
        self.dark_mode = bool(state)
        self.update_theme_styles()
        self.statusBar.showMessage(f"{'Dark' if self.dark_mode else 'Light'} mode enabled")

    def zoom_in_action(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab == self.tab1:
            canvas = self.canvas1
        else:
            canvas = self.canvas2
            
        if canvas and hasattr(canvas, 'ax'):
            canvas.ax.set_xlim([x*0.9 for x in canvas.ax.get_xlim()])
            canvas.ax.set_ylim([y*0.9 for y in canvas.ax.get_ylim()])
            canvas.draw()
            self.statusBar.showMessage("Zoomed in")

    def zoom_out_action(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab == self.tab1:
            canvas = self.canvas1
        else:
            canvas = self.canvas2
            
        if canvas and hasattr(canvas, 'ax'):
            canvas.ax.set_xlim([x*1.1 for x in canvas.ax.get_xlim()])
            canvas.ax.set_ylim([y*1.1 for y in canvas.ax.get_ylim()])
            canvas.draw()
            self.statusBar.showMessage("Zoomed out")

    def go_back_action(self):
        self.statusBar.showMessage("Back button pressed")
        print("Back button action")

    def go_next_action(self):
        self.statusBar.showMessage("Next button pressed")
        print("Next button action")

    def change_plot_color(self, canvas):
        self.statusBar.showMessage("Change Plot Color clicked")
        if canvas == self.canvas1:
            self.current_cmap_index_tab1 = (self.current_cmap_index_tab1 + 1) % len(self.colormaps_tab1)
            new_cmap_name = self.colormaps_tab1[self.current_cmap_index_tab1]
        else:
            self.current_cmap_index_tab1 = (self.current_cmap_index_tab1 + 1) % len(self.colormaps_tab1)
            new_cmap_name = self.colormaps_tab1[self.current_cmap_index_tab1]
        
        canvas.change_colormap(new_cmap_name)
        self.statusBar.showMessage(f"Colormap changed to {new_cmap_name}")

    def import_data_action(self):
        self.statusBar.showMessage("Import Data clicked")
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(f"Selected file: {fileName}")
            self.statusBar.showMessage(f"File selected: {fileName}")

    def read_from_usb_action(self):
        self.statusBar.showMessage("Read from USB clicked")
        QMessageBox.information(self, "USB Read", "Reading data from USB device...")
        print("Read from USB action")

    
    def plot_3d_on_canvas1(self):
        self.statusBar.showMessage("Plot 3D on Tab 1 clicked")
        self.canvas1.plot_3d_example()
        self.tab_widget.setCurrentWidget(self.tab1)

    
    def save_plot_action(self):
        self.statusBar.showMessage("Save Plot clicked")
        current_tab = self.tab_widget.currentWidget()
        if current_tab == self.tab1:
            canvas = self.canvas1
        else:
            canvas = self.canvas2
        
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()", "","PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)", options=options)
        if fileName:
            try:
                if not fileName.endswith(('.png', '.jpg', '.jpeg')):
                    fileName += '.png'
                
                canvas.fig.savefig(fileName, dpi=300, bbox_inches='tight')
                self.statusBar.showMessage(f"Plot saved to {fileName}")
            except Exception as e:
                self.statusBar.showMessage(f"Error saving plot: {str(e)}")

    def apply_offset_action(self):
        self.statusBar.showMessage("Apply Offset clicked")
        print("Apply Offset action")

    def check_offset_action(self):
        self.statusBar.showMessage("Check Offset clicked")
        print("Check Offset action")

    def open_settings_action(self):
        self.statusBar.showMessage("Settings clicked")
        print("Open Settings action")

# Note: Make sure to place your style.qss file in the same directory as this script or update the path in apply_external_qss().

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotMasterApp()
    window.show()
    sys.exit(app.exec())
