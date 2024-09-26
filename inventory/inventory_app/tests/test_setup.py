
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
User = get_user_model()


class TestSetup(APITestCase):
    def setUp(self):
        user_credentials = {
            "password": "password",
            "email" : "user1@gmail.com"
        }

        user = User.objects.create_user(**user_credentials)

        user_tokens = RefreshToken.for_user(user)
  
        self.user = "Bearer " + str(user_tokens.access_token)
        return super().setUp()