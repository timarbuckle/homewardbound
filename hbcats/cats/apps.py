from django.apps import AppConfig

from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup


class CatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cats"
