def extractTeaquilashotWordpressCom(item):
	'''
	Parser for 'teaquilashot.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('A Love So Beautiful (致我们单纯的小美好)',  'A Love So Beautiful',                           'translated'),
		('Tensei Shoujo no Rirekisho',                'Tensei Shoujo no Rirekisho',                    'translated'),
		('Master of Dungeon',                         'Master of Dungeon',                             'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	tagmap = [
		('A Love So Beautiful',       'A Love So Beautiful',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False