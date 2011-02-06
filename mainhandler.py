# Copyright 2010
# cmcdonough@wustl.edu (Colin McDonough) zwdumey@wustl.edu (Zachariah Dumey)

import logging

from google.appengine.ext import db
from google.appengine.ext import webapp

# Handles HTTP requests to '/'
class MainHandler(webapp.RequestHandler):
  # Render the '/' page
  def get(self):
    logging.debug('Main')
    logging.error('Problem?')
    self.response.out.write('<html>')
    self.response.out.write('<head>')
    self.response.out.write(
    '<link rel=StyleSheet href="stylesheets/style.css">')
    self.response.out.write('</head>')
    self.response.out.write('<body>Existing Soundboards:<br>')

    soundboards = db.GqlQuery("SELECT * "
                         "FROM Soundboard "
                         "WHERE session_id = NULL "
                         "ORDER BY name DESC LIMIT 10")

    for soundboard in soundboards:
      self.response.out.write('<blockquote>'
      '<a href="/board/%s">' % soundboard.key().id())
      self.response.out.write('%s</a></blockquote>' % soundboard.name)

    self.response.out.write(
    '<br><form action="/board/" method="post">'
    'Create your own soundboard here.<br>'
    'Title:<input type="text" name="name"><br>'
    '<input type="submit" value="Create this Soundboard">'
    '</form>')
    self.response.out.write('<a href="instructions">How do I use this site?</a>'
    '</body></html>')

