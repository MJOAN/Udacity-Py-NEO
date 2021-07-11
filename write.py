"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json
from  helpers import datetime_to_str

########### Code References: ###########################################################################
## 1. Udacity Lesson 5, File I/O, CSV I/O
## 2. Udacity Lesson 5, File I/O, JSON I/O
## 3. Python Documentation, DictWriter, Reference: https://docs.python.org/3/library/csv.html#csv.DictWriter
########################################################################################################

def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.
    Each output row corresponds to the information in a single close 
    approach from the `results` stream and its associated near-Earth object.
    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 'name', 'diameter_km', 'potentially_hazardous')
    
    with open(filename, 'w') as outfile:     
        reader = csv.DictWriter(outfile, fieldnames=fieldnames)               # 1 
        reader.writeheader() 
        
        for result in results:
            reader.writerow(
                {                                                                 # 3
                'datetime_utc': datetime_to_str( result.time ),
                'distance_au': result.distance,
                'velocity_km_s': result.velocity,
                'designation': result.designation,
                'name': result.name,
                'diameter_km': result.diameter,
                'potentially_hazardous': result.hazardous
                }
            )

def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.
    Output is a list containing dictionaries, each mapping `CloseApproach` attributes
    and values and the 'neo' key mapping to a dictionary of the associated NEO's attributes.
    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved. 
    """
    close_approaches = [] 
    for result in results: 
        close_approaches_dict = { 
                'datetime_utc': result.time,      # unable to use datetime_str() TypeError: Object of type 'method' is not JSON serializable          
                'distance_au': result.distance, 
                'velocity_km_s': result.velocity,
                'neo': { 
                    'designation': result.designation,
                    'name': result.name,
                    'diameter_km': result.diameter,
                    'potentially_hazardous': result.hazardous
                 }
        }
        close_approaches.append(close_approaches_dict)
    
    with open(filename, 'w') as outfile:              # 2
        json.dump(close_approaches, outfile)