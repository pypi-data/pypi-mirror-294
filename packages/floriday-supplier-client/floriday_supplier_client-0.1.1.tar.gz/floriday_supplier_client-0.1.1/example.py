import os
from pprint import pprint
import requests

import floriday_supplier_client
from floriday_supplier_client.rest import ApiException
from pprint import pprint

CLIENT_ID = os.getenv("FLORIDAY_CLIENT_ID")
CLIENT_SECRET = os.getenv("FLORIDAY_CLIENT_SECRET")
API_KEY = os.getenv("FLORIDAY_API_KEY")
AUTH_URL = os.getenv("FLORIDAY_AUTH_URL")
BASE_URL = os.getenv("FLORIDAY_BASE_URL")

payload = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": "role:app catalog:read sales-order:write organization:read supply:read supply:write sales-order:read delivery-conditions:read fulfillment:write fulfillment:read",
}

headers = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
}


def get_access_token():
    response = requests.request("POST", AUTH_URL, headers=headers, data=payload)
    response.raise_for_status()
    return response.json().get("access_token")


if __name__ == "__main__":
    print("=== Example ===\n")
    print("base url: ", BASE_URL)
    print("Auth url: ", AUTH_URL)

    access_token = get_access_token()
    configuration = floriday_supplier_client.Configuration()
    configuration.api_key["Authorization"] = access_token
    configuration.api_key_prefix["Authorization"] = "Bearer"
    configuration = floriday_supplier_client.Configuration()
    configuration.api_key["X-Api-Key"] = API_KEY
    api_instance = floriday_supplier_client.TradeItemsApi(
        floriday_supplier_client.ApiClient(configuration)
    )

    try:
        print("\n=== Get trade items by id ===\n")
        api_response = api_instance.get_trade_items_summary(
            trade_item_ids=["1987a15c-2c28-4ba6-89a1-3780e585b42c"]
        )
        pprint(api_response)

        print("\n=== Get trade items by supplier organization id ===\n")
        api_response = api_instance.get_trade_items_summary(
            supplier_organization_id="64a03e85-7792-3ce9-b5be-70b5ee7fa96c"
        )
        pprint(api_response)

    except ApiException as e:
        print(
            "Exception when calling AdditionalServicesApi->get_additional_service_by_id: %s\n"
            % e
        )
