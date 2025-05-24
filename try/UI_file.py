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
        # Store original data and view settings
        self.original_X = None
        self.original_Y = None
        self.original_Z = None
        self.has_data = False
        self.default_view = {'elev': 30, 'azim': 45}
        self.update_figure_style()

    def store_original_view(self):
        """Store the original 3D view settings"""
        if self.has_data:
            try:
                self.original_xlim = self.ax3.get_xlim()
                self.original_ylim = self.ax3.get_ylim()
                self.original_zlim = self.ax3.get_zlim()
                self.original_elev = self.ax3.elev
                self.original_azim = self.ax3.azim
            except:
                pass

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

            # Set pane colors for 3D plot (handle older/newer matplotlib versions)
            try:
                self.ax3.xaxis.pane.set_facecolor('#2D2D30')
                self.ax3.yaxis.pane.set_facecolor('#2D2D30')
                self.ax3.zaxis.pane.set_facecolor('#2D2D30')
                self.ax3.xaxis.pane.fill = False
                self.ax3.yaxis.pane.fill = False
                self.ax3.zaxis.pane.fill = False
            except Exception as e:
                try:
                    self.ax3.xaxis.pane.fill = False
                    self.ax3.yaxis.pane.fill = False
                    self.ax3.zaxis.pane.fill = False
                except Exception as e2:
                    print(f"Warning: Could not set 3D pane fill: {e2}")
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
        # Store original data
        self.original_X = np.array(X) if X is not None else None
        self.original_Y = np.array(Y) if Y is not None else None  
        self.original_Z = np.array(Z) if Z is not None else None
        self.has_data = True
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
        # Store the view settings after plotting
        self.store_original_view()
        self.draw()

    def change_colormap(self, cmap_name):
        """Change the colormap for the 3D surface plot and redraw if possible."""
        self.cmap = cmap_name
        # If a surface is already plotted, update it
        # Try to update the colorbar and surface if present
        try:
            # Find the last Poly3DCollection (surface) in the axes
            for artist in self.ax3.collections:
                if hasattr(artist, 'set_cmap'):
                    artist.set_cmap(self.cmap)
            if self._cbar:
                self._cbar.set_cmap(self.cmap)
            self.draw()
        except Exception as e:
            print(f"Warning: Could not update colormap directly: {e}. Replotting may be needed.")
            # Optionally, you could call plot_surface again with stored data if you keep it

    def zoom_in(self):
        """Fixed zoom in for 3D that preserves view integrity"""
        if self.ax3 and self.has_data:
            try:
                # Get current limits
                xlim = self.ax3.get_xlim()
                ylim = self.ax3.get_ylim()
                zlim = self.ax3.get_zlim()
                # Scale each axis by 0.9 around center
                for lim, setter in [(xlim, self.ax3.set_xlim), 
                                   (ylim, self.ax3.set_ylim), 
                                   (zlim, self.ax3.set_zlim)]:
                    lo, hi = lim
                    center = 0.5 * (lo + hi)
                    half = (hi - lo) * 0.9 / 2
                    setter((center - half, center + half))
                # Update stored limits
                self.store_original_view()
                self.draw_idle()
            except Exception as e:
                print(f"Error in 3D zoom in: {e}")

    def zoom_out(self):
        """Fixed zoom out for 3D that preserves view integrity"""
        if self.ax3 and self.has_data:
            try:
                # Get current limits
                xlim = self.ax3.get_xlim()
                ylim = self.ax3.get_ylim()
                zlim = self.ax3.get_zlim()
                # Scale each axis by 1.1 around center
                for lim, setter in [(xlim, self.ax3.set_xlim), 
                                   (ylim, self.ax3.set_ylim), 
                                   (zlim, self.ax3.set_zlim)]:
                    lo, hi = lim
                    center = 0.5 * (lo + hi)
                    half = (hi - lo) * 1.1 / 2
                    setter((center - half, center + half))
                # Update stored limits
                self.store_original_view()
                self.draw_idle()
            except Exception as e:
                print(f"Error in 3D zoom out: {e}")

    def reset_view(self):
        """Reset to original 3D view"""
        if self.has_data and all(x is not None for x in [self.original_X, self.original_Y, self.original_Z]):
            # Replot with original data to reset everything
            self.plot_surface(self.original_X, self.original_Y, self.original_Z)

