from datetime import timedelta

from location import Location
from timestamp import Timestamp

class Supermarket:
    def __init__(self):
        location_names = ['entry', 'dairy', 'drinks', 'fruit', 'spices', 'checkout']
        self.locations = {location_name: Location(location_name) for location_name in location_names}

    def open(self):
        self.time = timedelta(hours=7)

    def close(self, remaining_customers):
        """
        Every customer, who did not check out, is send to checkout
        """
        for customer in remaining_customers:
            if customer.get_last_location() != 'checkout':
                customer.history.append(Timestamp(self.time, self.locations['checkout']))

    def get_entry_location(self):
        return self.locations['entry']

