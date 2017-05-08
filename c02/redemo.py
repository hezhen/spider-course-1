import re

pub_pattern = re.compile('^public$')

pub_pattern.match('public')

print re.findall('^..Yes\d{1,5}', 'okYes02bugfix')

print re.findall('^.?OK', 'OK.')