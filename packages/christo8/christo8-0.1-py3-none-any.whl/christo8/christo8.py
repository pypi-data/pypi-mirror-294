def add(a,b):
    return a+b

def subtract(a,b):
    return a-b

def multiple(a,b):
    return a*b

def divide(a,b):
    return a/b

def area_of_triangle(a,b):
    return (a*b)/2

# Palindrome
def palindrome(a):
    x=a
    e=0
    while a:
        w=a%10
        e=e*10+w
        a=int(a/10)
    if(e==x):
        return "Palindrome"
    else:
        return "Not a Palindrome"
   
# Half_Pyramid 
def half_right_pyramid(n):
    for i in range (1,n+1):
        for j in range(1,i+1):
            print("*",end='')
        print()
  
# Half_left_pyramid      
def half_left_pyramid(n):
    for i in range (1,n+1):
        for j in range (1,n-i+1):
            print(" ",end='')
        for k in range (i):
            print("*",end='')
        print() 
   
# Full_pyramid     
def full_pyramid(n):
    for i in range (1,n+1):
        for j in range (1,n-i+1):
            print(" ",end='')
        for k in range (i):
            print(" *",end='')
        print()

# Inverted_full_pyramid
def inverted_full_pyramid(n):
    for i in range (1,n+1):
        for j in range(1,i):
            print(" ",end='')
        for k in range (1,n-i+2):
            print(" *",end='')
        print()

# Factorial
def factorial(a):
    result = 1
    for i in range(1,a+1):
        result*=i
    return result
 
# Swap       
def swap(a,b):
    c,a,b=a,b,a
    return(a,b)