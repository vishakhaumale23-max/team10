import schedule
import time
def job():
   print("Medication scheduler is running...")
# Schedule the job
schedule.every().day.at("15:23").do(job)
while True:
   schedule.run_pending()
   time.sleep(1)