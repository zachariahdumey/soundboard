# Copyright 2010
# cmcdonough@wustl.edu (Colin McDonough) zwdumey@wustl.edu (Zachariah Dumey)

from dbobjects import Soundboard

import cgi
import logging

from google.appengine.ext import db
from google.appengine.ext import webapp

class SaveHandler(webapp.RequestHandler):
  def post(self):
    soundboard_id = self.request.get('soundboard_id')
    if soundboard_id is None:
      logging.error('soundboard ID was none')
      self.redirect('/')
      return
    soundboard = Soundboard.get_by_id(long(soundboard_id))
    if soundboard is None:
      logging.error('soundboard was none')
      self.redirect('/')
      return
    session_id = self.request.cookies.get('id')
    if session_id is None:
      logging.error('session ID was none')
      self.redirect('/')
      return
    elif long(session_id) != long(soundboard.session_id):
      logging.error('session IDs were not equal')
      self.redirect('/')
      return
    new_soundboard = Soundboard.copy_sounds_only(soundboard)
    db.put(new_soundboard)
    
    self.response.out.write(
    'Share <a href="/board/%d">this link</a> with your friends' % long(new_soundboard.key().id())) 
    
    #self.redirect('/board/%d' % soundboard.key().id())
