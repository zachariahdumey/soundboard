# Copyright 2010
# cmcdonough@wustl.edu (Colin McDonough), zwdumey@wustl.edu (Zachariah Dumey)

import logging
import main

from google.appengine.ext import db

# Sound stores an id, a name, and a reference to a stored sound file
class Sound(db.Model):
  sound_file = db.BlobProperty()
  mime_type = db.StringProperty()
  reference_count = db.IntegerProperty()

  def incrementReferenceCount(sound_key):
    db.run_in_transaction(Sound.private_increment_counter, sound_key)

  def private_increment_counter(sound_key):
    sound = sound_key#Sound.get_by_id(sound_key.id())
    sound.reference_count = sound.reference_count + 1
    logging.info('incremented reference_count of sound id %s to %s'
    % (sound_key, sound.reference_count))
    db.put(sound)

# Store a reference to a sound file. Also store the name
class SoundReference(db.Model):
  id = db.IntegerProperty()
  reference = db.ReferenceProperty()
  name = db.StringProperty()
  sort_index = db.IntegerProperty()

  def copy(other):
    soundReference = SoundReference()
    soundReference.id = other.id
    soundReference.reference = other.reference
    Sound.incrementReferenceCount(soundReference.reference)
    soundReference.name = other.name
    soundReference.sort_index = other.sort_index
    return soundReference

# Soundboard is the model of a soundboard
# It holds an id, a list of references to Sound objects, a name,
# and the session_id of its creator
class Soundboard(db.Model):
  id = db.IntegerProperty()
  sound_references = db.ListProperty(db.Key)
  name = db.StringProperty()
  session_id = db.IntegerProperty()

  def copy(other):
    soundboard = Soundboard()
    soundboard.id = other.id
    # TODO: Deep copy sounds
    for soundReferenceKey in other.sound_references:
      soundReference = SoundReference.get_by_id(soundReferenceKey.id())
      soundReferenceCopy = SoundReference.copy(soundReference)
      db.put(soundReferenceCopy)
      soundboard.sound_references.append(soundReferenceCopy.key())
    soundboard.name = other.name
    soundboard.session_id = other.session_id
    return soundboard


  '''
    only copy sounds and get a random id for the board (allows for saving a 
    board explicitly)
  '''
  def copy_sounds_only(other): 
    soundboard = Soundboard()
    soundboard.id = main.newSessionId() 
    soundboard.session_id = None
    # TODO: Deep copy sounds
    for soundReferenceKey in other.sound_references:
      soundReference = SoundReference.get_by_id(soundReferenceKey.id())
      soundReferenceCopy = SoundReference.copy(soundReference)
      db.put(soundReferenceCopy)
      soundboard.sound_references.append(soundReferenceCopy.key())
    soundboard.name = other.name
    return soundboard
	

