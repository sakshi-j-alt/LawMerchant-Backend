from django.db import models
from db_connection import db


# Create your models here.
food = db['food']
electronics = db['electronics']
agriculture = db['agriculture']
hardware = db['hardware']
general = db['general']
reports = db['reports']