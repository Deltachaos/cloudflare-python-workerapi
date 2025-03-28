from workers import Response

class CloudflareResponse:
    headers = {}
    status_code = 200
    content = ""

    def __init__(self, content, status_code = 302, headers = None, media_type = "text/plain"):
        if headers is None:
            headers = {}
        self.content = content
        self.status_code = status_code
        self.headers = headers
        self.headers["Content-Type"] = media_type

    def convert(self):
        return Response(self.content, self.status_code, self.headers)

class HTMLResponse(CloudflareResponse):
    def __init__(self, content, status_code = 302, headers = None, media_type = "text/html"):
        super().__init__(content, status_code, headers, media_type)

class JsonResponse(CloudflareResponse):
    def __init__(self, content, status_code = 302, headers = None, media_type = "application/json"):
        super().__init__(content, status_code, headers, media_type)

    def convert(self):
        return Response.json(self.content, self.status_code, self.headers)

class RedirectResponse(CloudflareResponse):
    def __init__(self, url, status_code = 302, headers = None, media_type = "text/html"):
        if headers is None:
            headers = {}
        headers["Location"] = url
        super().__init__("", status_code, headers, media_type)
