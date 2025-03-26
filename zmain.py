import pandas as pd
import numpy as np
import plot  # Import the "plot.py" fichier 

def file1():
 
    df = pd.read_csv(r"courbe1.txt", header=None)
    df[0] = pd.to_numeric(df[0], errors='coerce')

    Vmin = df[0].min()
    Vmax = df[0].max()
    print(f"Max file 1: {Vmax}, Min: {Vmin}, Offset: {Vmin}")

    # If the max value is negative, adjust the data before plotting
    if Vmax < 0:
        df[0] -= Vmax
        df.to_csv("New_courbe1.txt", header=False, index=False)
        plot.file_handel("New_courbe1.txt")
    else:
        plot.file_handel("courbe1.txt")

def file2():
    """ Process and visualize data from courbe2.txt """
    df = pd.read_csv(r"courbe2.txt", header=None)
    df[0] = pd.to_numeric(df[0], errors='coerce')

    Vmin = df[0].min()
    Vmax = df[0].max()
    print(f"Max file 2: {Vmax}, Min: {Vmin}, Offset: {Vmin}")

    if Vmax < 0:
        df[0] -= Vmax
        df.to_csv("New_courbe2.txt", header=False, index=False)
        plot.file_handel("New_courbe2.txt")
    else:
        plot.file_handel("courbe2.txt")

def file3():
    """ Process and visualize data from courbe3.txt """
    df = pd.read_csv(r"courbe3.txt", header=None)
    df[0] = pd.to_numeric(df[0], errors='coerce')

    Vmin = df[0].min()
    Vmax = df[0].max()
    print(f"Max file 3: {Vmax}, Min: {Vmin}, Offset: {Vmin}")

    if Vmax < 0:
        df[0] -= Vmax
        df.to_csv("New_courbe3.txt", header=False, index=False)
        plot.file_handel("New_courbe3.txt")
    else:
        plot.file_handel("courbe3.txt")

def file4():
    """ Process and visualize data from courbe4.txt """
    df = pd.read_csv(r"courbe4.txt", header=None)
    df[0] = pd.to_numeric(df[0], errors='coerce')

    Vmin = df[0].min()
    Vmax = df[0].max()
    print(f"Max file 4: {Vmax}, Min: {Vmin}, Offset: {Vmin}")

    if Vmax < 0:
        df[0] -= Vmax
        df.to_csv("New_courbe4.txt", header=False, index=False)
        plot.file_handel("New_courbe4.txt")
    else:
        plot.file_handel("courbe4.txt")

def menu():
    """ Display a menu for the user to choose actions """
    while True:
        print("\nMenu Options:")
        print("1. Display File 1 in 2D")
        print("2. Display File 2 in 2D")
        print("3. Display File 3 in 2D")
        print("4. Display File 4 in 2D")
        print("5. Display Files 1 & 2 in 3D")
        print("6. Display Files 3 & 4 in 3D")
        print("7. Exit")

        choice = input("Select an option (1-7): ")

        match choice:
            case "1":
                print("Displaying File 1 in 2D")
                file1()
            case "2":
                print("Displaying File 2 in 2D")
                file2()
            case "3":
                print("Displaying File 3 in 2D")
                file3()
            case "4":
                print("Displaying File 4 in 2D")
                file4()
            case "5":
                print("Displaying Files 1 & 2 in 3D")
                plot.plot_3d("courbe1.txt", "courbe2.txt")
            case "6":
                print("Displaying Files 3 & 4 in 3D")
                plot.plot_3d("courbe3.txt", "courbe4.txt")
            case "7":
                print("Closing the program.")
                break
            case _:
                print("Invalid input. Please select a number between 1 and 7.")

menu()
