def extractXcaliburwnCom(item):
	'''
	Parser for 'xcaliburwn.com'
	Seems to now be redirecting to http://restart-wn.com/
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessageWithType(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False