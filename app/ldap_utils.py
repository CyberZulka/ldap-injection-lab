import os
from ldap3 import Server, Connection, ALL

LDAP_SERVER = "localhost"
LDAP_PORT = 389
LDAP_BASE_DN = "dc=cyberzulka,dc=lab"

LDAP_APP_DN = "cn=flask-reader,ou=ServiceAccounts,dc=cyberzulka,dc=lab"


def get_ldap_connection():
    server = Server(
        LDAP_SERVER,
        port=LDAP_PORT,
        get_info=ALL
    )

    connection = Connection(
        server,
        user=LDAP_APP_DN,
        password=os.environ.get("LDAP_APP_PASSWORD"),
        auto_bind=False
    )

    return connection

def authenticate_user(user_dn, password):
    server = Server(
        LDAP_SERVER,
        port=LDAP_PORT,
        get_info=ALL
    )

    user_connection = Connection(
        server,
        user=user_dn,
        password=password,
        auto_bind=False
    )

    authenticated = user_connection.bind()
    user_connection.unbind()

    return authenticated
