from datetime import datetime
from ninja import Schema

class EventSignalSchema(Schema):
    id: int
    title: str
    CSV: str
    
class NotFoundSchema(Schema):
    message: str


class SignalNameSchema(Schema):
    # csv_name: str
    signal_name: str
