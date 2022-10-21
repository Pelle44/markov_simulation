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

    def next_state(self, transition_matrix, time, locations):
        """
        This function implements Markov Chain Simulation, and
        returns the next state given an initial state
        """
        next_location_name = np.random.choice(
            a = transition_matrix.index,
            p = transition_matrix[self.get_last_timestamp().location.name]
        )
        next_location = locations[next_location_name]
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

    customers = []

    # for loop that checks if the supermarket is before 21:50
    #   If so then incerement one minute and simulate generation/movement of customers
    #   Else close store and send current customers to checkout

    transition_matrix = pd.read_csv('./data/transition_matrix.csv')
    transition_matrix.set_index('location', inplace=True)
    transition_matrix = transition_matrix.transpose()

    NEW_CUSTOMERS_PER_MIN = {7: 1.6333333333333333, #data should come from data. To implemented
                        8: 2.35,                
                        9: 1.5166666666666666,
                        10: 1.3166666666666667,
                        11: 1.1166666666666667,
                        12: 1.3166666666666667,
                        13: 1.7666666666666666,
                        14: 1.6166666666666667,
                        15: 1.3333333333333333,
                        16: 1.7833333333333334,
                        17: 1.8833333333333333,
                        18: 2.1666666666666665,
                        19: 2.5,
                        20: 1.6,
                        21: 0.9333333333333333}
    
    
    id = 1
    
    for i in range(899):
        supermarket.time = supermarket.time + timedelta(minutes=1) #increment by 1 minute
        if supermarket.time <= timedelta(hours=21, minutes=50): #if before closing time
            key = supermarket.time.seconds // 3600 #takes hour from time as key for dict
            no_of_customers = round(np.random.normal(NEW_CUSTOMERS_PER_MIN[key])) #generated customers per min
            for no in range(no_of_customers): #adds generated customers to list
                customer = Customer(id, supermarket.time, supermarket.get_entry_location())
                customers.append(customer)
                id = id + 1
            for customer in customers:
                if customer.get_last_location() != 'checkout':
                    customer.next_state(transition_matrix, supermarket.time, supermarket.locations)
        else:
            supermarket.close()

    for customer in customers:
        #if customer.id == 1: # You can test it for random Customers
            for timestamp in customer.history:
                print(f'{customer.id} is at {timestamp.location.name} at time {timestamp.time}')