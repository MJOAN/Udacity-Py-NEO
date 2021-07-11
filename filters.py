"""
Provide filters for querying close approaches and limit the generated results.

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
"""
import operator
import itertools

######### Code References:####################################################
## 1. Martijn Pieters, Stack Overflow: https://bit.ly/3r2CW5L
## 2. Shuaishuai, Mentor Board, https://knowledge.udacity.com/questions/599130 
## 3. Shuaishuai, Mentor Board, https://knowledge.udacity.com/questions/624020
##############################################################################

class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""

class AttributeFilter:
    """
    `AttributeFilter` is search criteria pattern comparing some
    attribute of a close approach (or its attached NEO) to reference value.
    It functions as a callable predicate for whether a `CloseApproach`
    object satisfies the encoded criterion.

    Constructed with a comparator operator and reference value,
    calling filter (with __call__) executes `get(approach) OP value`

    Concrete subclasses can override the `get` classmethod to provide custom
    behavior to fetch a desired attribute from the given `CloseApproach`.
    """
    def __init__(self, op, value):
        """
        Construct new `AttributeFilter` from binary predicate and reference value.

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
        """
        Concrete subclasses must override method to get attribute
        from the supplied `CloseApproach`.
        
        :param approach: `CloseApproach` on which to evaluate this filter.
        :return: Attribute value, comparable to `self.value` via `self.op`.
        """
        raise UnsupportedCriterionError

    def __repr__(self):
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"

class DateFilter(AttributeFilter):   
    @classmethod
    def get(self, approach):
        return approach.time.date()

class DistanceFilter(AttributeFilter):  
    @classmethod
    def get(self, approach):
        return approach.distance 

class VelocityFilter(AttributeFilter):  
    @classmethod
    def get(cls, approach):
        return approach.velocity

class DiameterFilter(AttributeFilter): 
    @classmethod
    def get(cls, approach):
        return approach.neo.diameter

class HazardousFilter(AttributeFilter): 
    @classmethod
    def get(cls, approach):
        return approach.neo.hazardous
        
def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None):
    """
    Each argument is provided by the main module with a value from the
    user's options at command line. Each corresponds to a different type
    of filter. For example, the `--date` option corresponds to `date`
    argument, represents a filter that selects close approaches occured
    on exactly that given date. Each option is `None` if not specified 
    at the command line (in particular, this means that the 
    `--not-hazardous` flag results in `hazardous=False`, 
    not to be confused with `hazardous=None`).

    The return value must be compatible with the `query` method of `NEODatabase`
    because the main module directly passes this result to that method. For now,
    this can be thought of as a collection of `AttributeFilter`s.

    :param date: `date` on which a matching `CloseApproach` occurs.
    :param start_date: `date` on or after `CloseApproach` occurs.
    :param end_date: `date` on or before `CloseApproach` occurs.
    :param distance_min: minimum nominal approach distance for `CloseApproach`.
    :param distance_max: maximum nominal approach distance for  `CloseApproach`.
    :param velocity_min: minimum relative approach velocity for `CloseApproach`.
    :param velocity_max: maximum relative approach velocity for  `CloseApproach`.
    :param diameter_min: minimum diameter of the NEO of `CloseApproach`.
    :param diameter_max: maximum diameter of the NEO of `CloseApproach`.
    :param hazardous: If NEO of a matching `CloseApproach` is hazardous.
    :return: A collection of filters for use with `query`.
    """
    result = [] 
    filter_args = locals().items()

    for key, value in filter_args.items():
       if date is not None:
            result.append( DateFilter(operator.eq, filter_args.get('date')))                    # 2

        if start_date is not None:
            result.append( DateFilter(operator.ge, filter_args.get('start_date')))

        if end_date is not None:
            result.append( DateFilter(operator.le, filter_args.get('end_date')))

        if distance_min is not None:
            result.append( DistanceFilter(operator.ge, filter_args.get('distance_min')))

        if distance_max is not None:
            result.append( DistanceFilter(operator.le, filter_args.get('distance_max')))

        if velocity_min is not None:
            result.append( VelocityFilter(operator.ge, filter_args.get('velocity_min')))

        if velocity_max is not None:
            result.append( VelocityFilter(operator.le, filter_args.get('velocity_max')))

        if diameter_min is not None:
            result.append( DiameterFilter(operator.ge, filter_args.get('diameter_min')))

        if diameter_max is not None:
            result.append( DiameterFilter(operator.le, filter_args.get('diameter_max')))
                           
        if hazardous is not None:
            result.append( HazardousFilter(operator.eq, filter_args.get('hazardous')))
            
    return result

    
def limit(iterator, n=None):
    """
    Produce a limited stream of values from an iterator, 
    if `n` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values. 
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """
    if n == 0 or n == None:
        return iterator

    return itertools.islice(iterator, n)                    # 3
      

   
 
   
        
        