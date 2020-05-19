#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
#// 
#// getID3() by James Heinrich <info@getid3.org>
#// available at https://github.com/JamesHeinrich/getID3
#// or https://www.getid3.org
#// or http://getid3.sourceforge.net
#// see readme.txt for more details
#// 
#// 
#// module.tag.apetag.php
#// module for analyzing APE tags
#// dependencies: NONE
#// 
#//
class getid3_apetag(getid3_handler):
    #// 
    #// true: return full data for all attachments;
    #// false: return no data for all attachments;
    #// integer: return data for attachments <= than this;
    #// string: save as file to this directory.
    #// 
    #// @var int|bool|string
    #//
    inline_attachments = True
    overrideendoffset = 0
    #// 
    #// @return bool
    #//
    def analyze(self):
        
        
        info_ = self.getid3.info
        if (not getid3_lib.intvaluesupported(info_["filesize"])):
            self.warning("Unable to check for APEtags because file is larger than " + round(PHP_INT_MAX / 1073741824) + "GB")
            return False
        # end if
        id3v1tagsize_ = 128
        apetagheadersize_ = 32
        lyrics3tagsize_ = 10
        if self.overrideendoffset == 0:
            self.fseek(0 - id3v1tagsize_ - apetagheadersize_ - lyrics3tagsize_, SEEK_END)
            APEfooterID3v1_ = self.fread(id3v1tagsize_ + apetagheadersize_ + lyrics3tagsize_)
            #// if (preg_match('/APETAGEX.{24}TAG.{125}$/i', $APEfooterID3v1)) {
            if php_substr(APEfooterID3v1_, php_strlen(APEfooterID3v1_) - id3v1tagsize_ - apetagheadersize_, 8) == "APETAGEX":
                #// APE tag found before ID3v1
                info_["ape"]["tag_offset_end"] = info_["filesize"] - id3v1tagsize_
                pass
            elif php_substr(APEfooterID3v1_, php_strlen(APEfooterID3v1_) - apetagheadersize_, 8) == "APETAGEX":
                #// APE tag found, no ID3v1
                info_["ape"]["tag_offset_end"] = info_["filesize"]
            # end if
        else:
            self.fseek(self.overrideendoffset - apetagheadersize_)
            if self.fread(8) == "APETAGEX":
                info_["ape"]["tag_offset_end"] = self.overrideendoffset
            # end if
        # end if
        if (not (php_isset(lambda : info_["ape"]["tag_offset_end"]))):
            info_["ape"] = None
            return False
        # end if
        #// shortcut
        thisfile_ape_ = info_["ape"]
        self.fseek(thisfile_ape_["tag_offset_end"] - apetagheadersize_)
        APEfooterData_ = self.fread(32)
        thisfile_ape_["footer"] = self.parseapeheaderfooter(APEfooterData_)
        if (not thisfile_ape_["footer"]):
            self.error("Error parsing APE footer at offset " + thisfile_ape_["tag_offset_end"])
            return False
        # end if
        if (php_isset(lambda : thisfile_ape_["footer"]["flags"]["header"])) and thisfile_ape_["footer"]["flags"]["header"]:
            self.fseek(thisfile_ape_["tag_offset_end"] - thisfile_ape_["footer"]["raw"]["tagsize"] - apetagheadersize_)
            thisfile_ape_["tag_offset_start"] = self.ftell()
            APEtagData_ = self.fread(thisfile_ape_["footer"]["raw"]["tagsize"] + apetagheadersize_)
        else:
            thisfile_ape_["tag_offset_start"] = thisfile_ape_["tag_offset_end"] - thisfile_ape_["footer"]["raw"]["tagsize"]
            self.fseek(thisfile_ape_["tag_offset_start"])
            APEtagData_ = self.fread(thisfile_ape_["footer"]["raw"]["tagsize"])
        # end if
        info_["avdataend"] = thisfile_ape_["tag_offset_start"]
        if (php_isset(lambda : info_["id3v1"]["tag_offset_start"])) and info_["id3v1"]["tag_offset_start"] < thisfile_ape_["tag_offset_end"]:
            self.warning("ID3v1 tag information ignored since it appears to be a false synch in APEtag data")
            info_["id3v1"] = None
            for key_,value_ in info_["warning"].items():
                if value_ == "Some ID3v1 fields do not use NULL characters for padding":
                    info_["warning"][key_] = None
                    sort(info_["warning"])
                    break
                # end if
            # end for
        # end if
        offset_ = 0
        if (php_isset(lambda : thisfile_ape_["footer"]["flags"]["header"])) and thisfile_ape_["footer"]["flags"]["header"]:
            thisfile_ape_["header"] = self.parseapeheaderfooter(php_substr(APEtagData_, 0, apetagheadersize_))
            if thisfile_ape_["header"]:
                offset_ += apetagheadersize_
            else:
                self.error("Error parsing APE header at offset " + thisfile_ape_["tag_offset_start"])
                return False
            # end if
        # end if
        #// shortcut
        info_["replay_gain"] = Array()
        thisfile_replaygain_ = info_["replay_gain"]
        i_ = 0
        while i_ < thisfile_ape_["footer"]["raw"]["tag_items"]:
            
            value_size_ = getid3_lib.littleendian2int(php_substr(APEtagData_, offset_, 4))
            offset_ += 4
            item_flags_ = getid3_lib.littleendian2int(php_substr(APEtagData_, offset_, 4))
            offset_ += 4
            if php_strstr(php_substr(APEtagData_, offset_), " ") == False:
                self.error("Cannot find null-byte (0x00) separator between ItemKey #" + i_ + " and value. ItemKey starts " + offset_ + " bytes into the APE tag, at file offset " + thisfile_ape_["tag_offset_start"] + offset_)
                return False
            # end if
            ItemKeyLength_ = php_strpos(APEtagData_, " ", offset_) - offset_
            item_key_ = php_strtolower(php_substr(APEtagData_, offset_, ItemKeyLength_))
            #// shortcut
            thisfile_ape_["items"][item_key_] = Array()
            thisfile_ape_items_current_ = thisfile_ape_["items"][item_key_]
            thisfile_ape_items_current_["offset"] = thisfile_ape_["tag_offset_start"] + offset_
            offset_ += ItemKeyLength_ + 1
            #// skip 0x00 terminator
            thisfile_ape_items_current_["data"] = php_substr(APEtagData_, offset_, value_size_)
            offset_ += value_size_
            thisfile_ape_items_current_["flags"] = self.parseapetagflags(item_flags_)
            for case in Switch(thisfile_ape_items_current_["flags"]["item_contents_raw"]):
                if case(0):
                    pass
                # end if
                if case(2):
                    #// Locator (URL, filename, etc), UTF-8 encoded
                    thisfile_ape_items_current_["data"] = php_explode(" ", thisfile_ape_items_current_["data"])
                    break
                # end if
                if case(1):
                    pass
                # end if
                if case():
                    break
                # end if
            # end for
            for case in Switch(php_strtolower(item_key_)):
                if case("replaygain_track_gain"):
                    if php_preg_match("#^([\\-\\+][0-9\\.,]{8})( dB)?$#", thisfile_ape_items_current_["data"][0], matches_):
                        thisfile_replaygain_["track"]["adjustment"] = php_float(php_str_replace(",", ".", matches_[1]))
                        #// float casting will see "0,95" as zero!
                        thisfile_replaygain_["track"]["originator"] = "unspecified"
                    else:
                        self.warning("MP3gainTrackGain value in APEtag appears invalid: \"" + thisfile_ape_items_current_["data"][0] + "\"")
                    # end if
                    break
                # end if
                if case("replaygain_track_peak"):
                    if php_preg_match("#^([0-9\\.,]{8})$#", thisfile_ape_items_current_["data"][0], matches_):
                        thisfile_replaygain_["track"]["peak"] = php_float(php_str_replace(",", ".", matches_[1]))
                        #// float casting will see "0,95" as zero!
                        thisfile_replaygain_["track"]["originator"] = "unspecified"
                        if thisfile_replaygain_["track"]["peak"] <= 0:
                            self.warning("ReplayGain Track peak from APEtag appears invalid: " + thisfile_replaygain_["track"]["peak"] + " (original value = \"" + thisfile_ape_items_current_["data"][0] + "\")")
                        # end if
                    else:
                        self.warning("MP3gainTrackPeak value in APEtag appears invalid: \"" + thisfile_ape_items_current_["data"][0] + "\"")
                    # end if
                    break
                # end if
                if case("replaygain_album_gain"):
                    if php_preg_match("#^([\\-\\+][0-9\\.,]{8})( dB)?$#", thisfile_ape_items_current_["data"][0], matches_):
                        thisfile_replaygain_["album"]["adjustment"] = php_float(php_str_replace(",", ".", matches_[1]))
                        #// float casting will see "0,95" as zero!
                        thisfile_replaygain_["album"]["originator"] = "unspecified"
                    else:
                        self.warning("MP3gainAlbumGain value in APEtag appears invalid: \"" + thisfile_ape_items_current_["data"][0] + "\"")
                    # end if
                    break
                # end if
                if case("replaygain_album_peak"):
                    if php_preg_match("#^([0-9\\.,]{8})$#", thisfile_ape_items_current_["data"][0], matches_):
                        thisfile_replaygain_["album"]["peak"] = php_float(php_str_replace(",", ".", matches_[1]))
                        #// float casting will see "0,95" as zero!
                        thisfile_replaygain_["album"]["originator"] = "unspecified"
                        if thisfile_replaygain_["album"]["peak"] <= 0:
                            self.warning("ReplayGain Album peak from APEtag appears invalid: " + thisfile_replaygain_["album"]["peak"] + " (original value = \"" + thisfile_ape_items_current_["data"][0] + "\")")
                        # end if
                    else:
                        self.warning("MP3gainAlbumPeak value in APEtag appears invalid: \"" + thisfile_ape_items_current_["data"][0] + "\"")
                    # end if
                    break
                # end if
                if case("mp3gain_undo"):
                    if php_preg_match("#^[\\-\\+][0-9]{3},[\\-\\+][0-9]{3},[NW]$#", thisfile_ape_items_current_["data"][0]):
                        mp3gain_undo_left_, mp3gain_undo_right_, mp3gain_undo_wrap_ = php_explode(",", thisfile_ape_items_current_["data"][0])
                        thisfile_replaygain_["mp3gain"]["undo_left"] = php_intval(mp3gain_undo_left_)
                        thisfile_replaygain_["mp3gain"]["undo_right"] = php_intval(mp3gain_undo_right_)
                        thisfile_replaygain_["mp3gain"]["undo_wrap"] = True if mp3gain_undo_wrap_ == "Y" else False
                    else:
                        self.warning("MP3gainUndo value in APEtag appears invalid: \"" + thisfile_ape_items_current_["data"][0] + "\"")
                    # end if
                    break
                # end if
                if case("mp3gain_minmax"):
                    if php_preg_match("#^[0-9]{3},[0-9]{3}$#", thisfile_ape_items_current_["data"][0]):
                        mp3gain_globalgain_min_, mp3gain_globalgain_max_ = php_explode(",", thisfile_ape_items_current_["data"][0])
                        thisfile_replaygain_["mp3gain"]["globalgain_track_min"] = php_intval(mp3gain_globalgain_min_)
                        thisfile_replaygain_["mp3gain"]["globalgain_track_max"] = php_intval(mp3gain_globalgain_max_)
                    else:
                        self.warning("MP3gainMinMax value in APEtag appears invalid: \"" + thisfile_ape_items_current_["data"][0] + "\"")
                    # end if
                    break
                # end if
                if case("mp3gain_album_minmax"):
                    if php_preg_match("#^[0-9]{3},[0-9]{3}$#", thisfile_ape_items_current_["data"][0]):
                        mp3gain_globalgain_album_min_, mp3gain_globalgain_album_max_ = php_explode(",", thisfile_ape_items_current_["data"][0])
                        thisfile_replaygain_["mp3gain"]["globalgain_album_min"] = php_intval(mp3gain_globalgain_album_min_)
                        thisfile_replaygain_["mp3gain"]["globalgain_album_max"] = php_intval(mp3gain_globalgain_album_max_)
                    else:
                        self.warning("MP3gainAlbumMinMax value in APEtag appears invalid: \"" + thisfile_ape_items_current_["data"][0] + "\"")
                    # end if
                    break
                # end if
                if case("tracknumber"):
                    if php_is_array(thisfile_ape_items_current_["data"]):
                        for comment_ in thisfile_ape_items_current_["data"]:
                            thisfile_ape_["comments"]["track_number"][-1] = comment_
                        # end for
                    # end if
                    break
                # end if
                if case("cover art (artist)"):
                    pass
                # end if
                if case("cover art (back)"):
                    pass
                # end if
                if case("cover art (band logo)"):
                    pass
                # end if
                if case("cover art (band)"):
                    pass
                # end if
                if case("cover art (colored fish)"):
                    pass
                # end if
                if case("cover art (composer)"):
                    pass
                # end if
                if case("cover art (conductor)"):
                    pass
                # end if
                if case("cover art (front)"):
                    pass
                # end if
                if case("cover art (icon)"):
                    pass
                # end if
                if case("cover art (illustration)"):
                    pass
                # end if
                if case("cover art (lead)"):
                    pass
                # end if
                if case("cover art (leaflet)"):
                    pass
                # end if
                if case("cover art (lyricist)"):
                    pass
                # end if
                if case("cover art (media)"):
                    pass
                # end if
                if case("cover art (movie scene)"):
                    pass
                # end if
                if case("cover art (other icon)"):
                    pass
                # end if
                if case("cover art (other)"):
                    pass
                # end if
                if case("cover art (performance)"):
                    pass
                # end if
                if case("cover art (publisher logo)"):
                    pass
                # end if
                if case("cover art (recording)"):
                    pass
                # end if
                if case("cover art (studio)"):
                    #// list of possible cover arts from http://taglib-sharp.sourcearchive.com/documentation/2.0.3.0-2/Ape_2Tag_8cs-source.html
                    if php_is_array(thisfile_ape_items_current_["data"]):
                        self.warning("APEtag \"" + item_key_ + "\" should be flagged as Binary data, but was incorrectly flagged as UTF-8")
                        thisfile_ape_items_current_["data"] = php_implode(" ", thisfile_ape_items_current_["data"])
                    # end if
                    thisfile_ape_items_current_["filename"], thisfile_ape_items_current_["data"] = php_explode(" ", thisfile_ape_items_current_["data"], 2)
                    thisfile_ape_items_current_["data_offset"] = thisfile_ape_items_current_["offset"] + php_strlen(thisfile_ape_items_current_["filename"] + " ")
                    thisfile_ape_items_current_["data_length"] = php_strlen(thisfile_ape_items_current_["data"])
                    while True:
                        thisfile_ape_items_current_["image_mime"] = ""
                        imageinfo_ = Array()
                        imagechunkcheck_ = getid3_lib.getdataimagesize(thisfile_ape_items_current_["data"], imageinfo_)
                        if imagechunkcheck_ == False or (not (php_isset(lambda : imagechunkcheck_[2]))):
                            self.warning("APEtag \"" + item_key_ + "\" contains invalid image data")
                            break
                        # end if
                        thisfile_ape_items_current_["image_mime"] = image_type_to_mime_type(imagechunkcheck_[2])
                        if self.inline_attachments == False:
                            thisfile_ape_items_current_["data"] = None
                            break
                        # end if
                        if self.inline_attachments == True:
                            pass
                        elif php_is_int(self.inline_attachments):
                            if self.inline_attachments < thisfile_ape_items_current_["data_length"]:
                                #// too big, skip
                                self.warning("attachment at " + thisfile_ape_items_current_["offset"] + " is too large to process inline (" + number_format(thisfile_ape_items_current_["data_length"]) + " bytes)")
                                thisfile_ape_items_current_["data"] = None
                                break
                            # end if
                        elif php_is_string(self.inline_attachments):
                            self.inline_attachments = php_rtrim(php_str_replace(Array("/", "\\"), DIRECTORY_SEPARATOR, self.inline_attachments), DIRECTORY_SEPARATOR)
                            if (not php_is_dir(self.inline_attachments)) or (not getID3.is_writable(self.inline_attachments)):
                                #// cannot write, skip
                                self.warning("attachment at " + thisfile_ape_items_current_["offset"] + " cannot be saved to \"" + self.inline_attachments + "\" (not writable)")
                                thisfile_ape_items_current_["data"] = None
                                break
                            # end if
                        # end if
                        #// if we get this far, must be OK
                        if php_is_string(self.inline_attachments):
                            destination_filename_ = self.inline_attachments + DIRECTORY_SEPARATOR + php_md5(info_["filenamepath"]) + "_" + thisfile_ape_items_current_["data_offset"]
                            if (not php_file_exists(destination_filename_)) or getID3.is_writable(destination_filename_):
                                file_put_contents(destination_filename_, thisfile_ape_items_current_["data"])
                            else:
                                self.warning("attachment at " + thisfile_ape_items_current_["offset"] + " cannot be saved to \"" + destination_filename_ + "\" (not writable)")
                            # end if
                            thisfile_ape_items_current_["data_filename"] = destination_filename_
                            thisfile_ape_items_current_["data"] = None
                        else:
                            if (not (php_isset(lambda : info_["ape"]["comments"]["picture"]))):
                                info_["ape"]["comments"]["picture"] = Array()
                            # end if
                            comments_picture_data_ = Array()
                            for picture_key_ in Array("data", "image_mime", "image_width", "image_height", "imagetype", "picturetype", "description", "datalength"):
                                if (php_isset(lambda : thisfile_ape_items_current_[picture_key_])):
                                    comments_picture_data_[picture_key_] = thisfile_ape_items_current_[picture_key_]
                                # end if
                            # end for
                            info_["ape"]["comments"]["picture"][-1] = comments_picture_data_
                            comments_picture_data_ = None
                        # end if
                        
                        if False:
                            break
                        # end if
                    # end while
                    break
                # end if
                if case():
                    if php_is_array(thisfile_ape_items_current_["data"]):
                        for comment_ in thisfile_ape_items_current_["data"]:
                            thisfile_ape_["comments"][php_strtolower(item_key_)][-1] = comment_
                        # end for
                    # end if
                    break
                # end if
            # end for
            i_ += 1
        # end while
        if php_empty(lambda : thisfile_replaygain_):
            info_["replay_gain"] = None
        # end if
        return True
    # end def analyze
    #// 
    #// @param string $APEheaderFooterData
    #// 
    #// @return array|false
    #//
    def parseapeheaderfooter(self, APEheaderFooterData_=None):
        
        
        #// http://www.uni-jena.de/~pfk/mpp/sv8/apeheader.html
        #// shortcut
        headerfooterinfo_["raw"] = Array()
        headerfooterinfo_raw_ = headerfooterinfo_["raw"]
        headerfooterinfo_raw_["footer_tag"] = php_substr(APEheaderFooterData_, 0, 8)
        if headerfooterinfo_raw_["footer_tag"] != "APETAGEX":
            return False
        # end if
        headerfooterinfo_raw_["version"] = getid3_lib.littleendian2int(php_substr(APEheaderFooterData_, 8, 4))
        headerfooterinfo_raw_["tagsize"] = getid3_lib.littleendian2int(php_substr(APEheaderFooterData_, 12, 4))
        headerfooterinfo_raw_["tag_items"] = getid3_lib.littleendian2int(php_substr(APEheaderFooterData_, 16, 4))
        headerfooterinfo_raw_["global_flags"] = getid3_lib.littleendian2int(php_substr(APEheaderFooterData_, 20, 4))
        headerfooterinfo_raw_["reserved"] = php_substr(APEheaderFooterData_, 24, 8)
        headerfooterinfo_["tag_version"] = headerfooterinfo_raw_["version"] / 1000
        if headerfooterinfo_["tag_version"] >= 2:
            headerfooterinfo_["flags"] = self.parseapetagflags(headerfooterinfo_raw_["global_flags"])
        # end if
        return headerfooterinfo_
    # end def parseapeheaderfooter
    #// 
    #// @param int $rawflagint
    #// 
    #// @return array
    #//
    def parseapetagflags(self, rawflagint_=None):
        
        
        #// "Note: APE Tags 1.0 do not use any of the APE Tag flags.
        #// All are set to zero on creation and ignored on reading."
        #// http://wiki.hydrogenaud.io/index.php?title=Ape_Tags_Flags
        flags_["header"] = php_bool(rawflagint_ & 2147483648)
        flags_["footer"] = php_bool(rawflagint_ & 1073741824)
        flags_["this_is_header"] = php_bool(rawflagint_ & 536870912)
        flags_["item_contents_raw"] = rawflagint_ & 6 >> 1
        flags_["read_only"] = php_bool(rawflagint_ & 1)
        flags_["item_contents"] = self.apecontenttypeflaglookup(flags_["item_contents_raw"])
        return flags_
    # end def parseapetagflags
    #// 
    #// @param int $contenttypeid
    #// 
    #// @return string
    #//
    def apecontenttypeflaglookup(self, contenttypeid_=None):
        
        
        APEcontentTypeFlagLookup_ = Array({0: "utf-8", 1: "binary", 2: "external", 3: "reserved"})
        return APEcontentTypeFlagLookup_[contenttypeid_] if (php_isset(lambda : APEcontentTypeFlagLookup_[contenttypeid_])) else "invalid"
    # end def apecontenttypeflaglookup
    #// 
    #// @param string $itemkey
    #// 
    #// @return bool
    #//
    def apetagitemisutf8lookup(self, itemkey_=None):
        
        
        APEtagItemIsUTF8Lookup_ = Array("title", "subtitle", "artist", "album", "debut album", "publisher", "conductor", "track", "composer", "comment", "copyright", "publicationright", "file", "year", "record date", "record location", "genre", "media", "related", "isrc", "abstract", "language", "bibliography")
        return php_in_array(php_strtolower(itemkey_), APEtagItemIsUTF8Lookup_)
    # end def apetagitemisutf8lookup
# end class getid3_apetag
