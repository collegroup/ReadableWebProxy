def extractIcedlattenoiceWordpressCom(item):
	'''
	Parser for 'icedlattenoice.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('pancake cart',           'pancake cart',                          'translated'),
		('find my bearings',       'find my bearings',                      'translated'),
		('jiang jiu',              'jiang jiu',                             'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False