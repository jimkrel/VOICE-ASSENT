from gradio_client import Client
import time

client = Client("http://127.0.0.1:7860/")
print("Connected to Gradio client!")

# Let's inspect all endpoints
endpoints = client.view_api(return_format="dict")["named_endpoints"]
for name in endpoints:
    print("Endpoint:", name)

# Test 1: Let's test design_generate endpoint
# From endpoints, find design_generate
try:
    print("\n--- Testing design_generate ---")
    res = client.predict(
        "male",
        "young adult",
        "low pitch",
        "american accent",
        "Testing voice design generation.",
        "English",
        "Eleven v4 (Turbo)",
        api_name="/design_generate"
    )
    print("design_generate result:", res)
except Exception as e:
    print("design_generate ERROR:", e)
