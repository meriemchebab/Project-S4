import numpy as np
import matplotlib.pyplot as plt
import mplcursors
from scipy.signal import savgol_filter
from mpl_toolkits.mplot3d import Axes3D
from scipy.signal import find_peaks


def file_reader(file_name): #to read the file 
    data = []
    with open(file_name, 'r') as file:
        for line in file:
            try:
                val = float(line)
                data.append(val)
            except ValueError:
                pass
    return data


def Normal(data): #idk dont do much 
        max_index = np.argmax(data) # find index of max value
        data[0], data[max_index] = data[max_index], data[0]  # swap
        return data
 

def Fix_Max(data): #get the max value and fix the values
    half_length = len(data) // 2
    plan_e = np.array(data[:half_length])
    plan_h = np.array(data[half_length:])

    plan_h_db = savgol_filter(plan_e, window_length=11, polyorder=2)
    plan_e_db = savgol_filter(plan_h, window_length=11, polyorder=2)
    plan_h_2d = plan_h_db - np.max(plan_h_db)
    plan_e_2d = plan_e_db - np.max(plan_e_db)

    return plan_e_2d, plan_h_2d #returns 2lists of the values


def plot_2d(values, max=True, same=True, highlight=True, max_min_box=True):
    half_length = len(values) // 2
    theta_deg = np.linspace(0, 360, half_length)
    theta_rad = np.radians(theta_deg)

    if max:  # switch the value max
        plan_e_2d, plan_h_2d = Fix_Max(values)
        np1 = Normal(plan_e_2d)
        np2 = Normal(plan_h_2d)

        # filter the values
        np1_filtered = savgol_filter(np1, window_length=11, polyorder=2)
        np2_filtered = savgol_filter(np2, window_length=11, polyorder=2)

        Afficher_2d(np1_filtered, np2_filtered, theta_rad,same=same, highlight=highlight, max_min_box=max_min_box)

    else:  # no max change
        plan_e = np.array(values[:half_length])
        plan_h = np.array(values[half_length:])

        plan_e_filtered = savgol_filter(plan_e, window_length=11, polyorder=2)
        plan_h_filtered = savgol_filter(plan_h, window_length=11, polyorder=2)

        Afficher_2d(plan_e_filtered, plan_h_filtered, theta_rad,same=same, highlight=highlight, max_min_box = max_min_box)


#function lobe here
def highlight_lobes_lines(ax, theta, data, label_prefix=''): #for a button to show the lobes

    peaks, _ = find_peaks(data)
    peak_values = data[peaks]

    if len(peak_values) == 0:
        print(f"No peaks found in {label_prefix}")
        return

    delta_theta = theta[1] - theta[0]
    window_degrees = 5
    window_size = int(window_degrees / (360 / len(theta)))

    def plot_lobe(idx, color, label, annotation=None):
        idx_start = max(0, idx - window_size)
        idx_end = min(len(theta), idx + window_size + 1)
        highlight_mask = np.full_like(data, np.nan)
        highlight_mask[idx_start:idx_end] = data[idx_start:idx_end]
        ax.plot(theta, highlight_mask, color=color, linewidth=2, label=label)

        if annotation:
            ax.annotate(
                annotation,
                xy=(theta[idx], data[idx]),
                xytext=(theta[idx], data[idx] + 3),
                arrowprops=dict(arrowstyle='->', color=color),
                ha='center',
                fontsize=10,
                color=color,
                bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.6)
            )

    # Main lobe
    main_idx = peaks[np.argmax(peak_values)]
    plot_lobe(main_idx, 'green', f'{label_prefix} Main Lobe', 'Main Lobe')

    # Secondary lobes — plot all, but annotate only once
    secondary_label = f'{label_prefix} Secondary Lobes'
    secondary_annotated = False
    for idx in peaks:
        if idx == main_idx:
            continue
        plot_lobe(idx, 'orange', secondary_label if not secondary_annotated else None,
                  'Secondary Lobe' if not secondary_annotated else None)
        secondary_annotated = True

    # Back lobe
    back_angle = (theta[main_idx] + np.pi) % (2 * np.pi)
    closest_idx = np.argmin(np.abs(theta - back_angle))
    plot_lobe(closest_idx, 'purple', f'{label_prefix} Back Lobe', 'Back Lobe')

    # Clean legend
    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    ax.legend(unique.values(), unique.keys(), loc='lower right')

