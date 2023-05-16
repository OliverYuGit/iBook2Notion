import math
import os
from typing import Type
import yaml
import datetime
import time

SAVE_FILE = os.path.join(os.path.dirname(__file__), "../..", "mark.yaml")

TIME_COMPENSATION = "978307200"

class Mark:

    def __init__(self, time_mark: str, last_time_mark: str) -> None:
        self.time_mark = time_mark
        self.last_time_mark = last_time_mark
        

    @classmethod
    def load(cls: "Type[Mark]", config_file: str = SAVE_FILE) -> "Type[Mark]":
        try:
            with open(config_file, encoding="utf-8") as file:
                marks = yaml.load(file, Loader=yaml.FullLoader)
        except FileNotFoundError as e:
            print(f"Failed to get mark.yaml file. Message: {e}")
        time_mark = marks.get("time_mark", "")
        last_time_mark = marks.get("last_time_mark", "")
        return cls(time_mark, last_time_mark)
    
    def save(self, config_file: str = SAVE_FILE) -> None:
        try:
            self.time_mark = datetime.datetime.fromtimestamp(
            math.ceil(float(self.time_mark)) + float(TIME_COMPENSATION))

            marks = {
                "time_mark": self.time_mark.strftime('%Y-%m-%d %H:%M:%S'),
                "last_time_mark": self.last_time_mark
            }

            with open(config_file, "w", encoding="utf-8") as file:
                yaml.dump(marks, file, allow_unicode=True)
            
        except Exception as e:
            print(f"Failed to save time mark. Message: {e}")
    
        
    def get_time_mark(self):
        if self.time_mark == "":
            return 0.0
        time_tuple = time.strptime(self.time_mark, '%Y-%m-%d %H:%M:%S')
        return float(time.mktime(time_tuple)) - float(TIME_COMPENSATION)