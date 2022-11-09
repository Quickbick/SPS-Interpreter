class Value:
    """
    "Value" objects represent the  array and code-array constant values that are pushed onto the stack.  
    
    In our interpreter,
        -  For simplicity, the integers and boolean values are pushed onto the opstack as integers and booleans, respectively. 
        -  Similarly, name constants (e.g. '/x') are pushed to the opstack as strings. 
        -  The array and codearray constant values are represented as ArrayValue and FunctionValue objects, 
           which are subclasses of the `Value`. 
        -  ArrayValue and FunctionValue implement the following methods in the `Value` interface:
            * apply : Evaluates the value. `apply` is only applicable to FunctionValue objects (applies the function, evaluates all the tokens in the function's code-array, i.e., FunctionValue )  
            * __str__: Conversts the value to  a human-readable version (i.e., string) for printing.
    """

    def __init__(self, value):
        self.value = value

    def apply(self, psstack):
        """
        Each subclass of Value implements its own `apply` method.
        Note that only `FunctionValue`s can be "applied"; attempting to apply an ArrayValue will give an error. 
        """
        raise NotImplementedError

    def __str__(self):
        """
        Returns a parsable and human-readable version of this value (i.e. the string to be displayed in the interpreter).
        """
        raise NotImplementedError

    def __repr__(self):
        """
        Returns how this value is printed in our Python representation.
        """
        return "{}({})".format(type(self).__name__, self.value)

# ------------------------------------------------------------

class ArrayValue(Value):
    """An array constant value delimited in square brackets. Attempting to apply an `array constant` will give an error.
      The `value` attribute is the Python list that this value represents.
    """
    def __init__(self, value):
        Value.__init__(self, value)
        self.value = value

    def apply(self, stacks):
        raise TypeError("Ouch! Cannot apply `array constant value` {} ".format(self.value))

    def __str__(self):
        return str(self.value)

# ------------------------------------------------------------

class FunctionValue(Value):
    """The codearray values that represents the body of a (user-defined) function. 
    
    The `body` attribute is a list of tokens.
        
    The `apply` method will evaluate each token in the `body` by calling token's `eval` method. 
    Tokens will be evaluated in in the current referencing environment (stacks).  
    """
    def __init__(self, body):
        Value.__init__(self, body)
        self.body = body

    def apply(self, stacks):
        # TO-DO in milestone2
        pass

    def __str__(self):
        return '<function {}>'.format(self.body)




