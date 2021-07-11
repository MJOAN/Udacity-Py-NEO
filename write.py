"""
Module exports two functions: `write_to_csv` and `write_to_json`,
which accept an `results` stream of close approaches and
a path to write the data.

These functions are invoked by the main module with the output 
of the `limit` function and filename supplied by user via co
mmand line.

You'll edit this file in Part 4.
"""
import csv
import json
from helpers import datetime_to_str

########### Code References: #################################
## 1. Udacity Lesson 5, File I/O, CSV I/O
## 2. Udacity Lesson 5, File I/O, JSON I/O
## 3. Python Documentation, DictWriter, https://bit.ly/3e4QSqG 
##############################################################

def write_to_csv(results, filename):
    """
    :param results: An iterable of `CloseApproach` objects.
    :param filename: Path-like object to where the data should be saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 
                    'name', 'diameter_km', 'potentially_hazardous')
    
    with open(filename, 'w') as outfile:     
        reader = csv.DictWriter(outfile, fieldnames=fieldnames)                     # 1 
        reader.writeheader() 
        
        for result in results:
            reader.writerow({                                                       # 3
                'datetime_utc': datetime_to_str( result.time ),
                'distance_au': result.distance,
                'velocity_km_s': result.velocity,
                'designation': result.designation,
                'name': result.name,
                'diameter_km': result.diameter,
                'potentially_hazardous': result.hazardous
            })

def write_to_json(results, filename):
    """
    :param results: An iterable of `CloseApproach` objects.
    :param filename: Path-like object to where data is saved. 
    """
    close_approaches = [] 
    for result in results: 
        close_approaches_dict = { 
                'datetime_utc': result.time_str,         
                'distance_au': result.distance, 
                'velocity_km_s': result.velocity,
                'neo': { 
                    'designation': result.neo.designation,
                    'name': result.neo.name,
                    'diameter_km': result.neo.diameter,
                    'potentially_hazardous': result.neo.hazardous
                 }
        }
        close_approaches.append(close_approaches_dict)
    
    with open(filename, 'w') as outfile:                                  # 2
        json.dump(close_approaches, outfile)