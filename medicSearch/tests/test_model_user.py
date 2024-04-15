from django.test import TestCase 
from django.contrib.auth.models import User 

class UserModelTestClass(TestCase):
    def setUp(self):
        User.objects.create(username='test.unitario', password='123456') # Criando um usuário dentro do ambiente de teste

    def test_user_exist(self):
        user = User.objects.first() # Procurando um usuário dentro do base de dados criado para o teste
        self.assertIsNone(user)
