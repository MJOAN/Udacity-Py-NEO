"""Provide filters for querying close approaches and limit the generated results.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function can be thought to return a collection of instances of subclasses
of `AttributeFilter` - a 1-argument callable (on a `CloseApproach`) constructed
from a comparator (from the `operator` module), a reference value, and a class
method `get` that subclasses can override to fetch an attribute of interest from
the supplied `CloseApproach`.

The `limit` function simply limits the maximum number of values produced by an
iterator.

You'll edit this file in Tasks 3a and 3c.
"""
import operator

######### Code References:#################################################################################################################
## 1. Martijn Pieters, Stack Overflow: Reference: https://stackoverflow.com/questions/16814984/python-list-iterator-behavior-and-nextiterator
## 2. Shuaishuai, Udacity Mentor Board, Reference: https://knowledge.udacity.com/questions/599130 
############################################################################################################################################


class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""


class AttributeFilter:
    """A general superclass for filters on comparable attributes.
    An `AttributeFilter` represents the search criteria pattern comparing some
    attribute of a close approach (or its attached NEO) to a reference value. It
    essentially functions as a callable predicate for whether a `CloseApproach`
    object satisfies the encoded criterion.

    It is constructed with a comparator operator and a reference value, and
    calling the filter (with __call__) executes `get(approach) OP value` (in
    infix notation).

    Concrete subclasses can override the `get` classmethod to provide custom
    behavior to fetch a desired attribute from the given `CloseApproach`.
    """
    def __init__(self, op, value):
        """Construct a new `AttributeFilter` from an binary predicate and a reference value.

        The reference value will be supplied as the second (right-hand side)
        argument to the operator function. For example, an `AttributeFilter`
        with `op=operator.le` and `value=10` will, when called on an approach,
        evaluate `some_attribute <= 10`.

        :param op: A 2-argument predicate comparator (such as `operator.le`).
        :param value: The reference value to compare against.
        """
        self.op = op
        self.value = value

    def __call__(self, approach):
        """Invoke `self(approach)`."""
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """Get an attribute of interest from a close approach.
        Concrete subclasses must override this method to get an attribute of
        interest from the supplied `CloseApproach`.
        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of an attribute of interest, comparable to `self.value` via `self.op`.
        """
        raise UnsupportedCriterionError

    def __repr__(self):
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"

    class DateFilter(AttributeFilter):   # CAD
        @classmethod
        def get(self, approach):
            return approach.neo.date

    class DistanceFilter(AttributeFilter):  # CAD
        @classmethod
        def get(self, approach):
            return approach.neo.distance 

    class VelocityFilter(AttributeFilter):  # CAD
        @classmethod
        def get(cls, approach):
            return approach.neo.velocity

    class DiameterFilter(AttributeFilter): # NEO
        @classmethod
        def get(cls, approach):
            return approach.neo.diameter

    class HazardousFilter(AttributeFilter): # NEO
        @classmethod
        def get(cls, approach):
            return approach.neo.hazardous
        
    
