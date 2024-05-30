import socket


def main():
    crlf = "\r\n"
    statusLine = "HTTP/1.1 200 OK"

    reqLine = "GET /index.html HTTP/1.1"
    header_host = "Host: localhost:4221"
    header_userAgent = "User-Agent: curl/7.64.1"
    header_accept = "Accept: */*\r\n"
    header = header_host + crlf + header_userAgent + crlf + header_accept + crlf
    body = ""

    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept()  # wait for client

    print(f"connection request from address {addr}")
    conn.accept()[0].sendall(b"GET /index.html HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n")


if __name__ == "__main__":
    main()
