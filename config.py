import json
from oracle_database_interface import *

def get_database(path: str = "config.json") -> database:
    try:
        with open(path, "r") as f:
            config = json.load(f)
        
            return oracle_database(
                config["username"],
                config["password"],
                config["database"],
                config["pool_min"],
                config["pool_max"],
                config["pool_inc"]
            )
    except FileNotFoundError:
        raise Exception(1, path + " not found!")
    except Exception as e:
        raise Exception(
            255,
            "Unknown error occurred while connecting to the database",
            "\t" + str(e)
        )
