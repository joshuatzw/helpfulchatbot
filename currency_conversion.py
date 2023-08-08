import requests


LATEST_URL = "http://api.exchangeratesapi.io/v1/latest?access_key=3183adf49aab0569d718c7beb0c56a5d"
    

def currency_conversion():
    # Divide according to the current currency's exchange rate to get EUR value 
    # Multiply it by target currency rate 
    
    answer = requests.get(LATEST_URL)
    answer = answer.json()
    print(answer['rates']['SGD'])
    
currency_conversion()