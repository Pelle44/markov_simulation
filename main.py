import numpy as np
import pandas as pd
from datetime import timedelta
from time import sleep

from supermarket import Supermarket
import avg_customers_per_min_calculator

if __name__ == '__main__':
    
    supermarket = Supermarket()
    supermarket.open()

    #log = pd.DataFrame() to be included

    transition_matrix = pd.read_csv('./data/transition_matrix.csv')
    transition_matrix.set_index('location', inplace=True)
    transition_matrix = transition_matrix.transpose()

    NEW_CUSTOMERS_PER_MIN = avg_customers_per_min_calculator.get_avg_customers_per_min()
    
    id = 1
    
    for i in range(899):
        supermarket.time = supermarket.time + timedelta(minutes=1) #increment by 1 minute
        if supermarket.time <= timedelta(hours=21, minutes=50): #if before closing time
            key = supermarket.time.seconds // 3600 #takes hour from time as key for dict
            no_of_customers = round(np.random.normal(NEW_CUSTOMERS_PER_MIN[key])) #generated customers per min
            for no in range(no_of_customers): #adds generated customers to list
                customer = supermarket.generate_new_customer(id)
                id = id + 1
            for location_name, location in supermarket.locations.items():
                sleep(0.1)
                if location_name != 'checkout':
                    for customer in location.customers:
                        customer.next_state(transition_matrix, supermarket.time, supermarket.locations)
        else:
            supermarket.close()
