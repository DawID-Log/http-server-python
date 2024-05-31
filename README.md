
# Passing the first stage

The entry point for your HTTP server implementation is in `app/main.py`.

# Stage 2
1. Ensure you to have `python (3.11)` installed locally
1. Run `./your_server.sh` to run your program, which is implemented in
   `app/main.py`.

If after running “your_server.sh”, it doesn't work and this error is reported: “./your_server.sh: line 8: exec: pipenv: not found” I recommend to open a git bash in the explorer and run a `pip install pipenv`.
In my case, the error showed even though pipenv was already installed.
I used WSL and I chose to use “Ubuntu”:
```sh
bash
wsl --install -d Ubuntu
```
To choose the distro:
```sh
wsl --list --online
```


# Stage 3
Start two bash:
1. In the first one, to start the server, run:
```sh
bash
exec pipenv run python3 -m app.main “$@”
```

2. In the second one, to test the server, run:
```sh
bash
curl --verbose 127.0.0.1:4221
curl -v http://localhost:4221/echo/abc
```
