# Project library imports
from lib.clients import farm_def_service_client


fdsc = farm_def_service_client()
crops = fdsc.search_crops(limit=1000)

print(f"{len(crops) = }")
print()

for crop in crops:
    if "BFFTEST" in crop["commonName"]:
        print(crop["name"])
        fdsc.delete_crop(crop["name"])
