## 1.27.4 - 2024-09-06
### Extractors
#### Additions
- [sexcom] add `likes` extractor ([#6149](https://github.com/mikf/gallery-dl/issues/6149))
- [wikimedia] add `wiki` extractor ([#6050](https://github.com/mikf/gallery-dl/issues/6050))
#### Fixes
- [bunkr] fix file downloads ([#6037](https://github.com/mikf/gallery-dl/issues/6037))
- [cyberdrop] fix extraction
- [deviantart] fix `"pagination": "manual"` for cursor-based endpoints ([#6079](https://github.com/mikf/gallery-dl/issues/6079))
- [deviantart] fix `"original": "images"` ([#6124](https://github.com/mikf/gallery-dl/issues/6124))
- [exhentai] fix `limits` option ([#6090](https://github.com/mikf/gallery-dl/issues/6090))
- [flickr] make `exif` and `context` metadata extraction non-fatal ([#6002](https://github.com/mikf/gallery-dl/issues/6002), [#6077](https://github.com/mikf/gallery-dl/issues/6077))
- [flickr] make `album` metadata extraction non-fatal ([#3441](https://github.com/mikf/gallery-dl/issues/3441))
- [furaffinity] fix `favorite` pagination ([#6151](https://github.com/mikf/gallery-dl/issues/6151))
- [gofile] fix `KeyError: 'childrenIds'` ([#5993](https://github.com/mikf/gallery-dl/issues/5993))
- [newgrounds] fix warning for age-restricted posts ([#6005](https://github.com/mikf/gallery-dl/issues/6005))
- [toyhouse] fix extraction of image URLs
- [tumblr] fix `401 Unauthorized` for likes when using api-key ([#5994](https://github.com/mikf/gallery-dl/issues/5994))
- [twitter] fix pinned Tweet extraction ([#6102](https://github.com/mikf/gallery-dl/issues/6102))
- [ytdl] fix processing playlists of playlists ([#6127](https://github.com/mikf/gallery-dl/issues/6127))
#### Improvements
- [bcbnsfw] use `*` as query when retrieving all posts ([#6135](https://github.com/mikf/gallery-dl/issues/6135))
- [bunkr] support `bunkr:` URL prefix ([#6017](https://github.com/mikf/gallery-dl/issues/6017))
- [e621] cache pool metadata API calls ([#6001](https://github.com/mikf/gallery-dl/issues/6001))
- [generic] better directory names ([#6104](https://github.com/mikf/gallery-dl/issues/6104))
- [koharu] improve format selection ([#6088](https://github.com/mikf/gallery-dl/issues/6088))
- [pixiv] implement downloading "original" ugoira frames ([#6056](https://github.com/mikf/gallery-dl/issues/6056))
- [pixiv] use mobile API for `series` ([#5983](https://github.com/mikf/gallery-dl/issues/5983))
#### Metadata
- [batoto] improve chapter info regex ([#5988](https://github.com/mikf/gallery-dl/issues/5988), [#5997](https://github.com/mikf/gallery-dl/issues/5997))
- [batoto] extract `chapter_url` metadata ([#5562](https://github.com/mikf/gallery-dl/issues/5562))
- [batoto] improve `title` extraction ([#5988](https://github.com/mikf/gallery-dl/issues/5988))
- [hitomi] extract `extension_original` metadata ([#6049](https://github.com/mikf/gallery-dl/issues/6049))
- [instagram] add `post_date` metadata field ([#6081](https://github.com/mikf/gallery-dl/issues/6081), [#6091](https://github.com/mikf/gallery-dl/issues/6091))
- [sankaku] restore old `tags` format ([#6043](https://github.com/mikf/gallery-dl/issues/6043))
- [twitter] extract `type` metadata ([#6111](https://github.com/mikf/gallery-dl/issues/6111))
#### Options
- [bunkr] add `tlds` option to match URLs with all possible TLDs ([#5875](https://github.com/mikf/gallery-dl/issues/5875), [#6017](https://github.com/mikf/gallery-dl/issues/6017))
- [instagram] add `max-posts` option ([#6054](https://github.com/mikf/gallery-dl/issues/6054))
- [instagram] add `info` as a possible `include` value
- [instagram] allow disabling `cursor` output
- [twitter] add `info` as a possible `include` value ([#6114](https://github.com/mikf/gallery-dl/issues/6114))
- [twitter] allow disabling `cursor` output ([#5990](https://github.com/mikf/gallery-dl/issues/5990))
### Post Processors
- [hash] add `hash` post processor to compute file hash metadata ([#6099](https://github.com/mikf/gallery-dl/issues/6099))
- [metadata] add `include` and `exclude` options ([#6058](https://github.com/mikf/gallery-dl/issues/6058))
- [metadata] fix using `..` in directories on Windows ([#5942](https://github.com/mikf/gallery-dl/issues/5942), [#6094](https://github.com/mikf/gallery-dl/issues/6094))
- [rename] add `rename` post processor to rename previously downloaded files ([#5846](https://github.com/mikf/gallery-dl/issues/5846), [#6044](https://github.com/mikf/gallery-dl/issues/6044))
- [ugoira] support converting "original" frames ([#6056](https://github.com/mikf/gallery-dl/issues/6056))
- [ugoira] add `skip` option ([#6056](https://github.com/mikf/gallery-dl/issues/6056))
### Miscellaneous
- [cookies:firefox] extract only cookies without container by default ([#5957](https://github.com/mikf/gallery-dl/issues/5957))
- [formatter] implement `A` format specifier ([#6036](https://github.com/mikf/gallery-dl/issues/6036))
- [tests] fix bug when running tests in a certain order
- [util] extend `CustomNone` with arithmetic operators ([#6007](https://github.com/mikf/gallery-dl/issues/6007), [#6009](https://github.com/mikf/gallery-dl/issues/6009))
- add `--rename` and `--rename-to` command-line options ([#5846](https://github.com/mikf/gallery-dl/issues/5846), [#6044](https://github.com/mikf/gallery-dl/issues/6044))
- add `input-files` config option ([#6059](https://github.com/mikf/gallery-dl/issues/6059))
