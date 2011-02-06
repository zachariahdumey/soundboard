# Copyright 2010
# cmcdonough@wustl.edu (Colin McDonough) zwdumey@wustl.edu (Zachariah Dumey)

from dbobjects import Sound

import logging

from google.appengine.ext import db
from google.appengine.ext import webapp

# Handles downloading of files
class SoundHandler(webapp.RequestHandler):
  def get(self, resource):
    sound = db.get(resource)
    # TODO: Fix this to prevent index-out-of-bounds errors
    mime_type = self.detect_mime_from_data(sound.sound_file)
    if mime_type is not None:
      self.response.headers['Content-Type'] = mime_type
    self.response.out.write(sound.sound_file)

  def detect_mime_from_data(self, data):
    # Use magic numbers to guess the file type
    if data[0:4] == 'RIFF' and data[8:15] == 'WAVEfmt':
      return 'audio/x-wav'
    elif data[0:3] == 'ID3':
      logging.error('audio/mpeg found')
      return 'audio/mpeg'
    logging.error('[0:3] = %s' % data[0:3])
    logging.error('no mime-type found')
    return 'text/plain'
