

# The processing pipeline has three stages.
# Preprocessors have access to the page content before it's fed through the filters
# Filters are for extracting additional information from the in-flight pages.
# Plugins rewrite the page content for more pleasant consumption.

import WebMirror.PreProcessors.LiveJournalPreprocess
import WebMirror.PreProcessors.RedditPreprocess
import WebMirror.PreProcessors.WattPadPreprocess
import WebMirror.PreProcessors.TgStoryTimePreprocess
import WebMirror.PreProcessors.RRLPreprocess
import WebMirror.PreProcessors.QidianPreprocess
import WebMirror.PreProcessors.GravityTalesPreprocess
import WebMirror.PreProcessors.WixsitePreprocess
import WebMirror.PreProcessors.LiteroticaPreprocess
import WebMirror.PreProcessors.CreativeNovelsPreprocess

PREPROCESSORS = [
	WebMirror.PreProcessors.LiveJournalPreprocess.LJPreprocessor,
	WebMirror.PreProcessors.RedditPreprocess.RedditPreprocessor,
	WebMirror.PreProcessors.WattPadPreprocess.WattPadPreprocessor,
	WebMirror.PreProcessors.TgStoryTimePreprocess.TgStoryTimePreprocessor,
	WebMirror.PreProcessors.QidianPreprocess.QidianPreprocessor,
	WebMirror.PreProcessors.GravityTalesPreprocess.GravityTalesPreprocessor,
	WebMirror.PreProcessors.WixsitePreprocess.JsRendererPreprocessor,
	WebMirror.PreProcessors.CreativeNovelsPreprocess.CreativeNovelsPreprocessor,

	WebMirror.PreProcessors.LiteroticaPreprocess.LiteroticaFavouritePreprocessor,

	# Disable the RRL Preprocessor since they rolled back the site.
	# WebMirror.PreProcessors.RRLPreprocess.RRLListPagePreprocessor,
	# WebMirror.PreProcessors.RRLPreprocess.RRLSeriesPagePreprocessor,
	# WebMirror.PreProcessors.RRLPreprocess.RRLChapterPagePreprocessor,
]


import WebMirror.OutputFilters.RoyalRoadL.RRLSeriesPageFilter
import WebMirror.OutputFilters.RoyalRoadL.RRLSeriesUpdateFilter
import WebMirror.OutputFilters.RoyalRoadL.RRLJsonXmlSeriesUpdateFilter
import WebMirror.OutputFilters.WattPad.WattPadSeriesPageFilter
import WebMirror.OutputFilters.JapTem.JapTemSeriesPageFilter
import WebMirror.OutputFilters.Booksie.BooksieSeriesPageFilter
import WebMirror.OutputFilters.LNDB.LNDBSeriesPageFilter
import WebMirror.OutputFilters.Twitter.TwitterFilter
import WebMirror.OutputFilters.Nu.NUHomepageFilter
import WebMirror.OutputFilters.Nu.NuSeriesPageFilter


# Filters are executed against fetched content first.
FILTERS = [
	WebMirror.OutputFilters.RoyalRoadL.RRLSeriesPageFilter.RRLSeriesPageProcessor,
	WebMirror.OutputFilters.RoyalRoadL.RRLSeriesUpdateFilter.RRLSeriesUpdateFilter,
	WebMirror.OutputFilters.RoyalRoadL.RRLJsonXmlSeriesUpdateFilter.RRLJsonXmlSeriesUpdateFilter,

	WebMirror.OutputFilters.Nu.NUHomepageFilter.NuHomepageFilter,
	WebMirror.OutputFilters.Nu.NuSeriesPageFilter.NUSeriesPageProcessor,
	WebMirror.OutputFilters.JapTem.JapTemSeriesPageFilter.JapTemSeriesPageProcessor,
	#WebMirror.OutputFilters.WattPad.WattPadSeriesPageFilter.WattPadSeriesPageFilter,
	WebMirror.OutputFilters.Booksie.BooksieSeriesPageFilter.BooksieSeriesPageProcessor,
	WebMirror.OutputFilters.LNDB.LNDBSeriesPageFilter.LNDBSeriesPageFilter,

	WebMirror.OutputFilters.Twitter.TwitterFilter.TwitterProcessor,
]



import WebMirror.processor.HtmlProcessor
import WebMirror.processor.GDriveDirProcessor
import WebMirror.processor.GDocProcessor
import WebMirror.processor.MarkdownProcessor
import WebMirror.processor.BinaryProcessor
import WebMirror.processor.JsonProcessor
import WebMirror.processor.XmlProcessor
import WebMirror.processor.RssProcessor
import WebMirror.processor.WattPadJsonProcessor
import WebMirror.processor.RoyalRoadLChapterPageProcessor
import WebMirror.processor.RoyalRoadLSeriesPageProcessor

import WebMirror.processor.NuProcessor
import WebMirror.processor.FontRemapProcessors
import WebMirror.processor.GarbageInlineProcessors
import WebMirror.processor.XiAiNovelProcessor


PLUGINS = [
	WebMirror.processor.HtmlProcessor.HtmlPageProcessor,
	WebMirror.processor.GDriveDirProcessor.GDriveDirProcessor,
	WebMirror.processor.GDocProcessor.GdocPageProcessor,
	WebMirror.processor.MarkdownProcessor.MarkdownProcessor,
	WebMirror.processor.BinaryProcessor.BinaryResourceProcessor,
	WebMirror.processor.JsonProcessor.JsonProcessor,
	WebMirror.processor.XmlProcessor.XmlProcessor,
	WebMirror.processor.RssProcessor.RssProcessor,
	WebMirror.processor.WattPadJsonProcessor.WattPadJsonProcessor,
	WebMirror.processor.RoyalRoadLChapterPageProcessor.RoyalRoadLChapterPageProcessor,
	WebMirror.processor.RoyalRoadLSeriesPageProcessor.RoyalRoadLSeriesPageProcessor,
	WebMirror.processor.RoyalRoadLSeriesPageProcessor.RoyalRoadLSeriesPageProcessor,
	#WebMirror.processor.FontRemapProcessors.KobatoChanDaiSukiPageProcessor,
	# WebMirror.processor.FontRemapProcessors.NepustationPageProcessor,
	WebMirror.processor.NuProcessor.NuProcessor,
	WebMirror.processor.GarbageInlineProcessors.HecatesCornerPageProcessor,
	WebMirror.processor.GarbageInlineProcessors.ZenithNovelsPageProcessor,
	WebMirror.processor.GarbageInlineProcessors.LightNovelsWorldPageProcessor,
	WebMirror.processor.GarbageInlineProcessors.WatashiWaSugoiDesuPageProcessor,
	WebMirror.processor.GarbageInlineProcessors.ShamelessOniisanPageProcessor,
	WebMirror.processor.GarbageInlineProcessors.FantasyBooksLiveProcessor,
	WebMirror.processor.GarbageInlineProcessors.MayonaizeShrimpLiveProcessor,
	WebMirror.processor.GarbageInlineProcessors.RebirthOnlineLiveProcessor,
	WebMirror.processor.GarbageInlineProcessors.ConvallariasLibraryProcessor,

	WebMirror.processor.XiAiNovelProcessor.XiAiNovelPageProcessor,
]


# import WebMirror.OutputFilters.WattPad.WattPadInit

INIT_CALLS = [
	#WebMirror.OutputFilters.WattPad.WattPadInit.init_call
]

print("Processing plugins: %s, active filters: %s" % (len(PLUGINS), len(FILTERS)))
