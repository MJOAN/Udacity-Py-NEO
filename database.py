"""
A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""
from collections import defaultdict
from filters import (AttributeFilter, DateFilter, DistanceFilter, VelocityFilter, 
DiameterFilter, HazardousFilter)

########### Code References: ################################################
## 1. Vanina W., Mentor Board, https://knowledge.udacity.com/questions/478946
## 2. Shuaishuai, Mentor Board, https://knowledge.udacity.com/questions/599130 
## 3. Mustafa, Mentor Board, https://knowledge.udacity.com/questions/633232
#############################################################################

class NEODatabase:
    """
    `NEODatabase` collection of NEOs and a collection of close approaches. 
    It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        """
        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos                
        self._approaches = list(approaches)    
        self._neo_designations = {}
        self._neo_names = {}
        
        for neo in self._neos:        
            self._neo_designations[neo.designation] = neo                   # 1
            if neo.name:
                self._neo_names[neo.name] = neo                             # 1
                
        for approach in self._approaches:
            neo = self._neo_designations[approach._designation]             # 1 
            approach.neo = neo                                              # 1
            neo.approaches.append(approach)     
            
    def get_neo_by_designation(self, designation):
        """
        Each NEO has a unique primary designation, as a string.
        Matching is exact check for spelling and capitalization 
        if no match is found, else `None`.

        :param designation: primary designation of the NEO to search.
        :return: The `NearEarthObject` designation, or `None`.
        """
        return self._neo_designations.get(designation, None)

    def get_neo_by_name(self, name):
        """
        Not every NEO in the data set has a name. No NEOs are associated 
        with the empty string or `None` singleton. Matching is exact
        check for spelling and capitalization if no match, else `None`.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        return self._neo_names.get(name, None)

    def query(self, filters=()):
        """
        Generates a stream of `CloseApproach` objects that match all provided 
        filters. If no arguments provided, generate all known close approaches.
        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: Collection of filters capturing user criteria.
        :return: Stream of matching `CloseApproach` objects.
        """
        
        for approach in self._approaches:                               # 3      
            flag = True
            for f in filters:        
                if not f(approach):
                    flag = False
                    break
            if flag:
                yield approach
