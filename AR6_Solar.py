
# Creating scatter plot of Capacity vs Capex color-coded by Model
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the data
file_path = os.getcwd() + "\\data\\PV_Capex_vs_Capacity.csv"
df = pd.read_csv(file_path)

# Clean numeric columns
df['Capacity'] = df['Capacity'].replace({',': ''}, regex=True).astype(float)
df['Capex'] = df['Capex'].astype(float)

# Set plot style
plt.style.use('seaborn-v0_8')

# Create scatter plot
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(df['Capacity'], df['Capex'], c=pd.factorize(df['Model'])[0], cmap='tab10', alpha=0.7)

# Add legend
legend_labels = df['Model'].unique()
legend_handles = [plt.Line2D([0], [0], marker='o', color='w', label=label,
                             markerfacecolor=scatter.cmap(scatter.norm(i)), markersize=10)
                  for i, label in enumerate(legend_labels)]
ax.legend(handles=legend_handles, title="Model")

# Label axes and title
ax.set_ylabel("Capex (Million USD2010)")
ax.set_xlabel("Capacity (GW)")
ax.set_title("PV Capacity vs Capex by Model")

# Save plot
output_path = "capacity_vs_capex_scatter2.png"
fig.savefig(output_path, bbox_inches='tight')

print("Scatter plot of Capacity vs Capex by Model saved as capacity_vs_capex_scatter.png")
