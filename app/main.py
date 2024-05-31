import socket

def send_req(client, req):
    response: bytes = req.encode()
    data: str = client.recv(1024).decode()
    request_data: list[str] = data.split("\r\n")
    if request_data[0].split(" ")[1] != "/":
        response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
    client.send(response)

def create_header(isFirstRequest):
    request_string = ""
    if isFirstRequest:
        crlf = "\r\n"
        statusLine = "HTTP/1.1 200 OK"
        request_string = statusLine+crlf+crlf
    else:
        reqLine = "GET /index.html HTTP/1.1"
        header_host = "Host: localhost:4221"
        header_userAgent = "User-Agent: curl/7.64.1"
        header_accept = "Accept: */*\r\n"
        header = header_host + crlf + header_userAgent + crlf + header_accept + crlf
        request_string = reqLine + crlf + header + crlf
    return request_string

def main():
    print("Logs from your program will appear here!")

    # Quando devo testare
    server_socket: socket.socket = socket.create_server(
        ("localhost", 4221), reuse_port=True
    )

    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # server_socket.bind(("localhost", 4221))
    # server_socket.listen()

    client, addr = server_socket.accept()

    # send_req(client, create_header(isFirstRequest=True))
    # send_req(client, create_header(isFirstRequest=False))

    with client:
        val = client.recv(1024)
        pars = val.decode()
        args = pars.split("\r\n")
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"

        if len(args) > 1:
            path = args[0].split(" ")

            #STATUS
            if path[1] == "/":
                response = b"HTTP/1.1 200 OK\r\n\r\n"
            if "echo" in path[1]:
                string = path[1].strip("/echo/")
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
            if "user-agent" in path[1]:
                string = path[1].strip("/user-agent/")
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n".encode()
                print(f"La stringa risposta: {string}")

            #HEADER
            args.pop(0)    
            for arg in args:
                if "User-Agent" in arg:
                    print(f"UserAgent: {arg}")
                    userAgent = arg.strip("User-Agent: ")
                    response += f"Content-Length: {len(userAgent)}\r\n\r\n{userAgent}".encode()
                    print(f"NEW RESPONSE: {response}")


        print(f"Received: {val}")
        client.sendall(response)

if __name__ == "__main__":
    main()
