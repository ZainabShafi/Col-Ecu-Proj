11/1/2024 - Kyle McDaniel

Any data contained here at the moment isn't novel, so it's a decent example of what
has been accomplished thus far.

database_reference_creator : creates a postgres SQL. My idea is for it to eventually
build the entirety of our backend and fill it with data with date records, and 
that is the direction I've been buidling it in.

pdf_extractor : does nothing of value yet, but I want to be able to parse
pdf files with it. Just a placeholder.

un_api_extractor : my various attempts at extracting data from the API 
managed by the United Nations. Never got it to work, but it likely is easier than I
found.

un_selenium_data_cleaner : cleans data and merges to a single .csv (see below).

un_selenium_extractor : this goes in with minimal supervison, downloads all
of the files for a given country, and deposits them in a given 
folder (un_selenium_rip_files). VERY shoddy, but hopefully not permenant. Needed
some data to work with.

Serious work in progress. This is a quick explanation.

Database code is mostly working, but it is still being built out. The rest is iffy.