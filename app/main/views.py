from flask import render_template, session
from . import main
from ..models import Permission, Role, User

import string, random

@main.route('/', methods=['GET'])
def index():
  state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
  session['state'] = state
  return render_template('index.html')

@main.route('/profile', methods=['GET'])
def profile():
  pass

@main.route('/tools/blocky', methods=['GET'])
def blocky():
  return render_template('blocky_frame.html')