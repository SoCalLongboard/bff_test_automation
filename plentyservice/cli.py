#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The script to run to use the project as a CLI."""

import argparse
import json
import sys

from termcolor import colored

from . import clients, common
from .common import Cfg
from .builder import get_client_application_versions
from .request_error import RequestError
from .constants import *


def main():
    """The main method."""
    top_level_parser = argparse.ArgumentParser(add_help=False, usage=argparse.SUPPRESS)
    for arg in common.TOP_LEVEL_ARGS:
        top_level_parser.add_argument(*arg[0], **arg[1])
    args, other_args = top_level_parser.parse_known_args()

    if args.versions:
        print(json.dumps(get_client_application_versions(), indent=4))
        sys.exit(0)

    env_ctx = args.environment_context
    args.environment_context = ENV_ABBR_TO_ENV_MAP.get(env_ctx, env_ctx)

    override_url = None
    if args.local:
        port = args.port or LOCAL_DEFAULT_PORT
        override_url = f"{LOCAL_SCHEMA}://{LOCAL_BASE_DOMAIN}:{port}"

    parser = argparse.ArgumentParser()
    top_subparsers = parser.add_subparsers()

    root_client = common.AuthenticatedClient(Cfg.get_plenty_api_key(), Cfg.get_plenty_api_secret(), 60)
    cli_context = common.CliContext(parser, top_subparsers)
    for client in clients.CLIENTS:
        url = override_url or common.get_service_url(client.service_name(), args.environment_context, False)
        cli_context.add_subcommand(*client(root_client, url).build_cli_subcommand())

    try:
        result = cli_context.execute_command(other_args)
        if result is not None:
            print(json.dumps(result, indent=2))
        else:
            print(colored("Done", "green"))
    except RequestError as e:
        print(colored(e, "red"))


if __name__ == "__main__":
    main()
