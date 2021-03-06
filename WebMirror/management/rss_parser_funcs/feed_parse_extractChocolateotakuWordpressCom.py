def extractChocolateotakuWordpressCom(item):
	'''
	Parser for 'chocolateotaku.wordpress.com'
	'''
	
	
	badwords = [
			'Rant',
			'Rants',
			'review',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None



	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('ihha',       'Quick Wear: I Have a Heroine Aura',                      'translated'),
		('ccgdd',      'Civil Servant Gets a Gentle Dream',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False