
import abc
import string
import re
import semantic.numbers
import traceback

POSTFIX_KEYS = [
		'prologue',
		'afterword',
		'epilogue',
		'interlude',
		'foreword',
		'appendix',
		'intermission',
		'sidestory',
		'side story',
		'extra',
		'illustrations',
	]

# Order matters! Items are checked from left to right.
VOLUME_KEYS_GLOBAL   = [
		'volume',
		'season',
		'book',
		'vol',
		'vol.',
		'arc',
		'v',
		'b',
		's',
	]


FRAGMENT_KEYS_GLOBAL = [
		'part',
		# 'episode',
		'pt',
		'part',
		'parts',
		'page',
		'p',
		'pt.',
	]

CHAPTER_KEYS_GLOBAL  = [
		'chapter',
		'chapters',
		'chp',
		'ch',
		'c',
	]

POSTFIX_SPLITS = [
		'-',
		'–',  # FUCK YOU UNICODE
		':',
	]

# Additional split characters
SPLIT_ON = [
		"!",
		")",
		"(",
		"[",
		"]",

		# Fucking quotes
		':',
		'"',
		'/',
		'\\',
	]

class NumberConversionException(Exception):
	pass

################################################################################################################################
################################################################################################################################
################################################################################################################################

def intersperse(iterable, delimiter):
	it = iter(iterable)
	yield next(it)
	for x in it:
		yield delimiter
		yield x

class SplitterBase(object):
	__metaclass__ = abc.ABCMeta

	def process(self, inarr):
		if isinstance(inarr, str):
			tmp = self.split_component(inarr)
			assert isinstance(tmp, (list, tuple))
			return tmp
		elif isinstance(inarr, (list, tuple)):
			ret = []
			for chunk in inarr:
				if isinstance(chunk, TokenBase):
					ret.append(chunk)
				else:
					tmp = self.split_component(chunk)
					assert isinstance(tmp, (list, tuple))
					[ret.append(subcmp) for subcmp in tmp]
			return ret

	@abc.abstractmethod
	def split_component(self, instr):
		pass

class SpaceSplitter(SplitterBase):
	def split_component(self, instr):
		return list(intersperse(instr.split(" "), " "))

class CharSplitter(SplitterBase):
	def split_component(self, instr):
		ret = []
		agg = ""
		for letter in instr:
			if letter in SPLIT_ON:
				if agg:
					ret.append(agg)
					agg = ""
				ret.append(letter)
			else:
				agg += letter
		if agg:
			ret.append(agg)
		return ret


class LetterNumberSplitter(SplitterBase):
	def split_component(self, instr):

		splits = [
			re.compile(r"([a-z]+)(\.?)([0-9]+)", re.IGNORECASE),
			re.compile(r"([0-9]+)(\.?)([a-z]+)", re.IGNORECASE),
		]
		for split in splits:
			match = split.fullmatch(instr)
			# print((split, match, instr))
			if match:
				return list(match.groups())
				# print("Match:", match, match.groups())

		return [instr]

class HyphenatedLetterSplitter(SplitterBase):
	def split_component(self, instr):

		splits = [
			re.compile(r"([a-z]+)(\-)([a-z]+)", re.IGNORECASE),
			re.compile(r"([a-z]+)(\-)([a-z]+)", re.IGNORECASE),
		]
		for split in splits:
			match = split.fullmatch(instr)
			if match:
				return list(match.groups())
				# print("Match:", match, match.groups())

		return [instr]

