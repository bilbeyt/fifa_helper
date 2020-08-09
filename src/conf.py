"""This module is a configuration for the application"""
import os
import jinja2


DB_USER = os.getenv("db_username")
DB_PASS = os.getenv("db_password")
DB = os.getenv("db_name")
DB_HOST = os.getenv("db_host")
DB_PORT = os.getenv("db_port")

APP_PATH = os.path.dirname(__file__)
TEMPLATE_PATH = os.path.join(APP_PATH, "templates")
STATIC_PATH = os.path.join(APP_PATH, "static")
TEMPLATE_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_PATH))