def blend_with_white(color, blend_factor=0.5): #extra thing but better makes the color lighter (so it looks better fl cursseur)
    rgba = np.array(mcolors.to_rgba(color))
    white = np.array([1, 1, 1, 1])
    blended = (1 - blend_factor) * rgba + blend_factor * white
    return blended

def add_cursor(ax_list): #to have a cursseur with the color of the graphe
    cursor = mplcursors.cursor(ax_list, hover=True)
    
    def custom_annotate(sel):
        artist = sel.artist
        color = artist.get_color()
        light_color = blend_with_white(color, blend_factor=0.5)  # try 0.3–0.7
        
        sel.annotation.set_text(
            f"Angle: {np.degrees(sel.target[0]):.1f}°\nValue: {sel.target[1]:.2f} dB"
        )
        sel.annotation.get_bbox_patch().set(fc=light_color, alpha=0.7)
    
    cursor.connect("add", custom_annotate)

def add_max_min_box(fig, ax, value_array, label, x_pos, y_pos, color): #for the max and min button 
    maxv = np.max(value_array)
    minv = np.min(value_array)
    
    # Show max/min in top-left info box
    fig.text(x_pos, y_pos, f"Max ({label}): {maxv:.2f} dB\nMin ({label}): {minv:.2f} dB",
             fontsize=12, va='center', ha='left',
             bbox=dict(facecolor=color, alpha=0.5, edgecolor='black'))
    
    # Get angle positions
    angles = np.linspace(0, 360, len(value_array))
    max_idx = np.argmax(value_array)
    min_idx = np.argmin(value_array)
    max_angle = angles[max_idx]
    min_angle = angles[min_idx]
    
    # Calculate coordinates for arrow annotations
    max_r = value_array[max_idx]
    min_r = value_array[min_idx]
    
    # Add arrow annotation for max
    ax.annotate(f'{maxv:.2f} dB',
                xy=(np.radians(max_angle), max_r),  # arrow tip
                xytext=(np.radians(max_angle), max_r + 5),  # text position
                textcoords='data',
                arrowprops=dict(arrowstyle="->", color='black', lw=1.5),
                ha='center', va='bottom', fontsize=10,
                bbox=dict(facecolor='white', edgecolor='black', alpha=0.7))
    
    # Add arrow annotation for min
    ax.annotate(f'{minv:.2f} dB',
                xy=(np.radians(min_angle), min_r),  # arrow tip
                xytext=(np.radians(min_angle), min_r + 5),  # text position
                textcoords='data',
                arrowprops=dict(arrowstyle="->", color='black', lw=1.5),
                ha='center', va='bottom', fontsize=10,
                bbox=dict(facecolor='white', edgecolor='black', alpha=0.7))



