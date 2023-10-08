#!/opt/alt/python36/bin/python3.6

import cgitb
cgitb.enable(display=0, logdir="OUTDIR",format="html")
from wsgiref.handlers import CGIHandler
from app import app
CGIHandler().run(app)
