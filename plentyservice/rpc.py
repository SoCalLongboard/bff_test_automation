import os

import requests
from plentyservice.constants import *
from .common import Cfg

IGNITION_API_BASE_URL = "https://ignitionapiservicedev.ocimum-basilicum-5.com/api/v0"


class RpcError(RuntimeError):
    def __init__(self, message, err_code):
        super(RuntimeError, self).__init__(message)
        self.message = message
        self.err_code = err_code

    def __str__(self):
        return str(self.err_code) + ": " + str(self.message)


def _rpc_call_wrapper(client_name, meth_name, poss_args, auth_dict):
    req_args = set([e["name"] for e in poss_args if "default" not in e])
    query_url = IGNITION_API_BASE_URL + "/rpc/cli/" + client_name + "/" + meth_name

    def rpc_call(*args, **kwargs):
        if args:
            raise RpcError("All args must be provided as keyword args", 400)

        provided_arg_names = set(kwargs.keys())
        missing_args = req_args - provided_arg_names
        if missing_args:
            raise RpcError('Missing args: "' + '", "'.join(missing_args) + '"', 400)

        extra_args = provided_arg_names - set([e["name"] for e in poss_args])
        if extra_args:
            raise RpcError('Extra args: "' + '", "'.join(extra_args) + '"', 400)

        json_res = requests.post(query_url, params=auth_dict, json={"args": kwargs}).json()

        code, result = json_res["statusCode"], json_res["result"]
        if code != 200:
            raise RpcError(result, code)
        return result

    return rpc_call


class _Client:
    def __init__(self, client_name, client_fns, auth_str):
        for meth_name, meth_args in client_fns.items():
            setattr(
                self,
                meth_name,
                _rpc_call_wrapper(client_name, meth_name, meth_args, auth_str),
            )


class Cli:
    def __init__(self):
        auth_dict = {
            "apiKey": Cfg.get_plenty_api_key(),
            "apiSecret": Cfg.get_plenty_api_secret(),
        }

        res = requests.get(IGNITION_API_BASE_URL + "/rpc/cli-options", params=auth_dict)
        if res.status_code != 200:
            raise RpcError(res.text, res.status_code)
        json_res = res.json()

        clients = json_res["clients"]
        for client_name, client_fns in clients.items():
            setattr(self, client_name, _Client(client_name, client_fns, auth_dict))


try:
    cli = Cli()
except RpcError:
    cli = None
