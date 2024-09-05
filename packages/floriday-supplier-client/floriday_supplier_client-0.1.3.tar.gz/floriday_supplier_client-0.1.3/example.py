import os
from pprint import pprint
import requests

from floriday_supplier_client import TradeItemsApi
from floriday_supplier_client.api_factory import ApiFactory
from floriday_supplier_client.rest import ApiException
from pprint import pprint


if __name__ == "__main__":
    factory = ApiFactory()
    client = factory.get_api_client()
    api_instance = TradeItemsApi(client)

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
