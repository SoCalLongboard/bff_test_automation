"""Utilities for CLIs in general."""

import base64
import json
import os
import random
import time
from datetime import datetime

import requests
from cachetools import cached, TTLCache

from . import jwt_util
from .constants import *
from .request_error import RequestError

TIMEOUT_DEFAULT = 60
TOP_LEVEL_ARGS = [
    (["-v"], {"dest": "versions", "action": "store_true"}),
    (
        ["-l"],
        {
            "dest": "local",
            "action": "store_true",
            "help": "if the request should be made locally",
        },
    ),
    (["-p"], {"dest": "port", "help": "the port to use; ignored if not local"}),
    (
        ["-e", "--env"],
        {
            "dest": "environment_context",
            "help": "which environment to route to",
            "default": PROD,
            "choices": [PROD, STAGING, DEV] + list(ENV_ABBR_TO_ENV_MAP.keys()),
        },
    ),
]


class Cfg:
    """Bundle for configuration"""

    @staticmethod
    def get_plenty_api_key():
        return os.environ[PLENTY_API_KEY]

    @staticmethod
    def get_plenty_api_secret():
        return os.environ[PLENTY_API_SECRET]

    @staticmethod
    def url_override_is_present(service_name: str):
        return Cfg.get_url_override(service_name) is not None

    @staticmethod
    def get_url_override(service_name: str):
        override_url_key = service_name.upper().replace("-", "_") + URL_SUFFIX
        return os.environ.get(override_url_key)

    @staticmethod
    def get_environment_context():
        return os.environ[ENVIRONMENT_CONTEXT]

    @staticmethod
    def is_in_kubernetes():
        in_k8s_envar = os.environ.get(IN_KUBERNETES)
        return in_k8s_envar and in_k8s_envar.lower() == "true"

    @staticmethod
    def get_google_sheet_auth_from_env():
        return json.loads(os.environ[GOOGLE_SHEET_AUTH])

    @staticmethod
    def get_google_sheet_auth_from_file(path):
        with open(path, "r") as auth_file:
            return json.load(auth_file)

    @staticmethod
    def get_aws_access_key_id():
        return os.environ[AWS_ACCESS_KEY_ID]

    @staticmethod
    def get_aws_secret_access_key():
        return os.environ[AWS_SECRET_ACCESS_KEY]


def format_map(s, **kwargs):
    """Formats a string partially or completely according to some key-value
    pairs.

    Args:
        s (str): The string to format.
    Returns:
        (str): The formatted string.
    """
    for key, val in kwargs.items():
        s = s.replace("{" + key + "}", val)
    return s


def get_kubernetes_url(service_name: str):
    return f"http://{service_name}:8080"


def format_url(service_name: str, domain: str):
    return f"https://{service_name}.{domain}"


def get_service_url(service_name, environment_context=None, in_kubernetes=None):
    if Cfg.url_override_is_present(service_name):
        return Cfg.get_url_override(service_name)
    if in_kubernetes:
        return get_kubernetes_url(service_name)
    if not environment_context:
        environment_context = Cfg.get_environment_context()
    domain = get_domain_from_environment(environment_context)
    return format_url(service_name, domain)


def format_url_with_version(url: str, version: str):
    """
    Formats the full url of a service for a client
    e.g.
    https:/test-service.plenty.tools/api/v0
    """
    return f"{url}/api/{version}"


def get_domain_from_environment(environment_context):
    if environment_context not in ENV_TO_DOMAIN_MAP:
        raise ValueError(f"Could not handle environment_context {environment_context}")
    return ENV_TO_DOMAIN_MAP[environment_context]


def validate_update_content(content, fname):
    """Takes some content and the supposed filename for that content. If
    exactly one of the arguments is None, the method supplies the data--
    either by returning the content directly or extracting it from the file.

    Raises an exception otherwise because either no or duplicate data was
    supplied.

    Args:
        content (str): The content in question.
        fname (str): The filename in question.

    Returns:
        (str): The content, either directly from the content input or
            extracted from the file specified by fname.

    Raises:
        (AssertionError): In the case that no or duplicate data is supplied,
            this exception is thrown.
    """
    assert (content is None) ^ (fname is None), "Exactly one of file " "name and file content must be None."
    if content is not None:
        return content
    with open(fname) as fin:
        return json.load(fin)


def parse_utc_datetime(datetime_obj):
    # TODO check tzinfo and assert UTC timestamp
    return datetime.strftime(datetime_obj, "%Y-%m-%dT%H:%M:%S.%fZ")


