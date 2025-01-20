import boto3
# Retrieve the website configuration
s3 = boto3.client('s3')
result = s3.get_bucket_website(Bucket='mi-primer-bucket-de-prueba-1')

# Define the website configuration
website_configuration = {
    'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix': 'index.html'},
}

# Set the website configuration
s3 = boto3.client('s3')
web = s3.put_bucket_website(Bucket='mi-primer-bucket-de-prueba-1',
                      WebsiteConfiguration=website_configuration)