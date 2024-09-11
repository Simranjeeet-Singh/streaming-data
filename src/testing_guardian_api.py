import requests

# Replace this with your actual API key
api_key = "3984eadc-8563-4939-b33e-572f4c3460bf"

# Define the URL for the Guardian API and a test search term
url = "https://content.guardianapis.com/search"
params = {
    'q': 'test',        # Example search term
    'api-key': api_key, # Your API key
    'page-size': 1      # We only want 1 result for testing purposes
}

# Send the request to The Guardian API
response = requests.get(url, params=params)

# Check if the response status code is 200 (OK)
if response.status_code == 200:
    print("Success! Here's a sample article:")
    articles = response.json().get('response', {}).get('results', [])
    for article in articles:
        print(f"Title: {article['webTitle']}")
        print(f"URL: {article['webUrl']}")
else:
    print(f"Failed to fetch articles. Status code: {response.status_code}")
    print(response.json())  # Print error details