def iso8601format(dt: datetime) -> str:
    return f"{dt.isoformat()}Z"


def fromiso8601format(dt_string: str) -> datetime:
    if not dt_string:
        return dt_string
    if dt_string.endswith("Z"):
        dt_string = dt_string[:-1]
    if "." in dt_string and len(dt_string.split(".")[1]) < 6:
        dt_string += "0" * (6 - len(dt_string.split(".")[1]))
    return datetime.fromisoformat(dt_string)


def str_to_json(value):
    if isinstance(value, str):
        return json.loads(value)
    return value


def filter_query_args(query_args: dict) -> dict:
    return {k: v for k, v in query_args.items() if v is not None}


class AuthenticatedServiceClient:
    """An authenticated client for a particular service."""

    def __init__(self, authenticated_client, service_url, http_basic_auth=False):
        """Create the authenticated service client.

        Args:
            authenticated_client (AuthenticatedClient): The root client.
            service_url (str): The URL of this particular service.
            http_basic_auth (bool): Force use of HTTP Basic auth to make request
            timeout (int): The timeout for all requests to this client.
        """
        self.__authenticated_client = authenticated_client
        self.__service_url = service_url
        self.__http_basic_auth = http_basic_auth

    def get(self, path_elems, query_args=None, additional_headers=None):
        """Make a GET against a specific URL with arguments.

        Args:
            path_elems (list | Object): Additional path parameters.
            query_args (dict): Query arguments to include.
            additional_headers (dict): additional headers to include with delete.
        Returns:
            (requests.Response): The REST response.
        """
        return self.__authenticated_client.make_request(
            requests.get,
            self.__service_url,
            path_elems,
            self.__http_basic_auth,
            query_args,
            req_json=None,
            files=None,
            additional_headers=additional_headers,
        )

    def post(self, path_elems, query_args=None, req_json=None, files=None, additional_headers=None):
        """Make a POST against a specific URL with arguments.

        Args:
            path_elems (list | Object): Additional path parameters.
            query_args (dict): Query arguments to include.
            req_json (dict): JSON to send in the request.
            additional_headers (dict): additional headers to include with post.
        Returns:
            (requests.Response): The REST response.
        """
        return self.__authenticated_client.make_request(
            requests.post,
            self.__service_url,
            path_elems,
            self.__http_basic_auth,
            query_args,
            req_json,
            files,
            additional_headers,
        )

    def put(self, path_elems, query_args=None, req_json=None, additional_headers=None):
        """Make a PUT against a specific URL with arguments.

        Args:
            path_elems (list | Object): Additional path parameters.
            query_args (dict): Query arguments to include.
            req_json (dict): JSON to send in the request.
            additional_headers (dict): additional headers to include with put.
        Returns:
            (requests.Response): The REST response.
        """
        return self.__authenticated_client.make_request(
            requests.put,
            self.__service_url,
            path_elems,
            self.__http_basic_auth,
            query_args,
            req_json,
            files=None,
            additional_headers=additional_headers,
        )

    def delete(self, path_elems, query_args=None, req_json=None, additional_headers=None):
        """Make a DELETE against a specific URL with arguments.

        Args:
            path_elems (list | Object): Additional path parameters.
            query_args (dict): Query arguments to include.
            req_json (dict): JSON to send in the request.
            additional_headers (dict): optional headers to include with delete.
        Returns:
            (requests.Response): The REST response.
        """
        return self.__authenticated_client.make_request(
            requests.delete,
            self.__service_url,
            path_elems,
            self.__http_basic_auth,
            query_args,
            req_json,
            files=None,
            additional_headers=additional_headers,
        )


