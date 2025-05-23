import schedule
import time
from datetime import datetime
from etl_pipeline import run_etl


def job():
    print(f"\nScheduled ETL run at {datetime.now().isoformat()}")
    run_etl()


# Schedule to run daily at midnight
schedule.every().day.at("00:00").do(job)


def start_scheduler():
    print("Scheduler started. Waiting for next run...")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    start_scheduler()