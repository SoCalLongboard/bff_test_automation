""" Helper functions to do asserts in tests """

import json

from plentyservice import RequestError


def assert_json_error(err: RequestError, code: int, assert_msg: str = None) -> dict:
    """
    Extracts info from raised error, such json, status code and message,
    and compare to arguments `code` and `assert_msg`.

    @param err: raised client error
    @param code: HTTP status code
    @param assert_msg: is present, make sure that message is present in error description
    @return: parsed JSON as dict
    """
    assert err.err_code == code
    res = json.loads(err.message)
    err_msg = res.get("error", "")
    details_msg = res.get("details", "")
    if assert_msg:
        assert (
            assert_msg in err_msg or assert_msg in details_msg
        ), f'Message "{assert_msg}" not found in:\n\terror="{err_msg}"\n\tdetails="{details_msg}"'
    return res


def assert_dict_in(search_dict: dict, context: dict):
    """Asserts that `search_dict` presented in `context`."""
    found_dict = {k: context[k] for k in search_dict if k in context}
    assert search_dict == found_dict, f"Cannot find subdict: {search_dict}\nin: {context}"
