from matplotlib.figure import Figure 
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QPushButton, QTabWidget, QSlider, QLabel, QComboBox, QFileDialog, 
    QStatusBar, QSizePolicy, QMessageBox, QStyle, QCheckBox, QMenu,
    QColorDialog
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPalette, QColor, QIcon, QAction

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import mplcursors
import matplotlib.colors as mcolors

# Color scheme constants
PRIMARY_COLOR = "#135CF8"
SECONDARY_COLOR = "#F3F3F3"
ACCENT_COLOR = "#0E4BD4"
TEXT_COLOR = "#333333"
BUTTON_TEXT_COLOR = "#FFFFFF"

# Dark mode colors
DARK_PRIMARY_COLOR = "#135CF8"
DARK_SECONDARY_COLOR = "#2D2D30"
DARK_ACCENT_COLOR = "#0E4BD4"
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

TOOLBAR_STYLE_TEMPLATE = """
    QToolBar {{
        background-color: {toolbar_bg};
        border: 1px solid {border_color};
        border-radius: 5px;
        padding: 5px;
        spacing: 3px;
    }}
    QToolBar QToolButton {{
        background-color: {button_bg};
        border: 1px solid {border_color};
        border-radius: 3px;
        padding: 5px;
        margin: 2px;
    }}
    QToolBar QToolButton:hover {{
        background-color: {button_hover};
        border-color: {border_hover};
    }}
    QToolBar QToolButton:pressed {{
        background-color: {button_pressed};
    }}
"""

