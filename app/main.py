import socket


def main():
    crlf = "\r\n"
    statusLine = "HTTP/1.1 200 OK"
    request_1 = statusLine+crlf+crlf

    reqLine = "GET /index.html HTTP/1.1"
    header_host = "Host: localhost:4221"
    header_userAgent = "User-Agent: curl/7.64.1"
    header_accept = "Accept: */*\r\n"
    header = header_host + crlf + header_userAgent + crlf + header_accept + crlf
    request_2 = reqLine + crlf + header + crlf

    print("Logs from your program will appear here!")

    server_socket: socket.socket = socket.create_server(
        ("localhost", 4221), reuse_port=True
    )
    client: socket.socket
    client, addr = server_socket.accept()

    response: bytes = request_1.encode()
    data: str = client.recv(1024).decode()
    request_data: list[str] = data.split("\r\n")

    if request_data[0].split(" ")[1] != "/":
        response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
    
    print(f"connection request from address {addr}")
    client.send(response)
    client.close()


if __name__ == "__main__":
    main()
