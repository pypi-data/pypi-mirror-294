import requests
import json

# Authentication - Return Access Token
def accessToken(tenant_id,client_id,client_secret,env_url):
    """
    Authenticate to access Dataverse based.

    Args:
    To learn how to create those variables please visit:
    https://medium.com/@muabusalah/how-to-access-microsoft-dynamics-365-rest-api-using-python-841198159140
    """
    try:
        auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        auth_headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        auth_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": env_url+".default"
        }
        auth_response = requests.post(auth_url, headers=auth_headers, data=auth_data)
        access_token = auth_response.json()["access_token"]
        return access_token
    except Exception as e:
        print(e)
        return ""


# Search Contact in Dynamics
def search_contacts(env_url, access_token, search_criteria, querystring):
    """
    Search for a contact in Dataverse based.

    Args:
    env_url: The URL of your Dynamics environment.
    access_token: The authentication token for accessing Dataverse.
    search_criteria: A dictionary containing fields to be search.
    querystring: A string containing fields to be returned. Example: "firstname,lastname"
    """
    if querystring == "":
        querystring = "contactid,firstname,lastname,emailaddress1"
    api_url = f"{env_url}/api/data/v9.2/contacts?$select={querystring}"

    # Add filter query based on search criteria
    filter_query = ""
    for key, value in search_criteria.items():
        filter_query += f" and {key} eq '{value}'"
    if filter_query:
        api_url += f"&$filter={filter_query[5:]}"  # Remove leading ' and '
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()['value']
    else:
        print(f"Error searching contacts: {response.text}")
        return ""

# Add Contact to Dynamics
def add_contact(contact, env_url, access_token):
    """
    Add a contact in Dataverse.

    Args:
    env_url: The URL of your Dynamics environment.
    access_token: The authentication token for accessing Dataverse.
    contact: A dictionary containing the contact fields.
    """
    # API endpoint
    api_url = f"{env_url}api/data/v9.2/contacts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(contact))
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return "Contact created successfully"
    except requests.exceptions.RequestException as e:
        return "Error creating contact:", e
        # Add more specific error handling based on response status code or error message

# Update Contacts in Dynamics
def update_contact(access_token, contact_id, update_data, env_url):

    """
    Updates a contact in Dataverse based on the provided contact ID and update data.

    Args:
    env_url: The URL of your Dynamics environment.
    access_token: The authentication token for accessing Dataverse.
    contact_id: The GUID of the contact to update.
    update_data: A dictionary containing the updated contact fields.
    """
    # API endpoint
    api_url = f"{env_url}/api/data/v9.2/contacts({contact_id})"

    headers = {
      "Authorization": f"Bearer {access_token}",
      "Content-Type": "application/json"
    }
    try:
        response = requests.patch(api_url, headers=headers, data=json.dumps(update_data))
        return "Contact updated successfully"
    except requests.exceptions.RequestException as e:
        return "Error updating contact:", e