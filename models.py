"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    def __init__(self, designation, name=None, diameter=float('nan'), hazardous=False, approaches=[], **info):
        """NearEarthObject class constructor
            :param designation (required): Primary designation of `NearEarthObject`
            :param name (optional/None): IAU name of `NearEarthObject
            :param diameter (optional, float/km): Diameter, in kilometers, of `NearEarthObject`
            :param hazardous (boolean): `NearEarthObject` if hazardous
        """
        
        self.designation = designation
        self.name = lambda x: x if x else None 
        self.diameter = lambda x: float(x) if x else float('nan') 
        self.hazardous = hazardous
        self.approaches = []
        
    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f"{self.designation} {self.name}"

    def designation(self):
        return self.designation

    def name(self):
        return self.name

    def diameter(self):
        return self.diameter

    def hazardous(self):
        return self.hazardous

    def __str__(self):
        """Return `str(self)`."""
        return f"NEO {self.fullname} has a diameter {self.diameter} km and is {self.hazardous} hazardous."
       
    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter!r}, hazardous={self.hazardous!r})")


class CloseApproach(NearEarthObject):
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    # def __init__(self, designation, time=None, distance=float('nan'), velocity=float('nan'), **info):
    def __init__(self, **info):
        """CloseApproach class constructor
            :param _designation (private, required): Primary designation of `NearEarthObject`
            :param time (datetime): Datetime UTC of `NearEarthObject` closest approach to Earth 
            :param distance (float): Distance in astronomical units (au) `NearEarthObject` closest point to Earth 
            :param velocity (float): Velocity in kilometers per second (kms) `NearEarthObject` closest point to Earth
        """
        self._designation = ''
        self.time = lambda x: cd_to_datetime(x) if x else None 
        self.distance = lambda x: float(x) if x else float('nan')      
        self.velocity = lambda x: float(x) if x else float('nan')  
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return f"NEO {NearEarthObject.fullname} had it's closest point near Earth on {datetime_to_str(self.time)}."

        def name(self):
            return NearEarthObject.fullname

        def time(self):
            return self.time

        def distance(self):
            return self.distance

        def velocity(self):
            return self.velocity
        
        def neo(self):
            return self.neo

    def __str__(self):
        """Return `str(self)`."""
        return f"NEO {self.name} has a distance of {self.diameter} and velocity at {self.velocity}."
  

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance!r}, "
                f"velocity={self.velocity!r}, neo={self.neo!r})")

   
