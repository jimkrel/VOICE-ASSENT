from gradio_client import Client
try:
    client = Client('http://127.0.0.1:7860')
    print("API Endpoints:")
    client.view_api()
except Exception as e:
    print("Error:", e)