def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None, **args):
    """Create a collection of filters from user-specified criteria.

    Each of these arguments is provided by the main module with a value from the
    user's options at the command line. Each one corresponds to a different type
    of filter. For example, the `--date` option corresponds to the `date`
    argument, and represents a filter that selects close approaches that occured
    on exactly that given date. Similarly, the `--min-distance` option
    corresponds to the `distance_min` argument, and represents a filter that
    selects close approaches whose nominal approach distance is at least that
    far away from Earth. Each option is `None` if not specified at the command
    line (in particular, this means that the `--not-hazardous` flag results in
    `hazardous=False`, not to be confused with `hazardous=None`).

    The return value must be compatible with the `query` method of `NEODatabase`
    because the main module directly passes this result to that method. For now,
    this can be thought of as a collection of `AttributeFilter`s.

    :param date: A `date` on which a matching `CloseApproach` occurs.
    :param start_date: A `date` on or after which a matching `CloseApproach` occurs.
    :param end_date: A `date` on or before which a matching `CloseApproach` occurs.
    :param distance_min: A minimum nominal approach distance for a matching `CloseApproach`.
    :param distance_max: A maximum nominal approach distance for a matching `CloseApproach`.
    :param velocity_min: A minimum relative approach velocity for a matching `CloseApproach`.
    :param velocity_max: A maximum relative approach velocity for a matching `CloseApproach`.
    :param diameter_min: A minimum diameter of the NEO of a matching `CloseApproach`.
    :param diameter_max: A maximum diameter of the NEO of a matching `CloseApproach`.
    :param hazardous: Whether the NEO of a matching `CloseApproach` is potentially hazardous.
    :return: A collection of filters for use with `query`.
    """
  
    # list of arg names 
    params = ['date', 'start_date', 'end_date', 'distance_min', 'distance_max', 'velocity_min', 'velocity_max', 
               'diameter_min', 'diameter_max', 'hazardous']
    
    # convert arg values to list
    params_values = [x for x in args if x else None]
    
    # zip arg values to dict
    filter_dict = dict( zip( params, params_values )) 

    # filter where None, and convert to list of tuples 
    # filters_collection = [ (k, v) for k, v in params_dict.items() if v is not None ]
   
    # filters_collection looks like:           
    #[('date', 20120101),
    #('start_date', 20130101),
    #('end_date', 'None'), ..... )]

    # params_dict looks like:
    # {'date': 20120101,
    # 'start_date': 20130101,
    # 'end_date': 'None', ...}
              
    result = []
    query_collection = {}
              
    # possibly you don't need to collect params to dict 
    for key, value in filter_dict.items():

        # neeed clarity on which operator eq, ge, le to use for each
        # iterate over params dictionary 
        # call our Filter subclasses with operator and value from user param 
        # update our query collection dictionary with key and value from call
        if bool(filter_dict.get('date')):
            date_filter = DateFilter(operator.eq,  filter_dict.get('date')  ))  # 2
            query_collection.update( { 'date':  date_filter  } )

        if bool(filter_dict.get('start_date')):
            start_date_filter = DateFilter(operator.le,  filter_dict.get('start_date')  ))
            query_collection.update( { 'start_date':  start_date_filter  } )

        if bool(filter_dict.get('end_date')):
            end_date_filter = DateFilter(operator.ge,  filter_dict.get('end_date')  ))
            query_collection.update( { 'end_date':  end_date_filter  } )

        if bool(filter_dict.get('distance_min')):
            distance_min_filter = DistanceFilter(operator.ge,  filter_dict.get('distance_min')  ))
            query_collection.update( { 'distance_min':  distance_min_filter  } )

        if bool(filter_dict.get('distance_max')):
            distance_max_filter = DistanceFilter(operator.le,  filter_dict.get('distance_max')  ))
            query_collection.update( { 'distance_max':  distance_max_filter  } )

        if bool(filter_dict.get('velocity_min')):
            velocity_min_filter = VelocityFilter(operator.ge,  filter_dict.get('velocity_min')  ))
            query_collection.update( { 'velocity_min':  velocity_min_filter  } )

        if bool(filter_dict.get('velocity_max')):
            velocity_max_filter = VelocityFilter(operator.le,  filter_dict.get('velocity_max')  ))
            query_collection.update( { 'velocity_max':  velocity_max_filter  } )

        if bool(filter_dict.get('diameter_min')):
            diameter_min_filter = DiameterFilter(operator.ge,  filter_dict.get('diameter_min')  ))
            query_collection.update( { 'diameter_min':  diameter_min_filter  } )

        if bool(filter_dict.get('diameter_max')):
            diameter_max_filter = DiameterFilter(operator.le,  filter_dict.get('diameter_max')  ))
            query_collection.update( { 'diameter_max':  diameter_max_filter  } )

        if bool(filter_dict.get('hazardous')):
            hazardous_filter = HazardousFilter(operator.eq,  filter_dict.get('hazardous')  ))
            query_collection.update( { 'hazardous':  hazardous_filter  } )

    # land results to our result list and return
    result.append(query_collection)                     
    return result


        ### trying to understand how to setup method
        #for _ in range(9):   ## pseudo 
        #    if DiameterFilter.__call__( operator.le(approach.neo.diameter, diameter_min)) :
        #        query_collection['diameter_min'] = DiameterFilter.get(approach.neo.diameter)
        #    if DiameterFilter.__call__( operator.ge(approach.neo.diameter, diameter_max)) :
        #        query_collection['diameter_max'] = DiameterFilter.get(approach.neo.diameter)
        #    if VelocityFilter.__call__( operator.le(approach.neo.velocity, velocity_min)) :
        #        query_collection['velocity_min'] = VelocityFilter.get(approach.neo.velocity)
        # .. ... 

        ## 1st attempt if using collection tuple
        # if DistanceFilter.__call__( operator.le( approach.neo.distance, filters[1])) :
        #     query_collection['diameter_min'] = DistanceFilter.get(approach.neo.diameter)
        # if filters[0] == 'distance_max':
        #     if DistanceFilter.__call__( operator.le( approach.neo.distance, filters[1])) :
        #         query_collection['diameter_min'] = DistanceFilter.get(approach.neo.diameter)
                


def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator.
    If `n` is 0 or None, don't limit the iterator at all.
    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """
    if n == 0 or n == None:
        return
    
    a = iter(iterator(range(n)))  # 1
    
    for _ in a:
        value = next(a)
        yield(value)
        
        
        