class NonNumericDecimalSplitter(SplitterBase):
	def split_component(self, instr):
		ret = []
		agg = ""
		prev = None
		# print("Splitting: '%s'" % instr)
		for letter in instr:
			if (prev and
					(
							prev in string.digits and letter not in string.digits
						or
							letter in string.digits and prev not in string.digits
						)):

				if prev.lower() == "r":
					# print("Not splitting (1):", letter, prev)
					prev = letter
					agg += letter

				# Don't split on letter-decimal sequences
				elif (
						(prev.lower() in string.digits and letter.lower() == ".")
						or
						(letter.lower() in string.digits and prev.lower() == ".")
						):
					# print("Not splitting (2):", letter, prev)
					prev = letter
					agg += letter
				else:
					if agg:
						ret.append(agg)
						agg = ""
					agg += letter
					# ret.append(letter)
					# print("Splitting, ", letter, prev)
					prev = letter
			else:
				# print("Not splitting (3):", (letter, prev, agg))
				prev = letter
				agg += letter

		# print("End: ", (ret, agg))
		if agg:
			ret.append(agg)
		# print("Split: '%s'" % ret)
		return ret

#############################

################################################################################################################################
################################################################################################################################
################################################################################################################################

class TokenBase(object):
	def __init__(self, prefix, intermediate, content):
		self.prefix       = prefix
		self.intermediate = intermediate
		self.content      = content

	def string(self):
		return self.content

	def __repr__(self):
		# print("Token __repr__ call!")
		ret = "<{:14} - contents: '{}' '{}' '{}'>".format(self.__class__.__name__, self.prefix, self.intermediate, self.content)
		return ret


class DateTextToken(TokenBase):
	def __init__(self, content):
		self.content      = content

	def __repr__(self):
		# print("Token __repr__ call!")
		ret = "<{:14} - contents: '{}'>".format(self.__class__.__name__, self.content)
		return ret

class FreeTextToken(TokenBase):
	def __init__(self, content):
		self.content      = content

	def __repr__(self):
		# print("Token __repr__ call!")
		ret = "<{:14} - contents: '{}'>".format(self.__class__.__name__, self.content)
		return ret

