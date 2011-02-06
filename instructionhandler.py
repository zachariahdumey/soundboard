# Copyright 2010
# cmcdonough@wustl.edu (Colin McDonough) zwdumey@wustl.edu (Zachariah Dumey)

from google.appengine.ext import webapp

class InstructionHandler(webapp.RequestHandler):
  # when the user clicks the "how do I use this site?" link the home page, we'll
  # give them instructions here
  def get(self):
    self.response.out.write(
    '<html><head><title>Instructions for 330 Soundboards</title>'
    '<link rel=stylesheet href="../stylesheets/style.css" /></head>'
    '<body><p>Welcome to 330 Soundboards! We you the ability to create your own'
    'soundboards and share them with others.</p>'
    '<p>To start the process, simply give your new soundboard a title from the '
    'home page. You will then be taken to the soundboard\'s page. From there, '
    'all you have to do is upload a sound, give it a name, and watch the magic '
    'happen. We automatically save all its revisions for you.</p>'
    '<p>When you\'ve finished creating your soundboard, you can share the link '
    'with your friends, and they\'ll only be able to play your soundboard. '
    'If you ever want to modify one of your soundboards (or someone else\'s!), '
    'simply click the "Copy this soundboard" button, and you will be given a '
    'copy of the soundboard that you can modify to your liking. Both the '
    'original and the copied soundboards will be saved.'
    '<br><a href="/">Ok! Get me started!</a>'
    '</body></html>'
    )
