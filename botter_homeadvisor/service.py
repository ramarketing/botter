import requests
from botter_base.config import config

class HomeAdvisorService:
    def __init__(self):
        self.api_base = config.HOMEADVISORY_API_BASE

    def get_credentials(self):
        r = requests.get('')
