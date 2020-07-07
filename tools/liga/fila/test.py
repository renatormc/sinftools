from sinf.servers import sinf_requests

resp = sinf_requests.post("http://localhost:8003/send-message", json={'name': 'renato', 'text': 'Teste'})
print(resp.content)
