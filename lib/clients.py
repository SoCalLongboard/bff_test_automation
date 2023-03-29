# Standard library imports
from os import environ
from pprint import pprint
import requests
from urllib.parse import urlparse, urlunparse

# Project library imports
from plentyservice import client_builder

DEBUG = False
FOUND_ENVARS = environ.keys()


def get_automation_username():
    # determine the user given the environment (implicit in client creation) and PLENTY_API_KEY value
    user = user_store_client().get_user_by_api_key(get_plenty_api_key())

    return user["username"]


def get_environment_context():
    return environ["ENVIRONMENT_CONTEXT"]


def get_plenty_api_key():
    if "BFF_PLENTY_API_KEY" in FOUND_ENVARS:
        return environ["BFF_PLENTY_API_KEY"]
    else:
        return environ["PLENTY_API_KEY"]


def get_plenty_api_secret():
    if "BFF_PLENTY_API_SECRET" in FOUND_ENVARS:
        return environ["BFF_PLENTY_API_SECRET"]
    else:
        return environ["PLENTY_API_SECRET"]


def get_sprout_root():
    # Ensure that the Sprout point-of-entry URL doesn't end with a slash
    return environ["BFF_ROOT"].rstrip("/")


# See footnote (1) for BFF inbound client authentication requirements
def get_bff_client_cookies():
    username = get_automation_username()

    # generate the magic_link URL (URL will be relative to prod environment)
    magic_link = user_store_client().create_magic_link_for_user(username)

    # tweak the magic_link URL to be environment-correct
    magic_link = adjust_magic_link_for_target_environment(magic_link)

    # GET the magic_link URL to get the goodies
    magic_link_response = requests.get(magic_link, allow_redirects=False)

    # return a RequestsCookieJar object
    return magic_link_response.cookies


# Magic links via plentyservice always return the prod link --
# cherry-pick the bits we like from the bff_root url and the magic_link url and
# build a contextually-correct magic_link url.
def adjust_magic_link_for_target_environment(magic_link_url):
    bff_root_url = get_sprout_root()

    # Split the contributing URLs into their components
    bff_root_parsed = urlparse(bff_root_url)
    magic_link_parsed = urlparse(magic_link_url)

    # Build the sequence to generate the environment-correct magic_link (2)
    new_url_parts = [
        bff_root_parsed.scheme,
        bff_root_parsed.netloc,
        magic_link_parsed.path,
        "",
        "",
        "",
    ]

    return urlunparse(new_url_parts)


# this is used to satisfy the need for a Referer (sic) header for BFF POST/PUSH/DELETE requests (1)
def get_referer_for_domain():
    referer = get_sprout_root()

    return referer


# ----- SPROUT / BFF requests -----
# OPTIONS
def options(path, expected_verbs=None):
    """
    This function checks the OPTIONS HTTP verb against the specified BFF endpoint,
    then confirms the expected verb set against the allowed verb set (with assertions).

    If expected_verbs are not passed, it is assumed that validation will be performed
    but the calling test function, not here.

    :param path: a BFF (Sprout server API) endpoint
    :type path: str

    :param expected_verbs: a string representing a list of HTTP verbs
    :type expected_verbs: str

    :return: a list of allowed verbs
    :rtype: list
    """

    response = requests.options(url=f"{get_sprout_root()}{path}")

    print(f"{response.status_code = }")
    print()

    allowed_verbs = response.headers["allow"].split(", ")

    if expected_verbs:
        for verb in expected_verbs.split(", "):
            assert verb in allowed_verbs
            print(f"Confirmed: {verb} in {allowed_verbs}")
    print()

    return allowed_verbs


# HEAD
def head(path, params=None):
    """
    This function performs a HEAD request against a BFF endpoint in the current environment
    then performs sanity checks (with assertions) against the returned header values.

    This function also authenticates itself to Sprout/BFF within the request by employing
    a cookie held by the client.

    :param path: a BFF (Sprout server API) endpoint
    :type path: str

    :param params: a dict of key/value pairs to resolve as a query string
    :type params: dict

    :return: a subset of header values
    :rtype: dict
    """

    bff_client_cookies = get_bff_client_cookies()

    response = requests.head(
        url=f"{get_sprout_root()}{path}",
        cookies=bff_client_cookies,
        params=params,
    )

    print(f"{response.status_code = }")
    print()

    assert response.status_code == 200
    print(f"Confirmed: response.status_code == 200")

    headers = response.headers
    content_type = headers["Content-Type"]
    assert content_type == "application/json"
    print("Confirmed: 'Content-Type' == 'application/json'")

    assert "Location" not in headers.keys()
    print("Confirmed: 'Location' not in response.headers.keys()")
    print()

    return {"headers": response.headers, "status_code": response.status_code}


# GET
def get_text(path, params=None):
    """
    This function performs a GET request against a BFF endpoint and returns the response text.
    It performs no validation unto itself -- it is expected that validation would be performed
    against the returned text.

    This function also authenticates itself to Sprout/BFF within the request by employing
    a cookie held by the client.

    :param path: a BFF (Sprout server API) endpoint
    :type path: str

    :param params: a dict of key/value pairs to resolve as a query string
    :type params: dict

    :return: response text
    :rtype: str
    """

    bff_client_cookies = get_bff_client_cookies()
    response = requests.get(
        url=f"{get_sprout_root()}{path}",
        cookies=bff_client_cookies,
        params=params,
    )

    print(f"{response.status_code = }")
    print()

    if DEBUG:
        print("GET response headers:")
        pprint(response.headers)
        print()

        print("GET response TEXT:")
        pprint(response.text)
        print()

    return response.text


