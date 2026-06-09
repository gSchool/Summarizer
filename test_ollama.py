import http.client
import json

# 1. Connect to your local Ollama server
conn = http.client.HTTPConnection("localhost", 11434)

# 2. Prepare the payload (uses 'qwen3.5' which points to your latest version)
payload = json.dumps({
    "model": "qwen3.5",
    "messages": [{"role": "user", "content": "Respond with only the word: 'Success!'"}],
    "stream": False
})

# 3. Send the POST request
headers = {"Content-Type": "application/json"}
conn.request("POST", "/api/chat", payload, headers)

# 4. Get and parse the response
response = conn.getresponse()
data = json.loads(response.read().decode())

# 5. Print the output
print(data["message"]["content"])
