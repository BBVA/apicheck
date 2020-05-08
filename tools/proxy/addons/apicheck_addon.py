from mitmproxy import http, ctx


class Counter:
    def __init__(self):
        self.num = 0

    def request(self, flow: http.HTTPFlow):
        self.num = self.num + 1
        ctx.log.info("XXXXXX")


addons = [
    Counter()
]

