import urllib.parse
import http.client
import base64
import hashlib
import os

from django.shortcuts import redirect
import json
from django.http import HttpResponse
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import logging

#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Grant:

    def __init__(self, client_id, client_secret, base_url, redirect_uri, certificate, grant_type):
        self.token = None
        self.glo_code_verifier = None
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.redirect_uri = redirect_uri
        self.certificate = certificate
        self.grant_type = grant_type

    def set_decoded_token(self, decoded_token):
        logging.info("In set_decoded_token ")
        logging.info(decoded_token)
        self.token = decoded_token

    def get_decoded_userdata(self):
        logging.info("In get_decoded_userdata ")
        return self.token

    @staticmethod
    def generate_code_verifier():

        code_verify = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('ascii')
        logging.info("In generate_code_verifier " + code_verify)
        return code_verify

    @staticmethod
    def generate_code_challenge(verifier):

        hashed = hashlib.sha256(verifier.encode('ascii')).digest()
        logging.info("In generate_code_challenge hashing code_verifier ")
        code_challenge = base64.urlsafe_b64encode(hashed).rstrip(b'=').decode('ascii')
        logging.info("In generate_code_challenge code challenge generated")
        logging.info(code_challenge)
        return code_challenge

    def grant_redirect(self):

        logging.info("grant_type")
        logging.info(self.grant_type)
        self.glo_code_verifier = Grant.generate_code_verifier()
        logging.info("grant_redirect code_verifier ")
        logging.info(self.glo_code_verifier)
        code_challenge = Grant.generate_code_challenge(self.glo_code_verifier)
        logging.info("grant_redirect code_challenge ")
        logging.info(code_challenge)

        scope = None
        logging.info("grant_redirect scope ")
        response_type = None
        logging.info("grant_redirect response_type ")

        if self.grant_type == "Autherization_code":
            scope = 'email'
            response_type = 'code'
            logging.info("grant_redirect in if self.grant_type Autherization_code")

        if self.grant_type == "PKCE":
            scope = 'openid'
            response_type = 'code'
            logging.info("grant_redirect in if self.grant_type PKCE")

        if self.grant_type == "Implicit":
            scope = 'openid'
            response_type = 'token'
            logging.info("grant_redirect in if self.grant_type Implicit")

        payload = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': scope,
            'response_type': response_type,
            'state': 'axylkijhgfvbmx675756756',
        }

        logging.info("temp payload")
        logging.info(payload)

        if self.grant_type == "PKCE":
            keys = {
                'code_challenge': code_challenge,
                'code_challenge_method': 'S256',
            }
            payload.update(keys)
            logging.info("grant_redirect in if self.grant_type PKCE update payload")
            logging.info(payload)

        query_string = urllib.parse.urlencode(payload)
        logging.info("final payload ")
        logging.info(payload)
        url = f"{self.base_url}?{query_string}"
        logging.info("Created url ")
        logging.info(url)
        return redirect(url)

    def grant_callback(self, request):

        logging.info("grant_type")
        logging.info(self.grant_type)

        token = None
        code = request.GET.get('code')
        logging.info("grant_callback Got the auth code ")
        logging.info(code)
        if code:
            payload = None
            logging.info(payload)
            logging.info("grant_callback In xecurify_callback ")
            logging.info(code)

            if self.grant_type == "Autherization_code":
                logging.info("grant_callback in if self.grant_type Autherization code")
                payload = urllib.parse.urlencode({
                    'grant_type': 'authorization_code',
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'redirect_uri': self.redirect_uri,
                    'scope': 'email openid profile',
                    'code': code
                })
                logging.info("grant_callback payload")
                logging.info(payload)

            if self.grant_type == "PKCE":
                logging.info("grant_callback in if self.grant_type PKCE code")
                payload = urllib.parse.urlencode({
                    'grant_type': 'authorization_code',
                    'client_id': 'w50QnzOOdrEVC0U',
                    'client_secret': 'DSPl1edToL53oked4k6gI-4x1qY',
                    'redirect_uri': self.redirect_uri,
                    'code': code,
                    'code_verifier': self.glo_code_verifier
                })
                logging.info("grant_callback payload")
                logging.info(payload)

            conn = http.client.HTTPSConnection('v.xecurify.com')

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            logging.info("grant_callback going inside try")
            logging.info("printing payload")
            logging.info(payload)
            try:
                conn.request('POST', '/moas/rest/oauth/token', body=payload, headers=headers)
                response = conn.getresponse()
                if response.status == 200:
                    response_body = response.read().decode()
                    result = json.loads(response_body)
                    token = result.get('id_token')
                    logging.info("grant_callback got token")
                    logging.info(token)
                    logging.info("grant_callback if statement")
                else:
                    result = {'error': f"Failed with status code {response.status}"}
                    logging.info("grant_callback else statement")

            except Exception as e:
                result = {'error': str(e)}
                logging.info("grant_callback except statement")

            finally:
                conn.close()
                logging.info("grant_callback connection completed")
        else:
            token = request.GET.get('id_token')
            logging.info("grant_callback got id_token for implicit")
            logging.info(token)
            # decode



        certificate = self.certificate
        logging.info("certificate")
        logging.info(certificate)
        logging.info("token")
        logging.info(token)
        logging.info("self.client_id")
        logging.info(self.client_id)

        public_key = serialization.load_pem_public_key(certificate.encode(), backend=default_backend())

        try:
            decoded_token = jwt.decode(token, public_key, algorithms=["RS256"], audience=self.client_id, leeway=60)
            logging.info("got decoded_token")
            logging.info(decoded_token)
            logging.info("setting decoded_token so that i can access when ever i want")
            self.set_decoded_token(decoded_token)
            return HttpResponse(f"Token extracted successfully. Logged in {decoded_token}")


        except jwt.ExpiredSignatureError:
            logging.info("expire token ")
            return HttpResponse("Token expired")

        except jwt.InvalidTokenError:
            logging.info("Invalid token")
            return HttpResponse("Invalid token")



class PasswordGrant:

    def set_data(self, user_data):
        self.data = user_data

    def get_user_data(self):
        return self.data

    def __init__(self, client_id, client_secret, username, password):
        self.data = None
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
                self.set_data(user_data)
                return HttpResponse(f"user_data {user_data}")
            else:
                return {'error': f"Failed with status code {response.status}"}
        except Exception as e:
            return {'error': str(e)}
        finally:
            conn.close()
