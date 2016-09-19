
import urllib.parse
import RawArchiver.ModuleBase

class WebComicsRawModule(RawArchiver.ModuleBase.RawScraperModuleBase):

	module_name = "WebComicsRawModule"

	# TODO: Support cloudfront resources
	target_urls = [
		'http://somethingpositive.net',
		'http://www.girlgeniusonline.com',
		'http://www.agirlandherfed.com',
		'http://cube-drone.com',
		'http://existentialcomics.com',
		'http://killsixbilliondemons.com',
		'http://strongfemaleprotagonist.com',
		'http://themonsterunderthebed.net',
		'http://www.alphaluna.net',
		'http://dcisgoingtohell.com',
		'http://dragonaur.comicgenesis.com',
		'http://dresdencodak.com',
		'http://www.exiern.com',
		'http://www.goblinscomic.org',
		'http://www.gunnerkrigg.com',
		'http://www.kevinandkell.com',
		'http://leth.smackjeeves.com',
		'http://www.lovemenicecomic.com',
		'http://www.egscomics.com',
		'http://www.misfile.com',
		'http://www.zebragirl.net',
		'http://forthewicked.net',
		'http://www.ourhomeplanet.net',
		'http://well-of-souls.com',
		'http://www.paradigmshiftmanga.com',
		'http://www.questionablecontent.net',
		'http://www.samandfuzzy.com',
		'http://www.smbc-comics.com',
		'http://amultiverse.com',
		'http://www.schlockmercenary.com',
		'http://sci-ence.org',
		'http://www.sdamned.com',
		'http://drmcninja.com',
		'http://www.thewotch.com',
		'http://twicedestined.comicgenesis.com',
		'http://kenjiandmokoto.comicgenesis.com',
		'http://www.twolumps.net',
		'http://wapsisquare.com',
		'http://xkcd.com',
		'http://www.wastedtalent.ca',
		'http://www.vgcats.com',

		# Fukkit, lets just archive the all of keenspot
		'http://twenty-seven.keenspot.com',
		'http://avengelyne.keenspot.com',
		'http://banzaigirl.keenspot.com',
		'http://barkercomic.keenspot.com',
		'http://brawlinthefamily.keenspot.com',
		'http://choppingblock.keenspot.com',
		'http://clicheflambe.keenspot.com',
		'http://countyoursheep.keenspot.com',
		'http://crowscare.keenspot.com',
		'http://dreamless.keenspot.com',
		'http://everythingjake.keenspot.com',
		'http://exposure.keenspot.com',
		'http://fallouttoyworks.keenspot.com',
		'http://thefirstdaughter.keenspot.com',
		'http://flipside.keenspot.com',
		'http://friarandbrimstone.keenspot.com',
		'http://genecatlow.keenspot.com',
		'http://godchild.keenspot.com',
		'http://godmode.keenspot.com',
		'http://greenwake.keenspot.com',
		'http://headtrip.keenspot.com',
		'http://herobynight.keenspot.com',
		'http://hoaxhunters.keenspot.com',
		'http://hopevirus.keenspot.com',
		'http://salamanstra.keenspot.com',
		'http://inhere.keenspot.com',
		'http://newshounds.keenspot.com',
		'http://jadewarriors.keenspot.com',
		'http://katrina.keenspot.com',
		'http://landis.keenspot.com',
		'http://lastblood.keenspot.com',
		'http://thelounge.keenspot.com',
		'http://lutherstrode.keenspot.com',
		'http://makeshiftmiracle.keenspot.com',
		'http://marksmen.keenspot.com',
		'http://marryme.keenspot.com',
		'http://medusasdaughter.keenspot.com',
		'http://monstermassacre.keenspot.com',
		'http://mysticrevolution.keenspot.com',
		'http://nopinkponies.keenspot.com',
		'http://noroomformagic.keenspot.com',
		'http://outthere.keenspot.com',
		'http://porcelain.keenspot.com',
		'http://punchanpie.keenspot.com',
		'http://quiltbag.keenspot.com',
		'http://rumblefall.keenspot.com',
		'http://redspike.keenspot.com',
		'http://samuraisblood.keenspot.com',
		'http://sharky.keenspot.com',
		'http://shockwave.keenspot.com',
		'http://somethinghappens.keenspot.com',
		'http://sorethumbs.keenspot.com',
		'http://striptease.keenspot.com',
		'http://supernovas.keenspot.com',
		'http://superosity.keenspot.com',
		'http://twokinds.keenspot.com',
		'http://thevault.keenspot.com',
		'http://weirdingwillows.keenspot.com',
		'http://wickedpowered.keenspot.com',
		'http://waywardsons.keenspot.com',
		'http://wisdomofmoo.keenspot.com',
		'http://yirmumah.keenspot.com',
		'http://2dgoggles.com',

		'http://kohtathesamurai.com',
		'http://bangbangbakochan.com',

		'http://oglaf.com/',
		'http://media.oglaf.com/',
	]

	target_tlds = [urllib.parse.urlparse(tmp).netloc for tmp in target_urls]

	badwords = [
		'search.php',
		"&replytocom=",
		"/viewtopic.php",
		'/viewforum.php',
		'/forum/index.php',
		"www.smbc-comics.com/smbcforum/",
		'destination=node',
		'rest_route=',
		'ucp.php',
		'mode=resend_act',
		'/archive/comments',
		'title=&field_comic_number_value',
		'%2Flist%3Forder%3Dcreated%26sort%3Dasc%26page%3D2%26date_filter%5Bmax',
		'title%3D%26field_comic_number_value%3D',
		'%3Fpage%3D20%26permalink%',
		'destination=taxonomy',
		'wasted-talent-newsletter',
		'/topic/misc',
		'permalink',
		'/shop/product/comic-print',
		'replytocom=',
		'wastedtalentca-website&q=forum/wastedtalentca-website&q=forum',
		'site-upgrade.html/feed.xml',
		'.html/feed',

	]

	@classmethod
	def cares_about_url(cls, url):
		if any([badword in url for badword in cls.badwords]):
			return False

		if RawArchiver.ModuleBase.duplicate_path_fragments(url):
			return False
		return urllib.parse.urlparse(url).netloc in cls.target_tlds

	@classmethod
	def get_start_urls(cls):
		return [tmp for tmp in cls.target_urls]