class NumericToken(TokenBase):

	def __repr__(self):
		# print("Token __repr__ call!")
		ret = "<{:14} - contents: '{}' '{}' '{}' (numeric: {}, ascii: {}, parsed: {}>".format(self.__class__.__name__,
			self.prefix,
			self.intermediate,
			self.content,
			self.is_decimal(),
			self.is_ascii(),
			self.to_number(tok_text=self.content, parse_ascii=True) if self.is_ascii() else 'No'
			)
		return ret

	def to_number(self, tok_text=None, parse_ascii=False):
		if tok_text is None:
			tok_text = self.content

		if not tok_text:
			raise NumberConversionException("Failed to convert '%s' to a number!" % (tok_text, ))
		# Handle strings with multiple decimal points, e.g. '01.05.15'
		if tok_text.count(".") > 1:
			raise NumberConversionException("Failed to convert '%s' to a number! Too many decimal points" % (tok_text, ))

		# NumberService() for some reason converts "a" to "one", which fucks everything up.
		# Anyways, if the token is "a", stop it from doing that.
		if tok_text.strip().lower() == 'a':
			raise NumberConversionException("Failed to convert '%s' to a number!" % (tok_text, ))

		# Make sure we have at least one digit
		if not parse_ascii and not any([char in '0123456789' for char in tok_text]):
			raise NumberConversionException("Failed to convert '%s' to a number! No numbers, and not trying to parse ascii numbers" % (tok_text, ))

		if all([char in '0123456789.' for char in tok_text]) and any([char in '0123456789' for char in tok_text]):
			return float(tok_text)

		if parse_ascii:
			# return float(tok_text)
			val = self.ascii_numeric(tok_text)
			# print("Ascii_numeric call return: ", val)
			if val != False:
				return val

			raise NumberConversionException("Call assumes '%s' is numeric, and it's not." % (tok_text))
			# assert self.is_valid(), "getNumber() can only be called if the token value is entirely numeric!"


		raise NumberConversionException("Failed to convert '%s' to a number!" % (tok_text, ))



	def is_valid(self, parse_ascii):
		'''
		Does the token contain a value that could (probably) be
		converted to an integer without issue.

		TODO: just use try float(x)?
		'''

		try:
			self.to_number(tok_text=self.content, parse_ascii=parse_ascii)
			return True
		except NumberConversionException:
			return False

	def is_decimal(self):
		try:
			self.to_number(tok_text=self.content, parse_ascii=False)
			return True
		except NumberConversionException:
			return False

	def is_ascii(self):
		return self.ascii_numeric(self.content) is not False

	def ascii_numeric(self, content):

		bad_chars = [":", ";", ",", "[", "]"]
		for bad_char in bad_chars:
			if bad_char in content:
				content = content.split(bad_char)[0]

		# text-to-number library does stupid things with "a" or "A" (converts them to 1)
		content = content.split(" ")
		if "a" in content: content.remove("a")
		if "A" in content: content.remove("A")
		content = " ".join(content)


		# Spot-patching to fix data corruption issues I've run into:

		content = content.replace("”", "")
		content = content.strip()
		# print("AsciiNumeric concatenated string: '%s'" % content)
		while content:
			try:
				# print("Parsing '%s' for numbers" % content)
				ret = semantic.numbers.NumberService().parse(content)
				# print("parsed: ", ret)
				# print(traceback.print_stack())
				return ret
			except semantic.numbers.NumberService.NumberException:
				# print("Failed to parse: ", content)
				try:
					# Try again with any trailing hyphens removed
					# semantic assumes "twenty-four" should parse as "twenty four".
					# this is problematic when you have "chapter one - Thingies", which
					# tries to parse as "one - thingies", and fails.
					# However, we only want to invoke this fallback if
					# we can't parse /with/ the hyphen, as lots of sources actually do release
					# as "twenty-four"
					if "-" in content:
						content = content.split("-")[0].strip()
						val = semantic.numbers.NumberService().parse(content)
						return val

					# It also mangles trailing parenthesis, for some reason.
					if ")" in content or "(" in content:
						content = content.split(")")[0].split("(")[0].strip()
						val = semantic.numbers.NumberService().parse(content)
						return val


				except semantic.numbers.NumberService.NumberException:
					pass

				# print("Parse failure!")
				# traceback.print_exc()
				if not " " in content:
					# print("Parse failure?")
					return False
				content = content.rsplit(" ", 1)[0]
		# print("Parse reached end of buffer without content")
		return False



class VolumeToken(NumericToken):
	pass
class ChapterToken(NumericToken):
	pass
class FreeChapterToken(NumericToken):
	pass
class FragmentToken(NumericToken):
	pass

class CompoundToken(NumericToken):

	def __init__(self, prefix, intermediate, component_1, spacer, component_2):
		self.prefix       = prefix
		self.intermediate = intermediate
		self.component_1  = component_1
		self.spacer       = spacer
		self.component_2  = component_2

	def string(self):
		return self.component_1+self.spacer+self.component_2
	def string_1(self):
		return self.component_1
	def string_2(self):
		return self.component_2

	def is_valid_1(self, parse_ascii):
		try:
			self.to_number(tok_text=self.component_1, parse_ascii=parse_ascii)
			return True
		except NumberConversionException:
			return False

	def is_valid_2(self, parse_ascii):
		try:
			self.to_number(tok_text=self.component_2, parse_ascii=parse_ascii)
			return True
		except NumberConversionException:
			return False

	def to_number_1(self, parse_ascii):
		return self.to_number(tok_text=self.component_1, parse_ascii=parse_ascii)

	def to_number_2(self, parse_ascii):
		return self.to_number(tok_text=self.component_2, parse_ascii=parse_ascii)


	def __repr__(self):
		# print("Token __repr__ call!")
		ret = "<{:14} - contents: '{}' '{}' '{}' '{}' '{}'>".format(self.__class__.__name__, self.prefix, self.intermediate, self.component_1, self.spacer, self.component_2)
		return ret