class Fig3D(FigureCanvas):
    def __init__(self, parent=None, figsize=(10, 8), dark_mode=False):
        # Create figure with appropriate size for the application
        fig = Figure(figsize=figsize, dpi=80, tight_layout=True)
        super().__init__(fig)
        if parent:
            self.setParent(parent)

        self.ax3 = self.figure.add_subplot(111, projection='3d')
        self._cbar = None
        self.cmap = 'plasma'
        self.dark_mode = dark_mode
        self.update_figure_style()

    def update_figure_style(self):
        """Update figure colors based on dark mode"""
        if self.dark_mode:
            self.figure.patch.set_facecolor('#2D2D30')
            self.ax3.set_facecolor('#2D2D30')
            self.ax3.tick_params(colors='#E0E0E0')
            self.ax3.xaxis.label.set_color('#E0E0E0')
            self.ax3.yaxis.label.set_color('#E0E0E0')
            self.ax3.zaxis.label.set_color('#E0E0E0')
            self.ax3.title.set_color('#E0E0E0')
            # Set pane colors for 3D plot
            self.ax3.xaxis.pane.fill = False
            self.ax3.yaxis.pane.fill = False
            self.ax3.zaxis.pane.fill = False
        else:
            self.figure.patch.set_facecolor('#FFFFFF')
            self.ax3.set_facecolor('#FFFFFF')
            self.ax3.tick_params(colors='#333333')
            self.ax3.xaxis.label.set_color('#333333')
            self.ax3.yaxis.label.set_color('#333333')
            self.ax3.zaxis.label.set_color('#333333')
            self.ax3.title.set_color('#333333')

    def toggle_dark_mode(self, is_dark):
        self.dark_mode = is_dark
        self.update_figure_style()
        self.draw()

    def plot_surface(self, X, Y, Z):
        self.ax3.clear()
        # Safely remove previous colorbar if it exists and is still valid
        if self._cbar:
            try:
                if hasattr(self._cbar, 'ax') and self._cbar.ax is not None:
                    self._cbar.remove()
            except Exception as e:
                print(f"Warning: Failed to remove previous colorbar: {e}")
            self._cbar = None

        surf = self.ax3.plot_surface(
            X, Y, Z,
            cmap=self.cmap,
            edgecolor='none',
            alpha=0.8
        )
        self._cbar = self.figure.colorbar(
            surf, ax=self.ax3, shrink=0.5,
            label='Radiation Intensity (linear)'
        )
        self.ax3.set_title('3D Antenna Radiation Pattern')
        self.ax3.set_xlabel('X')
        self.ax3.set_ylabel('Y')
        self.ax3.set_zlabel('Z')
        self.ax3.view_init(elev=30, azim=45)
        self.draw()
            
        
    def enable_click_annotation_3D(self, X, Y, Z):
        if self.ax3 is None:
            return

        # Création d'une annotation 2D dans l'espace de la figure
        self.annotation_box = self.fig.text(0.02, 0.92, '', fontsize=11,
                                          bbox=dict(facecolor='lightblue', alpha=0.6, edgecolor='black'))

        def on_click(event):
            if event.inaxes != self.ax3:
                return

            # Récupérer le clic en coordonnées x/y (pixels)
            x_click, y_click = event.x, event.y

            # Transformation 3D -> 2D pour tous les points
            from mpl_toolkits.mplot3d import proj3d
            min_dist = float('inf')
            closest_text = ""
            
            for i in range(X.shape[0]):
                for j in range(X.shape[1]):
                    x2D, y2D, _ = proj3d.proj_transform(X[i, j], Y[i, j], Z[i, j], self.ax3.get_proj())
                    x_disp, y_disp = self.ax3.transData.transform((x2D, y2D))
                    dist = np.hypot(x_click - x_disp, y_click - y_disp)
                    if dist < min_dist:
                        min_dist = dist
                        closest_text = f"X: {X[i,j]:.2f}\nY: {Y[i,j]:.2f}\nZ: {Z[i,j]:.2f}"

            self.annotation_box.set_text(closest_text)
            self.draw()

        self.mpl_connect("button_press_event", on_click)

    def zoom_in(self, factor=0.8):
        min_width = 1e-3
        for getter, setter in [
            (self.ax3.get_xlim, self.ax3.set_xlim),
            (self.ax3.get_ylim, self.ax3.set_ylim), 
            (self.ax3.get_zlim, self.ax3.set_zlim),
        ]:
            try:
                lo, hi = getter()
                center = 0.5*(lo+hi)
                half = max((hi-lo)*factor/2, min_width)
                setter((center-half, center+half))
            except Exception as e:
                print(f"Error in zoom_in: {e}")
                continue
        self.draw()

    def zoom_out(self, factor=1.25):
        max_width = 1e6
        for getter, setter in [
            (self.ax3.get_xlim, self.ax3.set_xlim),
            (self.ax3.get_ylim, self.ax3.set_ylim),
            (self.ax3.get_zlim, self.ax3.set_zlim),
        ]:
            try:
                lo, hi = getter()
                center = 0.5*(lo+hi)
                half = min((hi-lo)*factor/2, max_width)
                setter((center-half, center+half))
            except Exception as e:
                print(f"Error in zoom_out: {e}")
                continue
        self.draw()

