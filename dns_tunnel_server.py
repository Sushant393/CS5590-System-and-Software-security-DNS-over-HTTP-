from dnslib.server import DNSServer, DNSHandler, BaseResolver
from dnslib import DNSRecord, QTYPE, RR, TXT
import base64
import requests
import socket

class DNSTunnelResolver(BaseResolver):
    def resolve(self, request, handler):
        qname = str(request.q.qname).strip('.')

        # Decode the subdomain (HTTP request)
        try:
            http_data = base64.urlsafe_b64decode(qname.split('.')[0]).decode('utf-8')        
            print(f"[+] Received Encoded HTTP Request: {http_data}")

            # Make HTTP request
            response = requests.get(http_data)
            response_text = response.text[:200]  # Limit response size

            # Encode response in Base64
            encoded_response = base64.urlsafe_b64encode(response_text.encode('utf-8')).decode()
            chunks = [encoded_response[i:i+255] for i in range(0, len(encoded_response), 255)]
            
        except Exception as e:
            encoded_response = base64.urlsafe_b64encode(f"Error: {str(e)}".encode()).decode()

        # Create DNS TXT response
        reply = request.reply()
        for chunk in chunks:
            reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(chunk)))
        # reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(encoded_response)))
        return reply

# Start DNS server
resolver = DNSTunnelResolver()
server = DNSServer(resolver, port=53, address="0.0.0.0", tcp=True)

print(socket.gethostbyname(socket.gethostname()))
print("[+] DNS Tunnel Server Started on Port 53")
server.start()
