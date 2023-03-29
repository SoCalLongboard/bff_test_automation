# Standard library imports
from pprint import pprint

# 3rd party library imports
import pytest

# Project library imports
from lib.clients import (
    get_json,
    head,
    options,
)
from lib.core import get_user_store_user_for_username

pytestmark = [pytest.mark.user_store]

TEST_USERNAME = "frontend_test_service"


# Endpoint: /api/core/current-user [OPTIONS, HEAD, GET, PUT]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__core__current_user_options():
    verbs = options("/api/core/current-user", "OPTIONS, HEAD, GET, PUT")

    print(f"verbs supported for '/api/core/current-user' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.head()
def test__core__current_user_head():
    response = head("/api/core/current-user")

    pprint(response)


# @pytest.mark.isolate()
@pytest.mark.get()
def test__core__current_user_get():
    bff_user = get_json("/api/core/current-user")

    print("BFF-retrieved user:")
    pprint(bff_user)
    print()

    username = bff_user["username"]

    us_user = get_user_store_user_for_username(username)

    print("UserStore-retrieved user:")
    pprint(us_user)
    print()

    match_fields = [
        "currentFarmDefPath",
        "firstName",
        "lastName",
    ]
    for field in match_fields:
        assert bff_user[field] == us_user[field]
        print(f"Confirmed matching field: {field}")
    print()


# @pytest.mark.skip(
#     "This operation only supports changing the currentFarmDefPath field for the current user. "
#     "Using this may have very negative consequences for test automation in general."
# )
# # @pytest.mark.isolate()
# @pytest.mark.put()
# def test__core__current_user_put():
#     # First, get the current user via he plentyservice user-store client
#     user = user_store_client().get_user_by_api_key(environ["PLENTY_API_KEY"])
#     pprint(user)
#     print()
#
#     username = user["username"]
#     print(f"{username = }")
#     print()
#
#     # *** Implement this test when the operation supports less sensitive fields.


# Endpoint: /api/core/users [OPTIONS, HEAD, GET]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__core__users_options():
    verbs = options("/api/core/users", "OPTIONS, HEAD, GET")

    print(f"verbs supported for '/api/core/users' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.head()
def test__core__users_head():
    response = head("/api/core/users")

    pprint(response)


# @pytest.mark.isolate()
@pytest.mark.get()
def test__core__users_get():
    bff_users = get_json("/api/core/users")

    print("BFF-retrieved users:")
    pprint(bff_users)
    print()

    pprint(f"# of BFF users retrieved: {len(bff_users)}")
    print()

    # isolate a user
    bff_user = None
    for user in bff_users:
        if user["username"] == TEST_USERNAME:
            bff_user = user
            break

    # fail the test altogether if the target user cannot be located
    if not bff_user:
        print(f"Failed to find user: {TEST_USERNAME}")
        assert False

    us_user = get_user_store_user_for_username(TEST_USERNAME)

    print("UserStore-retrieved user:")
    pprint(us_user)
    print()

    match_fields = [
        "firstName",
        "lastName",
    ]
    for field in match_fields:
        assert bff_user[field] == us_user[field]
        print(f"Confirmed matching field: {field}")
    print()


# Endpoint: /api/core/users/<username> [OPTIONS, HEAD, GET]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__core__users__username_options():
    verbs = options(f"/api/core/users/{TEST_USERNAME}", "OPTIONS, HEAD, GET")

    print(f"verbs supported for '/api/core/users/[username]' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.head()
def test__core__users__username_head():
    response = head(f"/api/core/users/{TEST_USERNAME}")

    pprint(response)


# @pytest.mark.isolate()
@pytest.mark.get()
def test__core__users__username_get():
    bff_user = get_json(f"/api/core/users/{TEST_USERNAME}")

    print("BFF-retrieved user:")
    pprint(bff_user)
    print()

    us_user = get_user_store_user_for_username(TEST_USERNAME)

    print("UserStore-retrieved user:")
    pprint(us_user)
    print()

    match_fields = [
        "firstName",
        "lastName",
    ]
    for field in match_fields:
        assert bff_user[field] == us_user[field]
        print(f"Confirmed matching field: {field}")
    print()


# Endpoint: /login/magic-link/<token> [OPTIONS, HEAD, GET]
#
# Rather than individual tests, this is actually used implicitly
# in all BFF end-point interactions. The requests client engages
# the magic-link handshake to get credentials to navigate Sprout/BFF.
