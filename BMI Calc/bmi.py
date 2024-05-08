def category(w, h):
    bmi = w / h ** 2
    if bmi < 18.5:
        result= 'Underweight '
    elif 18.5 <= bmi < 25:
         result= 'Normal weight'
    elif 25 <= bmi < 30:
         result= 'Overweight'
    elif 30 <= bmi < 35:
         result= 'Obesity Class I (Moderate)'
    elif 35 <= bmi < 40:
         result= 'Obesity Class II (Severe)'
    else:
         result= 'Obesity Class III (Very severe or morbid)'
    return result +f' and your BMI is {round(bmi, 2)}'

print('Enter your weight and height below to determine your BMI category\n\n\n')

weight=input('What is your weight(kg)? ')
height=input('What is your height(m)? ')

print(f'\nYour Category Of Your BMI Scale is {category(float(weight),float(height))}')