def Afficher_2d(plan_e_2d, plan_h_2d, theta, same=True, highlight=True, max_min_box=True):
    fig, ax = None, None

    if same:
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

        ax.plot(theta, plan_e_2d, label='E-plane', color='blue')
        ax.plot(theta, plan_h_2d, label='H-plane', color='red')

        if highlight:
            highlight_lobes_lines(ax, theta, plan_e_2d, label_prefix='E-plane') #to hightligh the lobe (the call)
            highlight_lobes_lines(ax, theta, plan_h_2d, label_prefix='H-plane')

        ax.set_theta_direction(-1)
        ax.set_theta_offset(np.pi / 2)
        ax.set_title('Polar Plot - Combined', x=0.2, y=1.05)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.2))
        fig.set_size_inches(6, 6)

        add_cursor([ax])

        if max_min_box:
            add_max_min_box(fig, ax, plan_e_2d, 'E-plane', 0.05, 0.9, 'lightblue')  #to have the max and min (call)
            add_max_min_box(fig, ax, plan_h_2d, 'H-plane', 0.05, 0.75, 'lightpink')

    else:
        fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw={'projection': 'polar'}, figsize=(12, 6))

        ax1.plot(theta, plan_e_2d, label='E-plane', color='blue')
        if highlight:
            highlight_lobes_lines(ax1, theta, plan_e_2d, label_prefix='E-plane')
        ax1.set_title("E-plane Pattern", x=0.2, y=1.05)
        ax1.set_theta_direction(-1)
        ax1.set_theta_offset(np.pi / 2)
        ax1.legend(loc='upper right', bbox_to_anchor=(1.3, 1.2))

        ax2.plot(theta, plan_h_2d, label='H-plane', color='red')
        if highlight:
            highlight_lobes_lines(ax2, theta, plan_h_2d, label_prefix='H-plane')
        ax2.set_title("H-plane Pattern", x=0.2, y=1.05)
        ax2.set_theta_direction(-1)
        ax2.set_theta_offset(np.pi / 2)
        ax2.legend(loc='upper right', bbox_to_anchor=(1.3, 1.2))

        fig.suptitle("2D Radiation Patterns - Separate", fontsize=16)

        add_cursor([ax1, ax2])

        if max_min_box:
            add_max_min_box(fig, ax1, plan_e_2d, 'E-plane', 0.025, 0.9, 'lightblue')
            add_max_min_box(fig, ax2, plan_h_2d, 'H-plane', 0.5, 0.9, 'lightpink')

    plt.tight_layout()
    plt.show()

def plot_3d(data, max=True): #3d code
    half_length = len(data) // 2
    plan_e = np.array(data[:half_length])
    plan_h = np.array(data[half_length:])
    
   
    if max: #if we do the max thing 
        plan_e_db, plan_h_db = Fix_Max(data)  

    else: #no max thing
        plan_h_db = savgol_filter(plan_e, 11, 2)
        plan_e_db = savgol_filter(plan_h, 11, 2)

    # Convert theta to radians
    theta = np.linspace(0, 2 * np.pi, half_length)
    phi = np.linspace(0, np.pi, half_length)
    theta, phi = np.meshgrid(theta, phi)
    
    r = (np.outer(plan_h_db, np.ones_like(plan_e_db)) + np.outer(np.ones_like(plan_h_db), plan_e_db)) / 2

    X = r * np.sin(phi) * np.cos(theta)
    Y = r * np.sin(phi) * np.sin(theta)
    Z = r * np.cos(phi)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(X, Y, Z, cmap='jet', linewidth=0)

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis (dB)')
    ax.set_title('3D Radiation Pattern (E + H averaged)', fontsize=14)

    cbar = fig.colorbar(surf, shrink=0.6, aspect=10)
    cbar.set_label('La puissance en db', fontsize=12)

    #the box that show the value 
    annotation_box = ax.text2D(0.05, 0.9, '', transform=ax.transAxes, fontsize=12, va='center', ha='left',
                                bbox=dict(facecolor='lightblue', alpha=0.5, edgecolor='black'))

    def on_click(event): # the event of the click so that it shows
        if event.inaxes == ax: #check click in or out the plot 
            x_click, y_click = event.xdata, event.ydata #to get the coordenet

            distance = np.sqrt((X - x_click)**2 + (Y - y_click)**2)  # to get the nerest value
            min_dist_index = np.unravel_index(np.argmin(distance), distance.shape)

            angle = np.degrees(theta[min_dist_index])
            value = Z[min_dist_index]

            annotation_box.set_text(f"Angle: {angle:.1f}°\nValue: {value:.2f} dB" ) #update the vla in the box 
            plt.draw()  #to redraw the plot with the box 

    fig.canvas.mpl_connect('button_press_event', on_click) # to work (conest the bo=utton click the the event click)(kayen click the fuc is called)
    
    plt.show()

# Example of a main 
data = file_reader("3Dcourbe1.txt")
#plot_2d(data, max=True , same=True)
plot_3d(data, False)