class AuthenticatedClient:
    """Strategy for executing requests against services with credentials.

    Strategy for generating service URLs with query params (including those
    that supply credentails requried to authenticate a request) and executing
    requests against those urls.
    """

    @staticmethod
    def __make_full_url(service_url, path_elems):
        """Generates a URL path by combining the base URL elements given to this
        generator and any other path elements provided.

        Args:
            service_url (str): The service url for this  API.
            path_elems (list | Object): A list or individual object that will be
                converted to string(s) with str() and concatenated with the '/'
                separator.
        Returns:
            str: The generated URL.
        """
        if not isinstance(path_elems, list):
            path_elems = [path_elems]
        return "/".join([service_url] + [str(e) for e in path_elems])

    @staticmethod
    def __validate_should_retry(response):
        """Checks a response. Returns whether the request should be retried and
        raises an error if the request failed completely.

        Args:
            response (requests.models.Response): The response generated from a
                requests call.
        Returns:
            (bool): Whether the request should be retried.
        Raises:
            (RequestError): Raised if the request failed.
        """
        status_code = response.status_code

        if 200 <= status_code < 300:
            return False

        if status_code == 504:
            return True

        raise RequestError(response.text, status_code)

    def __init__(self, api_key, api_secret, timeout, use_jwt=False):
        """Create the authenticated client.

        Args:
            api_key (str): The API key.
            api_secret (str): The API secret.
        """
        self.__api_key = api_key
        self.__api_secret = api_secret
        self.__credentials_valid = api_key is not None and api_secret is not None
        self.__timeout = timeout
        self.__use_jwt = use_jwt

    def make_request(
        self,
        method_fn,
        service_url,
        path_elems,
        http_basic_auth,
        query_args,
        req_json,
        files=None,
        additional_headers=None,
    ):
        """Make an authenticated request against a specific URL with arguments.

        Args:
            method_fn (func): The REST method to use.
            service_url (str): The particular service's URL.
            path_elems (list | Object): Additional path parameters.
            http_basic_auth (bool) Force use of HTTP Basic auth to make request
            query_args (dict): Query arguments to include.
            req_json (dict): JSON to send in the request.
            additional_headers (dict): additional headers to send with the request.
        Returns:
            (requests.Response): The REST response.
        """
        url = self.__make_full_url(service_url, path_elems)

        params = self.__make_query_args(http_basic_auth, query_args)
        headers = self.__make_headers(http_basic_auth, additional_headers)
        timeout = self.__timeout if self.__timeout is not None else TIMEOUT_DEFAULT

        for _ in range(MAX_RETRIES + 1):
            response = method_fn(url, params=params, json=req_json, files=files, headers=headers, timeout=timeout)
            if not self.__validate_should_retry(response):
                return response
            time.sleep(random.uniform(0, 1))

        raise RuntimeError("Max retries exceeded")

    def __make_query_args(self, http_basic_auth, query_args):
        """Generates a dictionary of parameter arguments to supply to a requests
        call.

        Args:
            http_basic_auth (True | False): Whether to use HTTP Basic Auth,
                if False, include credentials as query parameters.
            query_args (dict): Other parameters to include. Defaults to None.
        Returns:
            (dict): The generated params, which can be supplied directly to a
                requests call with the 'params' keyword argument.
        """
        result = {} if query_args is None else query_args.copy()
        if http_basic_auth is False and self.__use_jwt is False:
            if not self.__credentials_valid:
                raise RuntimeError("Plenty API key/secret not loaded")
            # Legacy edge case for user_store_check_key PUP call
            if "user_store_check_key" in result:
                # Requesting api key/secret uses different query param names for this API end point
                # Do NOT overwrite apiSecret as it's always used as a query param
                # for purposes of the API call (check_key in user_store) itself, it's not used for request auth
                result["checkerApiKey"] = self.__api_key
                result["checkerApiSecret"] = self.__api_secret
            else:
                # Default, place api key/secret using default param names
                result["apiKey"] = self.__api_key
                result["apiSecret"] = self.__api_secret
        return result

    def __make_headers(self, http_auth, additional_headers=None):
        """Generate any required headers for requests.

        Args:
            http_auth (True | False): Whether to use HTTP Basic Auth,
                if True, include HTTP Basic Auth headers.
            additional_headers (dict): additional headers to send with the request.
        Returns:
            (dict): The generated params, which can be supplied directly to a
                requests call with the 'headers' keyword argument.
        """
        # Caller name defaults to API key if not explicitly provided
        caller_name = os.environ.get(SERVICE_NAME, self.__api_key)
        headers = {CALLER_HEADER: caller_name}
        if additional_headers is not None:
            headers.update(additional_headers)
        if http_auth and self.__use_jwt is False:
            self.apply_basic_auth_header(headers)
        elif self.__use_jwt:
            token = self.__get_jwt_token()
            if token is not None:
                headers["Authorization"] = "Bearer {}".format(token)
            else:
                self.apply_basic_auth_header(headers)

        return headers

    def apply_basic_auth_header(self, headers):
        base64_auth_string = base64.b64encode("{}:{}".format(self.__api_key, self.__api_secret).encode()).decode()
        headers["Authorization"] = "Basic {}".format(base64_auth_string)

    @cached(cache=TTLCache(maxsize=10, ttl=60 * 60 * 23))
    def __get_jwt_token(self):
        return jwt_util.get_jwt_with_creds(self.__api_key, self.__api_secret)