class CompoundVolChapterToken(CompoundToken):

	def valid_volume(self, parse_ascii):
		return self.is_valid_1(parse_ascii)
	def valid_chapter(self, parse_ascii):
		return self.is_valid_2(parse_ascii)

	def get_volume(self, parse_ascii):
		return self.to_number_1(parse_ascii)
	def get_chapter(self, parse_ascii):
		return self.to_number_2(parse_ascii)

class CompoundChapterFragmentToken(CompoundToken):

	def valid_chapter(self, parse_ascii):
		return self.is_valid_1(parse_ascii)
	def valid_fragment(self, parse_ascii):
		return self.is_valid_2(parse_ascii)

	def get_chapter(self, parse_ascii):
		return self.to_number_1(parse_ascii)
	def get_fragment(self, parse_ascii):
		return self.to_number_2(parse_ascii)

################################################################################################################################
################################################################################################################################
################################################################################################################################


# !?^%!$,
# !?^%!$,!

# class Token(object):
class GlobBase(object):
	__metaclass__ = abc.ABCMeta

	def get_preceeding_text(self, prefix_arr):
		intermediate = ""
		consumed = 0

		# print("Get preceeding text:", prefix_arr)
		for idx in range(len(prefix_arr)-1, 0-1, -1):
			if isinstance(prefix_arr[idx], TokenBase):
				# print("Get preceeding text returning:", (prefix_arr[:idx+1], None, intermediate))
				return prefix_arr[:idx+1], None, intermediate
			if all([char in string.punctuation+string.whitespace for char in prefix_arr[idx]]):
				intermediate = prefix_arr[idx] + intermediate
				consumed += 1
			else:
				# print("Get preceeding text returning:", (prefix_arr[:idx], prefix_arr[idx], intermediate))
				return prefix_arr[:idx], prefix_arr[idx], intermediate

		# print("get_preceeding_text", ([], None, intermediate))
		return [], None, intermediate

	def process(self, inarr):
		# print("Globber processing", inarr)
		assert isinstance(inarr, (list, tuple))
		negoff = 0
		original_length = len(inarr)
		for idx in range(original_length):
			locidx = idx - negoff

			# if inarr[locidx] == '24':
			# print("%s Passed: " % self.__class__.__name__, (inarr, ))
			before, target, after = self.attach_token(inarr[:locidx], inarr[locidx], inarr[locidx+1:])
			# if inarr[locidx] == '24':
			# 	print("%s Returning: " % self.__class__.__name__, (before, target, after))
			inarr = before
			if target:
				inarr = inarr + [target]
			if len(after):
				inarr = inarr + after

			negoff = original_length - len(inarr)
			# print("Globber step", inarr)

		# print("Globber return", inarr)
		return inarr

	@abc.abstractmethod
	def attach_token(self, before, target, after):
		raise RuntimeError("This should never be called!")


class VolumeChapterFragGlobber(GlobBase):


	VOLUME_KEYS   = VOLUME_KEYS_GLOBAL
	FRAGMENT_KEYS = FRAGMENT_KEYS_GLOBAL
	CHAPTER_KEYS  = CHAPTER_KEYS_GLOBAL

	ALLOWABLE_INTERMEDIATE_CHARS = [
		" ",
		".",
		":",
	]

	def attach_token(self, before, target, after):
		# print("AttachToken: ", (before, target, after))
		# if len(after) == 3:
		# 	target = before[-1] + target
		# 	before = before[:-1]


		before, prec, intervening = self.get_preceeding_text(before)
		# if target == '24':
		# 	print("(attach_token) Getting text preceding '%s' (%s)" % (target, type(target)))
		# 	print("(attach_token) Text '%s' '%s' '%s' " % (before, prec, intervening))

		if target in self.ALLOWABLE_INTERMEDIATE_CHARS or not isinstance(target, str):
			if prec:
				before.append(prec)
			if intervening:
				before.append(intervening)
		else:

			clstype = None
			if prec and prec.lower() in self.VOLUME_KEYS:
				clstype = VolumeToken
			elif prec and prec.lower() in self.CHAPTER_KEYS:
				clstype = ChapterToken
			elif prec and prec.lower() in self.FRAGMENT_KEYS:
				clstype = FragmentToken

			if clstype:
				tmp = clstype(prec, intervening, target)
				if tmp.is_decimal():
					target = tmp
				else:
					if prec:
						before.append(prec)
					if intervening:
						before.append(intervening)

			else:
				if prec:
					before.append(prec)
				if intervening:
					before.append(intervening)

		return before, target, after


