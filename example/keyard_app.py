# -*- coding: utf-8 -*-
from keyard import app
from keyard.helpers import config

config.load_file('example/config.json')
app = app.create_app()
