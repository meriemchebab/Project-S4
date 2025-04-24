import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import savgol_filter

def file_reader(file_name): #read our file 
    data = []
    with open(file_name, 'r') as file:
        for line in file:
            try:
                val = float(line)
                data.append(val)
            except ValueError:
                pass
    return data

def Fix_Max(data): 
    half_length = len(data) // 2
    plan_e = np.array(data[:half_length]) 
    plan_h = np.array(data[half_length:]) 

    plan_h_db = savgol_filter(plan_e, window_length=11, polyorder=2)
    plan_e_db = savgol_filter(plan_h, window_length=11, polyorder=2)
    plan_h_2d = plan_h_db - np.max(plan_h_db)
    plan_e_2d = plan_e_db - np.max(plan_e_db)

    return plan_e_2d, plan_h_2d 

def plot_2d(values, max=True, same=True):
    half_length = len(values) // 2
    theta = np.linspace(0, 360, half_length)

    if max:
        plan_e_2d, plan_h_2d = Fix_Max(values)  
        if same:
            Afficher(plan_e_2d, plan_h_2d, theta, separate=False)
        else:
            Afficher(plan_e_2d, plan_h_2d, theta, separate=True)
    else:
        plan_e = np.array(values[:half_length]) 
        plan_h = np.array(values[half_length:]) 

        plan_h_db = savgol_filter(plan_e, window_length=11, polyorder=2)
        plan_e_db = savgol_filter(plan_h, window_length=11, polyorder=2)

        if same:
            Afficher(plan_e_db, plan_h_db, theta, separate=False)
        else:
            Afficher(plan_e_db, plan_h_db, theta, separate=True)

def Afficher(plan_e_2d, plan_h_2d,theta,separate=True):

    if separate:  #the option to seperate them 
        fig_polar = make_subplots(
            rows=1, cols=2,
            specs=[[{'type': 'polar'}, {'type': 'polar'}]],
            subplot_titles=["H-plane Pattern", "E-plane Pattern"],
            horizontal_spacing=0.3
        )

        fig_polar.add_trace(
            go.Scatterpolar(
                r=plan_h_2d,
                theta=theta,
                mode='lines',
                name='H-plane',
                line=dict(color='blue')
            ),
            row=1, col=1
        )

        fig_polar.add_trace(
            go.Scatterpolar(
                r=plan_e_2d,
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
            r=plan_h_2d,
            theta=theta,
            mode='lines',
            name='H-plane',
            line=dict(color='blue')
        ))

        fig_polar.add_trace(go.Scatterpolar(
            r=plan_e_2d,
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


#test for a main
data = file_reader("3Dcourbe4.txt")
plot_2d(data, False, False)