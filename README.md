# Klippy #
A python program to parse Kindle clippings and import them into DevonThink

## Requirements: ##
py-appscript for importing to DevonThink

## Description: ##
My workflow when reading is if I like a passage, rather than highlighting it I select the content and I take a note on why I like the passage. This makes it easier to make sense of later and to make highlighting actually useful after you’ve done hundreds.

I have developed a group of tags to make this go quickly and to classify the information more readily.  They are based on what is accessible in the main keyboard view.  Tags thus all start with a period, and are the first thing (regex ^) in the note. I then write out four dots (“....”) with spaces on either side to distinguish my tags from what I want to say about the passage. This makes an easy marker to split the note into “tags here” and “notes there”.

### An example in context from my clippings: ###

    ==========
    Postwar: A History of Europe Since 1945 (Tony Judt)
    - Your Note Location 11839 | Added on Thursday, April 18, 2013 3:45:53 PM
    
    .int .... the social safety net can only be cut just so far  
    ==========
    Postwar: A History of Europe Since 1945 (Tony Judt)
    - Your Highlight Location 11836-11839 | Added on Thursday, April 18, 2013 3:45:53 PM
    
    Thus when Mrs. Thatcher and her successor John Major so much as hinted that they might begin privatizing the National Health Service or charging fees for state education, public support evaporated—among precisely those newly-prosperous but highly vulnerable sectors of the population that had been attracted to Thatcherism in the first place.  
    ==========  

In the above example, you can see a tag (“.int” for interesting) followed by a note.

The script loops through the My Clippings.txt file, breaks each note/highlight into blocks, and puts them into an array with the necessary fields (author, date, content, etc.).  The tags and notes are extracted from all “note”-type clippings and they are inserted into the next highlight's fields in the array (“tags”, “notes”).  The "Notes" data is not included in the array since it’s the same as the “Highlights” data.  This data is scrubbed and injection into a DevonThink database for storing, filtering, and especially connection-making by DevonThink's search engine.

The “My Clippings.txt” file itself is deleted to avoid duplicating clippings in your database at a later date (can be easily commented out in export-to-devonthink.py), and then stored in a zip file of clippings for backup.

### Potential issues ###

The parser is based on certain characters that the Kindle uses to format and separate parts of metadata. To get the title, it looks for all text until the first parenthesis "(", wherein traditionally the Kindle puts the author's name. If your book's title includes parentheses in the title, this will affect the parser. See this example from a book purchased from Amazon:

    Indignez-vous ! édition revue et augmentée (Ceux qui marchent contre le vent) (French Edition) (Hessel, Stéphane)
    - Your Note Location 149 | Added on Tuesday, May 7, 2013 11:11:09 AM

The parser will interpret the author of this book as "Ceux qui marchent contre le vent". At the moment I don't have a fix for this other than being cognizant of your book titles (most easily if you load them yourself via Calibre) and failing that by doing a search & replace beforehand. However, this is perhaps a rare occurence.

Another issue that can be seen is author formatting. In French, names can often be seen like this:

* "LASTNAME Firstname",
* "LASTNAME, Firstname",
* "Lastname, Firstname",
* "Firstname LASTNAME",
* or even "Firstname Lastname".

The parser takes whatever is in brackets as the name. I have only seen one instance of this name formatting in a Kindle book purchased from Amazon (though I've only had my Kindle for a month so I don't know if all French Amazon books are like this), so I'm not sure it's worth parsing out the comma and changing it to a traditional "Firstname Lastname" format. This may evolve.

### TODO ###

1. Write nosetests
