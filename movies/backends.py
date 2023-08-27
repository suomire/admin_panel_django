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
            # отправка запроса с логином и паролем и получение аксес токена
            login_response = requests.post(url + "/auth/login", data=json.dumps(payload))
            access_token = login_response.json()
            # создание заголовка
            headers = {"Authorization": f"Bearer {access_token}"}
            # получение пользователя
            user_data_response = requests.get(url + "/auth/me", headers=headers)
            # проверка на ошибку
            user_data_response.raise_for_status()
            # подготовка json
            user = user_data_response.json()
            # подготовка user_id
            params = {"user_id": user.get("uuid")}
            # получение user_role по user_id
            user_role_response = requests.get(url + "/role/user", params=params, headers=headers)
            # проверка на ошибку
            user_role_response.raise_for_status()
            # подготовка json
            roles = user_role_response.json()
            # подготовка списка имен
            roles = [role.get("name") for role in roles]

        except:
            return None

        if user_data_response.status_code != http.HTTPStatus.OK:
            return None

        data = user_data_response.json()
        roles = user_role_response.json()

        try:
            user, created = User.objects.get_or_create(email=data['email'], )
            user.username = data.get('login')
            user.email = data.get('email')
            user.first_name = data.get('name')
            user.last_name = data.get('surname')
            user.is_superuser = 'super_user' in [role.get('name', None) for role in roles]
            user.is_active = data.get('is_active', True)
            user.save()
        except Exception as err:
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
