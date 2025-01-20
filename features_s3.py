# Importar boto3 para poder realizar las acciones con AWS S3
import logging
import boto3
from botocore.exceptions import ClientError
import os

# Con AWSCLI2 realizamos una serie de comandos antes de continuar
# aws configure
# Creamos las credenciales en ~/.aws/credentials.
# -------------------------------------------------
# [default]
# aws_access_key_id = YOUR_ACCESS_KEY
# aws_secret_access_key = YOUR_SECRET_KEY
# -------------------------------------------------
# Configuramos la region en ~/.aws/config
# [default]
# region=us-east-1
# -------------------------------------------------------------------------------
# DESPUES DE CONFIGURAR - USAMOS BOTO3
s3 = boto3.resource('s3') # --> usamos Amazon s3 con este comando

# Imprimir los nombres de los buckets que tengamos ------------------------------
def print_buckets_name():
    try:
        s3 = boto3.resource('s3')
        for bucket in s3.buckets.all():
            print(bucket.name)
    except ClientError as e:
        print(f'Error: {e}')
    
# Subir nuevos archivos ---------------------------------------------------------
def upload_any_file(bucket_name='string', type_file='string'):
    try:
        s3 = boto3.resource('s3')
        with open(bucket_name, type_file) as data:
            s3.Bucket(bucket_name).put_object(Key=bucket_name, Body=data)
    except ClientError as e:
        print(f'Error: {e}')
        return False
    return True

# Crear un bucket de s3 amazon ---------------------------------------------------
# Desarrollamos la función para encapsular el proceso de creación
def create_new_bucket(bucket_name='string', region='string'):  # Correcto
    try:
        s3_cliente = boto3.client('s3', region_name=region)
        location = {'LocationConstraint': region}
        s3_cliente.create_bucket(
            Bucket=bucket_name, CreateBucketConfiguration = location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# Para ver los datos principales del los buckets que tenemos
def see_type_bucket():
    try:
        s3 = boto3.client('s3')
        response = s3.list_buckets()
        print(response)
    except ClientError as e:
        print(f'Error: {e}')
        return False
    return True

# Descargar archivos de S3
def download_files(bucket_name='string', url_file='string', name_file='string'):
    try:
        s3 = boto3.client('s3')
        s3.download_file(bucket_name, url_file, name_file)
    except ClientError as e:
        print(f'Error: {e}')
        return False
    return True

# Cargar archivos a un bucket especifico
# Desarrollamos la función para encapsular el proceso de subida de un documento
def upload_new_file(file_name='string', bucket='string', object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# en object_name hay que poner la extension
# Con esta opcion podemos introducir archivos en formato binario y no en texto
s3 = boto3.client('s3')
with open("FILE_NAME", "rb") as f:
    s3.upload_fileobj(f, "mi-primer-bucket-de-prueba-1", "OBJECT_NAME")


# Configuración web -------------------------------------------------------------
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
s3.put_bucket_website(Bucket='mi-primer-bucket-de-prueba-1',
                      WebsiteConfiguration=website_configuration)
# Delete the website configuration y deshabilita la configuracion
s3 = boto3.client('s3')
s3.delete_bucket_website(Bucket='mi-primer-bucket-de-prueba-1')

# Creando una queue -------------------------------------------------------------
# Obtenemos el recurso desde AWS
sqs = boto3.resource('sqs')

# Creamos la queue, esto devuelve una instancia SQS.Queue
queue = sqs.create_queue(QueueName='test', Attributes={'DelaySeconds': '5'})

# Ya se puede acceder a identificadores y atributos
print(queue.url)
print(queue.attributes.get('DelaySeconds'))

# Obteniendo una queue existente -------------------------------------------------
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='test')
print(queue.url)
print(queue.attributes.get('DelaySeconds'))