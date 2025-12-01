
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

# Load the CSV file
df = pd.read_csv(os.getcwd() + "\\data\\PV_Capacity.csv")

# Filter data for years between 2020 and 2100
df_filtered = df[(df['Year'] >= 2020) & (df['Year'] <= 2100)]

# Get unique Model_Groups and assign colors using Plotly's qualitative palette
model_groups = df_filtered['Model_Group'].unique()
color_map = px.colors.qualitative.Set2
colors = {group: color_map[i % len(color_map)] for i, group in enumerate(model_groups)}

# Create figure
fig = go.Figure()

# Add shaded ranges for each Model_Group
for group in model_groups:
    group_data = df_filtered[df_filtered['Model_Group'] == group]
    # Compute min and max PV_Capacity for each year
    range_data = group_data.groupby('Year')['PV_Capacity'].agg(['min', 'max']).reset_index()
    # Add filled area (lighter color)
    fig.add_trace(go.Scatter(
        x=pd.concat([range_data['Year'], range_data['Year'][::-1]]),
        y=pd.concat([range_data['max'], range_data['min'][::-1]]),
        fill='toself',
        fillcolor=colors[group].replace('rgb', 'rgba').replace(')', ',0.2)'),  # lighter shade
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo='skip',
        showlegend=False
    ))

# Add lines for each Model_Scenario_ID, colored by Model_Group
for scenario_id, scenario_data in df_filtered.groupby('Model_Scenario_ID'):
    group = scenario_data['Model_Group'].iloc[0]
    fig.add_trace(go.Scatter(
        x=scenario_data['Year'],
        y=scenario_data['PV_Capacity'],
        mode='lines',
        line=dict(color=colors[group], width=1),
        name=group,
        legendgroup=group,
        showlegend=False  # Avoid duplicate legend entries
    ))

# Add one legend entry per Model_Group
for group in model_groups:
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color=colors[group], width=3),
        name=group
    ))

# Update layout
fig.update_layout(
    title='PV Capacity from 2020 to 2100 by Model Scenario (Shaded by Model Group)',
    xaxis_title='Year',
    yaxis_title='PV Capacity (GW)',
    legend_title='Model Group',
    template='plotly_white'
)

# Save the plot as JSON and PNG
fig.write_json(os.getcwd() + '\\outputs\\pv_capacity_shaded_by_model_group.json')
fig.write_image(os.getcwd() + '\\outputs\\pv_capacity_shaded_by_model_group.png')
