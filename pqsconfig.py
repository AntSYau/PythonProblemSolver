import json
import os, sys
import time

# class Singleton(type):
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         x = time.time()
#         if cls not in cls._instances:
#             print("{:.3f} Really init {}".format(x, cls))
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]

import threading


class Singleton(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        x = time.time()
        if not hasattr(cls, "_instance"):
            print("{:.3f} Really init {}".format(x, cls))
            with Singleton._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        print("{:.3f} Calling existing {}".format(x, cls))
        return cls._instance


class Config(metaclass=Singleton):
    def __init__(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                self.__conf = json.loads(f.read())
        else:
            self.__conf = {"version": 1}

    def __save_to_disk(self):
        with open("config.json", "w") as f:
            f.write(json.dumps(self.__conf))

    def set_value(self, key: str, value):
        self.__conf[key] = value
        self.__save_to_disk()

    def get_value(self, key: str):
        if key in self.__conf.keys():
            return self.__conf[key]
        else:
            raise ValueError("Invalid key {}!".format(key))

    def get_questions_path(self):
        return self.get_value("questions_path")

    def get_answers_path(self):
        return self.get_value("answers_path")
