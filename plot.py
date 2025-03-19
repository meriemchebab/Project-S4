
import plotly.graph_objs as go

# Read the file and create a list of degree values
with open("courbe1.txt", 'r') as file:
    # Read all lines, strip whitespace, and convert valid numeric lines to floats
    degree = [float(line.strip()) for line in file]

# Create the theta (angle) values as the indices of the degree list
theta = list(range(len(degree)))

# Create a polar plot
fig = go.Figure(
    data=go.Scatterpolar(
        r=degree,  # Radial values (the degree values from the file)
        theta=theta,  # Angular values (indices of the degree list)
        mode='lines+markers',  # Plot as lines with markers
        name='Sensor Data'  # Legend label
    )
)


# Show the plot
fig.show()


