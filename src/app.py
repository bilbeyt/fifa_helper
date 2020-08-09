"""This module is the starting point of the application"""
from urllib.parse import parse_qs
import re
import cgi
import logging
from typing import Callable, Dict, Tuple, Any, List
from wsgiref.simple_server import make_server
from utils import field_storage_parser
from views import HomePageView, TeamBuilderPageView, StaticView, not_found_view

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class App:
    """Base App handles requests"""
    URL_MAP = {
        "/$": HomePageView(),
        "/builder$": TeamBuilderPageView(),
        "/static/(?P<path>.*)": StaticView()
    }

    def _find_handler(self, path: str, method: str) -> Tuple[Callable,
                                                             Dict[str, str]]:
        """This function returns the function for given path and method"""
        for pattern, view in self.URL_MAP.items():
            matched = re.match(pattern, path)
            if matched:
                return getattr(view, method), matched.groupdict()
        return not_found_view, {}

    def __call__(self, env: Dict[str, Any],
                 start_response: Callable) -> List[str]:
        """This magic handles every request"""
        method = env["REQUEST_METHOD"].lower()
        path = env["PATH_INFO"]

        request_body = {
            "get": lambda: parse_qs(env["QUERY_STRING"]),
            "post": lambda: field_storage_parser(cgi.FieldStorage(
                env["wsgi.input"], environ=env, keep_blank_values=True))
        }[method]()
        handler, path_params = self._find_handler(path, method)
        kwargs = {
            "path_params": path_params,
            "data": request_body
        }
        response, content_type, status = handler(**kwargs)
        start_response(
            status, headers=[("Content-Type", content_type)])
        return [response.encode()]

    def start_server(self) -> None:
        """This function start the server"""
        handler: Callable = self
        logger.info("Listening on port:8000")
        with make_server("", 8000, handler) as server:
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                logger.info("Server is shutdown")

if __name__ == "__main__":
    app = App()
    app.start_server()
