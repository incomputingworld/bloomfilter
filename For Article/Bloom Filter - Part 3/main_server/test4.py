import random
import requests
import time
from bf.input_data import DC_characters1

count = 0

suffix = ['3322', '1199', '21098', '5128']
for index in range(0, len(DC_characters1)):
    index = random.randrange(0, len(suffix))
    character = f"{DC_characters1[index]}{suffix[index]}"
    endpoint = f"http://127.0.0.1:5000/new_user/{character}"
    print(endpoint)
    time.sleep(1)
    result = requests.post(url=endpoint)
    print(result)
