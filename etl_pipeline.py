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
    frames = []

    if os.path.exists(csv_path):
        df_csv = pd.read_csv(csv_path)
        frames.append(process_dataframe(df_csv))

    if os.path.exists(xlsx_path):
        df_xlsx = pd.read_excel(xlsx_path)
        frames.append(process_dataframe(df_xlsx))

    if frames:
        return pd.concat(frames, ignore_index=True)
    return pd.DataFrame()

def save_to_csv(final_df, output_path='output/final_cleaned_data.csv'):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_df.to_csv(output_path, index=False)
    print(f"Saved cleaned data to: {output_path}")

def run_etl():
    print("Running ETL pipeline...")
    csv_path = "./data/sample_data.csv"
    xlsx_path = "./data/sample_weather.xlsx"
    final_df = read_and_process_data(csv_path, xlsx_path)
    if not final_df.empty:
        save_to_csv(final_df)
    else:
        print("No data processed.")

if __name__ == "__main__":
    from scheduler import start_scheduler
    start_scheduler()
