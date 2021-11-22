from typing import cast
import mutagen
from mutagen.easymp4 import MP4


import argparse

# Supported tags
# https://mutagen.readthedocs.io/en/latest/api/mp4.html#mutagen.mp4.MP4Tags

'''
ISSUES :

Problem with musicbrainz_* tags saving with only the first 4 chars of the key (musi)

'''

atomicParams = {
    "artist":				[str,	"\xa9ART",	                    "Set the artist tag"],
    "title":				[str,	"\xa9nam",	                    "Set the title tag"],
    "album":				[str,	"\xa9alb",	                    "Set the album tag"],
    "genre":				[str,	"\xa9gen",	                    "Genre tag"],
    "tracknum":				[str,	"pcst",		                    "Track number (or track number/total tracks)"],
    "disk":					[str,	"disk",		                    "Disk number (or disk number/total disks)"],
    "comment":				[str,	"\xa9cmt",	                    "Set the comment tag"],
    "year":					[str,	"\xa9day",	                    "Year tag"],
    "lyrics":				[str,	"\xa9lyr",	                    "Set lyrics (not subject to 256 byte limit)"],
    "composer":				[str,	"\xa9wrt",	                    "Set the composer tag"],
    "copyright":			[str,	"cprt",		                    "Set the copyright tag"],
    "grouping":				[str,	"\xa9grp",	                    "Set the grouping tag"],
    "artwork":				[argparse.FileType('rb'),	"covr",		"Set a piece of artwork (jpeg or png only)"],
    "bpm":					[int,	"tmpo",		                    "Set the tempo/bpm"],
    "albumArtist":			[str,	"aART",		                    "Set the album artist tag"],
    "compilation":			[bool,	"cpil",		                    "Set the compilation flag (true or false)"],
    "hdvideo":				[int,	"hdvd",		                    "Set the hdvideo flag to one of: 0 for standard definition, 1 for 720p, 2 for 1080p"],
    "stik":					[int,	"stik",		                    "Sets the iTunes 'stik' atom"],
    "description":			[str,	"desc",		                    "Set the description tag"],
    "TVShowName":			[str,	"tvsh",		                    "Set the TV Show name"],
    "TVSeasonNum":			[int,	"tvsn",		                    "Set the TV Season number"],
    "TVEpisodeNum":			[int,	"tves",		                    "Set the TV Episode number"],
    "category":				[str,	"catg",		                    "Sets the podcast category"],
    "keyword":				[str,	"keyw",		                    "Sets the podcast keyword"],
    "podcastURL":			[str,	"purl",		                    "Set the podcast feed URL"],
    "podcastGUID":			[str,	"egid",		                    "Set the episode's URL tag"],
    "purchaseDate":			[str,	"purd",		                    "Set time of purchase"],
    "encodedBy":			[str,	"\xa9too",	                    "Set the name of the Person/company who encoded the file"],
    "apID":					[str,	"apID",		                    "Set the Account Name"],
    "cnID":					[int,	"cnID",		                    "Set the iTunes Catalog ID"],
    "geID":					[int,	"geID",		                    "Set the iTunes Genre"],
    "xID":					[str,	"xID",		                    "Set the vendor-supplied iTunes xID"],
    "gapless":				[bool,	"pgap",		                    "Set the gapless playback flag"],
    "contentRating":		[str,	"rtng",		                    "Set tv/mpaa rating "],
    "mbArtistId":			[str,   "musicbrainz_artistid",         "Set MusicBrainz Artist Id"],
    "mbTrackId":			[str,   "musicbrainz_trackid",          "Set MusicBrainz Track Id"],
    "mbAlbumId":			[str,   "musicbrainz_albumid",          "Set MusicBrainz Album Id"],
    "mbAlbumArtistId":		[str,   "musicbrainz_albumartistid",    "Set MusicBrainz Album Artist Id"],
    "musicIpPuid":			[str,   "musicip_puid",                 "Set MusicIP PUID"],
    "mbAlbumStatus":		[str,   "musicbrainz_albumstatus",      "Set MusicBrainz Album Status"],
    "mbAlbumType":			[str,   "musicbrainz_albumtype",        "Set MusicBrainz Album Type"],
    "ReleaseCountry":		[str,   "releasecountry",               "Set MusicBrainz Release Country"],
    "albumSortOrder":		[str,	"soal",		                    "xxx"],
    "albumArtistSortOrder":	[str,	"soaa",		                    "xxx"],
    "artistSortOrder":		[str,	"soar",		                    "xxx"],
    "titleSortOrder":		[str,	"sonm",		                    "xxx"],
    "composerSortOrder":	[str,	"soco",		                    "xxx"],
    "showSortOrder":		[str,	"sosn",		                    "xxx"],
    "work":					[str,	"\xa9wrk",	                    "xxx"],
    "movement":				[str,	"\xa9mvn",	                    "xxx"],
    "movementCount":		[int,	"\xa9mvc",	                    "xxx"],
    "movementIndex":		[int,	"\xa9mvi",	                    "xxx"],
    #"xxx":					[int,	"xxx",		                    "xxx"],
}

# Instantiate the parser
parser = argparse.ArgumentParser(description='My python AtomicParsley')

# Required file argument
parser.add_argument('file', type=open, help='file to write metadata to')

# Add all supported arguments (From AtomicParsley)
for param, data in atomicParams.items():
    # Optional string arguments
    parser.add_argument("--" + param, type=data[0], help=data[2])

args = parser.parse_known_args()

params = vars(args[0])

try:
    audio = MP4(params['file'].name)
except Exception as e:
    print(f"Can't open file : {e}")
    exit(1)


# Log unhandled params (From freyr)
if args[1]:
    print(f"Found unknown params : {args[1]}")

# Special tags
if 'artwork' in params and params['artwork']:
    audio[atomicParams['artwork'][1]] = [params['artwork'].read()]
    del params['artwork']
if 'disk' in params:
    tmp = [tuple(map(int, params['disk'].split('/')))]
    audio[atomicParams['disk'][1]] = tmp
    del params['disk']

# Loop over basic tags
for key, val in params.items():
    if val and key in atomicParams:
        try:
            paramdata = atomicParams[key]
            audio[paramdata[1]] = val
        except Exception as e:
            print(f"Error [{key}] ({val}) : {e}")

audio.save()
