import os 

import requests
import time

FILE_NAME = 'lama_600px.png'

resp = requests.post('http://127.0.0.1:5000/upscale', json={
    'input_path': os.path.join('example', 'lama_300px.png'),
    'output_path': os.path.join('results', FILE_NAME)
})
resp_data = resp.json()
print(resp_data)
task_id = resp_data.get('task_id')

for _ in range(6): 
    resp = requests.get(f'http://127.0.0.1:5000/tasks/{task_id}', json={'filename': FILE_NAME})
    print(resp.json())
    time.sleep(3)