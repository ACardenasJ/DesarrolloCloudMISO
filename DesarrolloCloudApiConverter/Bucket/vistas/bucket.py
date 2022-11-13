
import os
from google.cloud import storage



os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'misonube2022equipo23-8093e2406c0a.json'



storage_client = storage.Client()
bucket_name = 'bucket_music_file_storage-1'
blob_name = 'upfiles/prueba'
blog_name = 'upfiles/prueba'



def post(file_path):
            # response = post('/docs/requirementABC', 'requirements.txt', bucket_name)
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.upload_from_filename(file_path)
            print('upload')
            return blob

def get(file_path):
            # get('Voice List', r'H:\PythonVenv\GoogleAI\Cloud Storage\Voice List.csv', bucket_name)
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(blog_name)
            with open(file_path, 'wb') as f:
                storage_client.download_blob_to_file(blob, f)
            print('download')

#post('upfiles/prueba','Prueba/prueba.json')
#get('upfiles/prueba', 'E:/Desarrollo/Practicas/Universidad/semestre2/Ciclo2/Nube/Desarrollo/DesarrolloCloudMISO/DesarrolloCloudApiConverter/Bucket/vistas/downloaded/prueba.json')


post('Prueba/prueba.json')
get('E:/Desarrollo/Practicas/Universidad/semestre2/Ciclo2/Nube/Desarrollo/DesarrolloCloudMISO/DesarrolloCloudApiConverter/Bucket/vistas/downloaded/prueba.json')