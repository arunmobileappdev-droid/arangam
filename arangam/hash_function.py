from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

def hash_password(password):
    return make_password(password)


def verify_password(input_password, stored_password):
    return check_password(input_password, stored_password)


