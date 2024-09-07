from fastapi import FastAPI, UploadFile, HTTPException  
from fastapi.responses import JSONResponse
import os, sys, subprocess
from urllib.request import urlretrieve
from uuid import uuid4
import asyncio
from collections import deque
import os
import sys
import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, ContentSettings, generate_account_sas, ResourceTypes, AccountSasPermissions

app = FastAPI()  

# Store processing status and output
job_status = {}


@app.post("/process-video")  
async def process_video(file: UploadFile):
    videoName = str(uuid4())
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = current_dir + "/demo/" + videoName + ".avi" 
    print(os.path.abspath(file_path))
    os.makedirs(current_dir + "/demo", exist_ok=True)
    try:
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        print("File saved successfully")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)   

    # Start the processing asynchronously
    asyncio.create_task(run_processing(videoName))
    
    return JSONResponse(content={
        "message": "Processing started",
        "uuid": videoName,
        "done": "processing"
    })
    
@app.get("/video-status/{videoName}")
async def get_video_status(videoName: str):
    if videoName not in job_status:
        raise HTTPException(status_code=404, detail="Video processing job not found")
    
    status = job_status[videoName]["status"]
    output = list(job_status[videoName]["output"])
    progressval , progress_message = get_progress(videoName)
    return JSONResponse(content={
        "videoName": videoName,
        "status": status,
        "output": output,
        "currentProgress": progressval,
        "progressStatus": progress_message
    })

async def run_processing(videoName: str):
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    command = ["python", "clipMorpher.py", "--videoName", videoName]
    job_status[videoName] = {
        "status": "processing",
        "output": deque(maxlen=100)  # Store last 100 lines
    }
    
    output_video_directory = os.path.join(current_dir, "demo", f"{videoName}", "pyavi", "video_out.avi")
    
    # Change to the directory of the current script
    os.chdir(current_dir)
    
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        line = line.decode().strip()
        job_status[videoName]["output"].append(line)
        print(line)  # Optional: print to server console
    
    await process.wait()
    
    if process.returncode == 0:
        job_status[videoName]["status"] = "completed"
        blob_url_json = await asyncio.to_thread(upload_blob, videoName, output_video_directory)

    else:
        job_status[videoName]["status"] = "failed"
        error = await process.stderr.read()
        job_status[videoName]["output"].append(f"Error: {error.decode()}")

def upload_blob(request_uuid, file_path):
    """
    Uploads a file to the container as a blob.
    """
    load_dotenv('../.env.common')

    # Determine the environment  
    environment = os.getenv('APP_ENV', 'development')  
    print("Current environment is", environment)
    # Load the appropriate .env file  
    if environment == 'production':  
        load_dotenv('../.env.prod')  
    else:  
        load_dotenv('../.env.dev')

    # Access environment variables
    account_name = os.environ.get("AZURE_STORAGE_ACCOUNT_NAME", "")
    account_key = os.environ.get("AZURE_STORAGE_ACCOUNT_KEY", "")
    container_name = os.environ.get("AZURE_STORAGE_CONTAINER_NAME", "")
    azure_output_directory = f'edited/video/{request_uuid}/videos/output.avi'

    logging.info("Uploading file to Azure Blob Storage")

    sas_token = generate_account_sas(
        account_name=account_name,
        account_key=account_key,
        resource_types=ResourceTypes(object=True),
        permission=AccountSasPermissions(read=True, write=True),
        expiry=datetime.now() + timedelta(days=365)
    )

    upload_options = ContentSettings(content_type='video/avi', content_disposition='inline')

    connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_url = None
    try:
        blob_client = container_client.get_blob_client(azure_output_directory)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True, content_settings=upload_options)
            blob_url = f"{blob_client.url}?{sas_token}"
        
        logging.info(f"Blob URL: {blob_url}")
        logging.info(f"File {file_path} uploaded to {blob_url} in container {container_name} with content settings.")

    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        return {"videoBlobUrl": ""}
    
    job_status[request_uuid]["output"] = "".join(blob_client.url) + "?".join(sas_token) 

def get_progress(uuid: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    progress_directory = os.path.join(current_dir, "demo", uuid, "pywork", "progress.log")
    with open(progress_directory, 'r') as file: 
        lines = file.readlines()
        progress_percentage = lines[-2].strip()  
        progress_message = lines[-1].strip()  
        return progress_percentage, progress_message 
    
    
if __name__ == "__main__":  
    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=8000)  