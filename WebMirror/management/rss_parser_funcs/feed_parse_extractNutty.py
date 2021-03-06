def extractNutty(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	if 'A Mistaken Marriage Match' in item['tags'] and 'a generation of military counselor' in item['tags']:
		return buildReleaseMessageWithType(item, 'A mistaken marriage match: A generation of military counselor', vol, chp, frag=frag, postfix=postfix)
	if 'A Mistaken Marriage Match' in item['tags'] and 'a-generation-of-military-counselor-' in item['linkUrl']:
		return buildReleaseMessageWithType(item, 'A mistaken marriage match: A generation of military counselor', vol, chp, frag=frag, postfix=postfix)
	if 'A Mistaken Marriage Match' in item['tags'] and 'Record of Washed Grievances Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'A mistaken marriage match: Record of washed grievances', vol, chp, frag=frag, postfix=postfix)
	if 'A Mistaken Marriage Match' in item['tags'] and 'record-of-washed-grievances' in item['linkUrl']:
		return buildReleaseMessageWithType(item, 'A mistaken marriage match: Record of washed grievances', vol, chp, frag=frag, postfix=postfix)
	if 'A Mistaken Marriage Match' in item['tags'] and 'the-general-only-fears-the-maidens-escape' in item['linkUrl']:
		return buildReleaseMessageWithType(item, 'A mistaken marriage match: The General Only Fears the Maiden\'s Escape', vol, chp, frag=frag, postfix=postfix)
	if 'A Mistaken Marriage Match' in item['tags'] and '/the-general-only-fear-the-maidens-escape-chapter' in item['linkUrl']:
		return buildReleaseMessageWithType(item, 'A mistaken marriage match: The General Only Fears the Maiden\'s Escape', vol, chp, frag=frag, postfix=postfix)
	if 'A Mistaken Marriage Match' in item['tags'] and '/destined-marriage-with-fragrance-chapter-' in item['linkUrl']:
		return buildReleaseMessageWithType(item, 'A mistaken marriage match: Destined Marriage With Fragrance', vol, chp, frag=frag, postfix=postfix)
		
		
		
		
	if 'Destined Marriages With Fragrance Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Destined Marriage with Fragrance', vol, chp, frag=frag, postfix=postfix)
		
	if item['tags'] == ['A Mistaken Marriage Match']:
		titlemap = [
			('DMSJ Chapter ',                             'A mistaken marriage match: Destined Marriage Of Shang Jun',      'translated'),
			('Destined Marriage Shang Jun: Chapter ',     'A mistaken marriage match: Destined Marriage Of Shang Jun',      'translated'),
			('Destined Marriage Of Shang Jun: Chapter ',  'A mistaken marriage match: Destined Marriage Of Shang Jun',      'translated'),
			('DMSJ: Ch ',                                 'A mistaken marriage match: Destined Marriage Of Shang Jun',      'translated'),
			('DMSJ: Chapter ',                            'A mistaken marriage match: Destined Marriage Of Shang Jun',      'translated'),
			('Destined Marriage With Fragrance ',         'A mistaken marriage match: Destined Marriage With Fragrance',    'translated'),
			('Tensei Shoujo no Rirekisho',                'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',                         'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False