# Copyright 2010
# cmcdonough@wustl.edu (Colin McDonough) zwdumey@wustl.edu (Zachariah Dumey)

from dbobjects import Soundboard
from dbobjects import SoundReference

import cgi
import logging

from google.appengine.ext import db
from google.appengine.ext import webapp

# Handles editing of a sound name
class EditSoundHandler(webapp.RequestHandler):
  def post(self):
    soundboard_id = self.request.get('soundboard_id')
    soundboard = Soundboard.get_by_id(long(soundboard_id))
    sound_id = self.request.get('sound_id')
    sound_reference = SoundReference.get_by_id(long(sound_id))
    #sound = sound_reference.reference
    new_name = self.request.get('new_name')
    # TODO(cmcdonough): change '20' to a variable constant, and use the same
    # constant in upload handler
    if len(new_name) > 20:
      new_name = new_name[0:20]
    sound_reference.name = new_name
    db.put(sound_reference)
    self.response.out.write(new_name)

