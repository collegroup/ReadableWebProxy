def extractProcrasTranslation(item):
	"""
	#'ProcrasTranslation'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Slowlife' in item['tags']:
		return buildReleaseMessageWithType(item, 'Tensei Shite Inaka de Slowlife wo Okuritai', vol, chp, frag=frag, postfix=postfix)
	return False
