import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import savgol_filter

def file_reader(file_name): #read our file 
    values = []
    with open(file_name, 'r') as file:
        for line in file:
            try:
                val = float(line)
                values.append(val)
            except ValueError:
                pass
    return values

def Polar_2d(data, separate=True): #the graph is with no changer (no 0 max and no rotation) plus option for the user to choose seretated or no
    half_length = len(data) // 2
    curve1 = np.array(data[:half_length])  # Plan H
    curve2 = np.array(data[half_length:])  # Plan E
    theta_deg = np.linspace(0, 360, half_length)

    if separate: #so if we seperated them 
        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{'type': 'polar'}, {'type': 'polar'}]],
            subplot_titles=("Plan H", "Plan E"),
            horizontal_spacing=0.3
        )

        fig.add_trace(go.Scatterpolar(
            r=curve1,
            theta=theta_deg,
            mode='lines',
            name='Plan H',
            line='blue'
        ), row=1, col=1)

        fig.add_trace(go.Scatterpolar(
            r=curve2,
            theta=theta_deg,
            mode='lines',
            name='Plan E',
            line=dict(color='red')
        ), row=1, col=2)

        fig.update_layout(
            title_text="Polar Plots - Plan H and Plan E (Separate)",
            showlegend=True,
            width=1200,
            height=600
        )
    else: #if they are in the same 
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=curve1,
            theta=theta_deg,
            mode='lines',
            name='Plan H',
            line='blue'
        ))

        fig.add_trace(go.Scatterpolar(
            r=curve2,
            theta=theta_deg,
            mode='lines',
            name='Plan E',
            line='red'
        ))

        fig.update_layout(
            title="Polar Plots - Combined",
            polar=dict(
                radialaxis=dict(visible=True)
            ),
            showlegend=True,
            width=600,
            height=600
        )

    fig.show()

def plot_radiation_2d(values, separate=True): #this is the part of 2d with every thing (meriem code)
    h_plane_raw = np.array(values[:360])
    e_plane_raw = np.array(values[360:720])

    # Smooth dB data
    h_plane_db = savgol_filter(h_plane_raw, window_length=11, polyorder=2)
    e_plane_db = savgol_filter(e_plane_raw, window_length=11, polyorder=2)

    # Normalize to dB max of H-plane
    h_plane_2d = h_plane_db - np.max(h_plane_db)
    e_plane_2d = e_plane_db - np.max(h_plane_db)
    theta = np.arange(len(h_plane_2d))  # 0 to 359 degrees

    if separate:  #the option to seperate them 
        fig_polar = make_subplots(
            rows=1, cols=2,
            specs=[[{'type': 'polar'}, {'type': 'polar'}]],
            subplot_titles=["H-plane Pattern", "E-plane Pattern"],
            horizontal_spacing=0.3
        )

        fig_polar.add_trace(
            go.Scatterpolar(
                r=h_plane_2d,
                theta=theta,
                mode='lines',
                name='H-plane',
                line=dict(color='blue')
            ),
            row=1, col=1
        )

        fig_polar.add_trace(
            go.Scatterpolar(
                r=e_plane_2d,
                theta=theta,
                mode='lines',
                name='E-plane',
                line=dict(color='red')
            ),
            row=1, col=2
        )

        fig_polar.update_layout(
            title=dict(
                text='2D Radiation Patterns',
                x=0.5,
                xanchor='center',
                font=dict(size=18)
            ),
            showlegend=True,
            title_text="Polar Plots - Plan H and Plan E (Separate)",
            polar=dict(
                angularaxis=dict(rotation=90, direction='clockwise')
            ),
            polar2=dict(
                angularaxis=dict(rotation=90, direction='clockwise')
            ),
            height=600,
            width=1200
        )
    else: # bioth in the same
        fig_polar = go.Figure()

        fig_polar.add_trace(go.Scatterpolar(
            r=h_plane_2d,
            theta=theta,
            mode='lines',
            name='H-plane',
            line=dict(color='blue')
        ))

        fig_polar.add_trace(go.Scatterpolar(
            r=e_plane_2d,
            theta=theta,
            mode='lines',
            name='E-plane',
            line=dict(color='red')
        ))

        fig_polar.update_layout(
            title="Polar Plots - Combined",
            polar=dict(
                angularaxis=dict(rotation=90, direction='clockwise'),
                radialaxis=dict(visible=True)
            ),
            showlegend=True,
            width=600,
            height=600
        )

    fig_polar.show()


def plot_radiation_3d(data):  #the 3d function for now (ta3 meriem)
    h_plane_db = np.array(values[:360])
    e_plane_db = np.array(values[360:720])
    # Convert dB to linear
    h_plane = 10 ** (h_plane_db / 10)
    e_plane = 10 ** (e_plane_db / 10)

    # Angles
    phi = np.radians(np.arange(360))     # H-plane: azimuth
    theta = np.radians(np.arange(360))   # E-plane: elevation

    theta_grid, phi_grid = np.meshgrid(theta, phi)

    # Radiation pattern
    radiation_pattern = np.outer(e_plane, h_plane)

    # Convert to Cartesian
    x = radiation_pattern * np.sin(theta_grid) * np.cos(phi_grid)
    y = radiation_pattern * np.sin(theta_grid) * np.sin(phi_grid)
    z = radiation_pattern * np.cos(theta_grid)

    fig_3d = go.Figure(data=[
        go.Surface(
            x=x,
            y=y,
            z=z,
            surfacecolor=radiation_pattern,
            colorscale='viridis',
            opacity=0.85,
            colorbar=dict(title='Radiation Intensity')
        )
    ])

    fig_3d.update_layout(
    title='3D Antenna Radiation Pattern',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
        aspectmode='manual',
        aspectratio=dict(x=1, y=1, z=0.8),  # z < 1 flattens it a bit (optional)
        camera=dict(
            eye=dict(x=1.3, y=1.3, z=0.8),  # closer camera
            center=dict(x=0, y=0, z=0)
        )
    ),
    margin=dict(l=0, r=0, b=0, t=30),  # tight layout
    width=800,  # increase figure size
    height=800
)


    fig_3d.show()


# the main exemple

values = file_reader("3Dcourbe4.txt") #reading the file 

plot_radiation_2d(values, True) #they'll be seperated
plot_radiation_2d(values, False) #in the same 
#plot_radiation_3d(values)
