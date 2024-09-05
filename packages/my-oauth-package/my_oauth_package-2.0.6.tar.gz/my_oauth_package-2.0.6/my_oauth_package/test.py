import urllib.parse
import http.client
import base64
import hashlib
import os
import urllib.parse
from django.shortcuts import redirect
import json
import urllib.parse
import http.client
from django.http import HttpResponse
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

class AutherizationGrant:

    def setDecodedToken(self, decoded_token):
        self.token = decoded_token

    def getDecodedUserData(self):
        return self.token

    def __init__(self, client_id, client_secret, base_url, redirect_uri, certificate):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.redirect_uri = redirect_uri
        self.certificate = certificate

    def oauth_login(self, request):
        payload = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'email',
            'response_type': 'code',
            'state': 'axylkijhgfvbmx675756756'
        }
        query_string = urllib.parse.urlencode(payload)
        url = f"{self.base_url}?{query_string}"
        return redirect(url)

    def xecurify_callback(self, request):
        code = request.GET.get('code')

        if code:
            response_content = f"Authorization Code: {code}"
        else:
            response_content = "Missing authorization code or state parameter."

        conn = http.client.HTTPSConnection('v.xecurify.com')

        payload = urllib.parse.urlencode({
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'scope': 'email openid profile',
            'code': code
        })

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            conn.request('POST', '/moas/rest/oauth/token', body=payload, headers=headers)
            response = conn.getresponse()
            if response.status == 200:
                response_body = response.read().decode()
                result = json.loads(response_body)
            else:
                result = {'error': f"Failed with status code {response.status}"}

        except Exception as e:
            result = {'error': str(e)}

        finally:
            conn.close()

        token = result.get('id_token')

        certificate = self.certificate

        public_key = serialization.load_pem_public_key(certificate.encode(), backend=default_backend())

        try:
            decoded_token = jwt.decode(token, public_key, algorithms=["RS256"], audience=self.client_id, leeway=60)
            self.setDecodedToken(decoded_token)
            return HttpResponse(f"Token extracted successfully. Logged in {decoded_token}")


        except jwt.ExpiredSignatureError:
            return HttpResponse("Token expired")

        except jwt.InvalidTokenError:
            return HttpResponse("Invalid token")




class PasswordGrant:

    def setData(self, user_data):
        self.data = user_data

    def getUserData(self):
        return self.data

    def __init__(self, client_id, client_secret, username, password):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = 'v.xecurify.com'
        self.username = username
        self.password = password

    def get_access_token(self, request):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = urllib.parse.urlencode({
            'grant_type': 'password',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': self.password
        })
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        try:
            conn.request('POST', '/moas/rest/oauth/token', body=payload, headers=headers)
            response = conn.getresponse()
            if response.status == 200:
                response_body = response.read().decode()
                result = json.loads(response_body)
            else:
                result = {'error': f"Failed with status code {response.status}"}
        except Exception as e:
            result = {'error': str(e)}
        finally:
            conn.close()

        access_token = result.get('access_token')
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {'Authorization': f'Bearer {access_token}'}

        try:
            conn.request('GET', '/moas/rest/oauth/getuserinfo', headers=headers)
            response = conn.getresponse()
            response_body = response.read().decode()
            if response.status == 200:
                user_data = json.loads(response_body)
                self.setData(user_data)
                return HttpResponse(f"user_data {user_data}")
            else:
                return {'error': f"Failed with status code {response.status}"}
        except Exception as e:
            return {'error': str(e)}
        finally:
            conn.close()



class pkce:

    def __init__(self, client_id, client_secret, base_url, redirect_uri, certificate):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.redirect_uri = redirect_uri
        self.certificate = certificate

    def setDecodedToken(self, decoded_token):
        self.token = decoded_token

    #def getDecodedUserData(self):
    #    return self.token

    def generate_code_verifier(self):

        code_verify = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('ascii')
        return code_verify

    def generate_code_challenge(self, verifier):

        hashed = hashlib.sha256(verifier.encode('ascii')).digest()
        code_challenge = base64.urlsafe_b64encode(hashed).rstrip(b'=').decode('ascii')
        return code_challenge

    def pkce_login(self, request):
        code_verifier = self.generate_code_verifier()

        code_challenge = self.generate_code_challenge(code_verifier)




        payload = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'openid',
            'response_type': 'code',
            'state': 'axylkijhgfvbmx675756756',
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256'
        }
        query_string = urllib.parse.urlencode(payload)
        url = f"{self.base_url}?{query_string}"

        return redirect(url)


    def pkce_callback(self, request):
        code = request.GET.get('code')
        state = request.GET.get('state')
        code_verifier = request.get('code_verifier')

        if not code:
            return HttpResponse("Missing authorization code", status=400)
        if not state:
            return HttpResponse("Missing state parameter", status=400)
        if not code_verifier:
            return HttpResponse("Missing code verifier.", status=400)

        conn = http.client.HTTPSConnection('v.xecurify.com')
        payload = urllib.parse.urlencode({
            'grant_type': 'authorization_code',
            'client_id': 'w50QnzOOdrEVC0U',
            'client_secret': 'DSPl1edToL53oked4k6gI-4x1qY',
            'redirect_uri': self.redirect_uri,
            'code': code,
            'code_verifier': code_verifier
        })
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        try:
            conn.request('POST', '/moas/rest/oauth/token', body=payload, headers=headers)
            response = conn.getresponse()
            response_body = response.read().decode()
            result = json.loads(response_body)
            print(result)
            print("Got id token")
        except Exception as e:
            result = {'error': str(e)}
            print("Exception occurred")
        finally:
            conn.close()

        token = result.get('id_token')
        print(token)

        if not token:
            return HttpResponse("Missing token", status=400)

        certificate = self.certificate

        public_key = serialization.load_pem_public_key(certificate.encode(), backend=default_backend())

        try:
            decoded_token = jwt.decode(token, public_key, algorithms=["RS256"], audience=self.client_id, leeway=60)
            self.setDecodedToken(decoded_token)

            #self.getDecodedUserData()
            return HttpResponse(f"Token extracted successfully. Logged in {decoded_token}")

        except jwt.ExpiredSignatureError:
            return HttpResponse("Token expired")

        except jwt.InvalidTokenError:
            return HttpResponse("Invalid token")
