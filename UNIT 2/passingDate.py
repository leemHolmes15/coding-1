# when we are buliding complex programs we need a way to pass in 
# date that is NOT from the user 

# Function arguments and parameters are ways to
#  pass in data to a function from possibly 
# another function. 


# Functios paramters- this is PLACEHOLDER DATA for a finctions 
# variables inside the curly brackets 

# memory trick - PARAMETER AND PLACEHOLDER BOTH
# START WITH THE LETTER P
def check_Water_Depth(depth):
    print(depth)
    print(depth > 10) # true if depth is greater than 10 feet
    # return depth

# functions arguments- this is the REAL DATA that we pass into 
#the functions call.

# Function Arguments- This is the REAL DATA that we pass into
# the function call. 
# memory trick- if you make a REAL world argument with a person
# you need to come with REAL facts (data)
# check_Water_Depth(3) 

#  Return-this keyword allow us to pass date from INSIDE 1 function
# into another function 

def username(name):
    print ("what is your name?:")
    name = input()
    return name 

def confirmLogin():
    name = username("saleem")
    print ("this is the user:" + name)

    confirmLogin() 