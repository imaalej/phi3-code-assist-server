import requests
import json
import sys

def main():
    # Read the content from stdin
    content = sys.stdin.read().strip()

    # Send the content to the Flask server
    url = 'http://127.0.0.1:5000/generate'
    data = {'text': content}
    response = requests.post(url, json=data)

    # Handle the server response
    if response.status_code == 200:
        result = response.json().get('result', '')
        # Print the result which will be captured in Vim
        print(result)
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    main()
