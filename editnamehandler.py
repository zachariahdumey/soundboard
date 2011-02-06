# Copyright 2010
# cmcdonough@wustl.edu (Colin McDonough) zwdumey@wustl.edu (Zachariah Dumey)

from dbobjects import Soundboard

import cgi
import logging

from google.appengine.ext import db
from google.appengine.ext import webapp

# Handles editing of the soundboard name
class EditNameHandler(webapp.RequestHandler):
  def post(self):
    soundboard_id = self.request.get('soundboard_id')
    soundboard = Soundboard.get_by_id(long(soundboard_id))
    new_name = cgi.escape(self.request.get('new_name'))
    if len(new_name) == 0:
      logging.info('New board name for board %s is empty; stopping'
      % long(soundboard_id))
      return
    if len(new_name) > 45:
      new_name = new_name[0:45]
    soundboard.name = new_name
    db.put(soundboard)
    self.response.out.write(soundboard.name)
    logging.info(
    'Board %s renamed to %s' % (long(soundboard_id), soundboard.name))
