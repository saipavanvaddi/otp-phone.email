import urllib.request
import json

def get_user_data(user_json_url):
    """
    Retrieve user data from the provided JSON URL
    """
    try:
        # Read JSON data from the URL
        with urllib.request.urlopen(user_json_url) as url:
            data = json.loads(url.read().decode())

        # Extract user information
        user_data = {
            "country_code": data["user_country_code"],
            "phone_number": data["user_phone_number"],
            "first_name": data["user_first_name"],
            "last_name": data["user_last_name"]
        }
        return user_data
    except Exception as e:
        print(f"Error retrieving user data: {str(e)}")
        return None 