class AsciiVolumeChapterFragGlobber(GlobBase):


	VOLUME_KEYS   = VOLUME_KEYS_GLOBAL
	FRAGMENT_KEYS = FRAGMENT_KEYS_GLOBAL
	CHAPTER_KEYS  = CHAPTER_KEYS_GLOBAL

	ALLOWABLE_INTERMEDIATE_CHARS = [
		" ",
		".",
		":",
	]

	def attach_token(self, before, target, after):
		# print("AttachToken: ", (before, target, after))
		# if len(after) == 3:
		# 	target = before[-1] + target
		# 	before = before[:-1]

		after = after
		before, prec, intervening = self.get_preceeding_text(before)
		# if target == '24':
		# 	print("(attach_token) Getting text preceding '%s' (%s)" % (target, type(target)))
		# 	print("(attach_token) Text '%s' '%s' '%s' " % (before, prec, intervening))

		if target in self.ALLOWABLE_INTERMEDIATE_CHARS or not isinstance(target, str):
			if prec:
				before.append(prec)
			if intervening:
				before.append(intervening)
		else:
			if prec:

				clstype = None
				if prec.lower() in self.VOLUME_KEYS:
					clstype = VolumeToken
				elif prec.lower() in self.CHAPTER_KEYS:
					clstype = ChapterToken
				elif prec.lower() in self.FRAGMENT_KEYS:
					clstype = FragmentToken

				last = None
				lasttok = None
				if clstype:
					tgtstr = target
					for idx, value in enumerate(after):
						if isinstance(value, str):
							tgtstr += value
							if value != ' ' and value.lower() != 'and':
								tok = clstype(prec, intervening, tgtstr)
								# print("Instantiating token: ", (tgtstr, clstype, tok, tok.content))
								if tok.is_ascii():
									num = tok.to_number(parse_ascii=True)
									if num != last:
										last = num
										lasttok = tok
									else:
										print("At end of number:", (prec, intervening, target, after))
										print("At end of number:")
										print(lasttok)
										print((before, tgtstr, after[idx-1:]))
										return before, lasttok, after[idx-1:]
						elif lasttok and lasttok.is_valid(parse_ascii=True):
							# print("Found non-string token. Forcing consume to halt.")
							return before, lasttok, after[idx-1:]
					if lasttok and lasttok.is_ascii():
						# print("Ending.")
						return before, lasttok, after[idx-1:]
										# break
					# clstype =
				# print("Value:", (prec, intervening, target, after))

			# 	target = VolumeToken(prec, intervening, target)
			# elif prec and prec.lower() in self.CHAPTER_KEYS:
			# 	target = ChapterToken(prec, intervening, target)
			# elif prec and prec.lower() in self.FRAGMENT_KEYS:
			# 	target = FragmentToken(prec, intervening, target)
			# else:
			# 	if prec:
			# 		before.append(prec)
			# 	if intervening:
			# 		before.append(intervening)

		return before, target, after

class VolumeSpotFixGlobber(VolumeChapterFragGlobber):

	# Order matters! Items are checked from left to right.
	VOLUME_KEYS   = [
			# Spot fixes: Make certain scanlators work:
			'rokujouma',
			'sunlight',
		]


