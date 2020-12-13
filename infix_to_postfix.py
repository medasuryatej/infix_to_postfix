# Need the below package for printing the output in a tabular format
try:
    import sys
    from prettytable import PrettyTable
except ImportError as e:
    print (f"Missing Python package for {e}")
    print ("pip install prettytable")
    sys.exit()

__author__ = "Meda Sai Krishna Pavan Suryatej"
__contact__ = "medasuryatej@gmail.com"

x = PrettyTable()
x.field_names = ["Symbol", "Stack", "PostFix"]

mathOperations = ["*", "/", "+", "-", "^"]
parenthesis = ["(", ")"]

OPEN_PARANTHESIS = 0
CLOSED_PARANTHESIS = 1
OPERAND = 2
OPERATION = 3

PRECEDENCE = ["^", "/", "*", "+", "-"]
PRECEDENCE = {"(" : -1, ")" : -1 , "^" : 2, "/": 1, "*": 1, "+": 0, "-": 0, "EOS": -2}
ASSOCIVITY = {"L-R": 0, "R_L": 1}
# Note Paranthesis have higher precedence than all other operations, but for code purpose
# their precedence is taken as -1

def associvity(operation):
    if operation == "^":
        return ASSOCIVITY["R-L"]
    else:
        return ASSOCIVITY["L-R"]

class Stack:
    stack = []
    def push(self, value):
        if value is None:
            # print ("Invalid Value")
            return None
        self.stack.append(str(value))
    def pop(self):
        if len(self.stack) < 1:
            # print ("Stack is Empty")
            return None
        poppedValue = self.stack.pop()
        # print (f"Popped-{poppedValue}")
        return poppedValue
    def size(self):
        return (len(self.stack))
    def print(self):
        if self.size() == 0:
            # print ("Empty Stack")
            return None
        else:
            return "".join(self.stack)
    def peak(self):
        if self.size() is 0:
            return "EOS"
        return self.stack[-1]

def operation(character):
    if character.isalnum():
        # character in [A-z0-9]
        return OPERAND
    elif character in mathOperations:
        # character in [+ - * / ^]
        return OPERATION
    elif character in parenthesis:
        # character in [ (, )]
        return parenthesis.index(character)
    else:
        # Unknow Character
        return None

def uniformExpression(input_expression):
    input_expression = input_expression.replace("[", "(")
    input_expression = input_expression.replace("]", ")")
    input_expression = input_expression.replace("{", "(")
    input_expression = input_expression.replace("}", ")")
    return input_expression

# input_expression = "K+L-M*N+(O^P)*W/U/V*T+Q"
input_expression = input("Enter your expression: ")
input_expression = uniformExpression(input_expression)
stack = Stack()

symbol = ""
stackvar = ""
postfix = ""
"""
Pseudo Code:
1. Parse the infix expression Left to Right once
2. if the character is 
    OPERAND
        - add it to the POSTFIX expression
    OPERATOR
        - if the precedence of incoming operator is greater than top of stack Push it to stack
        - if the precedence of incoming operator is equal to the top of stack and associvity is R to L push the incoming operator
            to the stack
        - if the precedence of incoming operator is less than or equal top of stack recursively pop stack and 
            add them to postfix expression untill precedence of incoming operator is greater than top of stack
    LEFT PARANTHESIS
        - Push it to stack
    RIGHT PARANTHESIS
        - recursively pop the values from stack and add to postfix expression until you encounter LEFT paranthesis
        - pop left paranthesis

"""
for everyCharacter in input_expression:
    symbol = everyCharacter
    wtd = operation(everyCharacter)
    if wtd == OPERAND:
        stackvar = stack.print()
        postfix += symbol
        x.add_row([symbol, stackvar, postfix])
    elif wtd == OPEN_PARANTHESIS:
        stack.push('(')
        stackvar = stack.print()
        x.add_row([symbol, stackvar, postfix])
    elif wtd == CLOSED_PARANTHESIS:
        while stack.peak() != "(":
            stackvalue = stack.pop()
            if stackvalue is not None:
                postfix += stackvalue
        # one more pop for removing ( from stack
        stack.pop()
        stackvar = stack.print()
        x.add_row([symbol, stackvar, postfix])
    elif wtd == OPERATION:
        incomingOperator = PRECEDENCE[everyCharacter]
        if incomingOperator > PRECEDENCE[stack.peak()]:
            stack.push(everyCharacter)
            stackvar = stack.print()
            x.add_row([symbol, stackvar, postfix])
            continue
        while PRECEDENCE[stack.peak()] >= incomingOperator:
            if (PRECEDENCE[stack.peak()] == incomingOperator): 
                if associvity(everyCharacter):
                    stack.push(everyCharacter)
                else:
                    stackValue = stack.pop()
                    if stackValue is not None:
                        postfix += stackValue
            else:
                stackValue = stack.pop()
                if stackValue is not None:
                    postfix += stackValue
        stack.push(everyCharacter)
        stackvar = stack.print()
        x.add_row([symbol, stackvar, postfix])
    else:
        pass

while stack.size() > 0:
    stackValue = stack.pop()
    if stackValue is not None:
        postfix += stackValue
x.add_row([None, None, " ".join(postfix)])
print(f"Infix Expression: {input_expression}")
print(x)
print(f"Postfix Expression: {postfix}")