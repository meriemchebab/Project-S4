import numpy as np
import matplotlib.pyplot as plt
import mplcursors
from scipy.signal import savgol_filter
from mpl_toolkits.mplot3d import Axes3D


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


def plot_2d(values, max=True, same=True):  # to draw the graph
    half_length = len(values) // 2
    theta_deg = np.linspace(0, 360, half_length)
    theta_rad = np.radians(theta_deg)

    if max:  # switch the value max 
        plan_e_2d, plan_h_2d = Fix_Max(values)
        np1 = Normal(plan_e_2d) #so swasp the index
        np2 = Normal(plan_h_2d)
        
        # filter the values
        np1_filtered = savgol_filter(np1, window_length=11, polyorder=2)
        np2_filtered = savgol_filter(np2, window_length=11, polyorder=2)
        
        if same:
            Afficher_2d(np1_filtered, np2_filtered, theta_rad, same=True)
        else:
            Afficher_2d(np1_filtered, np2_filtered, theta_rad, same=False)

    else:  # no max change
        plan_e = np.array(values[:half_length])
        plan_h = np.array(values[half_length:])

        plan_e_filtered = savgol_filter(plan_e, window_length=11, polyorder=2)
        plan_h_filtered = savgol_filter(plan_h, window_length=11, polyorder=2)

        if same:
            Afficher_2d(plan_e_filtered, plan_h_filtered, theta_rad, same=True)
        else:
            Afficher_2d(plan_e_filtered, plan_h_filtered, theta_rad, same=False)


def Afficher_2d(plan_e_2d, plan_h_2d, theta, same=True): #affichage fonction
    fig, ax = None, None

    if same: #si les deux graphe in the same plot
        # Create the same plot
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.plot(theta, plan_e_2d, label='E-plane', color='blue')
        ax.plot(theta, plan_h_2d, label='H-plane', color='red')
        ax.set_theta_direction(-1)
        ax.set_theta_offset(np.pi / 2)
        ax.set_title('Polar Plot - Combined')
        ax.legend(loc='upper right')
        fig.set_size_inches(6, 6)

        #~~~~form here (to have the curceur thing)
        cursor = mplcursors.cursor([ax], hover=True) #to get the values like plotly bl curser (can make it custom)
        
        def custom_annotate(sel):
            artist = sel.artist
            label = artist.get_label()
            if label == 'E-plane':
                color = 'lightblue'  # or any color you prefer
            elif label == 'H-plane':
                color = 'lightpink'  # or any color you prefer
            else:
                color = 'gray'
            sel.annotation.set_text(f"Angle: {np.degrees(sel.target[0]):.1f}°\nValue: {sel.target[1]:.2f} dB")
            sel.annotation.get_bbox_patch().set(fc=color, alpha=0.7)

        cursor.connect("add", custom_annotate)
        # ~~~~to here

        #~~~~from here (to have the box with the max and min)
        maxv = np.max(plan_e_2d)
        minv = np.min(plan_e_2d)
        fig.text(0.05, 0.9, f"Max (E-plane): {maxv:.1f} dB\nMin (E-plane): {minv:.2f} dB",
                 fontsize=12, va='center', ha='left',
                 bbox=dict(facecolor='lightblue', alpha=0.5, edgecolor='black'))
        

        maxv = np.max(plan_h_2d)
        minv = np.min(plan_h_2d)
        fig.text(0.05, 0.75, f"Max (H-plane): {maxv:.1f} dB\nMin (H-plane): {minv:.2f} dB",
                 fontsize=12, va='center', ha='left',
                 bbox=dict(facecolor='lightpink', alpha=0.5, edgecolor='black'))
        #~~~~~~to here
        
    else: #if les deux graphe they on seperat plot (the same plote 
        # Create separate plots
        fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw={'projection': 'polar'}, figsize=(12, 6))

        ax1.plot(theta, plan_e_2d, label='E-plane', color='blue')
        ax1.set_title("E-plane Pattern")
        ax1.set_theta_direction(-1)
        ax1.set_theta_offset(np.pi / 2)
        ax1.legend(loc='upper right')

        ax2.plot(theta, plan_h_2d, label='H-plane', color='red')
        ax2.set_title("H-plane Pattern")
        ax2.set_theta_direction(-1)
        ax2.set_theta_offset(np.pi / 2)
        ax2.legend(loc='upper right')

        fig.suptitle("2D Radiation Patterns - Separate", fontsize=16)

        #to get the values like plotly bl curser (can make it custom)
        cursor = mplcursors.cursor([ax1, ax2], hover=True)

        def custom_annotate(sel):
            artist = sel.artist
            label = artist.get_label()
            if label == 'E-plane':
                color = 'lightblue'  # or any color you prefer
            elif label == 'H-plane':
                color = 'lightpink'  # or any color you prefer
            else:
                color = 'gray'
            sel.annotation.set_text(f"Angle: {np.degrees(sel.target[0]):.1f}°\nValue: {sel.target[1]:.2f} dB")
            sel.annotation.get_bbox_patch().set(fc=color, alpha=0.7)

        cursor.connect("add", custom_annotate)

        maxv = np.max(plan_e_2d)
        minv = np.min(plan_e_2d)
        fig.text(0.025, 0.9, f"Max (E-plane): {maxv:.1f} dB\nMin (E-plane): {minv:.2f} dB",
                 fontsize=12, va='center', ha='left',
                 bbox=dict(facecolor='lightblue', alpha=0.5, edgecolor='black'))
        

        maxv = np.max(plan_h_2d)
        minv = np.min(plan_h_2d)
        fig.text(0.5, 0.9, f"Max (H-plane): {maxv:.1f} dB\nMin (H-plane): {minv:.2f} dB",
                 fontsize=12, va='center', ha='left',
                 bbox=dict(facecolor='lightpink', alpha=0.5, edgecolor='black'))

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

    surf = ax.plot_surface(X, Y, Z, cmap='plasma', linewidth=0.5)

    ax.set_title('3D Radiation Pattern (E + H averaged)', fontsize=14)

    #form here to get the values with click
    fig.colorbar(surf, shrink=0.6, aspect=10)
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
    #~~~~to here

    plt.show()

# Example of a main 
data = file_reader("3Dcourbe4.txt")
plot_2d(data, max=True , same=True)
#plot_3d(data, False)
