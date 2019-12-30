def extractAsadatranslationsWordpressCom(item):
	'''
	Parser for 'asadatranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('npc town building game',                   'NPC Town-building Game',                   'translated'),
		('reader',                                   'reader',                                   'translated'),
		('horror game escape guide',                 'horror game escape guide',                 'translated'),
		('PRC',                                      'PRC',                                      'translated'),
		('i am a summoning master',                  'I am a Summoning Master',                  'translated'),
		('the villain happy being a father',         'The Villain is Happy being a Father',      'translated'),
		('Loiterous',                                'Loiterous',                                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if item['tags'] == ['Announcements']:
		titlemap = [
			('[ISM] Chapter ',   'I am a Summoning Master',                  'translated'),
			('[VHBF] Chapter ',  'The Villain is Happy being a Father',      'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False