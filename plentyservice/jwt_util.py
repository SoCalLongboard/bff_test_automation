from cachetools import cached, TTLCache


@cached(cache=TTLCache(maxsize=1000, ttl=60 * 60 * 23.75))
def get_jwt_with_creds(__api_key, __api_secret):
    """
    Retrieves jwt token for plenty api key/secret pair
    Token expires in 24 hours, so we refresh earlier

    Args:
        __api_key(str): plenty api key
        __api_secret(str): plenty api secret

    Returns:
         (str) JWT token
    """
    import plentyservice

    client_builder = plentyservice.client_builder(api_key=__api_key, api_secret=__api_secret)
    user_store_client = client_builder.build_user_store_client()
    response = user_store_client.get_jwt()

    return response["jwt"] if "jwt" in response else None


def get_jwt():
    """
    Retrieves jwt token using Cfg - takes plenty api key/secret from environment variables

    Returns:
         (str): JWT token.
    """
    from plentyservice.common import Cfg

    return get_jwt_with_creds(Cfg.get_plenty_api_key(), Cfg.get_plenty_api_secret())
