import time
import requests

def test_get_request(url):
    print("\n" + 100 * "=")
    print(f"📋 Testing GET request to {url}...")
    try:
        # Send a GET request
        response = requests.get(url)
        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Extract the message field from the response
            message = data.get('message', '')
            
            # Print the test result based on the message field
            if message == "API is working":
                print("✅ Test passed")
            else:
                print("❌ Test failed")
        else:
            # Print an error message if the request was not successful
            print(f"❌ Failed to retrieve data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to retrieve data: {e}")

def test_mirror_reponse(url, body):
    print("\n" + 100 * "=")
    print(f"📋 Testing Mirror POST request to {url}...")
    try:
        # Send post request with body
        response = requests.post(url, json=body)
        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            data = response.json()
            print(f"  📥 request {body}")
            print(f"  📤 response {data}")
            # Extract the message field from the response
            message = data.get('request-sent', '')

            if message == body:
                print("✅ Test passed")
            else:
                print("❌ Test failed")
        else:
            # Print an error message if the request was not successful
            print(f"❌ Failed to retrieve data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to retrieve data: {e}")

def test_proxy(url, body):
    print("\n" + 100 * "=")
    print(f"📋 Testing Proxy POST request to {url}...")
    try:
        # Send post request with body
        response = requests.post(url, json=body)
        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            data = response.json()
            print(f"  📥 request {body}")
            print(f"  📤 response {data}")
            # Extract the message field from the response
            print("✅ Test passed")
        else:
            # Print an error message if the request was not successful
            print(f"❌ Failed to retrieve data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to retrieve data: {e}")

print("\n")
print("🧪 Running tests...")
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
test_get_request("http://localhost:8080/")
test_get_request("https://proxy.chuffed.app")
test_mirror_reponse("http://localhost:8080/mirror", {"test": "test"})
test_mirror_reponse("https://proxy.chuffed.app/mirror", {"test-live": "test"})
test_proxy("http://localhost:8080/proxy", 
                    {"target": "https://script.google.com/macros/s/AKfycbxgXjWfMPJjQWqIl6PjSicv6FaRibqtoh3-9Zarwf10bYHwuxAXiqFu56VU-GSg5OY50A/exec",
                    "body": {"scope":"signup", "source": "proxy.com", "email": "proxy-local@test.com"}
                     })
test_proxy("https://proxy.chuffed.app/proxy", 
                    {"target": "https://script.google.com/macros/s/AKfycbxgXjWfMPJjQWqIl6PjSicv6FaRibqtoh3-9Zarwf10bYHwuxAXiqFu56VU-GSg5OY50A/exec",
                    "body": {"scope":"signup", "source": "proxy.com", "email": "proxy-live@test.com"}
                     })

test_proxy("https://proxy.chuffed.app/proxy", 
                    {"target": "https://script.google.com/macros/s/AKfycbxgXjWfMPJjQWqIl6PjSicv6FaRibqtoh3-9Zarwf10bYHwuxAXiqFu56VU-GSg5OY50A/exec",
                    "body": {"scope":"visit", "source": "proxy.com"}
                     })