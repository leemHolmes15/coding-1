# Loop - a loop is a construct that repeats itself 
# in programming, a loop allows to repeat cod3 instructions 


# there are two type of loop: for  and while loop 

# While loop - a type of loop where so long as a conditions is equal 
# to true it will keep running forever 

# the keyword is while --> do while 

# syntax
# if/ else and while are all functions 
#if (2+2 == 4):
    # print("the program is running.. ")
    # num = int (input("please type in a number"))

# while loop will ALWAYS run unless change the condition!
# we can do this by writing instructions to manually 











def correct_password():  
    correctPassword= "leem123" 
    Attempts = 4
    print (" what is youe password ") 
    print (" please type in you password ")
    password =input("type in your password: ")
    while password !=correctPassword:
        print("Sorry wrong password try again")
        print(" try again")
        Attempts -= 4   
        print("you have this many attempts left: "+ str (Attempts))
        password = input("please type in your your password:")  
        print(" you have successfully logged in")
        
correct_password()
