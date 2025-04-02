import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.queries import aggregate_monthly_sinkings
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_monthly_trends(start_date=None, end_date=None, save_path=None):
    """
    Create a dual-axis line plot showing monthly trends of sinkings and tonnage.
    
    Args:
        start_date (str, optional): Start date in format 'YYYY-MM-DD'
        end_date (str, optional): End date in format 'YYYY-MM-DD'
        save_path (str, optional): If provided, save the plot to this path
    """
    # Get the data
    df = aggregate_monthly_sinkings(start_date, end_date)
    
    # Convert month_year to datetime for better x-axis formatting
    df['date'] = pd.to_datetime(df['sunk_month_year'])
    
    # Create the figure and axis objects with a single subplot
    fig, ax1 = plt.subplots(figsize=(15, 8))
    
    # Plot total_sinkings on primary y-axis
    color = '#1f77b4'  # Blue
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Number of Ships Sunk', color=color)
    line1 = ax1.plot(df['date'], df['total_sinkings'], color=color, label='Ships Sunk')
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Create second y-axis sharing same x-axis
    ax2 = ax1.twinx()
    color = '#ff7f0e'  # Orange
    ax2.set_ylabel('Total Tonnage', color=color)
    line2 = ax2.plot(df['date'], df['total_tonnage'], color=color, label='Tonnage')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Format y-axis labels for tonnage to show 'k' for thousands
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1000)}k'))
    
    # Add title
    title = 'Monthly Trends of Japanese Naval Losses'
    if start_date and end_date:
        title += f'\n{start_date} to {end_date}'
    plt.title(title)
    
    # Add legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save or show the plot
    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")
    else:
        plt.show()
    
    plt.close()

if __name__ == "__main__":
    # Create plots directory if it doesn't exist
    os.makedirs("plots", exist_ok=True)
    
    # Example 1: All-time plot
    plot_monthly_trends(save_path="plots/all_time_trends.png")
    
    # Example 2: 1942 plot
    plot_monthly_trends('1942-01-01', '1942-12-31', save_path="plots/1942_trends.png")
    
    # Example 3: 1944-1945 plot
    plot_monthly_trends('1944-01-01', '1945-08-31', save_path="plots/1944_1945_trends.png")
