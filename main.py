import numpy as np
import pandas as pd
from datetime import timedelta

class Supermarket:
    def __init__(self):
        location_names = ['entry', 'dairy', 'drinks', 'fruit', 'spices', 'checkout']
        self.locations = {location_name: Location(location_name) for location_name in location_names}

    def open(self):
        self.time = timedelta(hours=7)

    def close(self):
        ## send customers to checkout
        return True

    def get_entry_location(self):
        return self.locations['entry']

class Customer:
    def __init__(self, id, entry_time, entry_location):
        self.id = id
        self.history = [Timestamp(entry_time, entry_location)]

    def next_state(self, transition_matrix, time):
        """
        This function implements Markov Chain Simulation, and
        returns the next state given an initial state
        """
        next_location = Location(np.random.choice(
            a = transition_matrix.index,
            p = transition_matrix[self.get_last_timestamp().location.name]
        ))
        self.history.append(Timestamp(time, next_location))

    def get_last_timestamp(self):
        return self.history[-1]

    def get_last_location(self):
        return self.get_last_timestamp().location.name

class Location:
    def __init__(self, name):
        self.name = name
        self.customers = []

class Timestamp:
    def __init__(self, time, location):
        self.time = time
        self.location = location
    def __repr__(self):
        return (self.time, self.location)

if __name__ == '__main__':
    
    supermarket = Supermarket()
    supermarket.open()

    customer = Customer(1, supermarket.time, supermarket.get_entry_location())
    timestamp = customer.get_last_timestamp()
    print(f'Customer is at {timestamp.location.name} at time {timestamp.time}')

    customers = [customer]

    # for loop that checks if the supermarket is before 21:50
    #   If so then incerement one minute and simulate generation/movement of customers
    #   Else close store and send current customers to checkout

    transition_matrix = pd.read_csv('data/transition_matrix.csv')
    transition_matrix.set_index('location', inplace=True)
    transition_matrix = transition_matrix.transpose()

    for i in range(900):
        supermarket.time = supermarket.time + timedelta(minutes=1)
        if supermarket.time < timedelta(hours=21, minutes=50):
            for customer in customers:
                customer.next_state(transition_matrix, supermarket.time)
                timestamp = customer.get_last_timestamp()
                print(f'Customer is at {timestamp.location.name} at time {timestamp.time}')

            # filter out customers at checkout
            customers = filter(lambda customer: customer.get_last_location() != 'checkout', customers)
        else:
            supermarket.close()