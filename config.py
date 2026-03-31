import json


class Config:
    def __init__(self):
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        self.lesson = config["lesson"]
        self.deepseek_api = config["deepseek_api"]
        self.ocr_path = config["ocr_path"]
        self.edge_driver_path = config["edge_driver_path"]
        self.duration = config["duration"]
