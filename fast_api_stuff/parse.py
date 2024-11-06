import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Найти лица на изображении по пути
def detect_faces(file_with_faces):
    site = getenv('FACE_CLOUD_SITE')
    token = getenv('TOKEN')

    headers = {
        'Authorization': f'Bearer {token}', 
        'Content-Type': 'image/jpeg'
        }
    
    with open(file_with_faces, 'rb') as file:
        response = requests.post(
            f'{site}/api/v1/detect?demographics=true',
            headers=headers,
            data=file
        )

        try:
            data = response.json()
            print(data)
            return data
        except ValueError:
            print(response.text)
            return None

# Распарсить ответ
def faces_parse_unfold(data, name):
    code = data['status_code']
    if code != 200:
        return False
    
    datamain = data['data']
    
    res = {'name': name, 'faces': []}
    stat = {
        'faces_count': 0,
        'female_count': 0,
        'male_count': 0,
        'female_ages': 0.0,
        'male_ages': 0.0,
    }

    stat['female_ages'] = 0
    stat['male_ages'] = 0


    for d in datamain:
        u = unbox(d)
        
        stat['faces_count'] += 1
        if not 'gender' in u:
            continue

        if u['gender'] == 'male':
            stat['male_count'] += 1
            stat['male_ages'] += u['age']
        
        if u['gender'] == 'female':
            stat['female_count'] += 1
            stat['female_ages'] += u['age']
        
        res['faces'].append(u)
    
    if stat['female_count'] > 0:
        stat['female_ages'] /= stat['female_count']
    if stat['male_count'] > 0:
        stat['male_ages'] /= stat['male_count']
    
    return res, stat

# Получение данных лица
def unbox(item):
    if not 'bbox' in item or not 'demographics' in item:
        return {}
    return {
        'bbox': {
            'h': item['bbox']['height'],
            'w': item['bbox']['width'],
            'x': item['bbox']['x'],
            'y': item['bbox']['y'],
        },
        'age': item['demographics']['age']['mean'],
        'gender': item['demographics']['gender']
    }
