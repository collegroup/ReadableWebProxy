def extractChiisaiHimeDreamwidthOrg(item):
	'''
	Parser for 'chiisai-hime.dreamwidth.org'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('the villains all fell in love with me',       'the villains all fell in love with me',                      'translated'),
		('phantom skeleton painting',                   'Phantom Skeleton Painting',                                  'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False