class FractionGlobber(GlobBase):



	FRAGMENT_KEYS = FRAGMENT_KEYS_GLOBAL

	def attach_token(self, before, target, after):
		# print("AttachToken: ", (before, target, after))
		# if len(after) == 3:
		# 	target = before[-1] + target
		# 	before = before[:-1]

		# print("Getting text preceding '%s' (%s)" % (target, type(target)))

		before, prec, intervening = self.get_preceeding_text(before)

		if target == " ":
			if prec:
				before.append(prec)
			if intervening:
				before.append(intervening)

		elif isinstance(target, str):

			match = re.search(r'(\d+)/\d+', target)
			if prec and prec.lower() in self.FRAGMENT_KEYS and match:
				# print("FractionGlobber: ", target)
				p1,  = match.groups()
				# target = DateTextToken(target)
				target = FragmentToken(prec, intervening, p1)
			else:
				if prec:
					before.append(prec)
				if intervening:
					before.append(intervening)
		else:
			if prec:
				before.append(prec)
			if intervening:
				before.append(intervening)

		# print("target:", (prec, target))
		# print((before, prec, intervening, target, after))
		return before, target, after


class CompoundChapterGlobber(GlobBase):

	CHAPTER_KEYS = CHAPTER_KEYS_GLOBAL


	def attach_token(self, before, target, after):
		# print("AttachToken: ", (before, target, after))
		# if len(after) == 3:
		# 	target = before[-1] + target
		# 	before = before[:-1]

		# print("Getting text preceding '%s' (%s)" % (target, type(target)))

		before, prec, intervening = self.get_preceeding_text(before)

		if target == " ":
			if prec:
				before.append(prec)
			if intervening:
				before.append(intervening)

		elif isinstance(target, str):

			match = re.search(r'(\d+)(-)(\d+)', target)
			if prec and prec.lower() in self.CHAPTER_KEYS and match:
				# print("CompoundChapterGlobber: ", target)
				p1, divider, p2 = match.groups()
				# target = DateTextToken(target)
				target = CompoundChapterFragmentToken(prec, intervening, p1, divider, p2 )
			else:
				if prec:
					before.append(prec)
				if intervening:
					before.append(intervening)
		else:
			if prec:
				before.append(prec)
			if intervening:
				before.append(intervening)

		# print("target:", (prec, target))
		# print((before, prec, intervening, target, after))
		return before, target, after


class EpisodeGlobber(GlobBase):
	'''
	If we have a chapter entry, treat the episode entry as a fragment value.
	If we don't have a chapter entry, treat it as the chapter value.
	'''

	KEYS = [
			'episode',
			'ep',
		]

	def attach_token(self, before, target, after):
		# print("EpisodeGlobberAttachToken: ", (before, target, after))
		# if len(after) == 3:
		# 	target = before[-1] + target
		# 	before = before[:-1]

		# print("Getting text preceding '%s' (%s)" % (target, type(target)))

		have_chapter = any([isinstance(itm, ChapterToken) for itm in before+[target]+after])
		before, prec, intervening = self.get_preceeding_text(before)

		if target == " ":
			if prec:
				before.append(prec)
			if intervening:
				before.append(intervening)
		else:
			if prec and prec.lower() in self.KEYS:
				if not have_chapter:
					target = ChapterToken(prec, intervening, target)
				else:
					target = FragmentToken(prec, intervening, target)

			else:
				if prec:
					before.append(prec)
				if intervening:
					before.append(intervening)

		return before, target, after

class FreeNumericChapterGlobber(GlobBase):

	def attach_token(self, before, target, after):
		# print("Attach FreeNumericChapterGlobber: ", target)
		if isinstance(target, str):
			tmp = FreeChapterToken('', '', target)
			if tmp.is_valid(parse_ascii=False):
				# print("Interpreting as FreeChapterToken: ", target)
				target = tmp

		# print((before, prec, intervening, target, after))

		return before, target, after

