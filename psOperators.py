# written by Nathanael Ostheller
# 011717168

from psItems import Value, ArrayValue, FunctionValue
class Operators:
    def __init__(self, scoperule):
        #stack variables
        self.opstack = []  #assuming top of the stack is the end of the list
        self.dictstack = []  #assuming top of the stack is the end of the list
        self.scope = scoperule
        
        #The builtin operators supported by our interpreter
        self.builtin_operators = {
             "add":self.add, "sub":self.sub, "mul":self.mul, "mod":self.mod, "eq":self.eq, "lt":self.lt,
             "gt":self.gt, "length":self.length, "getinterval":self.getinterval,
             "putinterval":self.putinterval, "aload":self.aload, "astore":self.astore, "if":self.psIf,
             "ifelse":self.psIfelse, "repeat":self.repeat, "dup":self.dup, "copy":self.copy,
             "count":self.count, "pop":self.pop, "clear":self.clear, "exch":self.exch, "roll":self.roll,
             "stack":self.stack, "def":self.psDef, "stack":self.stack, "forall":self.forall 
        }
    #-------  Operand Stack Operators --------------
    """
        Helper function. Pops the top value from opstack and returns it.
    """
    def opPop(self):
        return self.opstack.pop()

    """
       Helper function. Pushes the given value to the opstack.
    """
    def opPush(self,value):
        self.opstack.append(value)
        
    #------- Dict Stack Operators --------------
    
    """
       Helper function. Pops the top dictionary from dictstack and returns it.
    """   
    def dictPop(self):
        return self.dictstack.pop()

    """
       Helper function. Pushes the given dictionary onto the dictstack. 
    """   
    def dictPush(self,link, d):
        self.dictstack.append((link, d))

    """
       Helper function. Adds name:value pair to the top dictionary in the dictstack.
       (Note: If the dictstack is empty, first adds an empty dictionary to the dictstack then adds the name:value to that. 
    """   
    def define(self,name, value):
        if (len(self.dictstack) == 0):
            newDict = {}
            self.dictPush(0, newDict)
        dict = self.dictPop()
        dict[1][name] = value
        jdict = dict[1]
        link = self.defineHelper(name)
        self.dictPush(link, jdict)

    def defineHelper(self, name):
        if (len(self.dictstack) == 0):
            return 0
        current = self.dictstack[-1]
        if name in current[1]:
            return current[0]
        if (self.scope == 'static'):
            if ("/" + name) in current[1]:
                return current[0]
            while (self.dictstack[current[0]] != None) and (self.dictstack[current[0]] != current):
                current = self.dictstack[current[0]]
                if ("/" + name) in current[1]:
                    return current[0]
        elif (self.scope == 'dynamic'):
            revlist = reversed(self.dictstack)
            for (link, dict) in revlist:
                if ("/" + name) in dict:
                    return link


    """
       Helper function. Searches the dictstack for a variable or function and returns its value. 
       (Starts searching at the top of the dictstack; if name is not found returns None and prints an error message.
        Make sure to add '/' to the begining of the name.)
    """
    def lookup(self,name):
        current = self.dictstack[-1]
        if (self.scope == 'static'):
            if ("/" + name) in current[1]:
                return current[1][name]
            while (self.dictstack[current[0]] != None) and (self.dictstack[current[0]] != current):
                current = self.dictstack[current[0]]
                if ("/" + name) in current[1]:
                    return current[1][name]
        elif (self.scope == 'dynamic'):
            revList = reversed(self.dictstack)
            for (link, dict) in revList:
                if ("/" + name) in dict:
                    return dict[("/" + name)]
        print("ERROR: Value does not exist to be looked up")
        return None

    
    #------- Arithmetic Operators --------------
    
    """
       Pops 2 values from opstack; checks if they are numerical (int); adds them; then pushes the result back to opstack. 
    """   
    def add(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1, int) and isinstance(op2, int):
                self.opPush(op1 + op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1)             
        else:
            print("Error: add expects 2 operands")
 
    """
       Pop 2 values from opstack; checks if they are numerical (int); subtracts them; and pushes the result back to opstack. 
    """   
    def sub(self):
        if len(self.opstack) > 1:
            op2 = self.opPop()
            op1 = self.opPop()
            if isinstance(op1, int) and isinstance(op2, int):
                self.opPush(op1 - op2)
            else:
                print("Error: one of the operands to sub is not a number value")
                self.opPush(op1)
                self.opPush(op2)
        else:
            print("Error: sub expects 2 operands")    

    """
        Pops 2 values from opstack; checks if they are numerical (int); multiplies them; and pushes the result back to opstack. 
    """    
    def mul(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1, int) and isinstance(op2, int):
                self.opPush(op1 * op2)
            else:
                print("Error: one of the operands to mul is not a number value")
                self.opPush(op2)
                self.opPush(op1)             
        else:
            print("Error: mul expects 2 operands")

    """
        Pops 2 values from stack; checks if they are int values; calculates the remainder of dividing the bottom value by the top one; 
        pushes the result back to opstack.
    """ 
    def mod(self):
        if len(self.opstack) > 1:
            op2 = self.opPop()
            op1 = self.opPop()
            if isinstance(op1, int) and isinstance(op2, int):
                self.opPush(op1 % op2)
            else:
                print("Error: one of the operands to mod is not a number value")
                self.opPush(op1)
                self.opPush(op2)
        else:
            print("Error: mod expects 2 operands") 
    #---------- Comparison Operators  -----------------
    """
       Pops the top two values from the opstack; pushes "True" is they are equal, otherwise pushes "False"
    """ 
    def eq(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (op1 == op2):
                self.opPush(True)
            else:
                self.opPush(False)
        else:
            print("Error: eq expects 2 operands") 

    """
       Pops the top two values from the opstack; pushes "True" if the bottom value is less than the top value, otherwise pushes "False"
    """ 
    def lt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (op1 > op2):
                self.opPush(True)
            else:
                self.opPush(False)
        else:
            print("Error: lt expects 2 operands") 

    """
       Pops the top two values from the opstack; pushes "True" if the bottom value is greater than the top value, otherwise pushes "False"
    """ 
    def gt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (op1 < op2):
                self.opPush(True)
            else:
                self.opPush(False)
        else:
            print("Error: gt expects 2 operands") 

    # ------- Array Operators --------------
    """ 
       Pops an array value from the operand opstack and calculates the length of it. Pushes the length back onto the opstack.
       The `length` method should support ArrayValue values.
    """
    def length(self):
        if len(self.opstack) > 0:
            op1 = self.opPop()
            if isinstance(op1, ArrayValue):
                self.opPush(len(op1.value))
            else:
                print("Error: the operand is not an array value")
        else:
            print("Error: len exprect an operand")

    """ 
        Pops the `count` (int), an (zero-based) start `index`, and an array constant (ArrayValue) from the operand stack.  
        Pushes the slice of the array of length `count` starting at `index` onto the opstack.(i.e., from `index` to `index`+`count`) 
        If the end index of the slice goes beyond the array length, will give an error. 
    """
    def getinterval(self):
        if len(self.opstack) > 2:
            count = self.opPop()
            inx = self.opPop()
            array = self.opPop()
            if isinstance(count, int) and isinstance(inx, int) and isinstance(array, ArrayValue):
                if (inx + count) <= len(array.value):
                    newArray = []
                    for x in range(count):
                        newArray.append(array.value[inx + x])
                    self.opPush(ArrayValue(newArray))
                else:
                    print("Error: subsection of array goes outside of given array bounds")
            else:
                print("Error: getinterval expects 2 ints and an array value")
        else:
            print("Error: getinterval exprects 3 operands")

    """ 
        Pops an array constant (ArrayValue), start `index` (int), and another array constant (ArrayValue) from the operand stack.  
        Replaces the slice in the bottom ArrayValue starting at `index` with the top ArrayValue (the one we popped first). 
        The result is not pushed onto the stack.
        The index is 0-based. If the end index of the slice goes beyond the array length, will give an error. 
    """
    def putinterval(self):
        if len(self.opstack) > 2:
            arr1 = self.opPop()
            inx = self.opPop()
            arr2 = self.opPop()
            if isinstance(arr1, ArrayValue) and isinstance(inx, int) and isinstance(arr2, ArrayValue):
                if (inx + len(arr1.value)) <= len(arr2.value):
                    for item in arr1.value:
                        arr2.value[inx] = item
                        inx = inx + 1
                else:
                    print("Error: subsection of array goes outside of given array bounds")
            else:
                print("Error: getinterval expects 2 array values and an int")
        else:
            print("Error: putinterval exprects 3 operands")
            

    """ 
        Pops an array constant (ArrayValue) from the operand stack.  
        Pushes all values in the array constant to the opstack in order (the first value in the array should be pushed first). 
        Pushes the orginal array value back on to the stack. 
    """
    def aload(self):
        if (len(self.opstack) > 0):
            op = self.opPop()
            if isinstance(op, ArrayValue):
                for item in op.value:
                    self.opPush(item)
                self.opPush(op)
            else:
                print("Error: aload expects an array value")
        else:
            print("Error: aload exprects an operand")
        
    """ 
        Pops an array constant (ArrayValue) from the operand stack.  
        Pops as many elements as the length of the array from the operand stack and stores them in the array constant. 
        The value which was on the top of the opstack will be the last element in the array. 
        Pushes the array value back onto the operand stack. 
    """
    def astore(self):
        if (len(self.opstack) > 0):
            array = self.opPop()
            if isinstance(array, ArrayValue):
                if (len(self.opstack) >= len(array.value)):
                    for x in range(len(array.value)):
                        array.value[x] = self.opPop()
                    array.value.reverse()
                    self.opPush(array)
                else:
                    print("Error: not enough items to fill array")
            else:
                print("Error: aload expects an array value")
        else:
            print("Error: astore exprects an operand")

    #------- Stack Manipulation and Print Operators --------------

    """
       This function implements the Postscript "pop operator". Calls self.opPop() to pop the top value from the opstack and discards the value. 
    """
    def pop (self):
        if (len(self.opstack) > 0):
            self.opPop()
        else:
            print("Error: pop expects an operand")

    """
       Prints the opstack. The end of the list is the top of the stack. 
    """
    def stack(self):
        print("===**opstack**===")
        for item in reversed(self.opstack):
            print(item)
        print("===**dictstack**===")
        m = 0
        for (link, item) in reversed(self.dictstack):
            print("{----" + m + "----"  + link + "----}")
            for key in item.keys():
                print(key, item[key])
            m = m + 1
        print("=================")

    """
       Copies the top element in opstack.
    """
    def dup(self):
        if (len(self.opstack) > 0):
            op1 = self.opPop()
            self.opPush(op1)
            self.opPush(op1)
        else:
            print("Error: dup expects an operand")

    """
       Pops an integer count from opstack, copies count number of values in the opstack. 
    """
    def copy(self):
        if (len(self.opstack) > 0):
            count = self.opPop()
            if (len(self.opstack) >= count):
                temp = []
                for x in range(count):
                    temp.append(self.opPop())
                for item in reversed(temp):
                    self.opPush(item)
                for item in reversed(temp):
                    self.opPush(item)
            else:
                print("Error: Not enough values to copy")
        else:
            print("Error: copy expects an operand")

    """
        Counts the number of elements in the opstack and pushes the count onto the top of the opstack.
    """
    def count(self):
        count = len(self.opstack)
        self.opPush(count)

    """
       Clears the opstack.
    """
    def clear(self):
        self.opstack.clear()
        
    """
       swaps the top two elements in opstack
    """
    def exch(self):
        if (len(self.opstack) > 1):
            op1 = self.opPop()
            op2 = self.opPop()
            self.opPush(op1)
            self.opPush(op2)
        else:
            print("Error: exch requires two operands")

    """
        Implements roll operator.
        Pops two integer values (m, n) from opstack; 
        Rolls the top m values in opstack n times (if n is positive roll clockwise, otherwise roll counter-clockwise)
    """
    def roll(self):
        if (len(self.opstack) > 1):
            n = self.opPop()
            m = self.opPop()
            if (len(self.opstack) >= m):
                tempList = []
                for x in range(m):
                    tempList.append(self.opPop())
                if (n >= 0):
                    for x in range(n):
                        op1 = tempList.pop(0)
                        tempList.append(op1)
                    tempList.reverse()
                else:
                    tempList.reverse()
                    for x in range(-n):
                        op1 = tempList.pop(0)
                        tempList.append(op1)
                for item in tempList:
                    self.opPush(item)
            else:
                print("Error: not enough values to roll")
        else:
            print("Error: roll requires two operands")

    """
       Pops a name and a value from opstack, adds the name:value pair to the top dictionary by calling define.  
    """
    def psDef(self): 
        if (len(self.opstack) > 1):
            value = self.opPop()
            name = self.opPop()
            if isinstance(name, str) and name[0] == '/':
                self.define(name, value)
            else:
                print("Error: def expects a name and a value")
        else:
            print("Error: def requires two operands")


    # ------- if/ifelse Operators --------------
    """
       Implements if operator. 
       Pops the `ifbody` and the `condition` from opstack. 
       If the condition is True, evaluates the `ifbody`.  
    """
    def psIf(self):
        if (len(self.opstack) > 1):
            self.dictPush(self.dictstack.count - 1, {})
            ifbody = self.opPop()
            condition = self.opPop()
            if (condition == True):
                ifbody.apply(self)
            self.dictPop()
        else:
            print("Error: if requires two operands")
        

    """
       Implements ifelse operator. 
       Pops the `elsebody`, `ifbody`, and the condition from opstack. 
       If the condition is True, evaluate `ifbody`, otherwise evaluate `elsebody`. 
    """
    def psIfelse(self):
        if (len(self.opstack) > 2):
            elsebody = self.opPop()
            ifbody = self.opPop()
            condition = self.opPop()
            if (condition == True):
                ifbody.apply(self)
            else:
                elsebody.apply(self)
        else:
            print("Error: ifelse requires 3 operands")


    #------- Loop Operators --------------
    """
       Implements repeat operator.   
       Pops the `loop_body` (FunctionValue) and loop `count` (int) arguments from opstack; 
       Evaluates (applies) the `loopbody` `count` times. 
       Will be completed in part-2. 
    """  
    def repeat(self):
        if (len(self.opstack) > 1):
            loopBody = self.opPop()
            count = self.opPop()
            if isinstance(loopBody, FunctionValue) and isinstance(count, int):
                self.dictPush(self.dictstack.count - 1, {})
                for x in range(count):
                    loopBody.apply(self)
                self.dictPop()
            else:
                print("Error: repeat requires a body and an integer")
        else:
            print("Error: repeat requires two operands")


        
    """
       Implements forall operator.   
       Pops a `codearray` (FunctionValue) and an `array` (ArrayValue) from opstack; 
       Evaluates (applies) the `codearray` on every value in the `array`.  
       Will be completed in part-2. 
    """ 
    def forall(self):
        if (len(self.opstack) > 1):
            codearray = self.opPop()
            array = self.opPop()
            if isinstance(codearray, FunctionValue) and isinstance(array, ArrayValue):
                self.dictPush(self.dictstack.count - 1, {})
                for item in array.value:
                    self.opPush(item)
                    codearray.apply(self)
                self.dictPop()
            else:
                print("Error: forall requires a body and an array")
        else:
            print("Error: forall requires 2 operands")

    #--- used in the setup of unittests 
    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []

    def cleanTop(self): 
        if len(self.opstack)>1: 
            if self.opstack[-1] is None: 
                self.opstack.pop() 