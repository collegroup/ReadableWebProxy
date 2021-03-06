def extractCwastranslationsWordpressCom(item):
	'''
	Parser for 'cwastranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('tsifb',                                                            'Transmigrated into a School Idol and Forced to Do Business',                      'translated'),
		('transmigrated into a school idol and forced to do business',       'Transmigrated into a School Idol and Forced to Do Business',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False