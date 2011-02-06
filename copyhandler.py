# Copyright 2010
# cmcdonough@wustl.edu (Colin McDonough) zwdumey@wustl.edu (Zachariah Dumey)

from dbobjects import Soundboard
import main

import cgi
import logging

from google.appengine.ext import db
from google.appengine.ext import webapp

# Handles making private copies of soundboards
class CopyHandler(webapp.RequestHandler):
  def post(self):
    soundboard_id = self.request.get('soundboard_id')
    if soundboard_id is None:
      self.redirect('/')
      return
    soundboard = Soundboard.get_by_id(long(soundboard_id))
    if soundboard is None:
      self.redirect('/')
      return
    session_id = self.request.cookies.get('id')
    if session_id is None:
      session_id_long = main.newSessionId()
      self.response.headers.add_header('Set-Cookie', 'id=%d' % session_id_long)
    else:
      session_id_long = long(session_id)
    new_soundboard = Soundboard.copy(soundboard)
    new_soundboard.session_id = session_id_long
    db.put(new_soundboard)
    self.redirect('/board/%d' % new_soundboard.key().id())
