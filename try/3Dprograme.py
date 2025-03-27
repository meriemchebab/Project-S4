import numpy as np
import matplotlib.pyplot as plt

def read_file(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    data_lines = lines[4:] #we skiped the 4 first lines

    cleaned_data = [] # to skip the 2 mid lines 
    count = 0
    i = 0
    while i < len(data_lines):
        if count > 0 and count % 360 == 0:
            i += 2  # Skip 2 lines
            if i >= len(data_lines): 
                break
        cleaned_data.append(float(data_lines[i].strip()))
        count += 1
        i += 1

    return cleaned_data  # Returns the values as a list to use for the 3d and 2d

def Polar_2d(data): #its to draw the paln h and plan e
   
    half_length = len(data) // 2
    curve1 = np.array(data[:half_length])  # First half as Curve 1
    curve2 = np.array(data[half_length:])  # Second half as Curve 2
    theta = np.linspace(0, 2 * np.pi, half_length)  # Create angle values

    fig, axes = plt.subplots(1, 2, subplot_kw={'projection': 'polar'}, figsize=(12, 6))

    axes[0].plot(theta, curve1, label="Plan H", color='b')
    axes[0].set_title("Plan H")
    axes[0].legend()

    axes[1].plot(theta, curve2, label="Plan E", color='r')
    axes[1].set_title("Plan E")
    axes[1].legend()

    plt.show()

def Surface_3d(data): # to make our 3d surface

    half_length = len(data) // 2
    curve1 = np.array(data[:half_length])  # X values
    curve2 = np.array(data[half_length:])  # Y values

    theta = np.linspace(0, 2 * np.pi, half_length)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    X, Y = np.meshgrid(theta, theta)  # Create grid for X and Y
    Z = np.outer(curve1, curve2)  # Compute Z values

    ax.plot_surface(X, Y, Z, cmap='plasma')

    ax.set_xlabel("Theta (X)")
    ax.set_ylabel("Theta (Y)")
    ax.set_zlabel("Z (Computed)")
    ax.set_title("3D Surface Plot")

    plt.show()

#the seconde file

 

def menu():
    while True:
        print("\nThe menu:")
        print("1. File 1")
        print("2. File 2")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        match choice:
            case "1":
                print("You have selected file 1")
                data1 = read_file("3Dcourbe1.txt")  # Read file
                Polar_2d(data1)  # Show 2D polar graphs
                Surface_3d(data1)  # Show 3D surface plot
            case "2":
                print("You have selected file 2")
                data2 = read_file("3Dcourbe2.txt") 
                Polar_2d(data2) 
                Surface_3d(data2)
            case "3":
                print("Exiting. Thank you!")
                break 
            case _:
                print("Invalid input. Enter a number from 1-3.")

menu()

