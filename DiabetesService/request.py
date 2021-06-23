import requests
url = 'http://localhost:5000/api'
r = requests.post(url,json={'Pregnancies':0,
                            'Glucose':1.8,
                            'BloodPressure':1.8,
                            'SkinThickness':1.8,
                            'Insulin':1.8,
                            'BMI':1.8,
                            'DiabetesPedigreeFunction':1.8,
                            'Age':1.8,})
print(r.json())