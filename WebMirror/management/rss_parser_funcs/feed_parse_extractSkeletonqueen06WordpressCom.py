def extractSkeletonqueen06WordpressCom(item):
	'''
	Parser for 'skeletonqueen06.wordpress.com'
	'''


	badwords = [
			'Anime Ending Song',
			'Manhua',
			'Manga',
			'Doujinshi',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None



	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('akuyaku reijo',       'Akuyaku Reijo Nanode Rasubosu o Katte Mimashita',                      'translated'),
		('isekai torippu',      'Isekai Torippu Shita sono Baa De Taberarechaimashita',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False