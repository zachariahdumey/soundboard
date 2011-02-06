# Copyright 2010
# cmcdonough@wustl.edu (Colin McDonough) zwdumey@wustl.edu (Zachariah Dumey)

from dbobjects import Soundboard
from dbobjects import SoundReference

import logging

from google.appengine.ext import db
from google.appengine.ext import webapp

class EditOrderHandler(webapp.RequestHandler):
  def update_index(self, sound_reference_id, index):
     sound_reference = SoundReference.get_by_id(sound_reference_id)
     if sound_reference is None:
       logging.error('166 == 166: %s' % (long(156) == sound_reference_id))
       logging.error('Could not get SoundReference with id %d'
       % sound_reference_id)
       return
     sound_reference.sort_index = index
     db.put(sound_reference)

  def post(self, resource=None):
    # TODO: Limit access based on cookies
    soundboard_id = self.request.get('soundboard_id')
    soundboard = Soundboard.get_by_id(long(soundboard_id))

    if soundboard is None:
      self.error(500)
      logging.error('While updating order, could not find SoundBoard with id %s'
      % soundboard_id)
      return

    logging.debug('EditOrderHandler invoked for soundboard id %s'
    % soundboard_id)
    serialized_ids = self.request.get('serialized_ids')
    logging.error('serialized_ids: %s' % serialized_ids)
    ordered_list = serialized_ids.split('&')
    order_dictionary = {}
    index = 0
    for key_pair_string in ordered_list:
      key_value = key_pair_string.split('[]=')
      order_dictionary[long(key_value[1])] = index
      index += 1

    for sound_reference_key in soundboard.sound_references:
      if (sound_reference_key.id()) in order_dictionary:
        try:
          index = int(order_dictionary[sound_reference_key.id()])
        except ValueError:
          index = 0
        db.run_in_transaction(self.update_index,
        long(sound_reference_key.id()), index)
      else:
        logging.error('While updating order, could not find SoundReference '
        'with id %d in serialized_ids' % (sound_reference_key.id()))
