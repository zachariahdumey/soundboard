#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from dbobjects import Sound
from dbobjects import Soundboard
from dbobjects import SoundReference
from boardhandler import BoardHandler
from copyhandler import CopyHandler
from editorderhandler import EditOrderHandler
from editnamehandler import EditNameHandler
from editsoundhandler import EditSoundHandler
from instructionhandler import InstructionHandler
from mainhandler import MainHandler
from savehandler import SaveHandler
from soundhandler import SoundHandler
from uploadhandler import UploadHandler
from deletehandler import DeleteHandler

import cgi
import logging
import sndhdr
import random
import urllib
import wave

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app

def newSessionId():
  handmade_key = db.Key.from_path('%s' % 
  random.randint(0, 99999999), random.randint(0, 73))
  id = db.allocate_ids(handmade_key, 1)
  return id[0]

def main():
  application = webapp.WSGIApplication(
  [
  ('/', MainHandler),
  ('/upload', UploadHandler),
  ('/editSound', EditSoundHandler),
  ('/editName', EditNameHandler),
  ('/editOrder', EditOrderHandler),
  ('/sound/([^/]+)?', SoundHandler),
  ('/board/([^/]+)?', BoardHandler),
  #('/copy', PublicPrivateHandler),
  ('/copy', CopyHandler),
  ('/save', SaveHandler),
  ('/delete', DeleteHandler),
  ('/instructions', InstructionHandler),
  ], debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
