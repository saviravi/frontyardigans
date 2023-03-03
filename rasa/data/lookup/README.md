
This was the most straightforward way i found to use txt files in nlu

Make the name of the text file (entity name).txt and keep it under /lookup/input
in /lookup: run ```python3 convert.py``` and type in the entity name when prompted

Rasa recursively reads all yml files in the /data folder, so every yml file created will be used.