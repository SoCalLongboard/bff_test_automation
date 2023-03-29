# Project library imports
from lib.clients import farm_def_service_client


skus = farm_def_service_client().search_skus(limit=1000)

print(f"{len(skus) = }")
print()

for sku in skus:
    if "BFFTEST" in sku["productName"]:
        print(sku["name"])
        farm_def_service_client().delete_sku(sku["name"])