class Fig2D(FigureCanvas):
    def __init__(self, parent=None, figsize=(12, 8), dark_mode=False):
        # Create figure with appropriate size for the application
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
        self.text_boxes = []
        # Store original data and limits to prevent toolbar interference
        self.original_data_h = None
        self.original_data_e = None
        self.default_ylim = (0, 1)
        self.has_data = False
        self.show_lobes = False  # Initialize show_lobes
        self.h_data = None  # Initialize h_data
        self.e_data = None  # Initialize e_data
        self.theta_h = None  # Initialize theta_h
        self.theta_e = None
        self.update_figure_style()

    def highlight_lobes_lines(self, ax, phi, data, label_prefix='', main_idx=None):
        try:
            if phi is None or data is None or len(phi) != len(data):
                print(f"No valid data or angles for {label_prefix} highlighting: phi={phi}, data={data}")
                return
            if np.any(np.isnan(data)) or np.any(np.isinf(data)):
                print(f"Invalid values in {label_prefix} data")
                return

            print(f"{label_prefix} - phi shape: {np.shape(phi)}, data shape: {np.shape(data)}")
            peaks, _ = find_peaks(data, distance=max(1, len(data)//36))  # Adjust distance based on data length
            print(f"{label_prefix} - Found {len(peaks)} peaks at indices: {peaks}")
            if len(peaks) == 0:
                print(f"No peaks found in {label_prefix}")
                return

            delta_theta = phi[1] - phi[0] if len(phi) > 1 else np.radians(1)
            window_degrees = 5
            window_size = max(1, int(window_degrees / np.degrees(delta_theta)))

            def plot_lobe(idx, color, label):
                idx_start = max(0, idx - window_size)
                idx_end = min(len(phi), idx + window_size + 1)
                highlight_mask = np.full_like(data, np.nan)
                highlight_mask[idx_start:idx_end] = data[idx_start:idx_end]
                line, = ax.plot(phi, highlight_mask, color=color, linewidth=2, label=label if not any(l.startswith(f"{label_prefix} {label.split()[-1]}") for l in ax.get_legend_handles_labels()[1]) else "")
                return line

            if main_idx is not None and 0 <= main_idx < len(data):
                selected_main_idx = main_idx
            else:
                peak_values = data[peaks]
                selected_main_idx = peaks[np.argmax(peak_values)] if len(peaks) > 0 else None

            if selected_main_idx is None:
                print(f"No valid main lobe index for {label_prefix}")
                return

            main_line = plot_lobe(selected_main_idx, 'green', f'{label_prefix} Main Lobe')
            secondary_indices = [idx for idx in peaks if idx != selected_main_idx]
            secondary_line = None
            if secondary_indices:
                secondary_line = plot_lobe(secondary_indices[0], 'orange', f'{label_prefix} Secondary Lobe')

            back_angle = (phi[selected_main_idx] + np.pi) % (2 * np.pi)
            closest_idx = np.argmin(np.abs(phi - back_angle))
            back_line = plot_lobe(closest_idx, 'purple', f'{label_prefix} Back Lobe')

            base_handles, base_labels = ax.get_legend_handles_labels()
            lobe_handles = [main_line]
            if secondary_line:
                lobe_handles.append(secondary_line)
                lobe_handles.append(back_line)
                lobe_labels = [l.get_label() for l in lobe_handles if l.get_label()]
                all_handles = [h for h in ax.lines if h.get_label() in ['H-plane', 'E-plane']] + lobe_handles
                all_labels = ['H-plane' if 'H-plane' in base_labels else '', 'E-plane' if 'E-plane' in base_labels else ''] + lobe_labels
                all_labels = [l for l in all_labels if l]
            if all_handles and all_labels:
                ax.legend(all_handles, all_labels, loc='upper right', bbox_to_anchor=(1.3, 1.0), frameon=True)

        except Exception as e:
            print(f"Error in highlight_lobes_lines ({label_prefix}): {e}")

    def store_original_limits(self):
        """Store the original axis limits after plotting data"""
        if self.has_data:
            try:
                # Store limits for both axes
                self.ax1_original_ylim = self.ax1.get_ylim()
                self.ax2_original_ylim = self.ax2.get_ylim()
            except:
                self.ax1_original_ylim = self.default_ylim
                self.ax2_original_ylim = self.default_ylim

    def restore_proper_limits(self):
        """Restore proper limits after toolbar interference"""
        if self.has_data:
            try:
                # Restore stored limits or use defaults
                if hasattr(self, 'ax1_original_ylim'):
                    self.ax1.set_ylim(self.ax1_original_ylim)
                if hasattr(self, 'ax2_original_ylim'):
                    self.ax2.set_ylim(self.ax2_original_ylim)
                self.draw_idle()
            except Exception as e:
                print(f"Warning: Could not restore limits: {e}")

    def update_figure_style(self):
        """Update figure colors based on dark mode"""
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

    def plot_2D(self, h, e):
    # Store original data
        self.original_data_h = np.array(h) if h is not None else None
        self.original_data_e = np.array(e) if e is not None else None
        self.h_data = np.array(h) if h is not None else None
        self.e_data = np.array(e) if e is not None else None
        self.has_data = self.h_data is not None and self.e_data is not None and len(self.h_data) > 0 and len(self.e_data) > 0
    
        if not self.has_data:
            print("No valid data for plotting")
            return
        
        if not hasattr(self, 'maxv_h_orig'):
            self.maxv_h_orig = np.max(h)
            self.minv_h_orig = np.min(h)
            self.delta_h_orig = self.maxv_h_orig - self.minv_h_orig

            self.maxv_e_orig = np.max(e)
            self.minv_e_orig = np.min(e)
            self.delta_e_orig = self.maxv_e_orig - self.minv_e_orig
    
        self.ax1.clear()
        self.ax2.clear()
        self.theta_h = np.radians(np.arange(len(self.h_data)))
        self.theta_e = np.radians(np.arange(len(self.e_data)))

        main_idx = None
        if self.show_lobes and self.use_two_plots and len(self.h_data) == len(self.e_data):
            try:
                combined_data = (self.h_data + self.e_data) / 2
                if np.any(np.isnan(combined_data)) or np.any(np.isinf(combined_data)):
                    print("Invalid values in combined data for peak detection")
                    return
                peaks, _ = find_peaks(combined_data, distance=10)
                if len(peaks) > 0:
                    peak_values = combined_data[peaks]
                    main_idx = peaks[np.argmax(peak_values)]
            except Exception as e:
                print(f"Error calculating main_idx: {e}")

        if self.use_two_plots:
            self.ax1.plot(self.theta_h, self.h_data, color=self.color_h, label='H-plane', linewidth=2)
            self.ax1.set_title('H-plane')
            self.ax1.legend()
            self.ax2.plot(self.theta_e, self.e_data, color=self.color_e, label='E-plane', linewidth=2)
            self.ax2.set_title("E-plane")
            self.ax2.set_theta_zero_location("N")
            self.ax2.set_theta_direction(1)
            self.ax2.legend()
        else:
            self.ax1.plot(self.theta_h, self.h_data, color=self.color_h, label='H-plane', linewidth=2)
            self.ax1.plot(self.theta_e, self.e_data, color=self.color_e, label='E-plane', linewidth=2)
            self.ax1.set_title('H & E overlay')
            self.ax1.legend()
            self.ax2.plot(self.theta_h, self.h_data, color=self.color_h, label='H-plane', linewidth=2)
            self.ax2.plot(self.theta_e, self.e_data, color=self.color_e, label='E-plane', linewidth=2)
            self.ax2.set_title('H & E rotated')
            self.ax2.set_theta_zero_location("N")
            self.ax2.set_theta_direction(1)
            self.ax2.legend()

        if hasattr(self, 'annotation_boxes'):
            for box in self.annotation_boxes:
                box.remove()
        self.annotation_boxes = []

        text1 = self.figure.text(
            0.01, 0.1,
            f"Max (H-plane): {self.maxv_h_orig:.2f} dB\n"
            f"Min (H-plane): {self.minv_h_orig:.2f} dB\n"
            f"Δ (H-plane): {self.delta_h_orig:.2f} dB",
            fontsize=12, va='center', ha='left',
            linespacing=1.8,
            bbox=dict(facecolor='lightgray', alpha=0.5, edgecolor='black')
        )
        text2 = self.figure.text(
            0.5, 0.1,
            f"Max (E-plane): {self.maxv_e_orig:.2f} dB\n"
            f"Min (E-plane): {self.minv_e_orig:.2f} dB\n"
            f"Δ (E-plane): {self.delta_e_orig:.2f} dB",
            fontsize=12, va='center', ha='left',
            linespacing=1.8,
            bbox=dict(facecolor='lightgray', alpha=0.5, edgecolor='black')
        )
        self.annotation_boxes.extend([text1, text2])

        if self.show_lobes:
            if self.use_two_plots:
                self.highlight_lobes_lines(self.ax1, self.theta_h, self.h_data, 'H-plane', main_idx)
                self.highlight_lobes_lines(self.ax2, self.theta_e, self.e_data, 'E-plane', main_idx)
            else:
                self.highlight_lobes_lines(self.ax1, self.theta_h, self.h_data, 'H-plane')
                self.highlight_lobes_lines(self.ax1, self.theta_e, self.e_data, 'E-plane')
                self.highlight_lobes_lines(self.ax2, self.theta_h, self.h_data, 'H-plane')
                self.highlight_lobes_lines(self.ax2, self.theta_e, self.e_data, 'E-plane')

        self.update_figure_style()
        self.store_original_limits()
        self.draw()

    def zoom_in(self, factor=0.8):
        """Fixed zoom in that preserves polar plot integrity"""
        min_ylim = 1e-3
        max_ylim = 1e6
        for ax in [self.ax1, self.ax2]:
            if ax is not None and self.has_data:
                try:
                    rmin, rmax = ax.get_ylim()
                    # Calculate new range
                    range_size = rmax - rmin
                    new_range = range_size * factor
                    center = (rmin + rmax) / 2
                    new_rmin = max(center - new_range/2, 0)  # Don't go below 0 for polar
                    new_rmax = min(center + new_range/2, max_ylim)
                    new_rmax = max(new_rmax, min_ylim)  # Ensure minimum range
                    if new_rmax > new_rmin:
                        ax.set_ylim(new_rmin, new_rmax)
                except Exception as e:
                    print(f"Error zooming axis: {e}")
                    continue
        # Update stored limits
        self.store_original_limits()
        self.draw_idle()

    def zoom_out(self, factor=1.25):
        """Fixed zoom out that preserves polar plot integrity"""
        min_ylim = 1e-3
        max_ylim = 1e6
        for ax in [self.ax1, self.ax2]:
            if ax is not None and self.has_data:
                try:
                    rmin, rmax = ax.get_ylim()
                    # Calculate new range
                    range_size = rmax - rmin
                    new_range = range_size * factor
                    center = (rmin + rmax) / 2
                    new_rmin = max(center - new_range/2, 0)  # Don't go below 0 for polar
                    new_rmax = min(center + new_range/2, max_ylim)
                    new_rmax = max(new_rmax, min_ylim)  # Ensure minimum range
                    if new_rmax > new_rmin:
                        ax.set_ylim(new_rmin, new_rmax)
                except Exception as e:
                    print(f"Error zooming axis: {e}")
                    continue
        # Update stored limits
        self.store_original_limits()
        self.draw_idle()

    def reset_view(self):
        """Reset to original view after plotting"""
        if self.has_data and self.original_data_h is not None and self.original_data_e is not None:
            # Replot with original data to reset everything
            self.plot_2D(self.original_data_h, self.original_data_e)

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
        
        self.save_button = QPushButton("Save Project")
        self.save_button.setIcon(QIcon.fromTheme("document-save"))
        
        self.offset_button = QPushButton("Apply Offset")
        self.offset_button.setCheckable(True)
        self.offset_button.setIcon(QIcon.fromTheme("transform-move"))
        
        self.online_view_button = QPushButton("Online View")
        self.online_view_button.setIcon(QIcon.fromTheme("network-wired"))
        
        
        
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
            self.online_view_button, 
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
        
        # Navigation toolbar layout
        nav_layout1 = QHBoxLayout()
        
        # Placeholder for matplotlib toolbar (will be added by Window class)
        self.tab1_canvas_layout = QVBoxLayout()
        
        # Custom navigation buttons
        
        
        self.color_button1 = QPushButton("Change Color")
        self.color_button1.setIcon(QIcon.fromTheme("color-picker"))
        #a button here fo details 
        self.highlight_lobes_button = QPushButton("Highlight Lobes")
        self.highlight_lobes_button.setIcon(QIcon.fromTheme("dialog-information"))
        self.highlight_lobes_button.setCheckable(True)
        
        nav_layout1.addStretch(1)
        
        nav_layout1.addWidget(self.color_button1)
        nav_layout1.addWidget(self.highlight_lobes_button)#the button here
        
        tab1_layout.addLayout(nav_layout1)
        tab1_layout.addLayout(self.tab1_canvas_layout)
        
        # Controls layout
        controls_layout1 = QHBoxLayout()
        
        self.back_button1 = QPushButton("Back")
        self.back_button1.setIcon(QIcon.fromTheme("go-previous"))
        
        self.smooth_label1 = QLabel("Smooth:")
        self.smoothness_slider1 = QSlider(Qt.Horizontal)
        
        self.smoothness_slider1.setValue(0)
        self.smoothness_slider1.setRange(0,15)
        self.smoothness_slider1.setSingleStep(2)  # Step size of 2
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
        
        self.smooth_button = QPushButton("Smooth")
        self.smooth_button.setCheckable(True)
        
        self.next_button2 = QPushButton("Next")
        self.next_button2.setIcon(QIcon.fromTheme("go-next"))
        
        controls_layout2.addWidget(self.back_button2)
        controls_layout2.addWidget(self.smooth_button)
        
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
            QSlider::sub-page:horizontal {{
                background: {primary_color};
                border-radius: 3px;
            }}
            QSlider::add-page:horizontal {{
                background: {button_bg};
                border-radius: 3px;
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
            self.online_view_button,
            
            self.color_button3D, self.zoom_in_button2, self.zoom_out_button2, self.smooth_button
        ]
        
        nav_buttons = [
            self.back_button1, self.next_button1, 
            self.back_button2, self.next_button2,
            self.highlight_lobes_button,self.color_button1
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

        # Create custom toolbars with reset functionality
        self.setup_custom_toolbars()

        # Add figures and toolbars to layouts
        self.view.tab1_canvas_layout.addWidget(self.toolbar1)
        self.view.tab1_canvas_layout.addWidget(self.fig2D)
        self.view.tab2_canvas_layout.addWidget(self.toolbar2)
        self.view.tab2_canvas_layout.addWidget(self.fig3D)
        
        # Connect theme toggle
        self.view.theme_toggle.stateChanged.connect(self.toggle_theme)
        self.view.highlight_lobes_button.toggled.connect(self.toggle_lobes_highlighting)
        # Connect custom reset buttons
        self.connect_toolbar_events()

    def toggle_lobes_highlighting(self, checked): #this too 
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
    def file_history(self, mode):
        """
        Open a file dialog for saving or opening a JSON file, depending on mode.
        mode: 'save' or 'open'
        Returns the selected file path or None if cancelled.
        """
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("JSON Files (*.json)")
        file_dialog.setDefaultSuffix("json")
        if mode == 'save':
            file_dialog.setAcceptMode(QFileDialog.AcceptSave)
            dialog_title = "Save History As"
        elif mode == 'open':
            file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
            dialog_title = "Open History File"
        else:
            raise ValueError("mode must be 'save' or 'open'")
        file_dialog.setWindowTitle(dialog_title)
        if file_dialog.exec():
            return file_dialog.selectedFiles()[0]
        return None

    def setup_custom_toolbars(self):
        """Create custom toolbars with reset functionality"""
        self.toolbar1 = NavigationToolbar(self.fig2D, self)
        self.toolbar2 = NavigationToolbar(self.fig3D, self)
        # Add custom reset actions to toolbars
        reset_action1 = QAction("Reset View", self)
        reset_action1.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        reset_action1.triggered.connect(self.fig2D.reset_view)
        self.toolbar1.addAction(reset_action1)
        reset_action2 = QAction("Reset View", self)
        reset_action2.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        reset_action2.triggered.connect(self.fig3D.reset_view)
        self.toolbar2.addAction(reset_action2)

    def connect_toolbar_events(self):
        """Connect toolbar events to fix axis drift"""
        # Override toolbar home button behavior
        try:
            # Find and override home button
            for action in self.toolbar1.actions():
                if action.text() == 'Home':
                    action.triggered.disconnect()  # Disconnect original
                    action.triggered.connect(self.home_2d)
                elif action.text() == 'Back':
                    action.triggered.connect(self.fix_2d_after_navigation)
                elif action.text() == 'Forward':
                    action.triggered.connect(self.fix_2d_after_navigation)
            for action in self.toolbar2.actions():
                if action.text() == 'Home':
                    action.triggered.disconnect()  # Disconnect original
                    action.triggered.connect(self.home_3d)
                elif action.text() == 'Back':
                    action.triggered.connect(self.fix_3d_after_navigation)
                elif action.text() == 'Forward':
                    action.triggered.connect(self.fix_3d_after_navigation)
        except Exception as e:
            print(f"Warning: Could not override toolbar buttons: {e}")

    def home_2d(self):
        """Custom home function for 2D plots"""
        self.fig2D.reset_view()

    def home_3d(self):
        """Custom home function for 3D plots"""
        self.fig3D.reset_view()

    def fix_2d_after_navigation(self):
        """Fix 2D plots after toolbar navigation"""
        from PySide6.QtCore import QTimer
        QTimer.singleShot(100, self.fig2D.restore_proper_limits)

    def fix_3d_after_navigation(self):
        """Fix 3D plots after toolbar navigation"""
        from PySide6.QtCore import QTimer
        QTimer.singleShot(100, self.fig3D.store_original_view)
