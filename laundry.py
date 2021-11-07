import os
import pytz
import time
from queue import Queue
from threading import Thread
from datetime import datetime
from pandas import DataFrame
from sheets_api import MySheet
#from gpio import MotionSensor

class Logger:

    def __init__(self, spreadsheet_id, csv_path='data.csv'):

        self.sheet = MySheet(spreadsheet_id)
        self.timestamp_queue = Queue()
        self.cached_records = []
        self.csv_path = csv_path

        if not os.path.exists(self.csv_path):
            DataFrame(columns=['Timestamp']).to_csv(
                self.csv_path, index=False)

    def update_csv(self):
        DataFrame(data={'Timestamp':self.timestamp}, index=[0]).to_csv(self.csv_path, mode='a', header=False, index=False)

    def update_cloud(self):
        self.cached_records.append(str(self.timestamp))
        if len(self.cached_records) >= 10:
            self.sheet.append(self.cached_records)
            self.cached_records = []

    def queue_handler(self):
        while True:
            self.timestamp = self.timestamp_queue.get()
            self.update_csv()
            self.update_cloud()
            self.timestamp_queue.task_done()

    def start(self, sensor):

        Thread(target=self.queue_handler, daemon=True).start()

        while True:
            time.sleep(1)
            # sensor.wait_for_motion()
            # sensor.wait_for_no_motion()
            self.timestamp_queue.put(datetime.now(pytz.utc))

# sensor = MotionSensor(GPIO_PORT)
# logger = Logger('my-spreadsheet-id').start(sensor)



