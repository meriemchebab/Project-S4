import pandas as pd  
import numpy as np 
import plotly.graph_objs as go 

def file_handel(file_name):
    """ 

    """
    with open(file_name, 'r') as file:
        degree = [float(line.strip()) for line in file]  # Read and convert values to float

    theta = list(range(len(degree)))  # Generate angles based on the number of data points

    # Create a polar plot
    fig = go.Figure(
        data=go.Scatterpolar(
            r=degree,  
            theta=theta,  
            mode='lines',  
            name='Sensor Data'
        )
    )
    fig.show()  # Display the plot

def plot_3d(file1, file2):
   
    df1 = pd.read_csv(file1, header=None)  # Load first file
    df2 = pd.read_csv(file2, header=None)  # Load second file

    # Convert values to numeric to avoid errors
    df1[0] = pd.to_numeric(df1[0], errors='coerce')
    df2[0] = pd.to_numeric(df2[0], errors='coerce')

    # Generate X values (index-based)
    x1 = np.linspace(0, len(df1[0]), len(df1[0]))
    y1 = df1[0].values  # Extract Y values from the first file

    x2 = np.linspace(0, len(df2[0]), len(df2[0]))
    y2 = df2[0].values  # Extract Y values from the second file

    # Create a 3D figure
    fig = go.Figure()

    # Add first curve
    fig.add_trace(go.Scatter3d(
        x=x1, y=y1, z=np.zeros_like(x1),  # Z=0 to keep it at the base
        mode='lines',
        name='Curve 1'
    ))

    # Add second curve
    fig.add_trace(go.Scatter3d(
        x=x2, y=y2, z=np.ones_like(x2),  # Z=1 to separate it from the first curve
        mode='lines',
        name='Curve 2'
    ))

    # Customize layout and axis labels
    fig.update_layout(
        title="3D Visualization of Two Curves",
        scene=dict(
            xaxis_title="Index",
            yaxis_title="Value",
            zaxis_title="Curves"
        )
    )

    fig.show()  # Display t 3D PLOT

