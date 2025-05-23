import time
from etl_pipeline import run_etl

def start_scheduler():
    print("Starting scheduler to run ETL every 10 seconds (after previous run completes)...")
    while True:
        start_time = time.time()

        try:
            run_etl()
        except Exception as e:
            print(f"Error during ETL run: {e}")

        elapsed_time = time.time() - start_time
        wait_time = max(10 - elapsed_time, 0)
        print(f"Waiting {wait_time:.2f} seconds before next run...\n")
        time.sleep(wait_time)