import random
import string

symbols = ['!', '@', '#', '$', '%', '^', '&','+','_']

random_password = {
    'option1': list(string.ascii_uppercase) + list(string.digits),
    'option2': list(string.ascii_uppercase) + symbols,
    'option3': symbols + list(string.digits),
    'option4': list(string.ascii_uppercase) + symbols + list(string.digits)
}
print('\n\nYour can choose 4 options of the type of characters you want you password to contain')
print('\n\noption 1 is alphabets and and numebrs')
print('option 2 is alphabets and sybmbols')
print('option 3 is sybmbols and numbers')
print('option 4 is symbols,numbers and alphabets (everything combined)\n\n')

def ValidLength():
    while True:
        size = input('\nWhat length do you want your password to be: ')
        if size.isdigit() and int(size) > 0:
            return int(size)
        print("Please enter a valid positive integer for the password length.")
        continue

def ValidInput():
    while True:
        choice = input('\nEnter your choice (1, 2, 3, or 4): ')
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= 4:
                return choice
        print('Invalid input. Please enter a number between 1 and 4.')


while True:
    user_choice =ValidInput()
    length=ValidLength()

    print('\n')
    if user_choice==1:
        print(''.join(random.choices(random_password['option1'],k=length)))
    elif user_choice==2:
        print(''.join(random.choices(random_password['option2'],k=length)))
    elif user_choice==3:
        print(''.join(random.choices(random_password['option3'],k=length)))
    else :
        print(''.join(random.choices(random_password['option4'],k=length)))
    repeat=input('\nDo you want to regenerate: (y\\n) :')
    if repeat !='y':
        break
