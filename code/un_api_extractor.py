import requests

import pandas as pd


# # THIS IS A POST REQUEST

# url = 'https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/ArchiveData/GetArchiveTable'
# headers = {
#     'accept': 'application/json'
# }

# # In this case, it seems you're sending an empty body.
# data = {}

# # Make the POST request
# response = requests.post(url, headers=headers, json=data)

# # Check the status of the request and print the response
# if response.status_code == 200:
#     print(response.json())  # If successful, print the JSON response
# else:
#     print(f"Error: {response.status_code}, {response.text}")  # Print any errors




# # THIS IS A GET REQUEST

# url = 'https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/DataAvailability/CountriesList'
# headers = {
#     'accept': 'application/json'
# }

# # In this case, it seems you're sending an empty body.
# data = {}

# # Make the GET request
# response = requests.get(url, headers=headers, json=data)

# # Check the status of the request and print the response
# if response.status_code == 200:
#     print(response.json())  # If successful, print the JSON response
# else:
#     print(f"Error: {response.status_code}, {response.text}")  # Print any errors



# 218 IS ECUADOR.

url = 'https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Series/Data?218'
headers = {
    'accept': 'application/json'
}

# In this case, it seems you're sending an empty body.
data = {}

# Make the POST request
response = requests.get(url, headers=headers, json=data)

# Check the status of the request and print the response
if response.status_code == 200:
    # Convert the JSON response to a DataFrame
    json_data = response.json()
    print(json_data)
    
    # # Assuming the relevant data is in a key called 'data'
    # # Adjust the key based on the actual structure of the response
    # df = pd.DataFrame(json_data['data'])
    
    # # Save the DataFrame to a CSV file
    # df.to_csv('archive_data.csv', index=False)
    # print("Data saved to archive_data.csv")
else:
    print(f"Error: {response.status_code}, {response.text}")  # Print any errors