class Fig2D(FigureCanvas):
    def __init__(self, parent=None, figsize=(12, 8), dark_mode=False):
        fig = Figure(figsize=figsize, dpi=80, tight_layout=True)
        super().__init__(fig)
        if parent:
            self.setParent(parent)
        
        self.color_h = "blue"
        self.color_e = "red"
        self.ax1 = self.figure.add_subplot(121, polar=True)
        self.ax2 = self.figure.add_subplot(122, polar=True)
        self.use_two_plots = True
        self.dark_mode = dark_mode
        self.theta_h = None
        self.theta_e = None
        self.h_data = None
        self.e_data = None
        self.show_lobes = False
        self.update_figure_style()

    def blend_with_white(self, color, blend_factor=0.5):
        rgba = np.array(mcolors.to_rgba(color))
        white = np.array([1, 1, 1, 1])
        blended = (1 - blend_factor) * rgba + blend_factor * white
        return blended

    def add_cursor(self, ax_list):
        cursor = mplcursors.cursor(ax_list, hover=True)

        def custom_annotate(sel):
            artist = sel.artist
            color = artist.get_color()
            light_color = self.blend_with_white(color, blend_factor=0.5)
            sel.annotation.set_text(
                f"Angle: {np.degrees(sel.target[0]):.1f}°\nValue: {sel.target[1]:.2f} dB"
            )
            sel.annotation.get_bbox_patch().set(fc=light_color, alpha=0.7)

        cursor.connect("add", custom_annotate)

    def highlight_lobes_lines(self, ax, phi, data, label_prefix='', main_idx=None):
        try:
            if phi is None or data is None or len(phi) != len(data):
                print(f"No valid data or angles for {label_prefix} highlighting")
                return
            peaks, _ = find_peaks(data, distance=10)
            peak_values = data[peaks]

            if len(peak_values) == 0:
                print(f"No peaks found in {label_prefix}")
                return

            delta_theta = phi[1] - phi[0]
            window_degrees = 5
            window_size = max(1, int(window_degrees / np.degrees(delta_theta)))

            def plot_lobe(idx, color, label):
                idx_start = max(0, idx - window_size)
                idx_end = min(len(phi), idx + window_size + 1)
                highlight_mask = np.full_like(data, np.nan)
                highlight_mask[idx_start:idx_end] = data[idx_start:idx_end]
                line, = ax.plot(phi, highlight_mask, color=color, linewidth=2, label=label if not any(l.startswith(f"{label_prefix} {label.split()[-1]}") for l in ax.get_legend_handles_labels()[1]) else "")
                return line

            if main_idx is not None:
                selected_main_idx = main_idx
            else:
                selected_main_idx = peaks[np.argmax(peak_values)]

            main_line = plot_lobe(selected_main_idx, 'green', f'{label_prefix} Main Lobe')
            secondary_indices = [idx for idx in peaks if idx != selected_main_idx]
            if secondary_indices:
                secondary_line = plot_lobe(secondary_indices[0], 'orange', f'{label_prefix} Secondary Lobe')
            back_angle = (phi[selected_main_idx] + np.pi) % (2 * np.pi)
            closest_idx = np.argmin(np.abs(phi - back_angle))
            back_line = plot_lobe(closest_idx, 'purple', f'{label_prefix} Back Lobe')

            base_handles, base_labels = ax.get_legend_handles_labels()
            lobe_handles = [main_line, secondary_line, back_line] if secondary_line else [main_line, back_line]
            lobe_labels = [l.get_label() for l in lobe_handles if l.get_label()]
            all_handles = [h for h in ax.lines if h.get_label() in ['H-plane', 'E-plane']] + lobe_handles
            all_labels = ['H-plane' if 'H-plane' in base_labels else '', 'E-plane' if 'E-plane' in base_labels else ''] + lobe_labels
            all_labels = [l for l in all_labels if l]
            if all_handles and all_labels:
                ax.legend(all_handles, all_labels, loc='upper right', bbox_to_anchor=(1.3, 1.0), frameon=True)

        except Exception as e:
            print(f"Error in highlight_lobes_lines ({label_prefix}): {e}")

    def update_figure_style(self):
        if self.dark_mode:
            self.figure.patch.set_facecolor('#2D2D30')
            for ax in [self.ax1, self.ax2]:
                ax.set_facecolor('#2D2D30')
                ax.tick_params(colors='#E0E0E0')
                ax.title.set_color('#E0E0E0')
                ax.grid(True, color='#555555', alpha=0.3)
        else:
            self.figure.patch.set_facecolor('#FFFFFF')
            for ax in [self.ax1, self.ax2]:
                ax.set_facecolor('#FFFFFF')
                ax.tick_params(colors='#333333')
                ax.title.set_color('#333333')
                ax.grid(True, color='#CCCCCC', alpha=0.3)

    def toggle_dark_mode(self, is_dark):
        self.dark_mode = is_dark
        self.update_figure_style()
        self.draw()

    def toggle_mode(self, two_plots: bool):
        self.use_two_plots = two_plots
        if self.h_data is not None and self.e_data is not None:
            self.plot_2D(self.h_data, self.e_data)

    def plot_2D(self, h, e):
        try:
            if h is None or e is None or len(h) == 0 or len(e) == 0:
                print("Invalid or empty data for plotting")
                return
            self.ax1.clear()
            self.ax2.clear()
            self.figure.texts.clear()
            self.theta_h = np.radians(np.arange(len(h)))
            self.theta_e = np.radians(np.arange(len(e)))
            self.h_data = h
            self.e_data = e

            main_idx = None
            if self.show_lobes and self.use_two_plots:
                combined_data = (self.h_data + self.e_data) / 2
                peaks, _ = find_peaks(combined_data, distance=10)
                if len(peaks) > 0:
                    peak_values = combined_data[peaks]
                    main_idx = peaks[np.argmax(peak_values)]

            if self.use_two_plots:
                h_line, = self.ax1.plot(self.theta_h, h, color=self.color_h, label='H-plane', linewidth=2)
                self.ax1.set_title('H-plane')
                e_line, = self.ax2.plot(self.theta_e, e, color=self.color_e, label='E-plane', linewidth=2)
                self.ax2.set_title("E-plane")
                self.ax2.set_theta_direction(-1)
                self.ax1.legend(handles=[h_line], labels=['H-plane'], loc='upper right', bbox_to_anchor=(1.0, 1.0))
                self.ax2.legend(handles=[e_line], labels=['E-plane'], loc='upper right', bbox_to_anchor=(1.0, 1.0))

                self.add_cursor([h_line, e_line])

                maxv_h = np.max(h)
                minv_h = np.min(h)
                self.figure.text(
                    0.1, 0.1,
                    f"Max (H-plane): {maxv_h:.2f} dB\nMin (H-plane): {minv_h:.2f} dB",
                    fontsize=12, va='center', ha='left',
                    bbox=dict(facecolor='lightgray', alpha=0.5, edgecolor='black')
                )

                maxv_e = np.max(e)
                minv_e = np.min(e)
                self.figure.text(
                    0.6, 0.1,
                    f"Max (E-plane): {maxv_e:.2f} dB\nMin (E-plane): {minv_e:.2f} dB",
                    fontsize=12, va='center', ha='left',
                    bbox=dict(facecolor='lightgray', alpha=0.5, edgecolor='black')
                )
            else:
                h_line, = self.ax1.plot(self.theta_h, h, color=self.color_h, label='H-plane', linewidth=2)
                e_line, = self.ax1.plot(self.theta_e, e, color=self.color_e, label='E-plane', linewidth=2)
                self.ax1.set_title('H & E overlay')
                self.ax1.legend(handles=[h_line, e_line], labels=['H-plane', 'E-plane'], loc='upper right', bbox_to_anchor=(1.0, 1.0))

                h_line2, = self.ax2.plot(self.theta_h, h, color=self.color_h, label='H-plane', linewidth=2)
                e_line2, = self.ax2.plot(self.theta_e, e, color=self.color_e, label='E-plane', linewidth=2)
                self.ax2.set_title('H & E rotated')
                self.ax2.set_theta_direction(1)
                self.ax2.legend(handles=[h_line2, e_line2], labels=['H-plane', 'E-plane'], loc='upper right', bbox_to_anchor=(1.0, 1.0))

                self.add_cursor([h_line, e_line, h_line2, e_line2])

                maxv_h = np.max(h)
                minv_h = np.min(h)
                self.figure.text(
                    0.1, 0.1,
                    f"Max (H-plane): {maxv_h:.2f} dB\nMin (H-plane): {minv_h:.2f} dB",
                    fontsize=12, va='center', ha='left',
                    bbox=dict(facecolor='lightgray', alpha=0.5, edgecolor='black')
                )

                self.figure.text(
                    0.6, 0.1,
                    f"Max (H-plane): {maxv_h:.2f} dB\nMin (H-plane): {minv_h:.2f} dB",
                    fontsize=12, va='center', ha='left',
                    bbox=dict(facecolor='lightgray', alpha=0.5, edgecolor='black')
                )

            if self.show_lobes:
                if self.use_two_plots:
                    self.highlight_lobes_lines(self.ax1, self.theta_h, self.h_data, 'H-plane', main_idx)
                    self.highlight_lobes_lines(self.ax2, self.theta_e, self.e_data, 'E-plane', main_idx)
                else:
                    self.highlight_lobes_lines(self.ax1, self.theta_h, self.h_data, 'H-plane')
                    self.highlight_lobes_lines(self.ax1, self.theta_e, self.e_data, 'E-plane')
                    self.highlight_lobes_lines(self.ax2, self.theta_h, self.h_data, 'H-plane')
                    self.highlight_lobes_lines(self.ax2, self.theta_e, self.e_data, 'E-plane')

            self.figure.tight_layout()
            self.figure.subplots_adjust(right=0.85, bottom=0.2)
            self.update_figure_style()
            self.draw()
        except Exception as e:
            print(f"Error in plot_2D: {e}")

    def zoom_in(self, factor=0.8):
        min_ylim = 1e-3
        max_ylim = 1e6
        for ax in [self.ax1, self.ax2]:
            if ax is not None:
                try:
                    rmin, rmax = ax.get_ylim()
                    new_rmax = max(min(rmax * factor, max_ylim), min_ylim)
                    if new_rmax > min_ylim:
                        ax.set_ylim(rmin, new_rmax)
                except Exception as e:
                    print(f"Error zooming axis: {e}")
                    continue
        if self.h_data is not None and self.e_data is not None:
            self.plot_2D(self.h_data, self.e_data)

    def zoom_out(self, factor=1.25):
        min_ylim = 1e-3
        max_ylim = 1e6
        for ax in [self.ax1, self.ax2]:
            if ax is not None:
                try:
                    rmin, rmax = ax.get_ylim()
                    new_rmax = max(min(rmax * factor, max_ylim), min_ylim)
                    if new_rmax > min_ylim:
                        ax.set_ylim(rmin, new_rmax)
                except Exception as e:
                    print(f"Error zooming axis: {e}")
                    continue
        if self.h_data is not None and self.e_data is not None:
            self.plot_2D(self.h_data, self.e_data)

