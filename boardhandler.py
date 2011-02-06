# Copyright 2010
# cmcdonough@wustl.edu (Colin McDonough) zwdumey@wustl.edu (Zachariah Dumey)

from dbobjects import Soundboard
from dbobjects import SoundReference

import cgi
import logging
import random

from google.appengine.ext import db
from google.appengine.ext import webapp

# Handles rendering and creation of Soundboards
class BoardHandler(webapp.RequestHandler):
  # If a POST request is recieved,
  # creates a new soundboard with the given name
  # and redirects the user to the new board
  def post(self, something):
    soundboard = Soundboard()
    name = cgi.escape(self.request.get('name'))
    if name is None or len(name) == 0:
      name = 'Unnamed Soundboard'
    soundboard.name = name
    session_id = self.request.cookies.get('id')
    if session_id is None:
      handmade_key = db.Key.from_path(name, random.randint(0, 99999999))
      id = db.allocate_ids(handmade_key, 1)
      session_id = id[0]
      self.response.headers.add_header('Set-Cookie', 'id=%d' %
      session_id)
    else:
      session_id = long(session_id)
    soundboard.session_id = session_id
    db.put(soundboard)
    self.redirect('/board/%d' % soundboard.key().id())

 # Renders a Soundboard as an HTML page
  # If the user has a cookie with the same id as the creator of
  # the Soundboard (e.g. the user is the creator), the soundboard
  # is presented as editable (although the creator is checked
  # again before actually making changes
  def get(self, resource):

    if self.request.get('rerender') != '':
      rerender = long(self.request.get('rerender'))
    else:
      rerender = 0

    soundboard = Soundboard.get_by_id(long(resource))
    if soundboard is None:
      self.redirect('/')
      return
    if rerender != 1:
      self.response.out.write('<html>')
      self.response.out.write('<head>'
      '<script '
      'src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js" '
      'type="text/javascript"></script>'
      '<script '
      'src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/jquery-ui.min.js"'
      ' type="text/javascript"></script>'
      '<link '
      'href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/themes/dark-hive/jquery.ui.all.css" '
      'type="text/css" rel="stylesheet" />'
      '<link href="/stylesheets/style.css" type="text/css" rel="stylesheet" />'
      '<script '
      'src="https://github.com/ssoper/jquery-binaryUpload/raw/master/jquery.binaryUpload.js" '
      'type="text/javascript"></script>'
      '<script type="text/javascript" src="/js/boardPage1.js"></script>'
      )
      self.response.out.write('<title>%s</title>' % soundboard.name)
      self.response.out.write('</head>')
      self.response.out.write('<body><div id="soundboard">')

    self.response.out.write('<a href="/">330 Soundboards!</a><p>')

    # Copy button (public/private)
    self.response.out.write('<form action="/copy" method="post">'
    '<input type="hidden" name="soundboard_id" value="%d">'
    % soundboard.key().id())
    self.response.out.write('<input type="submit" '
    'value="Copy this Soundboard"></form>')

    if soundboard.session_id is not None and self.request.cookies.get('id') is not None:
      if long(soundboard.session_id) == long(self.request.cookies.get('id')): 
        # publish button (saves this soundboard to the public realm)
        # input is the soundboard ID to be retrieved by the publish handler
        # (only to be there if the user can edit)
        self.response.out.write(
        '<form action="/save" method="post">'
        '<input type="hidden" name="soundboard_id" value="%d">'
        % soundboard.key().id())
        self.response.out.write('<input type="submit" value="Publish!"></form>')
        
        # delete button allows for deletion of the user owned board    
        self.response.out.write(
        '<form action="/delete" method="post">'
        '<input type="hidden" name="soundboard_id" value="%d">'
        % soundboard.key().id())
        self.response.out.write('<input type="submit" '
        'value = "Delete this Board!"></form>') 

    self.response.out.write('<p>Cookies: %s</p>'
    % self.request.cookies.get('id'))
    self.response.out.write('Soundboard session_id: %s'
    % soundboard.session_id)
    self.response.out.write('<div id="boarddiv"><ul id="sortable">')

    # Create a sorted list of the sound_references
    sound_references = []
    for sound_reference_key in soundboard.sound_references:
      sound_references.append(
      SoundReference.get_by_id(sound_reference_key.id()))
    sound_references_sorted = sorted(
    sound_references, key=lambda sound_reference: sound_reference.sort_index)
    for sound_reference in sound_references_sorted:
      sound = sound_reference.reference
      self.response.out.write(
      '<li name="sound" id="sound_%s">/sound/%d<p>'
      % (sound_reference.key().id(), sound_reference.key().id()) )
      # This button is the left part of the multipart button
      # It displays the sound's given name
      # Clicking it will play the sound
      self.response.out.write(
      '<button id="play_%s" name="sound_button" class="sound_button" '
      'label="%s" '
      'onClick="soundPlay(\'%s\')" >%s</button>'
      % (sound_reference.key().id(), sound_reference.name, sound.key(),
      sound_reference.name))
      # This is the edit button, which is the right part of the multipart button
      # It is referenced by name in the javascript instead of with .next()
      self.response.out.write(
      '<button id="edit_%s" name="button_edit_sound"></button>'
      % sound_reference.key().id() )
      # This is the hidden input which later appears in a dialog box
      self.response.out.write(
      '<div id="name_dialog_%s" name="name_dialog"><input type="text" '
      'name="new_name" id="name_%s"></div>'
      % (sound_reference.key().id(), sound_reference.key().id()))
      self.response.out.write('</li>')

    session_id = self.request.cookies.get('id')
    if session_id == self.request.cookies.get('id'):
      self.response.out.write(
      '<li name="sound">No Sound... Yet<p>')

      # This button is an empty name; the left part of a multipart jquery button
      self.response.out.write(
      '<button id="empty_sound" class="sound_button">&nbsp;</button>')

      # This is the add button, which is the right part of a multipart button.
      # When clicked, it opens a dialog which contains a file upload input.
      self.response.out.write(
      '<button id="add_sound_button"></button>')

      # This is the hidden input which later appears in a dialog box
      self.response.out.write(
      '<div id="add_sound_dialog">'
      '<input type="file" id="upload_file" name="file">'
      '<input type="hidden" id="board_id" name="board_id" value="%d">'
      '</div>'
      % soundboard.key().id())

    self.response.out.write('</ul></div>')

    # Start the soundboard author's section
    if session_id is not None:
      if soundboard.session_id == long(session_id):
        # This is the opening tag for the author div (things which only appear
        # for the author of a particular soundboard)
        self.response.out.write(
        '<div id="author_div">')

        # This button is the left part of the multipart button
        # It displays the soundboard's given name
        # Clicking it will do nothing
        self.response.out.write(
        '<button id="board_name_button" class="board_name_button" '
        'label="%s">%s</button>'
        % (soundboard.name, soundboard.name))
        # This is the edit button, which is the right part of the multipart
        # button. It is referenced by name in the javascript instead of with
        # .next()
        self.response.out.write(
        '<button id="edit_name_button"></button>')
        # This is the hidden input which later appears in a dialog box
        self.response.out.write(
        '<div id="board_name_dialog" name="board_name_dialog">'
        '<input type="text" name="new_board_name" id="new_board_name">'
        '<input type="hidden" id="soundboard_id" value="%d"'
        '</div>'
        % soundboard.key().id())

        # Close the author div
        self.response.out.write(
        '</div>')
    if soundboard.session_id is None:
      self.response.out.write('This is a public (read-only) Soundboard')

    if rerender != 1:
      self.response.out.write('</div></body></html>')
