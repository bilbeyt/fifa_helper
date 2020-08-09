"""This module has views that handle requests"""
import json
import logging
import os

from src.db import PlayerAdapter
import src.conf as conf
from src.builder import TeamBuilder


logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)



class HomePageView:
    """Homepage related method handlers"""
    template_name = "index.html"

    def get(self, **kwargs):
        """This function handling get requests for home page"""
        output = conf.TEMPLATE_ENV.get_template(self.template_name).render(
            kwargs)
        return output, "text/html", "200 OK"

    @staticmethod
    def post(**kwargs):
        """This function handling post requests and returns
        players from database"""
        word = kwargs["data"]["word"]
        adapter = PlayerAdapter()
        players = adapter.search_table(word)
        return json.dumps(players), "text/json", "200 OK"


class TeamBuilderPageView:
    """TeamBuilder related method handlers"""
    template_name = "builder.html"

    def get(self, **kwargs):
        """This function handling get requests for build page"""
        output = conf.TEMPLATE_ENV.get_template(self.template_name).render(
            kwargs)
        return output, "text/html", "200 OK"

    @staticmethod
    def post(**kwargs):
        """This function handling post requests and returns
        team generated with budget"""
        budget = int(kwargs["data"]["budget"])
        builder = TeamBuilder(budget)
        players = builder.build()
        return json.dumps(players), "text/json", "200 OK"


class StaticView:
    """This class is handling static assets"""

    @staticmethod
    def get_data_and_status(file_path):
        """This function reads the data from file and returns"""
        status = "200 OK"
        try:
            with open(file_path, "r") as _f:
                data = _f.read()
        except FileNotFoundError as err:
            logger.error(err)
            data = ""
            status = "404 Not Found"
        return data, status

    def get(self, **kwargs):
        """This function handling get requests for static assets"""
        rel_path = kwargs["path_params"]["path"]
        file_path = os.path.join(conf.STATIC_PATH, rel_path)
        data, status = self.get_data_and_status(file_path)
        ext = rel_path.split(".")[-1]
        if ext == "js":
            content_type = "application/javascript"
        elif ext == "css":
            content_type = "text/css"
        else:
            content_type = "text/plain"
        return data, content_type, status


def not_found_view(**kwargs):
    """This function handles the 404 Not Found pages"""
    logger.info("Not Found with path params %s", kwargs["path_params"])
    return "404 Not Found", "text/plain", "404 Not Found"
