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
    bodyInEcho = ""
    method = args[0].split(" ")[0]

    if (len(args) > 1):
        path = args[0].split(" ")[1]

        #STATUS
        if path == "/":
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        elif "echo" in path:
            bodyInEcho = path.replace("/echo/", "")
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(bodyInEcho)}"
        elif "user-agent" in path:
            string = path.replace("/user-agent/", "")
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
            print(f"La stringa risposta: {string}")
        elif "files" in path:
            directory = sys.argv[2]
            filename = path.replace("/files/", '')
            print(f"dir: {directory}")
            print(f"fName: {filename}")
            try:
                operDir = f"/{directory}/{filename}"
                if method.upper() == "GET":
                    with open(operDir, "r") as file:
                        body = file.read()
                        print(f"body: {body}")
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}"
                elif method.upper() == "POST":
                    body_data = args[len(args) - 1]
                    print(f"Write file: {body_data}")
                    with open(operDir, "wb") as file:
                        print(".")
                        file.write(body_data.encode())
                        response = "HTTP/1.1 201 Created\r\n\r\n"
            except Exception as error:
                print(f"Failed with method: {method} when read/write: {error}")
                response = f"HTTP/1.1 404 Not Found\r\n\r\n"

        #HEADER
        args.pop(0)    
        userAgent = ""
        for arg in args:
            if "User-Agent" in arg:
                print(f"UserAgent: {arg}")
                userAgent = arg.replace("User-Agent:" , '').replace(' ', '')
                response += f"Content-Length: {len(userAgent)}\r\n"
            if "Accept-Encoding" in arg:
                print(f"Accept-Encoding: {arg}")
                acceptEncoding = arg.replace("Accept-Encoding:" , '').replace(' ', '')
                response += f"Content-Encoding: {acceptEncoding}\r\n"
        response += f"\r\n{bodyInEcho if bodyInEcho != "" else userAgent}"
        print(f"response_NEW: {response}")


    print(f"Received: {val}")
    client.sendall(response.encode())
    

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
