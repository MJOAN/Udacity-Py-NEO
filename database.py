"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria. Under normal circumstances, the main module creates 
one NEODatabase from the data on NEOs and close approaches extracted by
 `extract.load_neos` and `extract.load_approaches`
"""
from collections import defaultdict
from filters import AttributeFilter, DateFilter, DistanceFilter, 
                    VelocityFilter, DiameterFilter, HazardousFilter

########### Code References: ####################################################################
## 1. Vanina W., Udacity Mentor Board, Reference: https://knowledge.udacity.com/questions/478946
## 2. Shuaishuai, Udacity Mentor Board, Reference: https://knowledge.udacity.com/questions/599130 
##################################################################################################

class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.
        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """

        self._neos = neos                
        self._approaches = list(approaches)    
        self._neo_designations = defaultdict()
        self._neo_names = defaultdict()
                
        for neo in neos:        
            self._neo_designations[neo.designation] = neo   # 1
            if neo.name:
                self._neo_names[neo.name] = neo             # 1
                
        for approach in approaches:
            neo = self._neo_designations[approach._designation]  # 1
            approach.neo = neo                                       # 1
            neo.approaches.append(approach)                          
        
#         1st attempt: Tried both for loops with list dict:
#         for neo in self._neos:         
#             if neo['pdes']:
#                 designation_dict = {  neo['pdes']: neo }            
#                 self._neo_designations.append( designation_dict )  
    
#             if neo['name']:
#                 name_dict = {  neo['name']: neo }
#                 self._neo_names.append( name_dict ) 
            
#         for cad in self._approaches:      
#             # linking occurs here if CAD's "des" (fields[]) == NEO's designation
#             if cad['des'] == self._neos['designation']:   
#                 # then append CAD to NEO's approaches []
#                 self._neos.approaches.append(cad['dist']) 
#                  # also add NEO name to CAD's neo
#                 cad['neo'] = self._neo_names['name']         
            

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.
        If no match is found, return `None` instead.
        Each NEO in the data set has a unique primary designation, as a string.
        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """

        result = []
        # iterate over NEO list of dict designation #s
        for item in self._neo_designations:
            # if NEO disignation == user input 
            if item['designation'] == designation:
                # find match in NEO object and return NEO object
                if self._neos['pdes'] == item['designation']:
                    return neo
                
        # else return None
        return None

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        result = []
        # iterate over NEO list of dict names
        for item in self._neo_designations:
            # if NEO name == user input 
            if item['name'] == name:
                # find match in NEO object and return NEO object
                if self._neos['name'] == item['name']:
                    return neo
                
        # else return None
        return None

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters. 
        
        This method will be recieving a list of filters requested and called from 
        the create_filters method then passed in here to filters=()

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        # Generate `CloseApproach` objects that match all of the filters.
        # TODO: flag to set status if filter is None else yield approach
        # TODO: use get_neo_by_designation? 
        
        flag = True 

        for approach in self._approaches:
            if AttributeFilter.DateFilter(approach):
                continue
            if AttributeFilter.DistancerFilter(approach):
                continue
            if AttributeFilter.VelocityFilter(approach):
                continue
            if AttributeFilter.DiameterFilter(approach):
                continue
            if AttributeFilter.HazardousFilter(approach):
                continue
    
            yield approach
