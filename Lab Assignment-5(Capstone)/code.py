import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta
import random

# Task 1: Data Ingestion and Validation
def ingest_and_validate_data(data_dir):
    df_combined = pd.DataFrame()
    data_path = Path(data_dir)
    
    csv_files = list(data_path.glob('*.csv')) if data_path.exists() else []
    
    if not csv_files:
        print(f"No CSV files found in {data_dir}. Generating sample data...")
        generate_sample_data(data_dir)
        csv_files = list(data_path.glob('*.csv'))
    
    for file in csv_files:
        try:
            df = pd.read_csv(file, on_bad_lines='skip')
            
            parts = file.stem.split('_')
            if len(parts) >= 2:
                building_name = parts[0]
                month = parts[1]
                df['building'] = building_name
                df['month'] = month
            else:
                print(f"Filename {file.name} does not match expected format. Skipping metadata addition.")
            
            # Append to combined DataFrame
            df_combined = pd.concat([df_combined, df], ignore_index=True)
            print(f"Successfully read and appended {file.name}")
        
        except FileNotFoundError:
            print(f"File {file.name} not found. Skipping.")
        except Exception as e:
            print(f"Error reading {file.name}: {e}. Skipping.")
    
    # Ensure timestamp is datetime
    if 'timestamp' in df_combined.columns:
        df_combined['timestamp'] = pd.to_datetime(df_combined['timestamp'], errors='coerce')
    
    return df_combined

def generate_sample_data(data_dir):
    """
    Generates sample CSV files for demonstration.
    Creates data for 3 buildings over 2 months, with hourly readings.
    """
    buildings = ['BuildingA', 'BuildingB', 'BuildingC']
    months = ['Jan', 'Feb']
    start_date = datetime(2023, 1, 1)
    
    os.makedirs(data_dir, exist_ok=True)
    
    for building in buildings:
        for month in months:
            data = []
            current_date = start_date
            if month == 'Feb':
                current_date = datetime(2023, 2, 1)
            
            # Generate hourly data for the month
            while current_date.month == (1 if month == 'Jan' else 2):
                kwh = random.uniform(10, 100)  # Random kWh consumption
                data.append({'timestamp': current_date, 'kwh': kwh})
                current_date += timedelta(hours=1)
            
            df = pd.DataFrame(data)
            filename = f"{building}_{month}.csv"
            df.to_csv(Path(data_dir) / filename, index=False)
            print(f"Generated sample file: {filename}")

# Task 2: Core Aggregation Logic
def calculate_daily_totals(df):
    """
    Calculates daily totals of kWh consumption.
    """
    if 'timestamp' not in df.columns or 'kwh' not in df.columns:
        print("Required columns 'timestamp' and 'kwh' not found.")
        return pd.DataFrame()
    return df.resample('D', on='timestamp')['kwh'].sum()

def calculate_weekly_aggregates(df):
    """
    Calculates weekly aggregates of kWh consumption.
    """
    if 'timestamp' not in df.columns or 'kwh' not in df.columns:
        print("Required columns 'timestamp' and 'kwh' not found.")
        return pd.DataFrame()
    return df.resample('W', on='timestamp')['kwh'].sum()

def building_wise_summary(df):
    """
    Provides a summary per building: mean, min, max, total kWh.
    """
    if 'building' not in df.columns or 'kwh' not in df.columns:
        print("Required columns 'building' and 'kwh' not found.")
        return pd.DataFrame()
    return df.groupby('building')['kwh'].agg(['mean', 'min', 'max', 'sum'])

# Task 3: Object-Oriented Modeling
class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh

class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []
    
    def add_reading(self, reading):
        self.meter_readings.append(reading)
    
    def calculate_total_consumption(self):
        return sum(reading.kwh for reading in self.meter_readings)
    
    def generate_report(self):
        total = self.calculate_total_consumption()
        return f"Building {self.name}: Total consumption {total:.2f} kWh"

class BuildingManager:
    def __init__(self):
        self.buildings = {}
    
    def add_building(self, building):
        self.buildings[building.name] = building
    
    def get_building(self, name):
        return self.buildings.get(name)
    
    def populate_from_dataframe(self, df):
        for _, row in df.iterrows():
            building_name = row['building']
            if building_name not in self.buildings:
                self.add_building(Building(building_name))
            reading = MeterReading(row['timestamp'], row['kwh'])
            self.get_building(building_name).add_reading(reading)

