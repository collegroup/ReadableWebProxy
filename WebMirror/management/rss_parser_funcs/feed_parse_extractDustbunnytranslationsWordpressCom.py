def extractDustbunnytranslationsWordpressCom(item):
	'''
	Parser for 'dustbunnytranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('wushuang',       'Wushuang',                      'translated'),
		('huo luan jiang hu',       'huo luan jiang hu',                      'translated'),
		('jun you ji fou',       'How is the Gentleman Feeling?',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False