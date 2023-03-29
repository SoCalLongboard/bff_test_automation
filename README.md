# bff_test_automation
The bff_test_automation project is test automation to monitor the health of the interrelationships between the Sprout Server API (aka **BFF**: [Backend For the Frontend](https://samnewman.io/patterns/architectural/bff/)) endpoints and the underlying services they engage.


## Overview

This test automation strives to monitor functional parity between Sprout server API endpoints and their underlying service equivalents (typically engaging those services via their plentyservice-based client wrappers). The primary motivations for engaging this monitoring are:

- the [Sprout Server API](https://github.com/PlentyAg/Sprout/tree/master/server/sprout) retrieves and assembles data to be rendered in the front-end
- [Sprout](https://github.com/PlentyAg/Sprout), [plenty-utils-python](https://github.com/PlentyAg/plenty-utils-python) (the source of [service clients](https://github.com/PlentyAg/plenty-utils-python/tree/master/plentyservice)), and the underlying services are all developed separately/independently

To the latter point, all three layers are engaged/being tested in any given test.

This automation is intended to be run within a CircleCI build job for Sprout or any of the services engaged by the Sprout Server API for both main/master branch builds and non-main/master branch builds.

Through this automation, we hope to catch/mitigate conflicts before they negatively impact users.



## Technology stack

This framework is implemented in [Python](https://www.python.org/) (currently Python 3.10.x). Novel among current Plenty projects, it uses [Poetry](https://python-poetry.org/) for dependency management.

Significant third-party libraries include:

| Library                                                                    | Use                                                                  |
|----------------------------------------------------------------------------|----------------------------------------------------------------------|
| [pytest](https://github.com/pytest-dev/pytest)                             | test execution flow; assertion handling; suite partitioning          |
| [pytest-html](https://github.com/pytest-dev/pytest-html)                   | reporting                                                            |
| [pytest-rerunfailures](https://github.com/pytest-dev/pytest-rerunfailures) | re-run failed tests (allow plural runs to achieve a PASS for a test) |
| [pytest-xdist](https://github.com/pytest-dev/pytest-xdist)                 | multi-threaded/parallel test execution                               |
| [requests](https://github.com/psf/requests)                                | HTTP client used for all BFF (Sprout Server API) requests            |

#### Other libraries

For engaging Plenty services directly, the various [plentyservice](https://github.com/PlentyAg/plenty-utils-python/tree/master/plentyservice) service client wrappers are employed.

This project's own [lib directory](./lib) provides utility functionality to support test implementations. That directory has its own [README](./lib/README.md).



## Testing approaches by-verb

This is the general manner in which HTTP verbs are tested for Sprout Server API endpoints:

### OPTIONS

A `lib.clients.options()` call is made against the Sprout Service API endpoint under test. The response is checked for the presence of the set of expected HTTP verbs.
All assertions and feedback arise from this function.

### HEAD

A `lib.clients.head()` request is made against the Sprout Service API endpoint under test. A positive response is expected.
All assertions and feedback arise from this function.

### GET

A service library is used to create a new artifact within the service.

Next, a `lib.clients.get_json()` request is made against the Sprout Service API endpoint under test. The retrieved artifact is then compared against the initial service-produced artifact for consistency.

Assertions and feedback generally arise from the test itself.

### POST

This is basically the inverse of the GET procedure.

A `lib.clients.post()` request is made against the Sprout Service API endpoint under test to create a new artifact in the service.

Next, a service client is used to retrieve the artifact. Again, the two artifacts are compared for consistency.

Assertions and feedback generally arise from the test itself.

### PUT

Generally, a service library is used to create a new artifact within the service.

Next, a `lib.clients.put()` request is made against the Sprout Service API endpoint under test to force a modification of the original record.

The service client is used to confirm the modification of the artifact.

Assertions and feedback generally arise from the test itself.



## Running the automation

The automation can be run by simply executing the `pytest` command from the project root directory.

### Run-time environment variables

These environment variables (all MANDATORY) need to be established beforehand:

| Variable name           | Sample value                                | Purpose                                                                                                                                       |
|-------------------------|---------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| `BFF_ROOT`              | https://sprout-preview-env.plenty-dev.tools | Sprout's base URL (otherwise a FarmOS root URL)                                                                                               |
| `ENVIRONMENT_CONTEXT`   | `dev` (or `staging`)                        | mostly for engaging UserStore (but not limited to that)                                                                                       |
| `BFF_PLENTY_API_KEY`    | 7Oxks3CM2z5ajwRjy3Xne2CBuRghZk              | the PLENTY_API key for the test user account for the stated ENVIRONMENT_CONTEXT (used to access the Sprout Server API and service clients)    |
| `BFF_PLENTY_API_SECRET` | O0rHcBMG62zBDcS8TBiyTeQ0PwA5pw              | the PLENTY_API secret for the test user account for the stated ENVIRONMENT_CONTEXT (used to access the Sprout Server API and service clients) |

NOTE: the BFF_PLENTY_API key pair must be set up with the rights (permissions and/or roles) to engage all the target services (including the Sprout Server API) in the target environment. Generally, this is going to be the key pair for the `frontend_test_service` user account. In the absence of this key pair, the standard PLENTY_API key pair will be used. The motivation behind the secondary BFF_PLENTY_API key pair is to avoid conflicts when integrating the bff_test_automation into a project's CircleCI configuration -- the PLENTY_API key pair for the project's CircleCI configuration and the BFF_PLENTY_API key pair for bff_test_automation's integration into the build process can be managed separately. 

### Marking (filtering test collection at run-time)

Generally, all tests from all suites are run for all Sprout Server API endpoint variations. It is possible to filter the test set by using the service-specific markings in the `pytest` command-line:

| Command                               | Impact                                                |
|---------------------------------------|-------------------------------------------------------|
| `pytest -m executive_service`         | only run tests which engage executive-service         |
| `pytest -m farm_def_service`          | only run tests which engage farm-def-service          |
| `pytest -m perception_object_service` | only run tests which engage perception-object-service |
| `pytest -m product_quality_service`   | only run tests which engage ProductQualityService     |
| `pytest -m traceability_service`      | only run tests which engage traceability-service      |
| `pytest -m user_store`                | only run tests which engage UserStore                 |

These variations should be employed when integrating this testing into their respective service projects.



### CircleCI build integration

When running this automation inside CircleCI build jobs, the environment variables previously mentioned should be established as Environment Variables within the Project Settings for their respective CircleCI projects. 

