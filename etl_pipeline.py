import pandas as pd
import os

def fahrenheit_to_celsius(f_temp):
    return (f_temp - 32) * 5.0 / 9.0

def calculate_weather_impact(temp, humidity, wind_speed):
    return 0.4 * temp + 0.3 * humidity + 0.3 * wind_speed

def process_dataframe(df):
    df = df.drop_duplicates()
    df = df.dropna(how='all')
    df = df.fillna(method='ffill')

    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        df['datetime'] = df['datetime'].dt.tz_localize('Asia/Karachi', ambiguous='NaT', nonexistent='shift_forward')
        df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%dT%H:%M:%S%z')

    if {'temp', 'humidity', 'windspeed'}.issubset(df.columns):
        df['weather_impact_score'] = calculate_weather_impact(df['temp'], df['humidity'], df['windspeed'])

    return df

def read_and_process_data(csv_path: str, xlsx_path: str):
    data_frames = {}

    if os.path.exists(csv_path):
        df_csv = pd.read_csv(csv_path)
        data_frames['csv_data'] = process_dataframe(df_csv)

    if os.path.exists(xlsx_path):
        df_xlsx = pd.read_excel(xlsx_path)
        data_frames['xlsx_data'] = process_dataframe(df_xlsx)

    return data_frames

def save_to_csv(df_dict, output_dir='output'):
    os.makedirs(output_dir, exist_ok=True)
    for name, df in df_dict.items():
        output_path = os.path.join(output_dir, f"{name}.csv")
        df.to_csv(output_path, index=False)
        print(f"Saved {name} to {output_path}")

def run_etl():
    print("Running ETL pipeline...")
    csv_path = "./data/sample_data.csv"
    xlsx_path = "./data/sample_weather.xlsx"
    data = read_and_process_data(csv_path, xlsx_path)
    save_to_csv(data)

if __name__ == "__main__":
    from scheduler import start_scheduler
    start_scheduler()
