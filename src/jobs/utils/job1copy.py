import boto3
import sys


# print("Before Append:" ,sys.path)
# print("====================================")
# sys.path.append('c:\\Users\\Shree\\bw-dse-retail-analytics\\src\\')
# # C:\\Users\\Shree\\bw-dse-retail-analytics\\utils'
# print("After Append:" ,sys.path)
# print("====================================")
from vaultUtils import VaultClient
from awsUtils import AWSConnector 
from snowflake import SnowflakeConnector
 
VAULT_URL = "http://127.0.0.1:8200" 
ROLE_ID = "865df005-e0c3-42c9-8ceb-883f3e88c8fd"
SECRET_ID = "87a07373-6f46-8651-2aab-49fb62154557"
SECRET_PATH = "secret/data/aws"

vault_client = VaultClient(VAULT_URL, ROLE_ID, SECRET_ID, SECRET_PATH)
token = vault_client.authenticate_with_approle()

if token:
    secret_data = vault_client.get_secret(token)
    if secret_data:
        print("Secret data:", secret_data)
    else:
        print("Failed to retrieve secret.")
else:
    print("Failed to authenticate with AppRole.")

aws_access_key = secret_data['data']['bw-aws-accesskey-dev']
aws_secret_key = secret_data['data']['bw-aws-secretkey-dev']

# Replace 'YOUR_ACCESS_KEY' and 'YOUR_SECRET_KEY' with your AWS access key and secret key.
# aws_access_key = 'YOUR_ACCESS_KEY'
# aws_secret_key = 'YOUR_SECRET_KEY'
region = 'us-east-1'  # Replace with your preferred AWS region

client ="iam"
aws_connector = AWSConnector(aws_access_key, aws_secret_key, client, region)
 
# Access the iam client through the instance
iam_client = aws_connector.aws_client_conn

# Now you can use iam_client to perform iam operations
response = iam_client.list_groups()

# response = client.list_groups()
print("IAM Groups:", response)


# Replace these with your Snowflake account details
account = 'latflkz-icb55504'

SECRET_PATH = "secret/data/aws"

vault_client = VaultClient(VAULT_URL, ROLE_ID, SECRET_ID, SECRET_PATH)
token = vault_client.authenticate_with_approle()

if token:
    secret_data = vault_client.get_secret(token)
    if secret_data:
        print("Secret data:", secret_data)
    else:
        print("Failed to retrieve secret.")
else:
    print("Failed to authenticate with AppRole.")

user = secret_data['data']['bw-snow-serviceusername-dev']
password = secret_data['data']['bw-snow-serviceuserpassword-dev']

# user = 'VAIBHAVSNOWFLAKE'
# password = 'Hellow@123'
warehouse = 'COMPUTE_WH'
database = 'SNOWFLAKE_SAMPLE_DATA'
schema = 'TPCH_SF1'

# Create an instance of SnowflakeConnector
snowflake_conn = SnowflakeConnector(account, user, password, warehouse, database, schema)

# Connect to Snowflake
snowflake_conn.connect()

# Execute a query
query_result = snowflake_conn.execute_query("SELECT * from SUPPLIER limit 5")

# Print the result
print("Query Result:", query_result)

# Close the connection
snowflake_conn.close_connection()
