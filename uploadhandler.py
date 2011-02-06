# Copyright 2010
# cmcdonough@wustl.edu (Colin McDonough) zdwdumey@wustl.edu (Zachariah Dumey)

from dbobjects import Sound
from dbobjects import Soundboard
from dbobjects import SoundReference

import cgi
import logging

from google.appengine.ext import db
from google.appengine.ext import webapp

# Handles uploading of files
class UploadHandler(webapp.RequestHandler):
  # Accepts post requests which contain a file and a name
  # Creates a Sound object
  # If an existing Soundboard is specified, adds a reference to the newly
  # created Sound object to the Soundboard's list of Sound references,
  # Otherwise creates a new Soundboard
  logging.debug('Upload')
  def post(self):
    resource = cgi.escape(self.request.get('board_id'))
    if resource is None or not resource.isdigit():
      soundboard = Soundboard()
    else:
      soundboard = Soundboard.get_by_id(long(resource))
    session_id = self.request.cookies.get('id')
    if session_id is not None:
      if soundboard.session_id == long(session_id):
        self.redirect('/')
    sound_reference = SoundReference()
    self.response.out.write('Uploading')
    file = self.request.get('file')
    if file != 'undefined' and len(file) != 0:
      sound = Sound()
      sound.reference_count = 1
      sound.sound_file = file
      sound.mime_type = self.get_mime_type_from_bytes(file)
      db.put(sound)
      sound_reference.sort_index = -1
      sound_reference.reference = sound.key()
      name = self.request.get('name')
      if name == 'undefined' or len(name) == 0:
        name = '???'
      elif len(name) > 20:
        name = name[0:20]
      sound_reference.name = name
      db.put(sound_reference)
      soundboard.sound_references.append(sound_reference.key())
      db.put(soundboard)
    self.response.out.write('something should be happening...')

  def get_mime_type_from_bytes(self, bytes):
    return ''
