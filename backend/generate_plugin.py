import requests

url = "http://127.0.0.1:8000/generate-plugin"
data = {
    "description": "A plugin that displays latest blog posts in a widget"
}

response = requests.post(url, json=data)

# Save the plugin ZIP
with open("plugin.zip", "wb") as f:
    f.write(response.content)

print("Plugin ZIP saved as plugin.zip")