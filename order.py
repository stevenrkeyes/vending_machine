from datetime import datetime

class Order:
    def __init__(self, requested_item: str):
        self.time_received = datetime.now()
        self.requested_item = requested_item

    def __repr__(self):
        time_string = self.time_received.strftime("%H:%M:%S")
        return time_string + " " + self.requested_item
