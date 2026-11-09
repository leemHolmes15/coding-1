# FUNCTION  are simple put a code block of instructions for
# computers to follow 

# built- in functions- a code black of
# instructions for a computer to follow 
# that was already written for us
# PRE WRITTEN CODE INSTRUCTIONS 

# input() - a built in function that allows us
# to print date in terminal.

name = input("what is your name? ")

# Date casting functions
# these are bulit in (pre written) functions 
# that change date types from one form into another





foodItem_1 = "apple"

groceryList = ["apples", "oranges","water","chips","ground beef"]

print(groceryList)

for i in groceryList:
    print("I need to buy " + i)

grades = [100, 98, 75, 77, 89, 80]

for grade in grades:
    # Show me the grades lower than 85
    if grade < 85:
        print(grade)

# we can include multiple data types in a list, including
# variable and other lists
fighter_A= ["Johnny Bravo", 100, 50]
fighter_B= ["Dexter Lab", 120, 40]

fighters = [fighter_B, fighter_A]

for fighterName in fighters:
    print("name of fighters: " +str(fighterName[0]))
    print("health of fighters: " +str(fighterName[1]))

    # list are usually used to keep track of date that can be 
    # pull