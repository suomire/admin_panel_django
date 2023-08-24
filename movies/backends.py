import http
import json

import requests
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        url = settings.AUTH_API_LOGIN_URL
        payload = {'login': username, 'password': password}
        try:
            login_response = requests.post(url + "/login", data=json.dumps(payload))
            access_token = login_response.json()
            headers = {"Authorization": f"Bearer {access_token}"}
            user_data_response = requests.get(url + "/me", headers=headers)
            user_role_response = requests.get(url + "/role", headers=headers)
        except:
            return None
        
        if user_data_response.status_code != http.HTTPStatus.OK:
            return None

        data = user_data_response.json()
        roles = user_role_response.json()

        try:
            user, created = User.objects.get_or_create(id=data['id'],)
            user.login = data.get('login')
            user.email = data.get('email')
            user.name = data.get('name')
            user.surname = data.get('surname')
            user.is_admin = 'super_user' in roles
            user.is_active = data.get('is_active')
            user.save()
        except Exception:
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None