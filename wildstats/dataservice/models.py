from django.db import models
import sys
# Create your models here.

import requests

def get_roster():
    response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/30/roster")
