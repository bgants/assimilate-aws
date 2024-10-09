import boto3


# create a function that lists all of the api gateways and date created
def list_api_gateways():
    apigateway = boto3.client("apigateway")
    response = apigateway.get_rest_apis()
    apis = response["items"]
    all_gateways = []
    for api in apis:
        print(f"{api['name']} created on {api['createdDate']}")
        all_gateways.append(api["name"])
    # print the total number of api gateways
    print(f"Total: {len(apis)}")

    return all_gateways 
