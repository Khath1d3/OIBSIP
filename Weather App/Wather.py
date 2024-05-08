import requests

api_key='Add you API key'

city=input('Enter City: ')

weather_data=requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}')
wd=weather_data.json()

if wd['cod'] =='404':
    print('city not found')
else: 
    humidity=wd['main']['humidity']
    temp=wd['main']['temp']
    windspeed=wd['wind']['speed']
    cloud_cover=wd['weather'][0]['description']
    visibility=wd['visibility']

    print(f'The temperature of {city} is {temp} degrees with {cloud_cover} and {visibility} visibility\n')
    print(f'Also has humidity of {humidity}% and wind speed of {windspeed} mph\n')
