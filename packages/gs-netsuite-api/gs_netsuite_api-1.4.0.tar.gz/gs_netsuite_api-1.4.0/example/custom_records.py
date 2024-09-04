from pprint import pprint

from gs_netsuite_api.custom_records import CustomRecordAPI
from gs_netsuite_api.ns_utils import NetSuiteCredential, SearchParams

Item_channel_Price = 214
PRODUCT_ID = 17373


if __name__ == "__main__":
    # Existe d'autre methode pour avoir un NetSuiteCredential
    cred = NetSuiteCredential.from_env_file("./auth_netsuite.env")

    api = CustomRecordAPI(Item_channel_Price, credential=cred, search_params=SearchParams(page_size=5, nb_pages=2))

    crit = api.default_criteria()
    crit.basic.customFieldList = api.netsuite_api.Core.SearchCustomFieldList(
        customField=[
            api.netsuite_api.Core.SearchMultiSelectCustomField(
                scriptId="custrecordnvg_channel_",
                operator="anyOf",
                searchValue=api.netsuite_api.Core.ListOrRecordRef(name="front_fr", internalId=1),
            ),
            api.netsuite_api.Core.SearchMultiSelectCustomField(
                scriptId="custrecordnvg_item",
                operator="anyOf",
                searchValue=api.netsuite_api.Core.ListOrRecordRef(internalId=str(PRODUCT_ID)),
            ),
        ]
    )
    pprint(api.search_records(crit))
