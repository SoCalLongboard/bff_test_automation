#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains utilities for service endpoint authentication.
Requires the importer to have PLENTY API access tokens for the user
store in env vars.
"""

from functools import wraps

import base64


class Authorizer:
    def __init__(self, user_store_client):
        self.user_store_client = user_store_client
        self.api_key = None
        self.api_secret = None

    def check_credentials(self, resource, level):
        """Creates a decorator to check credentials at the specified level.
        Args:
            resource (str): The resource to check permission for.
            level (str): The level of credentials to check.
        Returns:
            (func): The decorator function.
        """

        def real_decorator(f):
            """Wraps a function with a check for API credentials.
            Args:
                f (func): The function to wrap with a credentials check.
            Returns:
                (func): The wrapped function.
            """

            @wraps(f)
            def wrapper(*args, **kwargs):
                """Checks the user's credentials, then calls f if appropriate.
                Returns:
                    (str): A fail message, or the result of calling f.
                """
                # Check if request has incoming HTTP Basic auth payload; an HTTP 'authorization' header
                # TODO replace all instances of 'request' below given the removal of Flask from this
                # stripped-down plentyservice
                http_authorization_header = request.headers.get("authorization", None)
                if http_authorization_header:
                    try:
                        api_key, api_secret = Authorizer.parse_auth_header(http_authorization_header)
                    except Exception:
                        # return exception in case HTTP Basic Auth values could not be extracted
                        return (
                            "Not able to determine username(apiKey)/password(apiSecret) in HTTP Basic Auth header",
                            400,
                        )
                else:
                    # api key and secret not found in HTTP Basic auth payload, try query parameters
                    api_key = request.args.get("apiKey", None)
                    api_secret = request.args.get("apiSecret", None)
                # Check if api_key and api_secret were provided as HTTP Basic auth payload or query parameters
                if api_key is None or api_secret is None:
                    return (
                        "Missing username(apiKey)/password(apiSecret) in HTTP Basic Auth header or apiKey and apiSecret query params",
                        401,
                    )
                allowed = self.user_store_client.check_key(api_key, api_secret, resource, level)["allowed"]
                self.api_key = api_key
                self.api_secret = api_secret
                if not allowed:
                    return "Unauthorized.", 403
                return f(*args, **kwargs)

            return wrapper

        return real_decorator

    @staticmethod
    def parse_auth_header(auth_header):
        """
        Extract the contents of the http_authorization header
        NOTE: Value is a base-64 encoded string
        e.g. Basic anpqTGlBU1pob0VoRjNl==

        Args:
            auth_header:

        Returns:
            (username, password) from auth header

        """
        auth_type, auth_values = auth_header.split()

        # Decode values in auth_values are in the form api_key:api_secret
        username, password = base64.b64decode(auth_values).decode().split(":")
        return username, password
