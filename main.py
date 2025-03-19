import pandas as pd

def file1():
    df = pd.read_csv(r"courbe1.txt", header=None)
    #print(df)

    df[0] = pd.to_numeric(df[0], errors='coerce')  # to make sue we dont have a char in the file 

    Vmin = df[0].min()
    Vmax = df[0].max()

    print(f"The maximum value of our file 1 is: {Vmax}")
    print(f"The minimum value of our file 1 is: {Vmin}")


def file2():
    df = pd.read_csv(r"courbe2.txt", header=None)
    #print(df)

    df[0] = pd.to_numeric(df[0], errors='coerce')  # to make sue we dont have a char in the file 

    Vmin = df[0].min()
    Vmax = df[0].max()

    print(f"The maximum value of file 2 is: {Vmax}")
    print(f"The minimum value of file 2 is: {Vmin}")


def file3():
    df = pd.read_csv(r"courbe3.txt", header=None)
    #print(df)

    df[0] = pd.to_numeric(df[0], errors='coerce')  # to make sue we dont have a char in the file 

    Vmin = df[0].min()
    Vmax = df[0].max()

    print(f"The maximum value of file 2 is: {Vmax}")
    print(f"The minimum value of file 2 is: {Vmin}")


def file4():
    df = pd.read_csv(r"courbe4.txt", header=None)
    #print(df)

    df[0] = pd.to_numeric(df[0], errors='coerce')  # to make sue we dont have a char in the file 

    Vmin = df[0].min()
    Vmax = df[0].max()

    print(f"The maximum value of file 2 is: {Vmax}")
    print(f"The minimum value of file 2 is: {Vmin}")


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

