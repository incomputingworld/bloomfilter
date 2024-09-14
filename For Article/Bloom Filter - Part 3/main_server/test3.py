import requests
import time
from bf.input_data import DC_characters1

count = 0


for index in range(0, len(DC_characters1)):
    character = f"{DC_characters1[index]}5128"
    endpoint = f"http://127.0.0.1:5000/new_user/{character}"
    print(endpoint)
    time.sleep(.1)
    result = requests.post(url=endpoint)
    print(result)
