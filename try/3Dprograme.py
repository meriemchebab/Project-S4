import numpy as np
import matplotlib.pyplot as plt

def read_file(file_name):
    degree = []
    with open(file_name, 'r') as file:
        for line in file:
            try:
                lin = float(line.strip())
                degree.append(lin)
            except ValueError:
                continue
    return degree

def Polar_2d(data):
    half_length = len(data) // 2
    curve1 = np.array(data[:half_length])
    curve2 = np.array(data[half_length:])
    theta = np.linspace(0, 2 * np.pi, half_length)

    fig, axes = plt.subplots(1, 2, subplot_kw={'projection': 'polar'}, figsize=(12, 6))

    axes[0].plot(theta, curve1, label="Plan H", color='b')
    axes[0].set_title("Plan H")
    axes[0].legend()

    axes[1].plot(theta, curve2, label="Plan E", color='r')
    axes[1].set_title("Plan E")
    axes[1].legend()

    plt.tight_layout()
    plt.show()

def Surface_3d(data):
    half_length = len(data) // 2
    curve1 = np.array(data[:half_length])
    curve2 = np.array(data[half_length:])
    theta = np.linspace(0, 2 * np.pi, half_length)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    X, Y = np.meshgrid(theta, theta)
    Z = np.outer(curve1, curve2)

    ax.plot_surface(X, Y, Z, cmap='plasma')

    ax.set_xlabel("Theta (X)")
    ax.set_ylabel("Theta (Y)")
    ax.set_zlabel("Amplitude")
    ax.set_title("3D Surface Plot")

    plt.show()

def menu():
    while True:
        print("\nMenu :")
        print("1. Visualiser fichier 1")
        print("2. Visualiser fichier 2")
        print("3. Quitter")

        choice = input("Votre choix (1-3) : ")

        match choice:
            case "1":
                print("Fichier 1 sélectionné")
                path1 = r"C:\Users\hp\Desktop\Project\Project-S4\try\fich.txt"
                data1 = read_file(path1)
                Polar_2d(data1)
                Surface_3d(data1)
            case "2":
                print("Fichier 2 sélectionné")
                path2 = input("Entrez le chemin du fichier 2 : ")
                data2 = read_file(path2)
                Polar_2d(data2)
                Surface_3d(data2)
            case "3":
                print("Merci, au revoir.")
                break
            case _:
                print("Entrée invalide. Choisissez entre 1 et 3.")

menu()
