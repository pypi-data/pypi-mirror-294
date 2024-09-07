import requests, json

stored_uuid = None
while True:
    print("what do you want to test ?\n1.Current State\n2.New State")
    val = input()
    if  val == '1':
        url = 'http://localhost:8000/video-status/' + str(stored_uuid)
        response = requests.get(url)
        print(response.content)
        continue
    elif val == '2':
        url = 'http://localhost:8000/process-video'
        files = {'file': open('./clipmorpher/demo/123.avi', 'rb')}
        response = requests.post(url, files=files)

        # Decode the byte string to a regular string
        json_string = response.content.decode('utf-8')

        # Parse the JSON string into a Python dictionary
        content = json.loads(json_string)
        
        stored_uuid = content["uuid"]
