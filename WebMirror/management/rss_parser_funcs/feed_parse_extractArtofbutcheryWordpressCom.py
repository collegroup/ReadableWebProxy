def extractArtofbutcheryWordpressCom(item):
	'''
	Parser for 'artofbutchery.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if "VRMMO Chef" in item['tags']:
		return buildReleaseMessageWithType(item, "VRMMO Chef", vol, chp, frag=frag, postfix=postfix)

	return False