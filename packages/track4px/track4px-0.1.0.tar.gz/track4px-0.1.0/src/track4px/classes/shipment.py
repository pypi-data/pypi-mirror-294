from typing import List, Optional
from datetime import datetime

class Event:
    """ A class representing an individual event. """

    timestamp: datetime
    description: str
    category: str
    location: str
    raw: str

class Shipment:
    """ A class representing a shipment. """

    tracking_number: str
    courier: str
    events: Optional[List[Event]] = None
    raw: str