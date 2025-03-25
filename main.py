
# here we make the gui and call every function from ather files
import pandas as pd # reading and anylise the data
import numpy as np #array manipulation
import plotly.graph_objs as go # the liberary that will be used to creat the plot 

def file_handel(file_name):
# Read the file and create a list of degree values
    with open(file_name, 'r') as file:
        # Read all lines
        degree = [float(line.strip()) for line in file]

    # Create the angle valeur[the index in the list]
    theta = list(range(len(degree)))

    # Create a polar plot
    fig = go.Figure(
        data=go.Scatterpolar(
            r=degree,  # Radial values (the degree values from the file)
            theta=theta,  # Angular values (indices of the degree list)
            mode='lines',  # how we want to plot it
            name='Sensor Data' 
        )
    )
    # Show the plot
    fig.show()

def file1():
    df = pd.read_csv(r"courbe1.txt", header=None)

    df[0] = pd.to_numeric(df[0], errors='coerce')  # to make sue we dont have a char in the file 

    Vmin = df[0].min()
    Vmax = df[0].max()
    print(f"The maximum value of file 1 is: {Vmax}")
    print(f"The minimum value of file 1 is: {Vmin}")
    print(f"The offset is :{Vmin}")
    
    if Vmax < 0:  #we see it Vmax <0 to edit the offest
        df[0] -= Vmax
        NVmin = df[0].min()
        print(f"The new offset is: {NVmin}")
        df.to_csv("New_courbe1.txt",header = False, index = False) #a new file that saves all the new val
        file_handel("New_courbe1.txt") # draw the on with the edetied offeset 
    else:
        file_handel("courbe1.txt")  #if Vmax>=0 we draw the normal one 

def file2():
    df = pd.read_csv(r"courbe2.txt", header=None)

    df[0] = pd.to_numeric(df[0], errors='coerce')  # to make sue we dont have a char in the file 

    Vmin = df[0].min()
    Vmax = df[0].max()

    print(f"The maximum value of file 2 is: {Vmax}")
    print(f"The minimum value of file 2 is: {Vmin}")
    print(f"The offset is :{Vmin}")
    
    if Vmax < 0:
        df[0] -= Vmax
        NVmin = df[0].min()
        print(f"The new offset is: {NVmin}")
        df.to_csv("New_courbe2.txt",header = False, index = False)
        file_handel("New_courbe2.txt")
    else:
        file_handel("courbe2.txt")

def file3():
    df = pd.read_csv(r"courbe3.txt", header=None)

    df[0] = pd.to_numeric(df[0], errors='coerce')  # to make sue we dont have a char in the file 

    Vmin = df[0].min()
    Vmax = df[0].max()

    print(f"The maximum value of file 3 is: {Vmax}")
    print(f"The minimum value of file 3 is: {Vmin}")
    print(f"The offset is :{Vmin}")
    
    if Vmax < 0:
        df[0] -= Vmax
        NVmin = df[0].min()
        print(f"The new offset is: {NVmin}")
        df.to_csv("New_courbe3.txt",header = False, index = False)
        file_handel("New_courbe3.txt")
    else:
        file_handel("courbe3.txt")

def file4():
    df = pd.read_csv(r"courbe4.txt", header=None)

    df[0] = pd.to_numeric(df[0], errors='coerce')  # to make sue we dont have a char in the file 

    Vmin = df[0].min()
    Vmax = df[0].max()

    print(f"The maximum value of file 4 is: {Vmax}")
    print(f"The minimum value of file 4 is: {Vmin}")
    print(f"The offset is :{Vmin}")
    
    if Vmax < 0:
        df[0] -= Vmax
        NVmin = df[0].min()
        print(f"The new offset is: {NVmin}")
        df.to_csv("New_courbe4.txt",header = False, index = False)
        file_handel("New_courbe4.txt")
    else:
        file_handel("courbe4.txt")
# we dont need this in the app , this is the interface job

def menu():
    while True:
        print("\nThe menu:")
        print("1. File 1")
        print("2. File 2")
        print("3. File 3")
        print("4. File 4")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        match choice:
            case "1":
                print("You have selected file 1")
                file1()
            case "2":
                print("You have selected file 2")
                file2()
            case "3":
                print("You have selected file 3")
                file3()
            case "4":
                print("You have selected file 4")
                file4()
            case "5":
                print("Exiting. Thank you!")
                break 
            case _:
                print("Invalid input. Enter a number from 1-5.")

menu()

