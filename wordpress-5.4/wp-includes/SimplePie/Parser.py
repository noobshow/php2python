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
#// SimplePie
#// 
#// A PHP-Based RSS and Atom Feed Framework.
#// Takes the hard work out of managing a complete RSS/Atom solution.
#// 
#// Copyright (c) 2004-2012, Ryan Parman, Geoffrey Sneddon, Ryan McCue, and contributors
#// All rights reserved.
#// 
#// Redistribution and use in source and binary forms, with or without modification, are
#// permitted provided that the following conditions are met:
#// 
#// Redistributions of source code must retain the above copyright notice, this list of
#// conditions and the following disclaimer.
#// 
#// Redistributions in binary form must reproduce the above copyright notice, this list
#// of conditions and the following disclaimer in the documentation and/or other materials
#// provided with the distribution.
#// 
#// Neither the name of the SimplePie Team nor the names of its contributors may be used
#// to endorse or promote products derived from this software without specific prior
#// written permission.
#// 
#// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS
#// OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
#// AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS
#// AND CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#// SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#// OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#// POSSIBILITY OF SUCH DAMAGE.
#// 
#// @package SimplePie
#// @version 1.3.1
#// @copyright 2004-2012 Ryan Parman, Geoffrey Sneddon, Ryan McCue
#// @author Ryan Parman
#// @author Geoffrey Sneddon
#// @author Ryan McCue
#// @link http://simplepie.org/ SimplePie
#// @license http://www.opensource.org/licenses/bsd-license.php BSD License
#// 
#// 
#// Parses XML into something sane
#// 
#// 
#// This class can be overloaded with {@see SimplePie::set_parser_class()}
#// 
#// @package SimplePie
#// @subpackage Parsing
#//
class SimplePie_Parser():
    error_code = Array()
    error_string = Array()
    current_line = Array()
    current_column = Array()
    current_byte = Array()
    separator = " "
    namespace = Array("")
    element = Array("")
    xml_base = Array("")
    xml_base_explicit = Array(False)
    xml_lang = Array("")
    data = Array()
    datas = Array(Array())
    current_xhtml_construct = -1
    encoding = Array()
    registry = Array()
    def set_registry(self, registry_=None):
        
        
        self.registry = registry_
    # end def set_registry
    def parse(self, data_=None, encoding_=None):
        
        
        #// Use UTF-8 if we get passed US-ASCII, as every US-ASCII character is a UTF-8 character
        if php_strtoupper(encoding_) == "US-ASCII":
            self.encoding = "UTF-8"
        else:
            self.encoding = encoding_
        # end if
        #// Strip BOM:
        #// UTF-32 Big Endian BOM
        if php_substr(data_, 0, 4) == "  þÿ":
            data_ = php_substr(data_, 4)
            #// UTF-32 Little Endian BOM
        elif php_substr(data_, 0, 4) == "ÿþ  ":
            data_ = php_substr(data_, 4)
            #// UTF-16 Big Endian BOM
        elif php_substr(data_, 0, 2) == "þÿ":
            data_ = php_substr(data_, 2)
            #// UTF-16 Little Endian BOM
        elif php_substr(data_, 0, 2) == "ÿþ":
            data_ = php_substr(data_, 2)
            #// UTF-8 BOM
        elif php_substr(data_, 0, 3) == "ï»¿":
            data_ = php_substr(data_, 3)
        # end if
        pos_ = php_strpos(data_, "?>")
        if php_substr(data_, 0, 5) == "<?xml" and strspn(php_substr(data_, 5, 1), " \n\r ") and pos_ != False:
            declaration_ = self.registry.create("XML_Declaration_Parser", Array(php_substr(data_, 5, pos_ - 5)))
            if declaration_.parse():
                data_ = php_substr(data_, pos_ + 2)
                data_ = "<?xml version=\"" + declaration_.version + "\" encoding=\"" + encoding_ + "\" standalone=\"" + "yes" if declaration_.standalone else "no" + "\"?>" + data_
            else:
                self.error_string = "SimplePie bug! Please report this!"
                return False
            # end if
        # end if
        return_ = True
        xml_is_sane_ = None
        if xml_is_sane_ == None:
            parser_check_ = xml_parser_create()
            xml_parse_into_struct(parser_check_, "<foo>&amp;</foo>", values_)
            xml_parser_free(parser_check_)
            xml_is_sane_ = (php_isset(lambda : values_[0]["value"]))
        # end if
        #// Create the parser
        if xml_is_sane_:
            xml_ = xml_parser_create_ns(self.encoding, self.separator)
            xml_parser_set_option(xml_, XML_OPTION_SKIP_WHITE, 1)
            xml_parser_set_option(xml_, XML_OPTION_CASE_FOLDING, 0)
            xml_set_object(xml_, self)
            xml_set_character_data_handler(xml_, "cdata")
            xml_set_element_handler(xml_, "tag_open", "tag_close")
            #// Parse!
            if (not xml_parse(xml_, data_, True)):
                self.error_code = xml_get_error_code(xml_)
                self.error_string = xml_error_string(self.error_code)
                return_ = False
            # end if
            self.current_line = xml_get_current_line_number(xml_)
            self.current_column = xml_get_current_column_number(xml_)
            self.current_byte = xml_get_current_byte_index(xml_)
            xml_parser_free(xml_)
            return return_
        else:
            libxml_clear_errors()
            xml_ = php_new_class("XMLReader", lambda : XMLReader())
            xml_.xml(data_)
            while True:
                
                if not (php_no_error(lambda: xml_.read())):
                    break
                # end if
                for case in Switch(xml_.nodeType):
                    if case(constant("XMLReader::END_ELEMENT")):
                        if xml_.namespaceURI != "":
                            tagName_ = xml_.namespaceURI + self.separator + xml_.localName
                        else:
                            tagName_ = xml_.localName
                        # end if
                        self.tag_close(None, tagName_)
                        break
                    # end if
                    if case(constant("XMLReader::ELEMENT")):
                        empty_ = xml_.isEmptyElement
                        if xml_.namespaceURI != "":
                            tagName_ = xml_.namespaceURI + self.separator + xml_.localName
                        else:
                            tagName_ = xml_.localName
                        # end if
                        attributes_ = Array()
                        while True:
                            
                            if not (xml_.movetonextattribute()):
                                break
                            # end if
                            if xml_.namespaceURI != "":
                                attrName_ = xml_.namespaceURI + self.separator + xml_.localName
                            else:
                                attrName_ = xml_.localName
                            # end if
                            attributes_[attrName_] = xml_.value
                        # end while
                        self.tag_open(None, tagName_, attributes_)
                        if empty_:
                            self.tag_close(None, tagName_)
                        # end if
                        break
                    # end if
                    if case(constant("XMLReader::TEXT")):
                        pass
                    # end if
                    if case(constant("XMLReader::CDATA")):
                        self.cdata(None, xml_.value)
                        break
                    # end if
                # end for
            # end while
            error_ = libxml_get_last_error()
            if error_:
                self.error_code = error_.code
                self.error_string = error_.message
                self.current_line = error_.line
                self.current_column = error_.column
                return False
            else:
                return True
            # end if
        # end if
    # end def parse
    def get_error_code(self):
        
        
        return self.error_code
    # end def get_error_code
    def get_error_string(self):
        
        
        return self.error_string
    # end def get_error_string
    def get_current_line(self):
        
        
        return self.current_line
    # end def get_current_line
    def get_current_column(self):
        
        
        return self.current_column
    # end def get_current_column
    def get_current_byte(self):
        
        
        return self.current_byte
    # end def get_current_byte
    def get_data(self):
        
        
        return self.data
    # end def get_data
    def tag_open(self, parser_=None, tag_=None, attributes_=None):
        
        
        self.namespace[-1], self.element[-1] = self.split_ns(tag_)
        attribs_ = Array()
        for name_,value_ in attributes_.items():
            attrib_namespace_, attribute_ = self.split_ns(name_)
            attribs_[attrib_namespace_][attribute_] = value_
        # end for
        if (php_isset(lambda : attribs_[SIMPLEPIE_NAMESPACE_XML]["base"])):
            base_ = self.registry.call("Misc", "absolutize_url", Array(attribs_[SIMPLEPIE_NAMESPACE_XML]["base"], php_end(self.xml_base)))
            if base_ != False:
                self.xml_base[-1] = base_
                self.xml_base_explicit[-1] = True
            # end if
        else:
            self.xml_base[-1] = php_end(self.xml_base)
            self.xml_base_explicit[-1] = php_end(self.xml_base_explicit)
        # end if
        if (php_isset(lambda : attribs_[SIMPLEPIE_NAMESPACE_XML]["lang"])):
            self.xml_lang[-1] = attribs_[SIMPLEPIE_NAMESPACE_XML]["lang"]
        else:
            self.xml_lang[-1] = php_end(self.xml_lang)
        # end if
        if self.current_xhtml_construct >= 0:
            self.current_xhtml_construct += 1
            if php_end(self.namespace) == SIMPLEPIE_NAMESPACE_XHTML:
                self.data["data"] += "<" + php_end(self.element)
                if (php_isset(lambda : attribs_[""])):
                    for name_,value_ in attribs_[""].items():
                        self.data["data"] += " " + name_ + "=\"" + htmlspecialchars(value_, ENT_COMPAT, self.encoding) + "\""
                    # end for
                # end if
                self.data["data"] += ">"
            # end if
        else:
            self.datas[-1] = self.data
            self.data = self.data["child"][php_end(self.namespace)][php_end(self.element)][-1]
            self.data = Array({"data": "", "attribs": attribs_, "xml_base": php_end(self.xml_base), "xml_base_explicit": php_end(self.xml_base_explicit), "xml_lang": php_end(self.xml_lang)})
            if php_end(self.namespace) == SIMPLEPIE_NAMESPACE_ATOM_03 and php_in_array(php_end(self.element), Array("title", "tagline", "copyright", "info", "summary", "content")) and (php_isset(lambda : attribs_[""]["mode"])) and attribs_[""]["mode"] == "xml" or php_end(self.namespace) == SIMPLEPIE_NAMESPACE_ATOM_10 and php_in_array(php_end(self.element), Array("rights", "subtitle", "summary", "info", "title", "content")) and (php_isset(lambda : attribs_[""]["type"])) and attribs_[""]["type"] == "xhtml" or php_end(self.namespace) == SIMPLEPIE_NAMESPACE_RSS_20 and php_in_array(php_end(self.element), Array("title")) or php_end(self.namespace) == SIMPLEPIE_NAMESPACE_RSS_090 and php_in_array(php_end(self.element), Array("title")) or php_end(self.namespace) == SIMPLEPIE_NAMESPACE_RSS_10 and php_in_array(php_end(self.element), Array("title")):
                self.current_xhtml_construct = 0
            # end if
        # end if
    # end def tag_open
    def cdata(self, parser_=None, cdata_=None):
        
        
        if self.current_xhtml_construct >= 0:
            self.data["data"] += htmlspecialchars(cdata_, ENT_QUOTES, self.encoding)
        else:
            self.data["data"] += cdata_
        # end if
    # end def cdata
    def tag_close(self, parser_=None, tag_=None):
        
        
        if self.current_xhtml_construct >= 0:
            self.current_xhtml_construct -= 1
            if php_end(self.namespace) == SIMPLEPIE_NAMESPACE_XHTML and (not php_in_array(php_end(self.element), Array("area", "base", "basefont", "br", "col", "frame", "hr", "img", "input", "isindex", "link", "meta", "param"))):
                self.data["data"] += "</" + php_end(self.element) + ">"
            # end if
        # end if
        if self.current_xhtml_construct == -1:
            self.data = self.datas[php_count(self.datas) - 1]
            php_array_pop(self.datas)
        # end if
        php_array_pop(self.element)
        php_array_pop(self.namespace)
        php_array_pop(self.xml_base)
        php_array_pop(self.xml_base_explicit)
        php_array_pop(self.xml_lang)
    # end def tag_close
    def split_ns(self, string_=None):
        
        
        cache_ = Array()
        if (not (php_isset(lambda : cache_[string_]))):
            pos_ = php_strpos(string_, self.separator)
            if pos_:
                separator_length_ = None
                if (not separator_length_):
                    separator_length_ = php_strlen(self.separator)
                # end if
                namespace_ = php_substr(string_, 0, pos_)
                local_name_ = php_substr(string_, pos_ + separator_length_)
                if php_strtolower(namespace_) == SIMPLEPIE_NAMESPACE_ITUNES:
                    namespace_ = SIMPLEPIE_NAMESPACE_ITUNES
                # end if
                #// Normalize the Media RSS namespaces
                if namespace_ == SIMPLEPIE_NAMESPACE_MEDIARSS_WRONG or namespace_ == SIMPLEPIE_NAMESPACE_MEDIARSS_WRONG2 or namespace_ == SIMPLEPIE_NAMESPACE_MEDIARSS_WRONG3 or namespace_ == SIMPLEPIE_NAMESPACE_MEDIARSS_WRONG4 or namespace_ == SIMPLEPIE_NAMESPACE_MEDIARSS_WRONG5:
                    namespace_ = SIMPLEPIE_NAMESPACE_MEDIARSS
                # end if
                cache_[string_] = Array(namespace_, local_name_)
            else:
                cache_[string_] = Array("", string_)
            # end if
        # end if
        return cache_[string_]
    # end def split_ns
# end class SimplePie_Parser
