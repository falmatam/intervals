#
#Falmata Mohamed Lab 8 
#


# I used the following imports; feel free to add others
from goody import type_as_str
from math import sqrt


class Interval:
    
    compare = None 
    def __init__(self, minimum, maximum):
        self.min = minimum
        self.max = maximum
    
    @staticmethod
    def min_max(minimum, maximum=None):
        if isinstance(minimum, (int, float)) == False:
            raise AssertionError("Argument '{}' not of type int or float.".format(minimum))
        elif (isinstance(maximum, (int, float)) == False) and maximum != None:
            raise AssertionError("Argument '{}' not of type int, float or None.".format(maximum))
        elif maximum != None and minimum > maximum:
            raise AssertionError("First argument '{}' appears to be greater than second argument '{}'".format(minimum,maximum))
        else:
            return Interval(minimum,maximum)


    
    @staticmethod
    def mid_err(middle_value, plus_or_minus_error=0):
        if isinstance(middle_value, (int, float)) == False:
            raise AssertionError("Argument '{}' not of numeric type int or float.".format(middle_value))
        elif isinstance(plus_or_minus_error, (int, float)) == False and plus_or_minus_error != 0:
            raise AssertionError("Argument '{}' not of numeric type int or float.".format(plus_or_minus_error))
        elif plus_or_minus_error < 0:
            raise AssertionError("Argument '{}' is a negative numerical value.".format(plus_or_minus_error))
        else:
            return Interval(middle_value-plus_or_minus_error,plus_or_minus_error+plus_or_minus_error)

    
    def best(self):
        return (self.max+self.min)/2
    def error(self):
        return  (self.min - self.max)/ 2
    def relative_error(self):
        return abs(self.error()/self.best())*100
    
    def __repr__(self):        
        if self.max == None:
            self.max = self.min 
        return "Interval("+str(self.min)+","+str(self.max)+")" 
    
    def __str__(self):
        return str(self.best())+"(+/-"+str(self.error())+")"

    def __bool__(self):
        return True if self.error() != 0 else False

    def __pos__(self):
        return self
    
    def __neg__(self):         
        return Interval(-self.max, -self.min)
    
    def __add__(self, operand):
        if not type(operand) in [Interval, int, float]:
            raise TypeError("Operand types for '+' are unsupported for {} and {}".format(type_as_str(self),type_as_str(operand)))
        elif type(operand) in [int,float]:
            return Interval(self.min+operand, self.max+operand)
        elif type(operand) in [Interval]:
            return Interval(self.min+ operand.min, self.max+operand.max)

    
    def __radd__(self, left_operand):
        return self.__add__(left_operand)

        
    def __sub__(self, operand):
        if not type(operand) in [Interval, int, float]:
            raise TypeError("Operand types for '-' are unsupported for {} and {}".format(type_as_str(self),type_as_str(operand)))
        elif type(operand) in [Interval]:
            return Interval(self.min-operand.max, self.max-operand.min)
        elif type(operand) in [int,float]:
            return Interval(self.min-operand, self.max-operand)
        
    def __rsub__(self, left_operand):
        if not type(left_operand) in [Interval, int, float]:
            raise TypeError("Operand types for '-' are unsupported for {} and {}".format(type_as_str(self),type_as_str(left_operand)))
        elif type(left_operand) in [Interval]:
            return Interval(self.min-left_operand.max, self.max-left_operand.min)
        elif type(left_operand) in [int,float]:
            return Interval(left_operand-self.max, left_operand-self.min)
             
    def __mul__(self, operand): 
        if not type(operand) in [Interval, int, float]:
            raise TypeError("Operand types for '*' are unsupported for {} and {}".format(type_as_str(self),type_as_str(operand))) 
        elif type(operand) in [Interval]:
            return Interval(min(self.min*operand.min, self.min*operand.max, self.max*operand.min, self.max*operand.max), max(self.min*operand.min, self.min*operand.max, self.max*operand.min, self.max*operand.max))
        elif type(operand) in [int,float]:
            return Interval(self.min*operand, self.max*operand)
        
    def __rmul__(self, left_operand): 
        return self.__mul__(left_operand)

        
    def __truediv__(self, operand):
        if not type(operand) in [Interval, int, float]:
            raise TypeError("Operand types for '\' are unsupported for {} and {}".format(type_as_str(self),type_as_str(operand))) 
        elif type(operand) in [Interval]:            
            if ((operand.min < 0) and (operand.max > 0)) == True:
                raise ZeroDivisionError()
            minimum_val, maximum_val = min(self.min/operand.min, self.min/operand.max, self.max/operand.min, self.max/operand.max), max(self.min/operand.min, self.min/operand.max, self.max/operand.min, self.max/operand.max)
            return Interval(minimum_val, maximum_val) 
        elif type(operand) in [int,float]:
            return Interval(self.min/operand, self.max/operand)

  
    def __rtruediv__(self, left_operand):
        if not type(left_operand) in [Interval, int, float]:
            raise TypeError("Operand types for '\' are unsupported for {} and {}".format(type_as_str(self),type_as_str(left_operand))) 
        elif ((self.min < 0) and (self.max > 0)) == True:
            raise ZeroDivisionError()
        return Interval(left_operand/self.max,left_operand/self.min)
              
        
    def __pow__(self, operand):
        if type(operand) in [int]:
            if not (operand > 0):
                return Interval(self.max**operand, self.min**operand) 
            elif (operand > 0):  
                return Interval(self.min**operand,self.max**operand)
        elif not type(operand) in [int]:
            raise TypeError("Operand types for '**' are unsupported for {} and {}".format(type_as_str(self),type_as_str(operand))) 
         
         
    def __lt__(self, operand):
        if self.compare == 'liberal':
            if type(operand) in [int,float]:
                return (self.best() < operand)
            return (self.best() < operand.best())  
        if self.compare == 'conservative':
            if type(operand) in [int,float]:
                return (self.max < operand)
            return (self.max < operand.min)
        raise AssertionError('Liberal and/or Conservative mode is/are NOT specified!')
        
    
    def __le__(self, operand):  
        if self.compare == 'liberal':
            if type(operand) in [int,float]:
                return self.best() <= operand
            return self.best() <= operand.best()
        if self.compare == 'conservative':
            if type(operand) in [int,float]:
                return self.max <= operand
            return self.max <= operand.min
        raise AssertionError('Liberal and/or Conservative mode is/are NOT specified!')

    
    def __gt__(self, operand): 
        if self.compare == 'liberal':
            if type(operand) in [int,float]:
                return self.best() > operand
            return self.best() > operand.best()
        if self.compare == 'conservative':
            if type(operand) in [int,float]:
                return self.max > operand
            return self.max > operand.min
        raise AssertionError('Liberal and/or Conservative mode is/are NOT specified!')
        
        
    def __ge__(self, operand):    
        if self.compare == 'liberal':
            if type(operand) in [int,float]:
                return self.best() >= operand
            return self.best() >= operand.best()
        if self.compare == 'conservative':
            if type(operand) in [int,float]:
                return self.max >= operand
            return self.max >= operand.min
        raise AssertionError('Liberal and/or Conservative mode is/are NOT specified!')
    
    def __eq__(self, operator):     
        if type(operator) == Interval:
            return ((self.min == operator.min) and (self.max == operator.max))
        raise TypeError('Error. Comparison(s) MUST be of type Interval') 
    
    def __ne__(self, operator):      
        if (type(operator) == Interval):
            return ((self.min != operator.min) or (self.max != operator.max))       
        raise TypeError('Error. Comparison(s) MUST be of type Interval') 
    
    def __abs__(self):      
        if (self.max < 0 and self.min < 0) == True:
            return Interval(abs(self.max),abs(self.min))
        if self.min < 0:
            return Interval(0.0, self.max)
        return self 
            
    def sqrt(self):      
        return (Interval(sqrt(self.min),sqrt(self.max)))
    
    def __setattr__(self, key, val):
        if key in self.__dict__.keys():
            raise AssertionError('Given Key/Name already in dict keys. The object(s) in this class are immutable')
        elif not key in ['min', 'max']:
            raise AssertionError('{} not subscriptable. The objects in this class are immutable.'.format(key))
        self.__dict__[key] = val



   


    
if __name__ == '__main__':
     
    #put code here to test Interval directly
    x = Interval(2.0,3.0)
    #print("Min: ",x.min)
    #print("Max: ",x.max)
    
    #print(x)
    #print(x.min_max(2.0,3.0))
    #print(x.repr(j))
#   print(x.repr(x.mid_err(2.5,0.5)))
    j = x.min_max(2.5)
    #print("J min: ",j.min)
    #print("J max: ",j.max)
    #print(x.__repr__(x.min_max(2.5)))
    #print(x.__str__(j))
    #import driver
    #driver.driver()
