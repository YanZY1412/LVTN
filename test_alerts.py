import requests
import json

def test_alerts():
    url = 'http://127.0.0.1:5000/api/alerts/get_all_alert'
    
    try:
        # Make the GET request
        response = requests.get(url, stream=True)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Successfully connected to alerts endpoint")
            print("Streaming alerts...")
            
            # Process the SSE stream
            for line in response.iter_lines():
                if line:
                    # Decode the line and remove the 'data: ' prefix
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = line[6:]  # Remove 'data: ' prefix
                        try:
                            # Try to parse as JSON
                            alert = json.loads(data)
                            print("\nReceived alert:", alert)
                        except json.JSONDecodeError:
                            print("\nReceived raw data:", data)
        else:
            print(f"Error: Received status code {response.status_code}")
            print("Response:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure the Flask server is running.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    test_alerts() 