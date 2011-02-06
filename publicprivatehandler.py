# Copyright 2010
# cmcdonough@wustl.edu (Colin McDonough) zwdumey@wustl.edu (Zachariah Dumey)

from dbobjects import Soundboard

import cgi
import logging

from google.appengine.ext import db
from google.appengine.ext import webapp

# Handles making public (non-editable) copies of private Soundboards
# and making private (editable) copies of public Soundboards
class PublicPrivateHandler(webapp.RequestHandler):
  def post(self):
    soundboard_id = self.request.get('soundboard_id')
    if soundboard_id is None:
      self.response.out.write('soundboard_id is None')
      return
    self.response.out.write('soundboard_id: %s' % soundboard_id)
    soundboard = Soundboard.get_by_id(long(soundboard_id))
    if soundboard is None:
      self.response.out.write('soundboard is None')
      return
    session_id = self.request.cookies.get('id')
    if session_id is None:
      session_id_long = newSessionId()
      self.response.headers.add_header('Set-Cookie', 'id=%d' %
      session_id_long)
    else:
      session_id_long = long(session_id)
    # The soundboard is public
    if soundboard.session_id is None:
       new_soundboard = Soundboard.copy(soundboard)
       new_soundboard.session_id = session_id_long
       self.response.out.write(new_soundboard.session_id)
    # The soundboard is private (regardless of who is the creator)
    else:
       new_soundboard = Soundboard.copy(soundboard)
       # .session_id = None signifies being public
       new_soundboard.session_id = None
       self.response.out.write(new_soundboard.session_id)
    db.put(new_soundboard)
    self.redirect('/board/%d' % new_soundboard.key().id())
