# WorkerAPI

WorkerAPI is a minimalistic implementation of the FastAPI framework designed to run on Cloudflare Workers. Since Cloudflare Workers now support Python but only with the standard library, this framework provides a way to build simple web service applications that are API-compatible with FastAPI. This allows for easier future migration to FastAPI or even away from Cloudflare Workers if needed.

## Motivation

Unlike FastAPI, which launches a server, Cloudflare Workers expose a function that gets called with a request and should return a response. WorkerAPI adapts to this request flow model while keeping the FastAPI-style route definition.

## Repository

GitHub: [workerapi](https://github.com/Deltachaos/cloudflare-python-workerapi)

## Installation

Since WorkerAPI is a minimal framework designed for Cloudflare Workers, it cannot be installed via `pip`. Instead, you need to add it as a Git submodule:

```sh
cd src
git submodule add https://github.com/Deltachaos/cloudflare-python-workerapi workerapi
```

Then, you can import it in your project as follows:

```python
from workerapi import FastAPI
```

## Example Usage

A simple example using WorkerAPI:

### `src/main.py`

```python
from workerapi import FastAPI
from workerapi.responses import RedirectResponse

app = FastAPI()

@app.get("/{user}")
async def root(user):
    return {"some": "data" + user}

@app.get("/test")
async def root():
    return RedirectResponse("https://www.example.com")

on_fetch = app.on_fetch()
```

### `wrangler.toml`

```toml
name = "some-app"
main = "src/main.py"
compatibility_flags = ["python_workers"]
compatibility_date = "2024-03-29"
```

## Cloudflare Worker Python Support

Cloudflare has recently added support for Python in Workers. You can find more information in the official documentation:

- [Cloudflare Workers Python Documentation](https://developers.cloudflare.com/workers/languages/python/)
- [Cloudflare Workerd GitHub Repository](https://github.com/cloudflare/workerd)

## Contributions

Contributions are welcome! Feel free to open an issue or a pull request on the GitHub repository. If you have ideas for improvements or bug fixes, we’d love to hear about them.

## License

This project is licensed under the MIT License.