class CliContext:
    """Utilities for registering and running CLI operations."""

    def __init__(self, parser, top_subparsers):
        """Create the CLI context.

        Args:
            parser (argparse.parser): The top level parser.
            top_subparsers (argparse._SubParserActions): The top level
                subparsers.
        """
        self.__parser = parser
        self.__top_subparsers = top_subparsers
        self.__aliases = {}

    def add_subcommand(self, api_name, api_desc, alias, commands, gen_aliases):
        """Creates an argparse parser object based on the config objects
        provided. Alows simple heirarchical parsing of command line-style
        arguments.

        Args:
            api_name (str): The name of the file running the API.
            api_desc (str): The short-form name of the API.
            alias (str): The alias for this command.
            commands (dict): A dictionary of the form
                {str: (str, {str: (str, function, [([str], {str: str})])})}
                representing all of the information about the CLI API.
            gen_aliases (function): A function that maps strings to list of
                strings to provide aliases for commands and subcommands.
        Returns:
            (argparse.ArgumentParser): The parser created.
        """
        if alias in self.__aliases:
            raise RuntimeError("Repeat top-level alias '{}': {} and {}.".format(alias, self.__aliases[alias], api_name))
        s_aliases = {}
        for cmd, (_, subcmds) in commands.items():
            s_alias = gen_aliases(cmd, 1)
            if len(s_alias) != 1:
                raise RuntimeError("Alias list length is not 1.")
            s_alias0 = s_alias[0]
            if s_alias0 in s_aliases:
                raise RuntimeError(
                    "Repeat second-level alias '{} {}': {} and {}.".format(api_name, s_alias0, s_aliases[s_alias0], cmd)
                )
            s_aliases[s_alias0] = cmd
            ss_aliases = {}
            for subcmd, _ in subcmds.items():
                ss_alias = gen_aliases(subcmd, 2)
                if len(ss_alias) != 1:
                    raise RuntimeError("Alias list length is not 1.")
                ss_alias0 = ss_alias[0]
                if ss_alias0 in ss_aliases:
                    raise RuntimeError(
                        "Repeat third-level alias '{} {} {}': {} and {}.".format(
                            api_name, cmd, ss_alias0, ss_aliases[ss_alias0], subcmd
                        )
                    )
                ss_aliases[ss_alias0] = subcmd

        self.__aliases[alias] = api_name

        desc_1 = "A CLI for the {} API.".format(api_desc)
        epil_1 = "Run '{} [command] -h' for more information about a " "particular command.".format(api_name)
        epil_2 = "Run '{} {} [subcommand] -h' for more information about a " "particular subcommand."
        all_sp_kwargs = {
            "title": "{}commands",
            "description": "valid {}commands",
            "help": "each {}command accesses a different part of the API",
        }
        sp_kwargs = {k: v.format("") for k, v in all_sp_kwargs.items()}
        ssp_kwargs = {k: v.format("sub") for k, v in all_sp_kwargs.items()}

        parser = self.__top_subparsers.add_parser(name=api_name, aliases=[alias], description=desc_1, epilog=epil_1)

        subparsers = parser.add_subparsers(**sp_kwargs)

        for cmd, (desc, subcmds) in commands.items():
            subparser = subparsers.add_parser(
                cmd,
                aliases=gen_aliases(cmd, 1),
                description=desc,
                epilog=epil_2.format(api_name, cmd),
            )
            subsubparsers = subparser.add_subparsers(**ssp_kwargs)
            for subcmd, (subdesc, fn, subargs) in subcmds.items():
                subsubparser = subsubparsers.add_parser(subcmd, aliases=gen_aliases(subcmd, 2), description=subdesc)
                for arg in TOP_LEVEL_ARGS:
                    subsubparser.add_argument(*arg[0], **arg[1])
                for subarg, subkwarg in subargs:
                    subsubparser.add_argument(*subarg, **subkwarg)
                subsubparser.set_defaults(func=fn)

        return parser

    def execute_command(self, command):
        """Parses a supplied command and executes it.

        Args:
            command (list): A list of strings representing the different
                arguments supplied, by a command line or otherwise, to the CLI.

        Returns:
            (None): None.
        """
        args = self.__parser.parse_args(command)

        if "func" in args:
            fn = args.func
            vargs = vars(args)
            vargs.pop("func")
            for _, arg_info in TOP_LEVEL_ARGS:
                vargs.pop(arg_info["dest"])

            return fn(**vargs)
        else:
            self.__parser.print_help()