class FreeTextGlobber(GlobBase):

	def attach_token(self, before, target, after):
		if isinstance(target, str):
			target = FreeTextToken(target)

		return before, target, after

		# print("AttachToken: ", (before, target, after))
		# if len(after) == 3:
		# 	target = before[-1] + target
		# 	before = before[:-1]
	# FreeTextToken

class DateGlobber(GlobBase):
	'''
	Attach to text that looks like a date string, so it doesn't get further processed later.
	'''
	def attach_token(self, before, target, after):
		# print("Processing:", target)

		if isinstance(target, str):
			if re.search(r'\d+[/\-]\d+[/\-]\d+', target):
				target = DateTextToken(target)

		return before, target, after



################################################################################################################################
################################################################################################################################
################################################################################################################################

class TitleParser(object):

	PROCESSING_STEPS = [
		SpaceSplitter,
		DateGlobber,
		CompoundChapterGlobber,
		FractionGlobber,
		CharSplitter,
		LetterNumberSplitter,
		HyphenatedLetterSplitter,
		NonNumericDecimalSplitter,
		VolumeChapterFragGlobber,
		EpisodeGlobber,
		VolumeSpotFixGlobber,
		AsciiVolumeChapterFragGlobber,
		FreeNumericChapterGlobber,
		FreeTextGlobber,
	]

	def __init__(self, title):
		self.raw = title

		self.chunks = []

		# print()
		# print()
		# print()
		# print("Parsing title: '%s'" % title)

		for step in self.PROCESSING_STEPS:
			print("Splitter step before: ", step, title)
			title = step().process(title)
			print("Splitter step after: ", step, title)

		self.chunks = title

	def __getitem__(self, idx):
		return self.chunks[idx]

	def getTok(self, tok_cls, tok_func=['is_valid', 'to_number'], do_print=False):

		for do_ascii in [False, True]:
			for item in self.chunks:
				# if do_print:
				# 	print(item, tok_cls, isinstance(item, tok_cls))
				if isinstance(item, tok_cls):
					if getattr(item, tok_func[0])(parse_ascii=do_ascii):
						return getattr(item, tok_func[1])(parse_ascii=do_ascii)
		return None





	def getVolume(self):
		val = self.getTok(VolumeToken)
		if val is not None:
			return val
		val = self.getTok(CompoundVolChapterToken, tok_func=['valid_volume', 'get_volume'])
		if val is not None:
			return val
		return None

	def getChapter(self):
		val = self.getTok(ChapterToken)
		if val is not None:
			return val
		val = self.getTok(CompoundVolChapterToken, tok_func=['valid_chapter', 'get_chapter'])
		if val is not None:
			return val
		val = self.getTok(CompoundChapterFragmentToken, tok_func=['valid_chapter', 'get_chapter'])
		if val is not None:
			return val
		val = self.getTok(FreeChapterToken)
		if val is not None:
			return val
		return None

	def getFragment(self):
		val = self.getTok(FragmentToken)
		if val is not None:
			return val
		val = self.getTok(CompoundChapterFragmentToken, tok_func=['valid_fragment', 'get_fragment'])
		if val is not None:
			return val
		return None


	def _splitPostfix(self, inStr):

		return inStr.strip()

	def getPostfix(self):
		ret = []
		# print(re.split("([ ,])", self.raw))
		for chunk in re.split("([ ,])", self.raw):
			for p_key in POSTFIX_KEYS:
				if p_key in chunk.lower():
					idx = self.raw.find(chunk)
					if idx >= 0:
						postfix = self.raw[idx:]
						ret.append((len(postfix), postfix))

		# We want to select the longest found postfix.
		ret.sort(reverse=True)
		if ret:
			return ret[0][1]

		return ''

	def __repr__(self):
		ret = "<Parsed title: '{}' v:{}, c:{}, f:{}\n".format(self.raw, self.getVolume(), self.getChapter(), self.getFragment())
		for item in self.chunks:
			ret += "	{}\n".format(item)
		ret += ">"
		ret = ret.strip()
		return ret

