from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


# Это позволяет авторизироваться пользователю через email, а не никнейм
# Берем логику из под капота django
class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        
        # Делаем попытку найти пользователя по переданному email
        try:
            # Ищем пользователя с таким email
            # Далее если пароли совпадают - происходит авторизация
            user = user_model.objects.get(email=username)
            if user.check_password(password):
                return user
            
        except user_model.DoesNotExist:
            return None
        
        except user_model.MultipleObjectsReturned:
            return None
        
    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
        
        except user_model.MultipleObjectsReturned:
            return None