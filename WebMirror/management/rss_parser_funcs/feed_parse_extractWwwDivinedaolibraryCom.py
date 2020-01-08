def extractWwwDivinedaolibraryCom(item):
	'''
	Parser for 'www.divinedaolibrary.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Ring That Defies The Heavens',                                      'The Mightiest System',                                              'translated'), 
		('The Mightiest System',                                                  'The Mightiest System',                                              'translated'), 
		('My Amazing WeChat is Connected to the Three Realms',                    'My Amazing WeChat is Connected to the Three Realms',                'translated'), 
		('Pivot of the Sky',                                                      'Pivot of the Sky',                                                  'translated'), 
		('live dungeon!',                                                         'live dungeon!',                                                     'translated'), 
		('rebuild world',                                                         'rebuild world',                                                     'translated'), 
		('Omni-Magician',                                                         'Omni-Magician',                                                     'translated'), 
		('the principle of a philosopher by eternal fool “asley”',                'the principle of a philosopher by eternal fool “asley”',            'translated'), 
		('Martial Peak',                                                          'Martial Peak',                                                      'translated'), 
		('Dragon\'s Soul',                                                        'Dragon\'s Soul',                                                    'oel'), 
		('Martial Family',                                                        'Martial Family',                                                    'oel'), 
		('Rise of the Three Gods',                                                'Rise of the Three Gods',                                            'oel'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False