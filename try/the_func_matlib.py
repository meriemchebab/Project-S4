import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

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

def Fix_Max(data): #get the max value and fix the values
    half_length = len(data) // 2
    plan_e = np.array(data[:half_length])
    plan_h = np.array(data[half_length:])

    plan_h_db = savgol_filter(plan_e, window_length=11, polyorder=2)
    plan_e_db = savgol_filter(plan_h, window_length=11, polyorder=2)
    plan_h_2d = plan_h_db - np.max(plan_h_db)
    plan_e_2d = plan_e_db - np.max(plan_e_db)

    return plan_e_2d, plan_h_2d #returns 2lists of the values 

def plot_2d(values, max=True, same=True): #to draw the graph 
    half_length = len(values) // 2
    theta_deg = np.linspace(0, 360, half_length)
    theta_rad = np.radians(theta_deg)

    if max: #to switch the values
        plan_e_2d, plan_h_2d = Fix_Max(values)
        if same:
            Afficher(plan_e_2d, plan_h_2d, theta_rad, same=True)
        else:
            Afficher(plan_e_2d, plan_h_2d, theta_rad, same=False)
    else: #we dont 
        plan_e = np.array(values[:half_length])
        plan_h = np.array(values[half_length:])

        plan_h_db = savgol_filter(plan_e, window_length=11, polyorder=2)
        plan_e_db = savgol_filter(plan_h, window_length=11, polyorder=2)

        if same: #the'll have the same place
            Afficher(plan_e_db, plan_h_db, theta_rad, same=True)
        else:  #diffrent place
            Afficher(plan_e_db, plan_h_db, theta_rad, same=False)

def Afficher(plan_e_2d, plan_h_2d, theta, same=True): # the affichage fonction 

    if same: #of ots on the same 
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.plot(theta, plan_h_2d, label='H-plane', color='blue')
        ax.plot(theta, plan_e_2d, label='E-plane', color='red')
        ax.set_theta_direction(-1)
        ax.set_theta_offset(np.pi / 2)
        ax.set_title('Polar Plot - Combined')
        ax.legend(loc='upper right')
        fig.set_size_inches(6, 6)

    else: # seperated
        fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw={'projection': 'polar'}, figsize=(12, 6))
        ax1.plot(theta, plan_h_2d, label='H-plane', color='blue')
        ax1.set_title("H-plane Pattern")
        ax1.set_theta_direction(-1)
        ax1.set_theta_offset(np.pi / 2)

        ax2.plot(theta, plan_e_2d, label='E-plane', color='red')
        ax2.set_title("E-plane Pattern")
        ax2.set_theta_direction(-1)
        ax2.set_theta_offset(np.pi / 2)

        fig.suptitle("2D Radiation Patterns - Separate", fontsize=16)

    plt.tight_layout()
    plt.show()

# Example of a main 
data = file_reader("3Dcourbe4.txt")
plot_2d(data, max=False, same=True)
