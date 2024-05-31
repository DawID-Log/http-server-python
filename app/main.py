import sys
import argparse
import socket
import threading

FILE_DIR = ""

def send_request_demo(client, req):
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

def send_request(client):
    global FILE_DIR
    val = client.recv(1024)
    pars = val.decode()
    args = pars.split("\r\n")
    response = b"HTTP/1.1 404 Not Found\r\n\r\n"

    if len(args) > 1:
        module = args[0].split(" ")[0]
        path = args[0].split(" ")[1]
        print(f"MODULE: {module}")
        print(f"DIR: {FILE_DIR}")

        #STATUS
        if path == "/":
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        elif "echo" in path:
            string = path.replace("/echo/", "")
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
        elif "user-agent" in path:
            string = path.replace("/user-agent/", "")
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n".encode()
            print(f"La stringa risposta: {string}")
        elif "files" in path:
            directory = sys.argv[2]
            filename = path.replace("/files/", '')
            print(f"dir: {directory}")
            print(f"fName: {filename}")
            try:
                with open(f"/{directory}/{filename}", "r") as file:
                    body = file.read()
                    print(f"body: {body}")
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()
            except Exception:
                response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()

        #HEADER
        args.pop(0)    
        for arg in args:
            if "User-Agent" in arg:
                print(f"UserAgent: {arg}")
                userAgent = arg.replace("User-Agent:" , '').replace(' ', '')
                response += f"Content-Length: {len(userAgent)}\r\n\r\n{userAgent}".encode()
    print(f"Received: {val}")
    client.sendall(response)
    

def main():
    print("Logs from your program will appear here!")
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory")
    args = parser.parse_args()

    if "directory" in args:
        global FILE_DIR
        FILE_DIR = args.directory

    server_socket: socket.socket = socket.create_server(
        ("localhost", 4221), reuse_port=True
    )

    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # server_socket.bind(("localhost", 4221))
    # server_socket.listen()

    while True:
        client, addr = server_socket.accept()
        threading.Thread(target=lambda: send_request(client)).start()

if __name__ == "__main__":
    main()
