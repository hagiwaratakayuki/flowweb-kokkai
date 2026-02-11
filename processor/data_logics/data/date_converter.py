from datetime import datetime

FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

def convert(datestring):
    return datetime.strptime(FORMAT, datestring)