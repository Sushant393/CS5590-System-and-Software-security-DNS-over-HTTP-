import base64
import dns.resolver

DNS_SERVER = "10.0.0.183"  # Change this to your server's IP

def send_http_over_dns(url):
    # Encode URL in Base64
    encoded_url = base64.urlsafe_b64encode(url.encode()).decode()    
    dns_query = f"{encoded_url}.tunnel.com"
    response_chunks=[]
    # Send DNS TXT query
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [DNS_SERVER]

    try:
        response = resolver.resolve(dns_query, "TXT", tcp=True)

        for txt_record in response:
            encoded_response = txt_record.to_text().strip('"')
            print("[+] Encoded Response:", encoded_response)
            missing_padding = len(encoded_response) % 4
            if missing_padding:
                encoded_response += '=' * (4 - missing_padding)
            response_chunks.append(encoded_response)
            full_encoded_response = "".join(response_chunks)
            raw_bytes = base64.urlsafe_b64decode(full_encoded_response)
            print("[+] Raw decoded bytes:",raw_bytes)

            # Decode response
            decoded_response = base64.urlsafe_b64decode(encoded_response).decode()
            print("[+] Decoded Response:\n", decoded_response)
    except Exception as e:
        print("[-] Error:", e)

# Example usage
send_http_over_dns("http://example.com")
