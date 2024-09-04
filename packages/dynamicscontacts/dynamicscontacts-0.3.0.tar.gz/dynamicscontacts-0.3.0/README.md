# Dynamics Dataverse API Library - Contact Management
Dynamics Customer Insights - Journeys - Dataverse

This library provides a set of functions to interact with Microsoft Dataverse (formerly known as Common Data Service) using the Dynamics 365 REST API. It includes functionalities for authentication, searching contacts, adding contacts, and updating contacts.

## Installation

To use this library, you need to have `requests` and `json` modules installed. You can install `requests` using pip:
```sh
pip install requests
```
Now you need to install the Dynamics library:
```sh
pip install dynamics
```
## Usage
### Authentication - Return Access Token
This function authenticates and returns an access token required for accessing Dataverse.
```python
    # Replace these variables with your actual values
    tenant_id = 'tenant_id'
    client_id = 'client_id'
    client_secret = 'client_secret'
    tenant_name = 'tenant_name'
    crm_url = f"https://{tenant_name}.crm4.dynamics.com/"

    # Create Access Token
    access_token = dynamics.accessToken(tenant_id, client_id, client_secret, crm_url)
```
Now if the access_token is generated successfully you may proceed, otherwise make sure you setup the environment correctly.
You may need to go to this [reference](https://medium.com/@muabusalah/how-to-access-microsoft-dynamics-365-rest-api-using-python-841198159140).

## Search Contact in Dynamics
This function searches for a contact in Dataverse based on the provided search criteria.
```python
    # Search for a contact
    search_params = {
        "firstname": "fname",
        "lastname": "lname",
        "emailaddress1": "email"
    }
    # You may customize the returned fields here
    return_fields = "firstname,lastname,emailaddress1,mobilephone"
    contacts = dynamics.search_contacts(crm_url, access_token, search_params, return_fields)
    print(contacts)
```
## Add Contact to Dynamics
This function adds a new contact to Dataverse.
```python
   contact_data = {
        "firstname": "fname",
        "lastname": "lname",
        "birthdate": "%Y-%m-%d",
        "emailaddress1": "email",
        "mobilephone": "12345678"
    }
    # Add contact to Dataverse
    dynamics.add_contact(contact_data, crm_url, access_token)
```
If you want to know the fields that you can add to Dynamics, please check this [reference](https://learn.microsoft.com/es-es/power-apps/developer/data-platform/webapi/reference/contact?view=dataverse-latest&viewFallbackFrom=dynamics-ce-odata-9).
## Update Contacts in Dynamics
This function updates an existing contact in Dataverse based on the provided contact ID and update data.
```python
    # Update contracts
    update_data = {
        "firstname": "fname",
        "lastname": "lname"
    }
    contact_id= "contactid"
    updated_contact = dynamics.update_contact(access_token, contact_id, update_data, crm_url)
```
## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the Apache License. See the LICENSE file for details.

## Acknowledgements
* Microsoft Dynamics 365 REST [API](https://learn.microsoft.com/es-es/power-apps/developer/data-platform/webapi/reference/contact?view=dataverse-latest&viewFallbackFrom=dynamics-ce-odata-9)
* Medium Article on Accessing Microsoft Dynamics 365 REST API using [Python](https://medium.com/@muabusalah/how-to-access-microsoft-dynamics-365-rest-api-using-python-841198159140)

## Final note
I'd like to express my gratitude to the enchanting city of Tartu, Estonia, where I spent a delightful vacation and crafted this code. 