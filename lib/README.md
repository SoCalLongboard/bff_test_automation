# bff_test_automation libraries

### clients.py
This library contains routines for making requests to services.

In the case of BFF (Sprout Server API) requests, there are [requests](https://requests.readthedocs.io/en/latest/) wrapper functions for the HTTP verbs we care about (**OPTIONS**, **HEAD**, **GET**, **POST**, **PUT**). These wrappers implicitly deal with authentication to BFF by getting cookies after engaging UserStore's "magic link" facility.

For other Plenty services, there are functions for creating [plentyservice](https://github.com/PlentyAg/plenty-utils-python/tree/master/plentyservice)-based clients for the specific services:

| Service                                                                              | Client creation function           |
|--------------------------------------------------------------------------------------|------------------------------------|
| [[DeviceManagementService](https://github.com/PlentyAg/DeviceManagementService)]     | device_management_service_client() |
| [[executive-service](https://github.com/PlentyAg/executive-service)]                 | executive_service_client()         |
| [[farm-def-service](https://github.com/PlentyAg/farm-def-service)]                   | farm_def_service_client()          |
| [[perception-object-service](https://github.com/PlentyAg/perception-object-service)] | perception_object_service_client() |
| [[ProductQualityService](https://github.com/PlentyAg/ProductQualityService)]         | product_quality_service_client()   |
| [[traceability-service](https://github.com/PlentyAg/traceability-service)]           | traceability_service_client()      |
| [[UserStore](https://github.com/PlentyAg/UserStore)]                                 | user_store_service_client()        |
| [[workbin-service](https://github.com/PlentyAg/workbin-service)]                     | workbin_service_client()           |

Your Plenty API keypair will be used to authorize your client for the target environment. (Be sure to set your **ENVIRONMENT_CONTEXT** environment variable accordingly.)

### colors.py
Some of the testing for SKUs allows for setting of primary and secondary colors. This library provides the means to get the name of a named CSS color (a primary or a non-matching secondary) easily.

### core.py
This library contains routines for engaging UserStore.

### crops_skus.py
This library provides for the easy generation of the raw materials for crop and sku generation: randomized crop/sku names, randomized NetSuite IDs and GTINs, valid randomized crop and sku types, etc.

### devices.py
Much like crops_skus.py, this library does the same with respect to device names, types, and serials.

### perception.py
This library contains routines for establishing devices, perception objects, tags, and label sets for perception object service testing.

### product_quality.py
This library deals with the postharvest and sensory aspects of testing the ProductQualityService.

### production_actions.py
This library borrows heavily from the Sprout project for the purpose of extracting action information from a farm-def site object. Such objects may be tens of megabytes in size and the extraction of action information may require recursion through tiers of nested farm-def objects. Rather than reinventing a highly complex wheel, I've elected to rework a copy of the original code, tailored for use in this project.

### production_workcenters.py
This library facilitates the creation of artifacts for building workcenter tasks.

### production_workspaces.py
This library facilitates the creation of artifacts for building workbin tasks (and instances of same).

### utils.py
This library provides the tools for generating random booleans and strings of many kinds. You can see examples of its use in crops_skus.py.
