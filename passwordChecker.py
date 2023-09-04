from getpass import GetPassWarning, getpass
import re

# it calculates how long does hacker need to brute force it (without having a wordlist)
def calculator(dict, n):
    #first 3 are avg speed of cracking hashesh on PC, the last one is from this article: https://thesecurityfactory.be/password-cracking-speed/
    #At a current rate of 25$ per hour, an AWS p3.16xlarge nets you a cracking power of 632GH/s (assuming we’re cracking NTLM hashes)
    avg = [500000, 1000000, 2000000, 632000000000]
    # special can be much higher than 14, i check that many special characters, but can be added more
    numbers={'small':26, 'big':26, 'num':10, 'special':14, 'length':0}
    pot = 0
    for item in dict:
        if dict[item]:
            pot+=numbers[item]

    for num in avg:
        time = pot ** n // num
        print(time)

        years = time // (60 * 60 * 24 * 365)
        time -= (years * 365 * 24 * 3600)
        
        days = time // (60 * 60 * 24)
        time -= (days * 3600 * 24)
        
        hours = time //  (3600)
        time -= hours*3600

        minutes = time //  60
        time -= minutes*60

        print(f'Avg cracking speed = {num}\nYour password would be cracked after:\n{years} years, {days} days, {hours} hours, {minutes} minutes and {time} seconds\n')

#this function prints what's missing in our passwords
def missing(dict):
   steps = {'small':'You forgot to add letter to your password', 'big':'You forgot to add LETTER to your password', 'num':'2 + 2 equals no number in you password', 'special':'There is something special in your password, it contains no special characters', 'length':'Your password length is as small as your ...'}

   for key in dict:
       if not dict[key]:
           print(steps[key])


score = 0
password = getpass()
whatsWrong={'small':False, 'big':False, 'num':False, 'special':False, 'length':False}

if re.search('[a-z]', password) != None: 
    score+=1
    whatsWrong['small']=True
if re.search('[A-Z]', password) != None: 
    score+=1
    whatsWrong['big']=True
if re.search('[0-9]', password) != None: 
    score+=1
    whatsWrong['num']=True
if re.search('[!@#$%^&*()_+-=]', password) != None: 
    score+=1
    whatsWrong['special']=True
if len(password) > 12: 
    score+=1
    whatsWrong['length']=True

print()
print('*'*40)
print()

if score == 5:
    print('Congrats, that is really strong password')
elif 3 <= score <= 4:
    print('Your password is good, but could be better')
elif 1 <= score <= 2:
    print('Your password suck')
else:
    print('Nice password, nobody would crack this password... Because it does not need cracking')

print()
print('*'*40)
print()

if 0 <= score <= 4:
    missing(whatsWrong)

print()
print('*'*40)
print()

yn = input('Do you want us to calculate how long does it take to crack your password? Assuming it is not from wordlist [y/n]').lower()
print()

if yn == 'y' or yn == 'yes':
    calculator(whatsWrong, len(password))

print()
print('*'*40)
print()
