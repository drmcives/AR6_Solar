import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
#import kaleido
import plotly.graph_objects as go
import plotly.express as px

# Load the CSV file
df = pd.read_csv(os.getcwd() + "\\data\\PV_Capex_vs_GDP.csv")

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
    # Compute min and max PV_Capex for each year
    range_data = group_data.groupby('Year')['PV_Capex'].agg(['min', 'max']).reset_index()
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
        y=scenario_data['PV_Capex'],
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
        line=dict(color=colors[group], width=2),
        name=group
    ))

# Update layout
fig.update_layout(
    title='PV Capex from 2020 to 2100 by Model Scenario (Shaded by Model Group)',
    xaxis_title='Year',
    yaxis_title='PV Capex (GW)',
    yaxis=dict(range=[0, 10000]),
    legend_title='Model Group',
    template='plotly_white'
)

# Save the plot as JSON and PNG
#fig.write_json('pv_Capex_shaded_by_model_group.json')
#fig.show()

fig.write_image('pv_Capex_by_model_group.png')


fig2 = go.Figure()

# Add shaded ranges for each Model_Group
for group in model_groups:
    group_data = df_filtered[df_filtered['Model_Group'] == group]
    # Compute min and max PV_Capex for each year
    range_data = group_data.groupby('Year')['PV_Capex'].agg(['min', 'max']).reset_index()
    # Add filled area (lighter color)
    fig2.add_trace(go.Scatter(
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
    fig2.add_trace(go.Scatter(
        x=scenario_data['Year'],
        y=scenario_data['PV_Capex'],
        mode='lines',
        line=dict(color=colors[group], width=1),
        name=group,
        legendgroup=group,
        showlegend=False  # Avoid duplicate legend entries
    ))

# Add one legend entry per Model_Group
for group in model_groups:
    fig2.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color=colors[group], width=3),
        name=group
    ))

# Update layout with logarithmic y-axis
fig2.update_layout(
    title='PV Capex from 2020 to 2100 by Model Scenario (Logarithmic Scale)',
    xaxis_title='Year',
    yaxis_title='PV Capex (GW)',
    yaxis_type='log',  # Set y-axis to logarithmic
    legend_title='Model Group',
    template='plotly_white'
)

# Save the plot as JSON and PNG
#fig.write_json('pv_Capex_log_scale.json')
fig2.write_image('pv_Capex_log_scale.png')

fig2.show()



# # Filter data for years between 2020 and 2100
# df_filtered = df[(df['Year'] >= 2020) & (df['Year'] <= 2100)]

# # Create the line plot using Plotly Express
# fig = px.line(
#     df_filtered,
#     x='Year',
#     y='PV_Capex',
#     color='Model_Group',  # Color lines by Model_Group
#     title='PV Capex from 2020 to 2100 by Model Group',
#     labels={'Year': 'Year', 'PV_Capex': 'PV Capex (GW)', 'Model_Group': 'Model Group'}
# )

# # Save the plot as JSON and PNG
# fig.write_json('pv_Capex_by_model_group.json')
# #fig.write_image('pv_Capex_by_model_group.png')

# print("Graph created successfully: 'pv_Capex_by_model_group.json' and 'pv_Capex_by_model_group.png'")


# # Alternative using seaborn and matplotlib

# # Load your CSV
# df = pd.read_csv(os.getcwd() + "\\data\\PV_Capex_vs_GDP.csv")

# # Set style
# sns.set(style="whitegrid")

# # Plot each Model_Group
# plt.figure(figsize=(10,6))
# for group, data in df.groupby("Model_Group"):
#     # Plot line
#     sns.lineplot(x="Year", y="PV_Capex", data=data, label=group)
    
#     # Shade range (min to max per year)
#     grouped = data.groupby("Year")["PV_Capex"]
#     plt.fill_between(group,
#                      grouped.min(),
#                      grouped.max(),
#                      alpha=0.2)

# plt.title("PV Capex vs GDP by Model Group")
# plt.xlim(2020,2100)
# plt.ylim(0,5000)
# plt.xlabel("Year")
# plt.ylabel("PV Capex")
# plt.legend(title="Model Group")
# plt.show()
