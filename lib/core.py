# Project library imports
from lib.clients import user_store_client


def get_user_store_user_for_username(username):
    user = user_store_client().get_user(username)

    return user
