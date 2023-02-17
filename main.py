import requests
import jwt
import json
from time import time

api_key = 'YOUR API KEY'
api_secret = 'YOUR API SECRET KEY'
#user_id in this case is email
user_id = 'EMAIL'
JWT_token = 'YOUR JWT token'

# create a function to generate a token
# using the pyjwt library
def generateToken():
	token = jwt.encode(
 
		# Create a payload of the token containing
		# API Key & expiration time
		{'iss': api_key, 'exp': time() + 5000},
 
		# Secret used to generate token signature
		api_secret,
 
		# Specify the hashing alg
		algorithm='HS256'
	)

	return token
 

#download recording by id 
def downloadRecoding(meeting_id):
	headers = {'authorization': 'Bearer ' + generateToken(),
			   'content-type': 'application/json'}
	r = requests.get(
		f'https://api.zoom.us/v2/meetings/{meeting_id}/recordings',
		headers=headers)
	
	# Check the response status code
	if r.status_code != 200:
		raise ValueError(f'Ошибка: {r.status_code}')
	else:
		print(f'Успешный запрос на скачивание конференции {meeting_id}')
	
	print('Начинаем скачивание...')
	
	# Get the recording download URL
	#we choose first element of array 'recording_files' because second is audio-only 
	download_url = r.json()['recording_files'][0]['download_url']
	
	#adding jwt-token
	download_url = f'{download_url}?access_token={JWT_token}'

	topic = r.json()['topic']
	start_time = r.json()['start_time'].replace(':', '-')
	
	# Download the recording
	response = requests.get(download_url)

	#print(response.content)
	
	# Save the recording to a file
	with open(f'{topic} {start_time}.mp4', 'wb') as f:
		f.write(response.content)
			
	print('Скачивание завершено!')

	
def listAllRecordings():
	headers = {'authorization': 'Bearer ' + generateToken(),
			   'content-type': 'application/json'}
	r = requests.get(
		f'https://api.zoom.us/v2/users/{user_id}/recordings?from=2023-01-01',
		headers=headers)
	
	print(f'https://api.zoom.us/v2/users/{user_id}/recordings')
	
	# Check the response status code
	if r.status_code != 200:
		raise ValueError(f'Ошибка: {r.status_code}')
	else:
		print(f'Успешный запрос на просмотр записей пользователя {user_id}')

	print(r.json())
	
	
if __name__ == '__main__': 
	mi = input('Укажите ваш meeting_id: ').replace(' ', '')
	downloadRecoding(mi)
	
	#listAllRecordings()