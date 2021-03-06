def extractEmmaFanmilyOrg(item):
	'''
	Parser for 'emma.fanmily.org'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Legend of Concubine’s Daughter Minglan (The Story of Minglan)',       'The Legend of the Concubine\'s Daughter Minglan',                      'translated'),
		('Minglan',                                                             'The Legend of the Concubine\'s Daughter Minglan',                      'translated'),
		('History’s Strongest Senior Brother',                                  'History’s Strongest Senior Brother',                                   'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False