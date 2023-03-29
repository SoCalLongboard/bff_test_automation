"""This module implements methods which interact the web API for the Plenty
user store."""

from ..base_client import BaseClient
from ..common import (
    validate_update_content,
    AuthenticatedServiceClient,
    format_url_with_version,
)


class UserStoreClient(BaseClient):
    """Client communicating with the Plenty user store via REST."""

    _application_name = "User Store"
    _service_name = "userstore"
    _api_version = "v0"

    @staticmethod
    def application_name():
        """Get the application name of the service.

        Returns:
            (str): The application name of the service.
        """
        return UserStoreClient._application_name

    @staticmethod
    def service_name():
        """Get the name of the service.

        Returns:
            (str): The name of the service.
        """
        return UserStoreClient._service_name

    @staticmethod
    def api_version():
        """Get the api version of this client to service.

        Returns:
            (str): The api version of this client.
        """
        return UserStoreClient._api_version

    def __init__(self, authenticated_client, url):
        """Create a new traceability store client.

                Args:
                    authenticated_client (common.AuthenticatedClient): Plenty service
                        client that has credentials.
                    url (str): The url to use for the client.
        format_url_with_version
        """

        self.__service_client = AuthenticatedServiceClient(
            authenticated_client, format_url_with_version(url, self.api_version())
        )

    def build_commands(self):
        """Builds the commands for this client.

        Returns:
            ({str: (str,{str: str})}): The commands for the client.
        """
        api_key_arg = ["api_key"], {"help": "a device management API key file"}
        api_secret_arg = (
            ["api_secret"],
            {"help": "a device management API secret key file"},
        )
        username_arg = ["username"], {"help": "the user's username"}
        user_arg = ["user_fname"], {"help": "a file specifying a user in JSON format"}
        is_human_arg = (
            ["-n"],
            {
                "dest": "is_human",
                "action": "store_false",
                "help": "whether the user is human",
            },
        )
        password_arg = ["password"], {"help": "the user's password"}
        old_pw_arg = ["old_password"], {"help": "the user's old password"}
        new_pw_arg = ["new_password"], {"help": "the user's new password"}
        role_arg = ["role"], {"help": "the name of the role"}
        resource_arg = ["resource"], {"help": "the resource in question"}
        level_arg = ["level"], {"help": "the level of API access"}
        permissions_arg = (
            ["permissions"],
            {
                "nargs": "*",
                "help": "pairs of permissions to add to the role",
            },
        )
        start_dt_arg = ["start_datetime"], {"help": "the start datetime of the query"}
        end_dt_arg = ["end_datetime"], {"help": "the end datetime of the query"}
        pretty_arg = (
            ["-n"],
            {
                "dest": "pretty",
                "action": "store_true",
                "help": "whether to print the key and secret in pretty form",
            },
        )

        return {
            "user": (
                "Manage users.",
                {
                    "list": ("List all users.", self.list_users, []),
                    "get": ("Get info about a user.", self.get_user, [username_arg]),
                    "update": (
                        "Update or create a user.",
                        self.update_user,
                        [username_arg, user_arg],
                    ),
                    "human": (
                        "Update whether the user is human.",
                        self.update_user_is_human,
                        [username_arg, is_human_arg],
                    ),
                    "delete": ("Delete a user.", self.delete_user, [username_arg]),
                    "service": (
                        "List all service users and their resources.",
                        self.get_service_users_and_resources,
                        [],
                    ),
                    "permission_check": (
                        "Get users' permission level for a resource",
                        self.get_user_permission_level,
                        [username_arg, resource_arg],
                    ),
                    "access_list": (
                        "Get all user resource/permissions",
                        self.get_user_all_permissions,
                        [username_arg],
                    ),
                    "magic_link": (
                        "Create magic link for the given user",
                        self.create_magic_link_for_user,
                        [username_arg],
                    ),
                },
            ),
            "password": (
                "Manage passwords.",
                {
                    "validate": (
                        "Check if a password is correct.",
                        self.check_password,
                        [username_arg, password_arg],
                    ),
                    "change_own": (
                        "Change a user's own password.",
                        self.update_own_password,
                        [username_arg, old_pw_arg, new_pw_arg],
                    ),
                    "edit_other": (
                        "Edit a different user's password.",
                        self.update_other_password,
                        [username_arg, new_pw_arg],
                    ),
                    "set_other_must_change": (
                        "Edit a different user's password, forcing them to change again immediately.",
                        self.update_other_password_must_change,
                        [username_arg, new_pw_arg],
                    ),
                    "disable": (
                        "Disable a user's password.",
                        self.disable_password,
                        [username_arg],
                    ),
                },
            ),
            "role": (
                "Manage roles.",
                {
                    "list": ("List all roles.", self.list_roles, []),
                    "get": ("Get info about a role.", self.get_role, [role_arg]),
                    "create": (
                        "Create or update a role.",
                        self.create_or_update_role,
                        [role_arg, permissions_arg],
                    ),
                    "update": (
                        "Create or update a role.",
                        self.create_or_update_role,
                        [role_arg, permissions_arg],
                    ),
                    "delete": ("Delete a role.", self.delete_role, [role_arg]),
                    "assign": (
                        "Assign a role to a user.",
                        self.assign_role,
                        [role_arg, username_arg],
                    ),
                    "remove": (
                        "Unassign a role to a user.",
                        self.unassign_role,
                        [role_arg, username_arg],
                    ),
                },
            ),
            "key": (
                "Manage API keys.",
                {
                    "check": (
                        "Check if an API key provides a given level of access.",
                        self.check_key,
                        [api_key_arg, api_secret_arg, resource_arg, level_arg],
                    ),
                    "generate": (
                        "Generate an API key.",
                        self.generate_key,
                        [username_arg, pretty_arg],
                    ),
                    "disable": (
                        "Disable an API key.",
                        self.disable_key,
                        [username_arg],
                    ),
                    "user": (
                        "Get a user by API key.",
                        self.get_user_by_api_key,
                        [api_key_arg],
                    ),
                    "rotate": (
                        "Rotate a user's API key.",
                        self.rotate_key,
                        [username_arg],
                    ),
                    "backup_disable": (
                        "Disable a backup API key.",
                        self.disable_backup_key,
                        [username_arg],
                    ),
                    "list_rotate": (
                        "List the users that need to manually rotate their keys.",
                        self.get_list_to_rotate,
                        [],
                    ),
                    "set_must_rotate": (
                        "Resets the user's time to rotate keys.",
                        self.set_must_rotate_api_key,
                        [username_arg],
                    ),
                    "auth_logs": (
                        "Gets the bulk auth check logs.",
                        self.get_bulk_auth_check_logs,
                        [start_dt_arg, end_dt_arg],
                    ),
                },
            ),
        }

    def build_cli_subcommand(self):
        """Bulid the CLI subcommand for this client.

        Returns:
            ((str, str, str, ({str: (str,{str: str})}), func)): Everything
                needed for a CLI subcommand.
        """
        return (
            "user_store",
            "user store client",
            "u",
            self.build_commands(),
            lambda s, _: [s[0]],
        )

    def get_jwt_token(self):
        """Gets from the /jwt endpoint a list of all users.

        Returns:
            (string): Jwt token for current user
        """
        return self.__service_client.get(["jwt"]).json()

    def get_jwks_keys(self):
        """Gets from the /jwks endpoint a list jwks keys.

        Returns:
            (list): A list of jwks keys
        """
        return self.__service_client.get(["jwks"]).json()

    def list_users(self):
        """Gets from the /users endpoint a list of all users.

        Returns:
            (list): A list of all users.
        """
        return self.__service_client.get(["users"]).json()

    def get_user(self, username):
        """Gets from the /user/{username} endpoint a particular user.

        Args:
            username (str): The username of the user being requested.

        Returns:
            (dict): The user requested.
        """
        return self.__service_client.get(["user", username]).json()

    def update_user(self, username, user=None, user_fname=None):
        """Puts to the /user/{username} endpoint to create or update a user.

        Args:
            username (str): The username of the user being updated.
            user (str, optional): A formatted string with the user's
                information. Defaults to None. Either this or user_fname must be
                None.
            user_fname (str, optional): The filename of the file contatining the
                user's information. Defaults to None. Either this or user must
                be None.

        Returns:
            (dict): The updated user.
        """
        user = validate_update_content(user, user_fname)
        return self.__service_client.put(["user", username], req_json=user)

    def update_user_is_human(self, username, is_human):
        """Puts to the user/{username}/update-is-human endpoint to update
        whether a user is human.

        Args:
            username (str): The username of the user being updated.
            is_human (bool): Whether the user is human.
        """
        self.__service_client.put(
            ["user", username, "update-is-human"],
            query_args={"isHuman": str(is_human).lower()},
        )

    def delete_user(self, username):
        """Deletes from the /user/{username} endpoint a particular user.

        Args:
            username (str): The username of the user being updated.

        Returns:
            (None): None.
        """
        self.__service_client.delete(["user", username])

    def check_password(self, username, password):
        """Gets from /user/{username}/check_password to check if a password is
        valid.

        Args:
            username (str): The username of the user in question.
            password (str): The password to validate.

        Returns:
            (dict): A dictionary with a boolean property indiating the
                password's validity.
        """
        return self.__service_client.get(["user", username, "check_password"], query_args={"password": password}).json()

    def update_own_password(self, username, old_password, new_password):
        """Puts to the /user/{username}/update_own_password endpoint a new
        password or a user's own password.

        Args:
            username (str): The username of the user in question.
            old_password (str): The user's old password.
            new_password (str): The user's new password.

        Returns:
            (None): None.
        """
        params = {"oldPassword": old_password, "newPassword": new_password}
        self.__service_client.put(
            ["user", username, "update_own_password"],
            query_args=params,
        )

    def update_other_password(self, username, new_password):
        """Puts to the /user/{username}/update_other_password endpoint a new
        password for a different user's password.

        Args:
            username (str): The username of the user in question.
            new_password (str): The user's new password.

        Returns:
            (None): None.
        """
        self.__service_client.put(
            ["user", username, "update_other_password"],
            query_args={"password": new_password},
        )

    def update_other_password_must_change(self, username, new_password):
        """Puts to the /user/{username}/update_other_password_must_change
        endpoint a new password for a different user's password, forcing them
        to change immediately.

        Args:
            username (str): The username of the user in question.
            new_password (str): The user's new password.

        Returns:
            (None): None.
        """
        self.__service_client.put(
            ["user", username, "update_other_password_must_change"],
            query_args={"password": new_password},
        )

    def disable_password(self, username):
        """Puts to the /user/{username}/disable_password endpoint to disable a
        different user's password.

        Args:
            username (str): The username of the user in question.

        Returns:
            (None): None.
        """
        self.__service_client.post(["user", username, "disable_password"])

    def get_user_permission_level(self, username, resource):
        """Gets from the /user/{username}/permissions/{resource} endpoint to
        get the permission level of a user for a given resource

        Args:
            username (str): The username of the user in question.
            resource (str): The resource to get the permission level for

        Returns:
            (None): None.
        """
        return self.__service_client.get(["user", username, "permissions", resource]).json()

    def get_user_all_permissions(self, username):
        """Gets from the /user/{username}/permissions endpoint to
        get a map of all the resources and permission levels a user has

        Args:
            username (str): The username of the user in question.

        Returns:
            (dict): resource key to permission information dict
        """
        return self.__service_client.get(["user", username, "permissions"]).json()

    def get_service_users_and_resources(self):
        """Gets from the /service-users endpoint all of the service users and
        their associated resources.

        Returns:
            (dict): The service users.
        """
        return self.__service_client.get(["service-users"]).json()

    def list_roles(self):
        """Gets from the /roles endpoint a list of all roles.

        Returns:
            (list): A list of all roles.
        """
        return self.__service_client.get(["roles"]).json()

    def get_jwks(self):
        """Gets from the /jwks endpoint a set of public keys.

        Returns:
            (list): A list of jwk public keys
        """
        return self.__service_client.get(["jwks"]).json()

    def get_jwt(self):
        """Gets from the /jwt endpoint a jwt token

        Returns:
            (dict): A jwt token
        """
        return self.__service_client.get(["jwt"]).json()

    def get_role(self, role):
        """Gets from the /role/{roleName} endpoint a particular role.

        Args:
            role (str): The name of the role being requested.

        Returns:
            (dict): The role requested.
        """
        return self.__service_client.get(["role", role]).json()

    def create_or_update_role(self, role, permissions):
        """Puts to the /role/{roleName} endpoint an newly created role.

        Args:
            role (str): The name of the role to be created.
            permissions (list): List of pairs of permissions to add to the role.

        Returns:
            (None): None.
        """
        assert len(permissions) % 2 == 0, "Permissions must be alternating resource and levels."
        j_body = {
            "name": role,
            "permissions": {k: v for k, v in zip(*[iter(permissions)] * 2)},
        }
        print(j_body)
        self.__service_client.put(["role", role], req_json=j_body)

    def delete_role(self, role):
        """Deletes from the /role/{roleName} endpoint a particular role.

        Args:
            role (str): The name of the role being deleted.

        Returns:
            (None): None.
        """
        self.__service_client.delete(["role", role])

    def assign_role(self, role, username):
        """Posts to /role/{roleName}/assign a username that this role should be
        applied to.

        Args:
            role (str): The role to apply to a user.
            username (str): The username of the user being updated.

        Returns:
            (None): None.
        """
        self.__service_client.post(["role", role, "assign"], query_args={"username": username})

    def unassign_role(self, role, username):
        """Posts to /role/{roleName}/unassign a username that this role should
        be removed from.

        Args:
            role (str): The role to be removed from a user.
            username (str): The username of the user being updated.

        Returns:
            (None): None.
        """
        self.__service_client.post(["role", role, "unassign"], query_args={"username": username})

    def check_key(self, api_key, api_secret, resource, level):
        """Gets from the /apikey/key/(apiKey}/check endpoint whether a given key
        allows access to a resource at a certain level.

        Args:
            api_key (str): The API key to check.
            api_secret (str): The API secret to check.
            resource (str): The resource the key may have access to.
            level (str): The level of access the key may grant to the resource.

        Returns:
            (dict): A dictionary with a boolean property indiating the key's
                validity.
        """
        return self.__service_client.get(
            ["apikey/key", api_key, "check"],
            query_args={"resource": resource, "level": level, "apiSecret": api_secret, "user_store_check_key": True},
        ).json()

    def generate_key(self, username, pretty):
        """Posts to the /apikey/user/{username}/generate endpoint to generate a
        key for the supplied user.

        Args:
            username (str): The name of the user to generate a key for.

        Returns:
            (dict): A dictionary with a properties for the API key and API
                secret key.
        """
        res = self.__service_client.post(["apikey/user", username, "generate"]).json()
        if pretty:
            api_key, api_secret = res["apiKey"], res["apiSecret"]
            print(f"PLENTY_API_KEY={api_key}\nPLENTY_API_SECRET={api_secret}")
            return
        return res

    def disable_key(self, username):
        """Posts to the /apikey/user/{username}/disable endpoint to disable a
        key for the supplied user.

        Args:
            username (str): The name of the user to generate a key for.

        Returns:
            (None): None.
        """
        self.__service_client.delete(["apikey/user", username])

    def get_user_by_api_key(self, api_key):
        """Gets from the /apikey/key/{targetApiKey} endpoint to get a user by
        api key.

        Args:
            api_key (str): The api key of the user being requested.

        Returns:
            (dict): The user requested.
        """
        return self.__service_client.get(["apikey/key", api_key]).json()

    def rotate_key(self, username):
        """Posts to the /apikey/user/{username}/rotate endpoint to rotate the
        API key and secret for the supplied user.

        Args:
            username (str): The name of the user to rotate the key for.
        Returns:
            (dict): A dictionary with a properties for the new API key and API
                secret key.
        """
        return self.__service_client.post(["apikey/user", username, "rotate"])

    def disable_backup_key(self, username):
        """Posts to /backupapikey/user/{username}/disable to disable the backup
        api key.

        Args:
            username (str): The name of the user to disable the backup API key
                for.
        Returns:
            (None): None.
        """
        self.__service_client.delete(["backupapikey/user", username])

    def get_list_to_rotate(self):
        """Gets from /userstorotate and returns the list of users that need to
        manually rotate their API key.

        Returns:
            (list): List of users that need to manually rotate API keys.
        """
        return self.__service_client.get(["userstorotate"]).json()

    def set_must_rotate_api_key(self, username):
        """Posts to /apikeyactivationtime/user/{username} to reset the API key
        activation timestamp for the given user.

        Args:
            username (str): The name of the user to reset API key activation
                time for.
        """
        self.__service_client.post(["mustrotateapikey", "user", username])

    def get_bulk_auth_check_logs(self, start_datetime, end_datetime):
        """Gets from /apikey/bulk-auth-check-logs all of the bulk auth check
        logs for a time period

        Args:
            start_datetime (str): The start datetime in UTC ISO8601, inclusive,
                of the query.
            end_datetime (str): The end datetime in UTC ISO8601, inclusive, of
                the query.

        Returns:
            (dict): The bulk auth checks.
        """
        return self.__service_client.get(
            ["apikey", "bulk-auth-check-logs"],
            query_args={"startDatetime": start_datetime, "endDatetime": end_datetime},
        ).json()

    def get_all_magic_links(self):
        """Gets from the /magic-links endpoint a list of all magic links

        Returns:
            (list): A list of magic links in the database
        """
        return self.__service_client.get(["magic-links"]).json()

    def get_magic_link_for_token(self, token):
        """Gets from the /magic-links/{token}

        Args:
            token (str): The token of the magic link being requested.

        Returns:
            (dict): The magic link requested
        """
        return self.__service_client.get(["magic-links", token]).json()

    def create_magic_link(self, link):
        """Posts to the /magic-links endpoint to create a new magic link.

        Args:
            link (object): the magic link to create.
        Returns:
            (dict): The magic link created.
        """
        return self.__service_client.post(["magic-links"], req_json=link).json()

    def create_magic_link_for_user(self, username):
        """Posts to the /magic-links endpoint to create a new magic link.

        Args:
            username (str): the user for which we need to create the magic link.
        Returns:
            (str): The magic link created.
        """
        res = self.__service_client.post(["magic-links"], req_json={"username": username})
        magic_link_dict = res.json()
        token = magic_link_dict["token"]
        return f"https://farmos.plenty.tools/login/magic-link/{token}"

    def activate_magic_link(self, token):
        """Posts to the /magic-links/activate endpoint to activate a magic link
        for given token.

        Args:
            token (str): The token for the magic link to be activated.

        Returns:
            (dict): The magic link created.
        """
        return self.__service_client.post(["magic-links/activate", token]).json()

    def delete_magic_link(self, token):
        """Deletes from the /magic-links/{token} endpoint a particular magic link.

        Args:
            token (str): The token for the magic link to be deleted.

        Returns:
            (None): None.
        """
        self.__service_client.delete(["magic-links", token])

    def update_for_token(self, token):
        """Puts to the /magic-links/{token} endpoint to update a particular magic link.

        Args:
            token (str): The token for the magic link to be deleted.

        Returns:
            (dict): The updated magic link.
        """
        self.__service_client.put(["magic-links", token]).json()