# Task 4: Visual Output with Matplotlib
def create_dashboard(df_combined):
    """
    Creates a dashboard with three visualizations and saves as PNG.
    """
    if df_combined.empty:
        print("No data available for visualization.")
        return
    
    df_combined['timestamp'] = pd.to_datetime(df_combined['timestamp'])
    
    df_combined['hour'] = df_combined['timestamp'].dt.hour

    # 1. Daily totals per building
    df_daily = df_combined.groupby([pd.Grouper(key='timestamp', freq='D'), 'building'])['kwh'].sum().unstack()

    # 2. Weekly totals per building and average
    df_weekly = df_combined.groupby([pd.Grouper(key='timestamp', freq='W'), 'building'])['kwh'].sum().unstack()
    avg_weekly = df_weekly.mean()

    # Create subplots
    fig, axs = plt.subplots(3, 1, figsize=(12, 18))

    # Trend Line: Daily consumption
    df_daily.plot(ax=axs[0])
    axs[0].set_title("Daily Consumption Trend by Building")
    axs[0].set_ylabel("kWh")
    axs[0].legend(title="Building")
    axs[0].grid(True)

    # Bar Chart: Average weekly usage
    avg_weekly.plot(kind='bar', ax=axs[1], color='skyblue')
    axs[1].set_title("Average Weekly Usage by Building")
    axs[1].set_ylabel("kWh")
    axs[1].grid(axis='y')

    # Scatter Plot: Peak-hour consumption
    for building in df_combined['building'].unique():
        subset = df_combined[df_combined['building'] == building]
        axs[2].scatter(subset['hour'], subset['kwh'], alpha=0.6, label=building)
    axs[2].set_title("Peak-Hour Consumption per Building")
    axs[2].set_xlabel("Hour of Day")
    axs[2].set_ylabel("kWh")
    axs[2].legend(title="Building")
    axs[2].grid(True)

    # Layout adjustment and save figure
    plt.tight_layout()
    plt.savefig('dashboard.png')
    print("Dashboard saved as dashboard.png")
    plt.show()

# Task 5: Persistence and Executive Summary
def export_data_and_summary(df_combined, building_summary):
    """
    Exports data and generates a summary report.
    """
    # Export cleaned data
    df_combined.to_csv('cleaned_energy_data.csv', index=False)
    print("Exported cleaned data to cleaned_energy_data.csv")
    
    # Export building summary
    building_summary.to_csv('building_summary.csv', index=True)
    print("Exported building summary to building_summary.csv")
    
    # Generate summary report
    total_campus = df_combined['kwh'].sum()
    highest_building = building_summary['sum'].idxmax() if not building_summary.empty else "N/A"
    peak_time = df_combined.loc[df_combined['kwh'].idxmax(), 'timestamp'] if not df_combined.empty else "N/A"
    
    # Weekly trends: Simple description of averages
    weekly_trends = building_summary['mean'].to_dict() if not building_summary.empty else {}
    
    summary_text = f"""
Executive Summary:
- Total Campus Consumption: {total_campus:.2f} kWh
- Highest-Consuming Building: {highest_building}
- Peak Load Time: {peak_time}
- Weekly Trends (Average Consumption per Building): {weekly_trends}
"""
    
    with open('summary.txt', 'w') as f:
        f.write(summary_text)
    print("Summary report saved to summary.txt")
    print(summary_text)  # Also print to console

# Main Execution
if __name__ == "__main__":
    data_dir = '/data/'
    
    # Task 1
    df_combined = ingest_and_validate_data(data_dir)
    
    if df_combined.empty:
        print("No data loaded. Exiting.")
        exit()
    
    # Task 2
    daily_totals = calculate_daily_totals(df_combined)
    weekly_aggregates = calculate_weekly_aggregates(df_combined)
    building_summary = building_wise_summary(df_combined)
    
    # Task 3
    manager = BuildingManager()
    manager.populate_from_dataframe(df_combined)
    
    # Example: Generate report for each building
    for building in manager.buildings.values():
        print(building.generate_report())
    
    # Task 4
    create_dashboard(df_combined)
    
    # Task 5
    export_data_and_summary(df_combined, building_summary)
