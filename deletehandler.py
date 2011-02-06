# Created by zwdumey@wustl.edu (Zachariah Dumey)

import logging

from dbobjects import Soundboard

from google.appengine.ext import db
from google.appengine.ext import webapp

class DeleteHandler(webapp.RequestHandler):

  '''
  this class will allow users to delete a soundboard they're working on
  it will only allow deletion of boards with the same session_id as the cookie,
  so other saves of an existing soundboard will remain intact
  '''

  def post(self):
    soundboard = Soundboard.get_by_id(long(self.request.get('soundboard_id')))
 
    # the usual checks to make sure the user is authorized
    if soundboard is None or soundboard.session_id is None or self.request.cookies.get('id') is None:
      logging.error('tried to delete a nonexistent or public soundboard '
      'or invalid cookies')
      self.redirect('/')
    
    elif long(soundboard.session_id) != long(self.request.cookies.get('id')):
      logging.error('tried to delete a soundboard they did not own')
      self.redirect('/')
    
    elif long(soundboard.session_id) == long(self.request.cookies.get('id')):
      # the business end 
      soundboard.delete()
      self.redirect('/')
  
