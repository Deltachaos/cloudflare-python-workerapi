import re
from workers import Response
from urllib.parse import urlparse, parse_qs

class CloudflareResponse:
    headers = {}
    status_code = 200
    content = ""

    def convert(self):
        return Response(self.content, self.status_code, self.headers)

class RedirectResponse(CloudflareResponse):
    def __init__(self, url, status_code = 302):
        self.status_code = status_code
        self.headers["Location"] = url

class JsonResponse(CloudflareResponse):
    def __init__(self, data, status_code = 200):
        self.status_code = status_code
        self.content = data

    def convert(self):
        return Response.json(self.content, self.status_code, self.headers)

class FastAPI:
    def __init__(self):
        self.routes = {}

    def get(self, path):
        def decorator(func):
            self.routes[(path, "GET")] = func
            return func

        return decorator

    def post(self, path):
        def decorator(func):
            self.routes[(path, "POST")] = func
            return func

        return decorator

    def put(self, path):
        def decorator(func):
            self.routes[(path, "PUT")] = func
            return func

        return decorator

    def delete(self, path):
        def decorator(func):
            self.routes[(path, "DELETE")] = func
            return func

        return decorator

    def patch(self, path):
        def decorator(func):
            self.routes[(path, "PATCH")] = func
            return func

        return decorator

    def options(self, path):
        def decorator(func):
            self.routes[(path, "OPTIONS")] = func
            return func

        return decorator

    def match_route(self, path):
        for (route, method), handler in self.routes.items():
            pattern = re.sub(r"{(\w+)}", r"(?P<\1>[^/]+)", route)
            match = re.fullmatch(pattern, path)
            if match:
                return handler, match.groupdict()
        return None, {}

    async def __call__(self, request, env):
        url = urlparse(request.url)
        path = url.path
        query = parse_qs(url.query)

        handler, params = self.match_route(path)
        if handler and request.method == "GET":
            merged_params = {**query, **params}
            merged_params = {k: v[0] for k, v in merged_params.items()}
            response = await handler(**merged_params)
            if not isinstance(response, CloudflareResponse):
                response = JsonResponse(response)
            return response

        return JsonResponse({"error": "Not found"}, 404)

    def on_fetch(self):
        async def handler(request, env):
            response = await self(request, env)
            return response.convert()
        return handler
