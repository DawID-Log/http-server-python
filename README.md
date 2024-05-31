
# Passing the first stage

The entry point for your HTTP server implementation is in `app/main.py`.

# Stage 2
1. Ensure you have `python (3.11)` installed locally
1. Run `./your_server.sh` to run your program, which is implemented in
   `app/main.py`.

In case opening the file “your_server.sh” does not start, reporting: “./your_server.sh: line 8: exec: pipenv: not found” I recommend to open in the explorer a git bash and run a `pip install pipenv`.
In my case, even though it was already installed, it would not start.
I used WSL, installed as distro: “ubuntu” and starting two bash
In the first one:
```sh
bash
exec pipenv run python3 -m app.main “$@”
```

And in the second one test the server with:
```sh
bash
curl --verbose 127.0.0.1:4221
curl -v http://localhost:4221/echo/abc
```