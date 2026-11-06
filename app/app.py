
from flask import Flask, request, jsonify
from ldap3.utils.conv import escape_filter_chars
from ldap_utils import get_ldap_connection, authenticate_user

app = Flask(__name__)

BASE_DN = "ou=People,dc=cyberzulka,dc=lab"


def search_users(search_filter):
    connection = get_ldap_connection()

    if not connection.bind():
        error = connection.result
        connection.unbind()
        return None, error

    connection.search(
        search_base=BASE_DN,
        search_filter=search_filter,
        attributes=["uid", "cn", "mail"]
    )

    users = [
        {
            "dn": entry.entry_dn,
            **entry.entry_attributes_as_dict
        }
        for entry in connection.entries
    ]

    connection.unbind()
    return users, None


@app.route("/")
def home():
    return "Cyber Zulka LDAP Injection Lab"


@app.route("/vulnerable/search")
def vulnerable_search():
    username = request.args.get("username", "")

    # Intentionally vulnerable: raw input enters the LDAP filter.
    ldap_filter = f"(&(objectClass=inetOrgPerson)(uid={username}))"

    users, error = search_users(ldap_filter)

    if error:
        return jsonify({"error": error}), 500

    return jsonify(users)


@app.route("/secure/search")
def secure_search():
    username = request.args.get("username", "")

    # Secure: escape special LDAP filter characters.
    safe_username = escape_filter_chars(username)

    ldap_filter = f"(&(objectClass=inetOrgPerson)(uid={safe_username}))"

    users, error = search_users(ldap_filter)

    if error:
        return jsonify({"error": "LDAP search failed"}), 500

    return jsonify(users)


@app.route("/secure/login", methods=["POST"])
def secure_login():
    data = request.get_json(silent=True) or {}

    username = data.get("username", "")
    password = data.get("password", "")

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"error": "Invalid input"}), 400

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    safe_username = escape_filter_chars(username)

    ldap_filter = f"(&(objectClass=inetOrgPerson)(uid={safe_username}))"

    users, error = search_users(ldap_filter)

    if error:
        return jsonify({"error": "LDAP search failed"}), 500

    if len(users) != 1:
        return jsonify({"error": "Invalid username or password"}), 401

    authenticated = authenticate_user(users[0]["dn"], password)

    if not authenticated:
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "Authentication successful"}), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