def get_json(path, params=None):
    """
    This function performs a GET request against a BFF endpoint and returns the response JSON.
    It performs no validation unto itself -- it is expected that validation would be performed
    against the returned JSON.

    This function also authenticates itself to Sprout/BFF within the request by employing
    a cookie held by the client.

    :param path: a BFF (Sprout server API) endpoint
    :type path: str

    :param params: a dict of key/value pairs to resolve as a query string
    :type params: dict

    :return: response JSON
    :rtype: dict
    """

    bff_client_cookies = get_bff_client_cookies()

    print("Cookies:")
    pprint(bff_client_cookies.get_dict())
    print()

    response = requests.get(
        url=f"{get_sprout_root()}{path}",
        cookies=bff_client_cookies,
        params=params,
    )

    print(f"{response.status_code = }")
    print()

    if DEBUG:
        print("GET response headers:")
        pprint(response.headers)
        print()

        print("GET response JSON:")
        pprint(response.json())
        print()

    return response.json()


# PUT
def put(path, payload):
    """
    This function PUTs a JSON payload to a BFF endpoint and returns the response body in JSON.
    It will either alter an existing object in the target service or create a new object if
    a prior object does not exist.

    This function also authenticates itself to Sprout/BFF within the request by employing
    a cookie held by the client.

    :param path: a BFF (Sprout server API) endpoint
    :type path: str

    :param payload: the JSON representation of a Python object
    :type payload: json

    :return: JSON response
    :rtype: json
    """

    bff_client_cookies = get_bff_client_cookies()
    headers = {
        "Referer": get_referer_for_domain(),
        "x-csrftoken": bff_client_cookies["SPROUT_CSRF"],
    }

    print("Cookies:")
    pprint(bff_client_cookies.get_dict())
    print()

    print("Headers:")
    pprint(headers)
    print()

    response = requests.put(
        url=f"{get_sprout_root()}{path}",
        json=payload,
        cookies=bff_client_cookies,
        headers=headers,
    )

    print(f"{response.status_code = }")
    print()

    if DEBUG:
        print("PUT response headers:")
        pprint(response.headers)
        print()

        print("PUT response JSON:")
        pprint(response.json())
        print()

    return response.json()


# POST
def post(path, payload):
    """
    This function POSTs a JSON payload to a BFF endpoint and returns the response body in JSON.
    It will create or replace an object in the target service.

    This function also authenticates itself to Sprout/BFF within the request by employing
    a cookie held by the client.

    :param path: a BFF (Sprout server API) endpoint
    :type path: str

    :param payload: the JSON representation of a Python object
    :type payload: dict

    :return: JSON response
    :rtype: json
    """

    bff_client_cookies = get_bff_client_cookies()
    headers = {
        "Referer": get_referer_for_domain(),
        "x-csrftoken": bff_client_cookies["SPROUT_CSRF"],
    }

    print("Cookies:")
    pprint(bff_client_cookies.get_dict())
    print()

    print("Headers:")
    pprint(headers)
    print()

    response = requests.post(
        url=f"{get_sprout_root()}{path}",
        json=payload,
        cookies=bff_client_cookies,
        headers=headers,
    )

    print(f"{response.status_code = }")
    print()

    if DEBUG:
        print("POST response headers:")
        pprint(response.headers)
        print()

        print("POST response JSON:")
        pprint(response.json())
        print()

    return response.json()


# plentyservice clients
def device_management_service_client():
    return client_builder(
        api_key=get_plenty_api_key(),
        api_secret=get_plenty_api_secret(),
        environment_context=get_environment_context(),
    ).build_device_management_client()


def executive_service_client():
    return client_builder(
        api_key=get_plenty_api_key(),
        api_secret=get_plenty_api_secret(),
        environment_context=get_environment_context(),
    ).build_executive_service_client()


def farm_def_service_client():
    return client_builder(
        api_key=get_plenty_api_key(),
        api_secret=get_plenty_api_secret(),
        environment_context=get_environment_context(),
    ).build_farm_def_service_client()


def perception_object_service_client():
    return client_builder(
        api_key=get_plenty_api_key(),
        api_secret=get_plenty_api_secret(),
        environment_context=get_environment_context(),
    ).build_perception_object_service_client()


def product_quality_service_client():
    return client_builder(
        api_key=get_plenty_api_key(),
        api_secret=get_plenty_api_secret(),
        environment_context=get_environment_context(),
    ).build_product_quality_service_client()


def traceability_service_client():
    return client_builder(
        api_key=get_plenty_api_key(),
        api_secret=get_plenty_api_secret(),
        environment_context=get_environment_context(),
    ).build_traceability3_client()


def user_store_client():
    return client_builder(
        api_key=get_plenty_api_key(),
        api_secret=get_plenty_api_secret(),
        environment_context=get_environment_context(),
    ).build_user_store_client()


def workbin_service_client():
    return client_builder(
        api_key=get_plenty_api_key(),
        api_secret=get_plenty_api_secret(),
        environment_context=get_environment_context(),
    ).build_workbin_service_client()


# Footnotes:
#
# (1)   Cookies/headers for Sprout BFF GET, POST, and PUT requests
#       https://plentyag.atlassian.net/wiki/spaces/EN/pages/2180678132/Using+Postman+against+Sprout+REST+APIs
#
# (2)   Building a url from parts
#       https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlunparse
