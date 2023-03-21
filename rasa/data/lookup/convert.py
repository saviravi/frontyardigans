import os
import re
#https://github.com/ChrisRahme/FYP-Chatbot/blob/main/data/lookups/txt_to_yml.py

entity = input('Enter entity name: ')

text  = 'version: "3.1"\n'
text += 'nlu:\n'
text += '  - lookup: {}\n'.format(entity)
text += '    examples: |\n'

with open(os.path.join(os.path.dirname(__file__), 'input/' + entity + '.txt'), 'r', encoding='utf-8') as f:
    for line in f:
        bad_chars = ['','\u008a'] # There is an invisible char here
        regex     = '|'.join(bad_chars)
        new_line  = re.sub(regex, '', line.strip())#.encode('utf-8').decode('utf-8')
        text += '      - ' + new_line + '\n'

with open(os.path.join(os.path.dirname(__file__), 'output/' + entity + '.yml'), 'w', encoding='utf-8') as f:
    f.write(text)
    print('Written to output/' + entity + '.yml')