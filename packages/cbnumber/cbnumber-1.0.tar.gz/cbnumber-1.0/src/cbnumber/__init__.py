"""
NumberBase © 2024 by Jean Moïse Talec is licensed under CC BY-NC-SA 4.0. 
To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

from enum import Enum
from typing import Iterable, Union
from copyreg import pickle


__author__ = "Jean Moïse Talec"
__all__ = ["NumberBase", "Bases"]
__version__ = "1.0"

class Bases(Enum):
    """
    Enum representing different base systems.
    
    Attributes:
        DECIMAL (str): Represents the decimal system (base 10) using digits 0-9.
        BINARY (str): Represents the binary system (base 2) using digits 0 and 1.
        HEXADECIMAL (str): Represents the hexadecimal system (base 16) using digits 0-9 and A-F.
    """
    DECIMAL = "0123456789"
    BINARY  = "01"
    HEXADECIMAL = "0123456789ABCDEF"

class NumberBase(int):
    """
    A class representing numbers in arbitrary bases, extending the built-in `int` type.
    Supports pickling.

    Attributes:
        base (int): The base of the number system being used.
        base_map (tuple): A tuple representing the mapping of digits or characters for the base.
        null (object): The representation of zero in the base system.
        _immutable (tuple): A tuple of attribute names that are immutable.
        _locked (bool): A flag indicating if attribute modification is locked.
    
    Methods:
        __new__(cls, x, base_map, null): Creates a new instance of the NumberBase class.
        __init__(self, x, base_map, null): Initializes the NumberBase instance.
        to_base(self, base_map, null): Converts the current number to another base system.
        __setattr__(self, name, value): Restricts modification of immutable attributes.
        __delattr__(self, name): Restricts deletion of immutable attributes.
        __iter__(self): Returns an iterator that yields the digits of the number in the current base.
        __str__(self): Returns the string representation of the number.
        __repr__(self): Returns a string representation of the number with a prefix.
        Arithmetic and bitwise operators: Overloaded operators to support operations between NumberBase and int or another NumberBase.
    """
    def __new__(cls, x: int, base_map: Union[Iterable[object], Bases] = Bases.DECIMAL, null: object = None):
        """
        Creates a new instance of the NumberBase class.
        
        Args:
            x (int): The integer value of the number.
            base_map (Union[Iterable[object], Bases], optional): The base system to be used. Defaults to Bases.DECIMAL.
            null (object, optional): The representation of zero in the base system. Defaults to None.
        
        Returns:
            NumberBase: A new instance of the NumberBase class.
        """
        return super().__new__(cls, x)
    
    def __init__(self, x: int, base_map: Union[Iterable[object], Bases] = Bases.DECIMAL, null: object=None) -> None:
        """
        Initializes a NumberBase instance.
        
        Args:
            x (int): The integer value of the number.
            base_map (Union[Iterable[object], Bases], optional): The base system to be used. Can be an iterable or a Bases enum. Defaults to Bases.DECIMAL.
            null (object, optional): The representation of zero in the base system. Defaults to None.
        """
        if type(base_map) == Bases:
            self.base = len(base_map.value)  
            self.base_map = tuple(base_map.value)
            self._field = dict(enumerate(base_map.value))  
        else:

            self.base = len(base_map)
            self.base_map = tuple(base_map)
            self._field = dict(enumerate(base_map))

        if null:
            self.null = null
        else:
            self.null = self._field[0]
        
        self._immutable = ("base", "base_map", "null", "_immutable", "_locked")
        self._locked = True

    def to_base(self, base_map, null=None):
        """
        Converts the current number to another base system.
        
        Args:
            base_map (Union[Iterable[object], Bases]): The base system to convert to. Can be an iterable or a Bases enum.
            null (object, optional): The representation of zero in the new base system. Defaults to None.
        
        Returns:
            NumberBase: A new NumberBase instance in the specified base system.
        """
        return NumberBase(self, base_map, null)

    def __setattr__(self, name, value):
        """
        Restricts modification of immutable attributes.
        
        Args:
            name (str): The name of the attribute to set.
            value (object): The value to assign to the attribute.
        
        Raises:
            AttributeError: If the attribute is immutable.
        """
        if hasattr(self, '_locked') and name in self._immutable:
            raise AttributeError(f"The '{name}' attribute is immutable")
        super().__setattr__(name, value)

    def __delattr__(self, name):
        """
        Restricts deletion of immutable attributes.
        
        Args:
            name (str): The name of the attribute to delete.
        
        Raises:
            AttributeError: If the attribute is immutable.
        """
        if name in self._immutable:
            raise AttributeError(f"The '{name}' attribute is immutable")
        super().__delattr__(name)

    def __iter__(self):
        """
        Returns an iterator that yields the digits of the number in the current base.
        
        Yields:
            object: The next digit of the number in the current base.
        """
        result = []
        num = self
        if num == 0:
            yield self.null
            return 
        elif self.base == 1:
            result = [self.base_map[0] for x in range(self)]
        else:
            while num > 0:
                remainder = num % self.base
                result.append(self._field[remainder])
                num //= self.base
            result.reverse()
        while result:
            yield result.pop(0)

    def __str__(self) -> str:
        """
        Returns the string representation of the number.
        
        Returns:
            str: The string representation of the number.
        """
        return str().join([str(x) for x in self])

    def __repr__(self):
        """
        Returns a string representation of the number with a prefix.
        
        Returns:
            str: The string representation of the number with the prefix "[bn]: ".
        """
        return "[bn]: "+str(self)
 
    def __add__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__add__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__add__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
        
    def __and__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__and__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__and__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
                
    def __divmod__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__divmod__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__divmod__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
    
    def __floordiv__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__floordiv__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__floordiv__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
        
    def __lshift__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__lshift__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__lshift__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
        
    def __mod__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__mod__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__mod__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
        
    def __mul__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__mul__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__mul__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
        
    def __pow__(self, value, mod=None):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        v = super().__pow__(value, mod)
        if v == NotImplemented:
            raise TypeError(f"Value or mod not supported: {value}, {mod}")
        if v >= 0:
            return NumberBase(v, self.base_map, self.null)
        else:
            return v
        
    def __radd__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__radd__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__radd__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
        
    def __rand__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__rand__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__rand__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
    
    def __rdivmod__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__rdivmod__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__rdivmod__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
        
    def __rfloordiv__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__rfloordiv__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__rfloordiv__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
        
    def __rlshift__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__rlshift__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__rlshift__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
    
    def __rmod__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__rmod__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__rmod__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
        
    def __rmul__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__rmul__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__rmul__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
        
    def __rpow__(self, value, mod=None):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        v = super().__rpow__(value, mod)
        if v >= 0:
            return NumberBase(v, self.base_map, self.null)
        else:
            return v
        
    def __rrshift__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__rrshift__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__rrshift__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
        
    def __rshift__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__rshift__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__rshift__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
        
    def __rsub__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__rsub__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__rsub__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
        
    def __rtruediv__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__rtruediv__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__rtruediv__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
    
    def __rxor__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__rxor__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__rxor__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
        
    def __sub__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__sub__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__sub__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
        
    def __truediv__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__truediv__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__truediv__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented
        
    def __xor__(self, other):
        """
        Overloads the operator for performing a NumberBase or int to this NumberBase instance.
        
        Args:
            other (Union[int, NumberBase]): The number to perform.
        
        Returns:
            NumberBase: A new NumberBase instance representing the result of the performance.
        """
        if isinstance(other, NumberBase):
            return NumberBase(super().__xor__(other), base_map=self.base_map, null=self.null)
        elif isinstance(other, int):
            return NumberBase(super().__xor__(other), base_map=self.base_map, null=self.null)
        else:
            return NotImplemented

def _pickle_number_base(nb: NumberBase):
    return NumberBase, (int(nb), nb.base_map, nb.null)

pickle(NumberBase, _pickle_number_base)

def _main():
    num = NumberBase(243, Bases.BINARY)
    print(repr(num))
    print(repr(num+1))
    num **= 2
    num **= 1/2

if __name__ == "__main__":
    _main()