class Ui_Window:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)  # Appropriate size for the application
        MainWindow.setMinimumSize(1000, 700)
        MainWindow.setWindowTitle("Antenna Radiation Pattern Analyzer")
        
        # Initialize dark mode state
        self.dark_mode = False
        
        # Central widget
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Main grid layout
        self.grid_layout = QGridLayout(self.centralwidget)
        self.grid_layout.setContentsMargins(15, 15, 15, 15)
        self.grid_layout.setSpacing(10)
        
        # Sidebar layout
        self.setup_sidebar()
        
        # Tab widget
        self.setup_tabs()
        
        # Add to main layout
        self.grid_layout.addLayout(self.sidebar_layout, 0, 0)
        self.grid_layout.addWidget(self.tab_widget, 0, 1)
        
        # Set column stretch factors
        self.grid_layout.setColumnStretch(0, 0)  # Sidebar fixed width
        self.grid_layout.setColumnStretch(1, 1)  # Tab widget expandable
        
        # Menu bar
        
        # Status bar
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready")
        
        # Apply initial styles
        self.apply_styles(MainWindow)

    def setup_sidebar(self):
        self.sidebar_layout = QVBoxLayout()
        
        # Main action buttons
        self.import_button = QPushButton("Import Data")
        self.import_button.setIcon(QIcon.fromTheme("document-open"))
        
        self.usb_button = QPushButton("Read from USB")
        self.usb_button.setIcon(QIcon.fromTheme("drive-harddisk"))
        
        # Display mode combo button
        self.display_mode_button = QPushButton("2D Split Planes")
        self.display_mode_button.setIcon(QIcon.fromTheme("view-split-left-right"))
        
        self.display_mode_menu = QMenu()
        self.display_mode_menu.addAction("2D Split Planes")
        self.display_mode_menu.addAction("2D Both Planes")
        self.display_mode_button.setMenu(self.display_mode_menu)
        
        self.plot_3d_button = QPushButton("Plot 3D")
        self.plot_3d_button.setIcon(QIcon.fromTheme("view-3d"))
        
        self.save_button = QPushButton("Save Plot")
        self.save_button.setIcon(QIcon.fromTheme("document-save"))
        
        self.offset_button = QPushButton("Apply Offset")
        self.offset_button.setCheckable(True)
        self.offset_button.setIcon(QIcon.fromTheme("transform-move"))
        
        self.online_view_button = QPushButton("Online View")
        self.online_view_button.setIcon(QIcon.fromTheme("network-wired"))
        
        self.show_details_button = QPushButton("Show Details")
        self.show_details_button.setIcon(QIcon.fromTheme("dialog-information"))
        
        # Theme toggle
        self.theme_layout = QHBoxLayout()
        self.theme_label = QLabel("Dark Mode:")
        self.theme_toggle = QCheckBox()
        self.theme_toggle.setChecked(False)
        self.theme_layout.addWidget(self.theme_label)
        self.theme_layout.addWidget(self.theme_toggle)
        
        # Add all widgets to sidebar
        widgets = [
            self.import_button, self.usb_button, self.display_mode_button,
            self.plot_3d_button, self.save_button, self.offset_button,
            self.online_view_button, self.show_details_button
        ]
        
        for widget in widgets:
            self.sidebar_layout.addWidget(widget)
        
        self.sidebar_layout.addLayout(self.theme_layout)
        self.sidebar_layout.addStretch(1)

    def setup_tabs(self):
        self.tab_widget = QTabWidget()
        
        # Tab 1: 2D Visualization
        self.tab1 = QWidget()
        self.tab_widget.addTab(self.tab1, "2D Visualization")
        self.setup_tab1()
        
        # Tab 2: 3D Visualization  
        self.tab2 = QWidget()
        self.tab_widget.addTab(self.tab2, "3D Visualization")
        self.setup_tab2()

    def setup_tab1(self):
        tab1_layout = QVBoxLayout(self.tab1)
        nav_layout1 = QHBoxLayout()
        self.tab1_canvas_layout = QVBoxLayout()

        self.zoom_in_button1 = QPushButton("Zoom In")
        self.zoom_in_button1.setIcon(QIcon.fromTheme("zoom-in"))
        self.zoom_out_button1 = QPushButton("Zoom Out")
        self.zoom_out_button1.setIcon(QIcon.fromTheme("zoom-out"))
        self.color_button1 = QPushButton("Change Color")
        self.color_button1.setIcon(QIcon.fromTheme("color-picker"))
        self.highlight_lobes_button = QPushButton("Highlight Lobes")
        self.highlight_lobes_button.setIcon(QIcon.fromTheme("dialog-information"))
        self.highlight_lobes_button.setCheckable(True)

        nav_layout1.addStretch(1)
        nav_layout1.addWidget(self.zoom_in_button1)
        nav_layout1.addWidget(self.zoom_out_button1)
        nav_layout1.addWidget(self.color_button1)
        nav_layout1.addWidget(self.highlight_lobes_button)  # Add the button here

        tab1_layout.addLayout(nav_layout1)
        tab1_layout.addLayout(self.tab1_canvas_layout)

        controls_layout1 = QHBoxLayout()
        self.back_button1 = QPushButton("Back")
        self.back_button1.setIcon(QIcon.fromTheme("go-previous"))
        self.smooth_label1 = QLabel("Smooth:")
        self.smoothness_slider1 = QSlider(Qt.Horizontal)
        self.smoothness_slider1.setRange(5, 50)
        self.smoothness_slider1.setValue(5)
        self.next_button1 = QPushButton("Next")
        self.next_button1.setIcon(QIcon.fromTheme("go-next"))

        controls_layout1.addWidget(self.back_button1)
        controls_layout1.addWidget(self.smooth_label1)
        controls_layout1.addWidget(self.smoothness_slider1)
        controls_layout1.addWidget(self.next_button1)

        tab1_layout.addLayout(controls_layout1)

    def setup_tab2(self):
        tab2_layout = QVBoxLayout(self.tab2)
        
        # Navigation toolbar layout
        nav_layout2 = QHBoxLayout()
        
        # Placeholder for matplotlib toolbar (will be added by Window class)
        self.tab2_canvas_layout = QVBoxLayout()
        
        # Custom navigation buttons
        self.zoom_in_button2 = QPushButton("Zoom In")
        self.zoom_in_button2.setIcon(QIcon.fromTheme("zoom-in"))
        
        self.zoom_out_button2 = QPushButton("Zoom Out")
        self.zoom_out_button2.setIcon(QIcon.fromTheme("zoom-out"))
        
        self.color_button3D = QPushButton("Change Colormap")
        self.color_button3D.setIcon(QIcon.fromTheme("color-picker"))
        
        nav_layout2.addStretch(1)
        nav_layout2.addWidget(self.zoom_in_button2)
        nav_layout2.addWidget(self.zoom_out_button2)
        nav_layout2.addWidget(self.color_button3D)
        
        tab2_layout.addLayout(nav_layout2)
        tab2_layout.addLayout(self.tab2_canvas_layout)
        
        # Controls layout
        controls_layout2 = QHBoxLayout()
        
        self.back_button2 = QPushButton("Back")
        self.back_button2.setIcon(QIcon.fromTheme("go-previous"))
        
        self.smooth_label2 = QLabel("Smooth:")
        self.smoothness_slider2 = QSlider(Qt.Horizontal)
        self.smoothness_slider2.setRange(5, 50)
        self.smoothness_slider2.setValue(5)
        
        self.next_button2 = QPushButton("Next")
        self.next_button2.setIcon(QIcon.fromTheme("go-next"))
        
        controls_layout2.addWidget(self.back_button2)
        controls_layout2.addWidget(self.smooth_label2)
        controls_layout2.addWidget(self.smoothness_slider2)
        controls_layout2.addWidget(self.next_button2)
        
        tab2_layout.addLayout(controls_layout2)

    

    def apply_styles(self, MainWindow):
        self.update_theme_styles(MainWindow)

    def update_theme_styles(self, MainWindow):
        if self.dark_mode:
            primary_color = DARK_PRIMARY_COLOR
            secondary_color = DARK_SECONDARY_COLOR
            accent_color = DARK_ACCENT_COLOR
            text_color = DARK_TEXT_COLOR
            button_text_color = DARK_BUTTON_TEXT_COLOR
            darker_accent = "#0D45C0"
            nav_color = "#4D4D50"
            nav_hover = "#5D5D60"
            nav_pressed = "#3D3D40"
            toolbar_bg = "#3D3D40"
            button_bg = "#4D4D50"
            button_hover = "#5D5D60"
            button_pressed = "#3D3D40"
            border_color = "#555555"
            border_hover = "#777777"
        else:
            primary_color = PRIMARY_COLOR
            secondary_color = SECONDARY_COLOR
            accent_color = ACCENT_COLOR
            text_color = TEXT_COLOR
            button_text_color = BUTTON_TEXT_COLOR
            darker_accent = "#0D45C0"
            nav_color = "#6c757d"
            nav_hover = "#5a6268"
            nav_pressed = "#4e555b"
            toolbar_bg = "#F8F9FA"
            button_bg = "#E9ECEF"
            button_hover = "#DEE2E6"
            button_pressed = "#CED4DA"
            border_color = "#D0D0D0"
            border_hover = "#A6B0B8"
        
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
        
        toolbar_style = TOOLBAR_STYLE_TEMPLATE.format(
            toolbar_bg=toolbar_bg,
            border_color=border_color,
            button_bg=button_bg,
            button_hover=button_hover,
            button_pressed=button_pressed,
            border_hover=border_hover
        )
        
        MainWindow.setStyleSheet(f"""
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
            QTabWidget::pane {{
                border: 1px solid {border_color};
                border-top: none;
                border-radius: 0 0 5px 5px;
                padding: 10px;
                background: {secondary_color};
            }}
            QTabBar::tab {{
                background: {button_bg};
                border: 1px solid {border_color};
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                padding: 10px 20px;
                min-width: 120px;
                font-weight: bold;
                color: {text_color};
            }}
            QTabBar::tab:selected {{
                background: {secondary_color};
                border-color: {border_color};
                color: {primary_color};
            }}
            QTabBar::tab:hover:!selected {{
                background: {button_hover};
            }}
            QSlider::groove:horizontal {{
                border: 1px solid {border_color};
                height: 6px;
                background: {button_bg};
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
            QCheckBox {{
                color: {text_color};
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 1px solid {border_color};
                border-radius: 3px;
                background-color: {button_bg};
            }}
            QCheckBox::indicator:checked {{
                background-color: {primary_color};
                border-color: {primary_color};
            }}
            QStatusBar {{
                background-color: {button_bg};
                color: {text_color};
                border-top: 1px solid {border_color};
            }}
            QMenuBar {{
                background-color: {button_bg};
                color: {text_color};
            }}
            QMenuBar::item:selected {{
                background-color: {primary_color};
                color: {button_text_color};
            }}
            QMenu {{
                background-color: {secondary_color};
                border: 1px solid {border_color};
                color: {text_color};
            }}
            QMenu::item:selected {{
                background-color: {primary_color};
                color: {button_text_color};
            }}
            {toolbar_style}
        """)
        
        # Apply button styles
        main_buttons = [
            self.import_button, self.usb_button, self.display_mode_button,
            self.plot_3d_button, self.save_button, self.offset_button,
            self.online_view_button, self.show_details_button,
            self.color_button1, self.zoom_in_button1, self.zoom_out_button1,
            self.color_button3D, self.zoom_in_button2, self.zoom_out_button2,
            self.highlight_lobes_button
        ]
        
        nav_buttons = [
            self.back_button1, self.next_button1, 
            self.back_button2, self.next_button2
        ]
        
        for button in main_buttons:
            button.setStyleSheet(button_style)
        
        for button in nav_buttons:
            button.setStyleSheet(nav_button_style)

    def toggle_dark_mode(self, MainWindow, is_dark):
        self.dark_mode = is_dark
        self.update_theme_styles(MainWindow)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.view = Ui_Window()
        self.view.setupUi(self)

        # Create figures with appropriate sizes for the application
        self.fig2D = Fig2D(self, figsize=(10, 6), dark_mode=self.view.dark_mode)
        self.fig3D = Fig3D(self, figsize=(8, 6), dark_mode=self.view.dark_mode)

        # Create toolbars
        self.toolbar1 = NavigationToolbar(self.fig2D, self)
        self.toolbar2 = NavigationToolbar(self.fig3D, self)

        # Add figures and toolbars to layouts
        self.view.tab1_canvas_layout.addWidget(self.toolbar1)
        self.view.tab1_canvas_layout.addWidget(self.fig2D)
        self.view.tab2_canvas_layout.addWidget(self.toolbar2)
        self.view.tab2_canvas_layout.addWidget(self.fig3D)
        
        # Connect theme toggle
        self.view.theme_toggle.stateChanged.connect(self.toggle_theme)
        self.view.highlight_lobes_button.toggled.connect(self.toggle_lobes_highlighting)

    def toggle_lobes_highlighting(self, checked):
        self.fig2D.show_lobes = checked
        # Replot to apply or remove highlighting
        if self.fig2D.h_data is not None and self.fig2D.e_data is not None:
            self.fig2D.plot_2D(self.fig2D.h_data, self.fig2D.e_data)

    def toggle_theme(self, state):
        is_dark = bool(state)
        self.view.toggle_dark_mode(self, is_dark)
        self.fig2D.toggle_dark_mode(is_dark)
        self.fig3D.toggle_dark_mode(is_dark)

    def pick_color_for(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Select Plane")
        msg.setText("Which plane's color do you want to change?")
        h_button = msg.addButton("H-plane", QMessageBox.AcceptRole)
        e_button = msg.addButton("E-plane", QMessageBox.AcceptRole)
        msg.exec()

        if msg.clickedButton() == h_button:
            plane = 'h'
        elif msg.clickedButton() == e_button:
            plane = 'e'
        else:
            return  # User closed dialog

        color = QColorDialog.getColor()
        if color.isValid():
            hex_color = color.name()
            if plane == 'h':
                self.fig2D.color_h = hex_color
            elif plane == 'e':
                self.fig2D.color_e = hex_color
    def open_file(self):
            dialog = QFileDialog()
            dialog.setFileMode(QFileDialog.AnyFile)
            dialog.setNameFilter("atn files (*.atn);;Text Files (*.txt)")
            if dialog.exec():
                 file_name = dialog.selectedFiles()[0]
                 return file_name
    def file_history(self):
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("JSON Files (*.json)")
        file_dialog.setDefaultSuffix("json")
        if file_dialog.exec():
            return file_dialog.selectedFiles()[0]

