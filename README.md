# DIMO Python Developer SDK

## Installation

You can install the SDK using `pip`

```bash
pip install dimo-python-sdk
```

## Unit Testing

Coming Soon

## API Documentation

Please visit the DIMO [Developer Documentation](https://docs.dimo.org/developer-platform) to learn more about building on DIMO and detailed information on the API.


### Developer License

In order to build on DIMO, you’ll need to get a [DIMO Developer License](https://docs.dimo.zone/developer-platform/getting-started/developer-license) via the [DIMO Dev Console](https://console.dimo.org/). The DIMO Developer license is our approach and design to a more secured, decentralized access control. As a developer, you will need to perform the following steps:

1. Sign Up for an Account - You can use your Google or Github account to register.
2. Complete Registration - Enter the details of the application that you’re building.
3. Create An App - Click “Create App”, fill out the form & select your preferred environment (at this time, please select “Production” until we’re ready to launch our Sandbox environment), then hit “Create Application”.
4. Finish Configuring Your Application - Once your project is initialized, you’ll use your connected wallet to generate an API Key and any optional Redirect URIs.

More information about this process can be found on our docs [here](https://docs.dimo.org/developer-platform/getting-started/developer-guide/developer-console)

## How to Use the SDK

Importing the SDK:

```python
from dimo import DIMO
```

Initiate the SDK depending on the envionrment of your interest, we currently support both `Production` and `Dev` environments:

```python
dimo = DIMO("Production")
```

or

```python
dimo = DIMO("Dev")
```

### Authentication

To get authenticated as a developer, you must have already obtained a [Developer License via the Console](https://docs.dimo.org/developer-platform/getting-started/developer-guide/developer-console#getting-a-license). To learn more about authentication, including the User JWT, Developer JWT, and Vehicle JWT needed for accessing certain endpoints, please read: [Authentication Docs](https://docs.dimo.org/developer-platform/getting-started/developer-guide/authentication). 

#### API Authentication

##### (Option 1) 3-Step Function Calls

The SDK offers 3 basic functions that maps to the steps listed in [Wallet-based Authentication Flow](https://docs.dimo.zone/developer-platform/getting-started/authentication/wallet-based-authentication-flow): `generate_challenge`, `sign_challenge`, and `submit_challenge`. You can use them accordingly depending on how you build your application.

```python
    challenge = dimo.auth.generate_challenge(
        client_id = '<client_id>',
        domain = '<domain>',
        address = '<address>'
    )

    signature = dimo.auth.sign_challenge(
        message = challenge['challenge'],
        private_key = '<private_key>'
    )

    tokens = dimo.auth.submit_challenge(
        client_id = '<client_id>',
        domain = '<domain>',
        state = challenge['state'],
        signature = signature
    )
```

##### (Option 2) Auth Endpoint Shortcut Function

As mentioned earlier, this is the streamlined function call to directly get the `access_token`. The `address` field in challenge generation is omitted since it is essentially the `client_id` of your application per Developer License:

```python
auth_header = dimo.auth.get_token(
    client_id = '<client_id>',
    domain = '<domain>',
    private_key = '<private_key>'
)

# Store the Developer JWT from the auth_header dictionary
dev_jwt = auth_header["access_token"]
```

### Querying the DIMO REST API

The SDK uses the [requests](https://requests.readthedocs.io/en/latest/) library for making HTTP requests. You can perform a query like so:

```python
def decode_vin():
    device_makes = dimo.device_definitions.decode_vin(
        developer_jwt = dev_jwt,
        country_code = "USA",
        vin = "<VIN>"
    )
    # Do something with the response
```

#### Query Parameters

For query parameters, simply feed in an input that matches with the expected query parameters:

```python
dimo.device_definitions.search_device_definitions(
    query = "Lexus gx 2023"
)
```


#### Vehicle JWTs

As the 2nd leg of the API authentication, applications may exchange for short-lived Vehicle JWTs for specific vehicles that granted privileges to the app. This uses the [DIMO Token Exchange API](https://docs.dimo.org/developer-platform/api-references/token-exchange-api).

For the end users of your application, they will need to share their vehicle permissions via the DIMO Mobile App or through your implementation of the [Login with DIMO flow](https://docs.dimo.org/developer-platform/getting-started/developer-guide/login-with-dimo). You can use the pre-built React component SDK, or redirect users to the URLs included in the documentation [here](https://docs.dimo.org/developer-platform/getting-started/developer-guide/login-with-dimo#dont-use-react).

Typically, any endpoints that uses a NFT `tokenId` in path parameters will require JWTs. You can use this flow to obtain a privilege token.

```python

get_vehicle_jwt = dimo.token_exchange.exchange(
    developer_jwt = dev_jwt, 
    # The Developer JWT you received using either the three step function calls, or the .get_token() shortcut 
    privileges=[1, 3, 4, 5],
    # The privileges you've set for this vehicle, in list format (e.g. [1, 3, 4])
    token_id="<token_id>" 
    # The Vehicle NFT Token ID that you are requesting permission to
    )
vehicle_jwt = get_vehicle_jwt['token']
```

Once you have the privilege token, you can pipe it through to corresponding endpoints like so:

```python

dimo.trips.trips(vehicle_jwt=vehicle_jwt, token_id=<token_id>)
```

### Querying the DIMO GraphQL API

The SDK accepts any type of valid custom GraphQL queries, but we've also included a few sample queries to help you understand the DIMO GraphQL APIs.

#### Authentication for GraphQL API

The GraphQL entry points are designed almost identical to the REST API entry points. For any GraphQL API that requires auth headers (Telemetry API for example), you can use the same pattern as you would in the REST protected endpoints.

```python

telemetry_data = dimo.telemetry.query(
    vehicle_jwt=vehicle_jwt,
    query= """
        query {
            some_valid_GraphQL_query
            }
        """
    )
```

#### Send a custom GraphQL query

To send a custom GraphQL query, you can simply call the `query` function on any GraphQL API Endpoints and pass in any valid GraphQL query. To check whether your GraphQL query is valid, please visit our [Identity API GraphQL Playground](https://identity-api.dimo.zone/) or [Telemetry API GraphQL Playground](https://telemetry-api.dimo.zone/).

```python
my_query = """
    {
    vehicles (first:10) {
        totalCount
        }
    }
    """

total_network_vehicles = dimo.identity.query(query=my_query)
```

## How to Contribute to the SDK

You can read more about contributing [here](https://github.com/DIMO-Network/dimo-python-sdk/blob/dev-barrettk/CONTRIBUTING.md)
