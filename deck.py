import csv
from notes import Note


DEFAULT_ANKI_CSV_HEADER_LINES = [
  '#separator:tab',
  '#html:true',
  '#guid column:1',
  '#notetype column:2',
  '#deck column:3',
  '#tags column:9'
]

class Deck(dict[str, Note]):
  def __init__(self, *arg, **kw):
    super(Deck, self).__init__(*arg, **kw)

  def update(self, new_note: Note):
    new_note_id = new_note.guid
    if new_note_id is None or new_note_id == '':
      new_note_id = new_note.korean
    self[new_note_id] = new_note

  @classmethod
  def from_csv_file(
    cls,
    file_name: str,
    header_marker: str = '#',
    newline: str = '\n',
    delimiter: str = '\t',
    quotechar:str = '"'
  ) -> tuple[list[Note], list[str]]:
    new_deck: cls

    with open(file_name, newline=newline) as csv_file:
      input_reader = csv.reader(
        csv_file,
        delimiter=delimiter,
        quotechar=quotechar
      )

      # Skipping header lines
      cursor_pos = csv_file.tell()
      header_lines = []
      while True:
        new_line = csv_file.readline()
        if new_line.startswith(header_marker):
          cursor_pos = csv_file.tell()
          header_lines.append(new_line.strip())
        else:
          break
      csv_file.seek(cursor_pos)
      
      for row in input_reader:
        new_note = Note.from_list(row)
        new_deck.update(new_note)
    
    return new_deck, header_lines

  def to_csv_file(
    self,
    file_name: str,
    header_lines = DEFAULT_ANKI_CSV_HEADER_LINES,
    newline='\n',
    delimiter='\t',
    quotechar='"'
  ):
    with open(file_name, 'w', newline=newline) as csv_file:
      output_writer = csv.writer(
        csv_file,
        delimiter=delimiter,
        quoting=csv.QUOTE_ALL,
        quotechar=quotechar
      )
      csv_file.write(newline.join(header_lines) + newline)
      for _, note in self.items():
        output_writer.writerow(note.to_list())
  
  def has_korean(self, note: str | Note) -> bool:
    cmp_val = note
    if note is Note:
      cmp_val = note.korean
    
    return next(
      (deck_note for deck_note in self.values()
       if deck_note.korean == cmp_val),
      None
    ) is not None
  
  def has_french(self, note: str | Note) -> bool:
    cmp_val = note
    if note is Note:
      cmp_val = note.french
    
    return next(
      (deck_note for deck_note in self.values()
       if deck_note.french == cmp_val),
      None
    ) is not None