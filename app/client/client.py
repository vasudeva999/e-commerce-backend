import requests

query = '''
    mutation {
  auth(email:"vasudeva@gmail.com", password:"123"){
    accessToken
    refreshToken
    error
  }
}
'''

response = requests.post("http://127.0.0.1:5000/", params={'query': query})

print(response.text)
