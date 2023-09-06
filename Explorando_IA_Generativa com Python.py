import pandas 
import requests
import json
import openai


openai_api_key = "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"
openai.api_key = openai_api_key

sdw2023_api_url = "https://sdw-2023-prd.up.railway.app"
df = pandas.read_csv(r"D:\Desenvolvimento\Python\trilha-python-dio\Explorando_IA_Generativa\Santander_Dev_Week.csv")
user_id = df['UserID'].to_list()

def get_user(id):
  response = requests.get(f"{sdw2023_api_url}/users/{id}")
  return response.json() if response.status_code ==200 else None

users =[user for id in user_id if (user := get_user(id)) is not None]

#print(json.dumps(users, indent=2))

def generate_api_news(user):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages= [
                {"role": "system", 
                 "content": "Você é um especialista em marketing."},
                {"role": "user", 
                 "content": f"Crie uma mensagem para o {user ['name']} sobre a importãncia dos investimentos (máximo de 90 caracteres)"
                 }
              ]
  )

  return completion.choices[0].message.content.strip('\"')

x = 0
for user in users:
    if x == 3: break #necessário por causa da limitação de consulta do ChatGpt para conta gratuíta
    news = generate_api_news(user)
    print(f"{user['id']} - {news}")
    x += 1

def update_user(user):
  response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
  return True if response.status_code ==200 else False

x = 0
for user in users:
   if x == 3: break #necessário por causa da limitação de consulta do ChatGpt para conta gratuíta
   success = update_user(user)
   print(f"User: {user['id']} - User: {user['name']} update? {success}")
   x +=1
