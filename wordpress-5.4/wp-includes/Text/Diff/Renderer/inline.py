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
#// "Inline" diff renderer.
#// 
#// Copyright 2004-2010 The Horde Project (http://www.horde.org/)
#// 
#// See the enclosed file COPYING for license information (LGPL). If you did
#// not receive this file, see http://opensource.org/licenses/lgpl-license.php.
#// 
#// @author  Ciprian Popovici
#// @package Text_Diff
#// 
#// Text_Diff_Renderer
#// WP #7391
php_include_file(php_dirname(php_dirname(__FILE__)) + "/Renderer.php", once=True)
#// 
#// "Inline" diff renderer.
#// 
#// This class renders diffs in the Wiki-style "inline" format.
#// 
#// @author  Ciprian Popovici
#// @package Text_Diff
#//
class Text_Diff_Renderer_inline(Text_Diff_Renderer):
    #// 
    #// Number of leading context "lines" to preserve.
    #// 
    #// @var integer
    #//
    _leading_context_lines = 10000
    #// 
    #// Number of trailing context "lines" to preserve.
    #// 
    #// @var integer
    #//
    _trailing_context_lines = 10000
    #// 
    #// Prefix for inserted text.
    #// 
    #// @var string
    #//
    _ins_prefix = "<ins>"
    #// 
    #// Suffix for inserted text.
    #// 
    #// @var string
    #//
    _ins_suffix = "</ins>"
    #// 
    #// Prefix for deleted text.
    #// 
    #// @var string
    #//
    _del_prefix = "<del>"
    #// 
    #// Suffix for deleted text.
    #// 
    #// @var string
    #//
    _del_suffix = "</del>"
    #// 
    #// Header for each change block.
    #// 
    #// @var string
    #//
    _block_header = ""
    #// 
    #// Whether to split down to character-level.
    #// 
    #// @var boolean
    #//
    _split_characters = False
    #// 
    #// What are we currently splitting on? Used to recurse to show word-level
    #// or character-level changes.
    #// 
    #// @var string
    #//
    _split_level = "lines"
    def _blockheader(self, xbeg_=None, xlen_=None, ybeg_=None, ylen_=None):
        
        
        return self._block_header
    # end def _blockheader
    def _startblock(self, header_=None):
        
        
        return header_
    # end def _startblock
    def _lines(self, lines_=None, prefix_=" ", encode_=None):
        if encode_ is None:
            encode_ = True
        # end if
        
        if encode_:
            php_array_walk(lines_, Array(self, "_encode"))
        # end if
        if self._split_level == "lines":
            return php_implode("\n", lines_) + "\n"
        else:
            return php_implode("", lines_)
        # end if
    # end def _lines
    def _added(self, lines_=None):
        
        
        php_array_walk(lines_, Array(self, "_encode"))
        lines_[0] = self._ins_prefix + lines_[0]
        lines_[php_count(lines_) - 1] += self._ins_suffix
        return self._lines(lines_, " ", False)
    # end def _added
    def _deleted(self, lines_=None, words_=None):
        if words_ is None:
            words_ = False
        # end if
        
        php_array_walk(lines_, Array(self, "_encode"))
        lines_[0] = self._del_prefix + lines_[0]
        lines_[php_count(lines_) - 1] += self._del_suffix
        return self._lines(lines_, " ", False)
    # end def _deleted
    def _changed(self, orig_=None, final_=None):
        
        
        #// If we've already split on characters, just display.
        if self._split_level == "characters":
            return self._deleted(orig_) + self._added(final_)
        # end if
        #// If we've already split on words, just display.
        if self._split_level == "words":
            prefix_ = ""
            while True:
                
                if not (orig_[0] != False and final_[0] != False and php_substr(orig_[0], 0, 1) == " " and php_substr(final_[0], 0, 1) == " "):
                    break
                # end if
                prefix_ += php_substr(orig_[0], 0, 1)
                orig_[0] = php_substr(orig_[0], 1)
                final_[0] = php_substr(final_[0], 1)
            # end while
            return prefix_ + self._deleted(orig_) + self._added(final_)
        # end if
        text1_ = php_implode("\n", orig_)
        text2_ = php_implode("\n", final_)
        #// Non-printing newline marker.
        nl_ = " "
        if self._split_characters:
            diff_ = php_new_class("Text_Diff", lambda : Text_Diff("native", Array(php_preg_split("//", text1_), php_preg_split("//", text2_))))
        else:
            #// We want to split on word boundaries, but we need to preserve
            #// whitespace as well. Therefore we split on words, but include
            #// all blocks of whitespace in the wordlist.
            diff_ = php_new_class("Text_Diff", lambda : Text_Diff("native", Array(self._splitonwords(text1_, nl_), self._splitonwords(text2_, nl_))))
        # end if
        #// Get the diff in inline format.
        renderer_ = php_new_class("Text_Diff_Renderer_inline", lambda : Text_Diff_Renderer_inline(php_array_merge(self.getparams(), Array({"split_level": "characters" if self._split_characters else "words"}))))
        #// Run the diff and get the output.
        return php_str_replace(nl_, "\n", renderer_.render(diff_)) + "\n"
    # end def _changed
    def _splitonwords(self, string_=None, newlineEscape_="\n"):
        
        
        #// Ignore \0; otherwise the while loop will never finish.
        string_ = php_str_replace(" ", "", string_)
        words_ = Array()
        length_ = php_strlen(string_)
        pos_ = 0
        while True:
            
            if not (pos_ < length_):
                break
            # end if
            #// Eat a word with any preceding whitespace.
            spaces_ = strspn(php_substr(string_, pos_), " \n")
            nextpos_ = strcspn(php_substr(string_, pos_ + spaces_), " \n")
            words_[-1] = php_str_replace("\n", newlineEscape_, php_substr(string_, pos_, spaces_ + nextpos_))
            pos_ += spaces_ + nextpos_
        # end while
        return words_
    # end def _splitonwords
    def _encode(self, string_=None):
        
        
        string_ = htmlspecialchars(string_)
    # end def _encode
# end class Text_Diff_Renderer_inline
