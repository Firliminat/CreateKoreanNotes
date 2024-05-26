DEFAULT_NOTE_TYPE = 'Korean Words Type Answer'
DEFAULT_DECK = 'Coréen::Vocabulaire'

DEFAULT_ATTRIBUTE_LIST_MAPPING = {
  'guid': 0,
  'notetype': 1,
  'deck': 2,
  'korean': 3,
  'french': 4,
  'sound': 5,
  'precision': 6,
  'context': 7,
  'tags': 8,
}

class Note:
  def __init__(
      self,
      guid: str = '',
      notetype: str = DEFAULT_NOTE_TYPE,
      deck: str = DEFAULT_DECK,
      korean: str = '',
      french: str = '',
      sound: str = '',
      precision: str = '',
      context: str = '',
      tags: str = ''
  ):
    self.guid = guid
    self.notetype = notetype
    self.deck = deck
    self.korean = korean
    self.french = french
    self.sound = sound
    self.precision = precision
    self.context = context
    self.tags = tags

  @classmethod
  def from_list(cls, row: list[str], mapping: dict[str, int]=DEFAULT_ATTRIBUTE_LIST_MAPPING):
    new_note = cls()
    for attr, idx in mapping.items():
      setattr(new_note, attr, row[idx])
    
    return new_note
  
  def to_list(self, mapping: dict[str, int]=DEFAULT_ATTRIBUTE_LIST_MAPPING) -> list[str]:
    new_list = [None] * (max(mapping.values()) + 1)
    for attr, idx in mapping.items():
      new_list[idx] = getattr(self, attr)
    
    return new_list