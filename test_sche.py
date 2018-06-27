import schedule
import time

def script():
    print("Juan come semen")

schedule.every(1).minutes.do(script)
while True:
    schedule.run_pending()
    time.sleep(1)


