
import pandas as pd
import matplotlib.pyplot as plt

def load_sprint_data(filepath):
    """Load sprint data from a CSV file."""
    return pd.read_csv(filepath)

def calculate_velocity(df):
    """Calculate velocity: total story points completed."""
    return df[df['Status'] == 'Done']['Story Points'].sum()

def calculate_carryover(df):
    """Calculate carryover: story points not completed."""
    return df[df['Status'] != 'Done']['Story Points'].sum()

def plot_task_distribution(df):
    """Plot task type distribution."""
    task_counts = df['Type'].value_counts()
    task_counts.plot(kind='bar', title='Task Type Distribution')
    plt.xlabel('Task Type')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('task_distribution.png')
    plt.close()

def generate_report(df):
    """Generate a simple sprint summary report."""
    velocity = calculate_velocity(df)
    carryover = calculate_carryover(df)
    total = velocity + carryover
    print(f"Sprint Summary Report")
    print(f"----------------------")
    print(f"Total Story Points: {total}")
    print(f"Completed (Velocity): {velocity}")
    print(f"Carryover: {carryover}")
    plot_task_distribution(df)
    print("Task distribution chart saved as 'task_distribution.png'.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python agile_insights.py <sprint_data.csv>")
    else:
        filepath = sys.argv[1]
        df = load_sprint_data(filepath)
        generate_report(df)
