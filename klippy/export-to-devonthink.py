from appscript import *
import zipfile
import parser, archive_clippings

# =============================
# Script variables

path_to_clippings = '/Users/zach/Desktop/My Clippings.txt'
# path_to_clippings = '/Volumes/Kindle/documents/My Clippings.txt'
path_to_devon_db = 'x-devonthink-item://34310C73-BA49-4713-8CF1-0E12384642B7' # My "Reading Notes" folder in my "Research" Devonthink db
# path_to_devon_db = 'x-devonthink-item://9211E9D3-B3C8-4548-A2E5-EA5F43486827' # Testing db
path_to_backup = '/Users/zach/Dropbox/Apps/klippy/clippings_backup.zip'

# =============================
# Open and parse clippings

parsed_data = parser.parse(path_to_clippings)
joined_highlights = [] # My new array for only the highlights
parser.join_notes(parsed_data, joined_highlights)

# =============================
# Open DevonThink and relevant DB

dev_pro = app(u'DEVONthink Pro')

dev_pro.database.close #close whichever database is open
dev_pro.open_database(path_to_devon_db)
current_db = dev_pro.current_database

# =============================
# Add clippings to DevonThink

for clipping in joined_highlights:
    
    book_title = clipping['title'].decode('utf-8')
    highlight = clipping['highlight'].decode('utf-8')
    note = clipping['note'].decode('utf-8')
    author = clipping['author'].decode('utf-8')
    date = clipping['date']
    tags = clipping['tag']

    comment_titles = {
        'comments' : 'Thoughts',
        'economics' : 'Econ',
        'disenfranchisement' : 'Dis-Vote',
        'history' : 'History',
        'interesting' : 'Interesting',
        'legal' : 'Judicial',
        'more attention' : 'Investigate',
        'motif' : 'Motif',
        'politics' : 'Politics',
        'quotable' : 'Quotable',
        'race' : 'Race',
        'research ideas' : 'Research ideas',
        'resource' : 'Resource',
        'restrictions' : 'Restrict-Vote',
        'society' : 'Society',
        'supreme court' : 'Supreme Court',
        'statistics' : 'Statistics',
        'theme' : 'Theme',
        'voting' : 'Voting',
    }

    def format_devonthink_name():
        if tags[0] != 'kindle' and note != '':
            return comment_titles[tags[0]] + ': ' '"' + note + '"'
        elif note != '':
            return 'Thoughts: ' + '"' + note + '"'
        else:
            return 'Fact: ' + highlight


    folder = current_db.create_location('Reading notes/' + book_title + ' (' + author + ')')
    
    record = current_db.create_record_with({
        k.creation_date: date,
        k.rich_text: highlight if clipping['note'] == '' else highlight + '\n\n' + 'Notes:' + '\n\n' + note,
        k.type: k.rtf,
        k.name: format_devonthink_name(),
        k.tags: tags,
        },
        in_ = folder)

    print "Created one record for: " + book_title

# =============================
# Rename and archive "My Clippings.txt" to zip file

archive_clippings.archive_clippings(path_to_backup, path_to_clippings)
archive_clippings.remove_clippings(path_to_clippings)
archive_clippings.print_info(path_to_backup)