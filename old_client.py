import requests
import json
import base64
# r = requests.get('http://localhost:5000/api/register')
# print("r", r.text)
# token_el = BeautifulSoup(r.json()['csrf_token'], 'html.parser')
# token_val = token_el.input.attrs['value']
# print("token_val", type(token_val))

# custom_header = {
# 	"X-CSRFToken": token_val
# }
p = requests.post('http://localhost:5000/api/login', data=dict({
	"username": 'admin',
	"password": 'admin'
}))
cookie = p.headers['Set-Cookie']

# logout = requests.post('http://localhost:5000/api/logout')
# print("logout", logout.text)


image = requests.get('http://127.0.0.1:5000/api/image-list/bicycle.png/download', headers={
	"Cookie": cookie
})

data = json.loads(image.text)
imgData = data['data']['img_content']
imgName = data['data']['img_name']
with open(imgName, 'wb') as f:
	f.write(imgData.encode('ISO-8859-1'))