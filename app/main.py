import socket


def main():
    statusLine = b"HTTP/1.1 200 OK \r\n"
    header = "\r\n"
    body = ""

    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.accept()[0].sendall(b"HTTP/1.1 200 OK \r\n\r\n")


if __name__ == "__main__":
    main()
