import socket


def main():
    crlf = "\r\n"
    statusLine = b"HTTP/1.1 200 OK"
    header = ""
    body = ""

    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.accept()[0].sendall(statusLine+crlf+crlf)


if __name__ == "__main__":
    main()
