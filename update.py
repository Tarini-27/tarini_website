import os
import boto3
import yaml
import zipfile

gl = boto3.client('glue')
s3 = boto3.client('s3')
lb = boto3.client('lambda')

fileNames_allowed = ["function.py", "update.py", "sunlife-tarini.py"]
print(os.environ['NAME1'], flush=True)
path=os.environ['NAME1']
path=path.split(' ')

print(path, flush=True)

def get_job(filename):
    try:
        response = gl.get_job(
        JobName=filename
        )
        return response
    except:
        response = gl.create_job(
        Name=filename,
        Role='arn:aws:iam::130159455024:role/SunLifeCyberSecurity-Developer-3857',
        Command={
            'Name': 'glueetl',
            'ScriptLocation': 's3://sunlife-lambda-deploy',
            'PythonVersion': '3'
            }
        )
        print("job created")
        return response
    

def update_job(filename, s3_path):
    response = gl.update_job(
        JobName=filename,
        JobUpdate={
            'Role': 'arn:aws:iam::130159455024:role/SunLifeCyberSecurity-Developer-3857',
            'Command': {
             'Name': 'glueetl',
             'ScriptLocation': s3_path,
             'PythonVersion': '3'
            }
          }      
        )
    return response


for i in path:
    if i in fileNames_allowed:
            filename = os.path.basename(i)
            filename1 = filename.split('.')[0]
            print("filename1 "+ filename1)
            #zipfile.ZipFile(filename + '.zip', mode='w').write(filename)
            #filename = filename + '.zip'
            print(filename)
            s3.upload_file(Filename=filename, Bucket='bucket-22097', Key=filename)
            s3_path = f's3://bucket-22097/{filename}'
            print(s3_path)
            print("file uploaded to s3 successfully")
            
            glue_job = get_job(filename1)
            
            response = update_job(filename1, s3_path)
            print(response)
            print("job updated successfully")
           
    else:
        print("filename not allowed")
            


    
            
            
