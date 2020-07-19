import requests
import json
import secrets
import time
import threading

class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key 
        }
        self.data = self.get_data()

    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params= self.params)
        self.data = json.loads(response.text)
        return self.data

    def get_total_cases(self):
        data = self.data['total']

        for content in data:
            if content['name'] == 'Coronavirus Cases:':
                return content['value']
        return "0"
    
    def get_total_deaths(self):
        data = self.data['total']

        for content in data:
            if content['name'] == 'Deaths:':
                return content['value']
        return "0"
        
    def get_total_recovered(self):
        data = self.data['total']

        for content in data:
            if content['name'] == 'Recovered:':
                return content['value']
        return "0"
    
    def get_country_data(self, country):
        data = self.data['country']

        for content in data:
            if content['name'].lower() == country.lower():
                return content
        return "0"

    def get_country_dict(self):
        country_dict={}
        id = 0
        for country in self.data['country']:
            country_dict[id] = country['name']
            id+=1
        return country_dict

    def update_data(self): 
        requests.post('https://www.parsehub.com/api/v2/projects/{self.project_token}/run', params=self.api_key)
        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data=self.get_data()
                if old_data != new_data:
                    self.data = new_data
                    print("Data updated")
                    break
                time.sleep(5)

        t = threading.Thread(target=poll)
        t.start()


def main():
    user_input=None
    data = Data(secrets.API_KEY, secrets.PROJECT_TOKEN)

    while (user_input != 'E'):
        user_input = input(" A) View Total Cases \n B) View Total Deaths \n C) View Total Recoveries \n D)View Data per Country \n U)Update info \n E)Exit")
        if(user_input == "A"):
            print(data.get_total_cases())

        elif(user_input == "B"):
            print(data.get_total_deaths())

        elif(user_input == "C"):
            print(data.get_total_recovered())

        elif(user_input == "D"):

            country_ids= data.get_country_dict()

            print("Select country by ID")
            print(country_ids)
            country_id = input("ID: ")
            
            if int(country_id) in country_ids:
                print(data.get_country_data(country_ids[int(country_id)]))
            else:
                print("Inexistent key")


main()

