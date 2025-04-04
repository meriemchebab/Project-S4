import numpy as np
import matplotlib.pyplot as plt

def read_file(file_name):
    with open(file_name, 'r') as file:
        degree = []
    for line in file:
        try :
            lin = float(line)
            degree.append(lin)
        except ValueError:
            pass
         # Returns the values as a list to use for the 3d and 2d
    return degree
def Polar_2d(data): #its to draw the paln h and plan e
   
    half_length = len(data) // 2
    curve1 = np.array(data[:half_length])  # First half as Curve 1
    curve2 = np.array(data[half_length:])  # Second half as Curve 2
    theta = np.linspace(0, 2 * np.pi, half_length)  # Create angle values

    axes = plt.subplots(1, 2, subplot_kw={'projection': 'polar'}, figsize=(12, 6))

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
                data1 = read_file('C:\Users\hp\Desktop\Project\Project-S4\try\fich.txt')  # Read file
                Polar_2d(data1)  # Show 2D polar graphs
                Surface_3d(data1)  # Show 3D surface plot
            case "2":
                print("You have selected file 2")
                data2 = read_file() 
                Polar_2d(data2) 
                Surface_3d(data2)
            case "3":
                print("Exiting. Thank you!")
                break 
            case _:
                print("Invalid input. Enter a number from 1-3.")

menu()

