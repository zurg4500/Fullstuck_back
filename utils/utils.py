from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken


def now():
    return datetime.now().strftime("-%d-%m-%Y-%H-%M-%S")


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
