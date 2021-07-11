"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach

######### Code References ###########################################################
## 1. Vanina W, Udacity Mentor Board, https://knowledge.udacity.com/questions/465782
#####################################################################################

def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neo_data = []
    with open(neo_csv_path, 'r') as c:
        reader = csv.DictReader(c)
        for row in reader:
            designation = row['pdes']
            name= row['name']
            diameter = row['diameter']
            hazardous = row['pha']      
            neo_data.append( NearEarthObject( designation, name, diameter, hazardous )  )
    return neo_data

def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.
    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`'s.
    """
    cad_data = []
    with open(cad_json_path, 'r') as j: 
        row = json.load(j)
        for approaches in row['data']:                       
            approaches = dict(zip(row['fields'], approaches))    # 1  (not sure if I need to do variadic unpacking)
            cad_data.append(CloseApproach(**approaches))         # 1  
    return cad_data
