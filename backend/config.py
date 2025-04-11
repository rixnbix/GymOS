import os
import json
from models.oracle_dbinterface import *

def get_database(path: str = None) -> Database:
    if path is None:
        # Automatically find config.json in the root directory
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(root_dir, "config.json")

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
