#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core_Util", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core_Util
#//
class ParagonIE_Sodium_Core_Util():
    #// 
    #// @param int $integer
    #// @param int $size (16, 32, 64)
    #// @return int
    #//
    @classmethod
    def abs(self, integer_=None, size_=0):
        
        
        #// @var int $realSize
        realSize_ = PHP_INT_SIZE << 3 - 1
        if size_:
            size_ -= 1
        else:
            #// @var int $size
            size_ = realSize_
        # end if
        negative_ = -integer_ >> size_ & 1
        return php_int(integer_ ^ negative_ + negative_ >> realSize_ & 1)
    # end def abs
    #// 
    #// Convert a binary string into a hexadecimal string without cache-timing
    #// leaks
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $binaryString (raw binary)
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def bin2hex(self, binaryString_=None):
        
        
        #// Type checks:
        if (not php_is_string(binaryString_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(binaryString_) + " given."))
        # end if
        hex_ = ""
        len_ = self.strlen(binaryString_)
        i_ = 0
        while i_ < len_:
            
            #// @var array<int, int> $chunk
            chunk_ = unpack("C", binaryString_[i_])
            #// @var int $c
            c_ = chunk_[1] & 15
            #// @var int $b
            b_ = chunk_[1] >> 4
            hex_ += pack("CC", 87 + b_ + b_ - 10 >> 8 & (1 << (38).bit_length()) - 1 - 38, 87 + c_ + c_ - 10 >> 8 & (1 << (38).bit_length()) - 1 - 38)
            i_ += 1
        # end while
        return hex_
    # end def bin2hex
    #// 
    #// Convert a binary string into a hexadecimal string without cache-timing
    #// leaks, returning uppercase letters (as per RFC 4648)
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $bin_string (raw binary)
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def bin2hexupper(self, bin_string_=None):
        
        
        hex_ = ""
        len_ = self.strlen(bin_string_)
        i_ = 0
        while i_ < len_:
            
            #// @var array<int, int> $chunk
            chunk_ = unpack("C", bin_string_[i_])
            #// 
            #// Lower 16 bits
            #// 
            #// @var int $c
            #//
            c_ = chunk_[1] & 15
            #// 
            #// Upper 16 bits
            #// @var int $b
            #//
            b_ = chunk_[1] >> 4
            #// 
            #// Use pack() and binary operators to turn the two integers
            #// into hexadecimal characters. We don't use chr() here, because
            #// it uses a lookup table internally and we want to avoid
            #// cache-timing side-channels.
            #//
            hex_ += pack("CC", 55 + b_ + b_ - 10 >> 8 & (1 << (6).bit_length()) - 1 - 6, 55 + c_ + c_ - 10 >> 8 & (1 << (6).bit_length()) - 1 - 6)
            i_ += 1
        # end while
        return hex_
    # end def bin2hexupper
    #// 
    #// Cache-timing-safe variant of ord()
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $chr
    #// @return int
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def chrtoint(self, chr_=None):
        
        
        #// Type checks:
        if (not php_is_string(chr_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(chr_) + " given."))
        # end if
        if self.strlen(chr_) != 1:
            raise php_new_class("SodiumException", lambda : SodiumException("chrToInt() expects a string that is exactly 1 character long"))
        # end if
        #// @var array<int, int> $chunk
        chunk_ = unpack("C", chr_)
        return php_int(chunk_[1])
    # end def chrtoint
    #// 
    #// Compares two strings.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $left
    #// @param string $right
    #// @param int $len
    #// @return int
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def compare(self, left_=None, right_=None, len_=None):
        if len_ is None:
            len_ = None
        # end if
        
        leftLen_ = self.strlen(left_)
        rightLen_ = self.strlen(right_)
        if len_ == None:
            len_ = php_max(leftLen_, rightLen_)
            left_ = php_str_pad(left_, len_, " ", STR_PAD_RIGHT)
            right_ = php_str_pad(right_, len_, " ", STR_PAD_RIGHT)
        # end if
        gt_ = 0
        eq_ = 1
        i_ = len_
        while True:
            
            if not (i_ != 0):
                break
            # end if
            i_ -= 1
            gt_ |= self.chrtoint(right_[i_]) - self.chrtoint(left_[i_]) >> 8 & eq_
            eq_ &= self.chrtoint(right_[i_]) ^ self.chrtoint(left_[i_]) - 1 >> 8
        # end while
        return gt_ + gt_ + eq_ - 1
    # end def compare
    #// 
    #// If a variable does not match a given type, throw a TypeError.
    #// 
    #// @param mixed $mixedVar
    #// @param string $type
    #// @param int $argumentIndex
    #// @throws TypeError
    #// @throws SodiumException
    #// @return void
    #//
    @classmethod
    def declarescalartype(self, mixedVar_=None, type_="void", argumentIndex_=0):
        if mixedVar_ is None:
            mixedVar_ = None
        # end if
        
        if php_func_num_args() == 0:
            #// Tautology, by default
            return
        # end if
        if php_func_num_args() == 1:
            raise php_new_class("TypeError", lambda : TypeError("Declared void, but passed a variable"))
        # end if
        realType_ = php_strtolower(gettype(mixedVar_))
        type_ = php_strtolower(type_)
        for case in Switch(type_):
            if case("null"):
                if mixedVar_ != None:
                    raise php_new_class("TypeError", lambda : TypeError("Argument " + argumentIndex_ + " must be null, " + realType_ + " given."))
                # end if
                break
            # end if
            if case("integer"):
                pass
            # end if
            if case("int"):
                allow_ = Array("int", "integer")
                if (not php_in_array(type_, allow_)):
                    raise php_new_class("TypeError", lambda : TypeError("Argument " + argumentIndex_ + " must be an integer, " + realType_ + " given."))
                # end if
                mixedVar_ = php_int(mixedVar_)
                break
            # end if
            if case("boolean"):
                pass
            # end if
            if case("bool"):
                allow_ = Array("bool", "boolean")
                if (not php_in_array(type_, allow_)):
                    raise php_new_class("TypeError", lambda : TypeError("Argument " + argumentIndex_ + " must be a boolean, " + realType_ + " given."))
                # end if
                mixedVar_ = php_bool(mixedVar_)
                break
            # end if
            if case("string"):
                if (not php_is_string(mixedVar_)):
                    raise php_new_class("TypeError", lambda : TypeError("Argument " + argumentIndex_ + " must be a string, " + realType_ + " given."))
                # end if
                mixedVar_ = php_str(mixedVar_)
                break
            # end if
            if case("decimal"):
                pass
            # end if
            if case("double"):
                pass
            # end if
            if case("float"):
                allow_ = Array("decimal", "double", "float")
                if (not php_in_array(type_, allow_)):
                    raise php_new_class("TypeError", lambda : TypeError("Argument " + argumentIndex_ + " must be a float, " + realType_ + " given."))
                # end if
                mixedVar_ = php_float(mixedVar_)
                break
            # end if
            if case("object"):
                if (not php_is_object(mixedVar_)):
                    raise php_new_class("TypeError", lambda : TypeError("Argument " + argumentIndex_ + " must be an object, " + realType_ + " given."))
                # end if
                break
            # end if
            if case("array"):
                if (not php_is_array(mixedVar_)):
                    if php_is_object(mixedVar_):
                        if type(mixedVar_).__name__ == "ArrayAccess":
                            return
                        # end if
                    # end if
                    raise php_new_class("TypeError", lambda : TypeError("Argument " + argumentIndex_ + " must be an array, " + realType_ + " given."))
                # end if
                break
            # end if
            if case():
                raise php_new_class("SodiumException", lambda : SodiumException("Unknown type (" + realType_ + ") does not match expect type (" + type_ + ")"))
            # end if
        # end for
    # end def declarescalartype
    #// 
    #// Evaluate whether or not two strings are equal (in constant-time)
    #// 
    #// @param string $left
    #// @param string $right
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def hashequals(self, left_=None, right_=None):
        
        
        #// Type checks:
        if (not php_is_string(left_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(left_) + " given."))
        # end if
        if (not php_is_string(right_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string, " + gettype(right_) + " given."))
        # end if
        if php_is_callable("hash_equals"):
            return hash_equals(left_, right_)
        # end if
        d_ = 0
        #// @var int $len
        len_ = self.strlen(left_)
        if len_ != self.strlen(right_):
            return False
        # end if
        i_ = 0
        while i_ < len_:
            
            d_ |= self.chrtoint(left_[i_]) ^ self.chrtoint(right_[i_])
            i_ += 1
        # end while
        if d_ != 0:
            return False
        # end if
        return left_ == right_
    # end def hashequals
    #// 
    #// Convert a hexadecimal string into a binary string without cache-timing
    #// leaks
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $hexString
    #// @param bool $strictPadding
    #// @return string (raw binary)
    #// @throws RangeException
    #// @throws TypeError
    #//
    @classmethod
    def hex2bin(self, hexString_=None, strictPadding_=None):
        if strictPadding_ is None:
            strictPadding_ = False
        # end if
        
        #// Type checks:
        if (not php_is_string(hexString_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(hexString_) + " given."))
        # end if
        #// @var int $hex_pos
        hex_pos_ = 0
        #// @var string $bin
        bin_ = ""
        #// @var int $c_acc
        c_acc_ = 0
        #// @var int $hex_len
        hex_len_ = self.strlen(hexString_)
        #// @var int $state
        state_ = 0
        if hex_len_ & 1 != 0:
            if strictPadding_:
                raise php_new_class("RangeException", lambda : RangeException("Expected an even number of hexadecimal characters"))
            else:
                hexString_ = "0" + hexString_
                hex_len_ += 1
            # end if
        # end if
        chunk_ = unpack("C*", hexString_)
        while True:
            
            if not (hex_pos_ < hex_len_):
                break
            # end if
            hex_pos_ += 1
            #// @var int $c
            c_ = chunk_[hex_pos_]
            #// @var int $c_num
            c_num_ = c_ ^ 48
            #// @var int $c_num0
            c_num0_ = c_num_ - 10 >> 8
            #// @var int $c_alpha
            c_alpha_ = c_ & (1 << (32).bit_length()) - 1 - 32 - 55
            #// @var int $c_alpha0
            c_alpha0_ = c_alpha_ - 10 ^ c_alpha_ - 16 >> 8
            if c_num0_ | c_alpha0_ == 0:
                raise php_new_class("RangeException", lambda : RangeException("hex2bin() only expects hexadecimal characters"))
            # end if
            #// @var int $c_val
            c_val_ = c_num0_ & c_num_ | c_alpha_ & c_alpha0_
            if state_ == 0:
                c_acc_ = c_val_ * 16
            else:
                bin_ += pack("C", c_acc_ | c_val_)
            # end if
            state_ ^= 1
        # end while
        return bin_
    # end def hex2bin
    #// 
    #// Turn an array of integers into a string
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param array<int, int> $ints
    #// @return string
    #//
    @classmethod
    def intarraytostring(self, ints_=None):
        
        
        #// @var array<int, int> $args
        args_ = ints_
        for i_,v_ in args_.items():
            args_[i_] = php_int(v_ & 255)
        # end for
        array_unshift(args_, php_str_repeat("C", php_count(ints_)))
        return php_str(call_user_func_array("pack", args_))
    # end def intarraytostring
    #// 
    #// Cache-timing-safe variant of ord()
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $int
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def inttochr(self, int_=None):
        
        
        return pack("C", int_)
    # end def inttochr
    #// 
    #// Load a 3 character substring into an integer
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $string
    #// @return int
    #// @throws RangeException
    #// @throws TypeError
    #//
    @classmethod
    def load_3(self, string_=None):
        
        
        #// Type checks:
        if (not php_is_string(string_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(string_) + " given."))
        # end if
        #// Input validation:
        if self.strlen(string_) < 3:
            raise php_new_class("RangeException", lambda : RangeException("String must be 3 bytes or more; " + self.strlen(string_) + " given."))
        # end if
        #// @var array<int, int> $unpacked
        unpacked_ = unpack("V", string_ + " ")
        return php_int(unpacked_[1] & 16777215)
    # end def load_3
    #// 
    #// Load a 4 character substring into an integer
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $string
    #// @return int
    #// @throws RangeException
    #// @throws TypeError
    #//
    @classmethod
    def load_4(self, string_=None):
        
        
        #// Type checks:
        if (not php_is_string(string_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(string_) + " given."))
        # end if
        #// Input validation:
        if self.strlen(string_) < 4:
            raise php_new_class("RangeException", lambda : RangeException("String must be 4 bytes or more; " + self.strlen(string_) + " given."))
        # end if
        #// @var array<int, int> $unpacked
        unpacked_ = unpack("V", string_)
        return php_int(unpacked_[1] & 4294967295)
    # end def load_4
    #// 
    #// Load a 8 character substring into an integer
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $string
    #// @return int
    #// @throws RangeException
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def load64_le(self, string_=None):
        
        
        #// Type checks:
        if (not php_is_string(string_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string, " + gettype(string_) + " given."))
        # end if
        #// Input validation:
        if self.strlen(string_) < 4:
            raise php_new_class("RangeException", lambda : RangeException("String must be 4 bytes or more; " + self.strlen(string_) + " given."))
        # end if
        if PHP_VERSION_ID >= 50603 and PHP_INT_SIZE == 8:
            #// @var array<int, int> $unpacked
            unpacked_ = unpack("P", string_)
            return php_int(unpacked_[1])
        # end if
        #// @var int $result
        result_ = self.chrtoint(string_[0]) & 255
        result_ |= self.chrtoint(string_[1]) & 255 << 8
        result_ |= self.chrtoint(string_[2]) & 255 << 16
        result_ |= self.chrtoint(string_[3]) & 255 << 24
        result_ |= self.chrtoint(string_[4]) & 255 << 32
        result_ |= self.chrtoint(string_[5]) & 255 << 40
        result_ |= self.chrtoint(string_[6]) & 255 << 48
        result_ |= self.chrtoint(string_[7]) & 255 << 56
        return php_int(result_)
    # end def load64_le
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $left
    #// @param string $right
    #// @return int
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def memcmp(self, left_=None, right_=None):
        
        
        if self.hashequals(left_, right_):
            return 0
        # end if
        return -1
    # end def memcmp
    #// 
    #// Multiply two integers in constant-time
    #// 
    #// Micro-architecture timing side-channels caused by how your CPU
    #// implements multiplication are best prevented by never using the
    #// multiplication operators and ensuring that our code always takes
    #// the same number of operations to complete, regardless of the values
    #// of $a and $b.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $a
    #// @param int $b
    #// @param int $size Limits the number of operations (useful for small,
    #// constant operands)
    #// @return int
    #//
    @classmethod
    def mul(self, a_=None, b_=None, size_=0):
        
        
        if ParagonIE_Sodium_Compat.fastMult:
            return php_int(a_ * b_)
        # end if
        defaultSize_ = None
        #// @var int $defaultSize
        if (not defaultSize_):
            #// @var int $defaultSize
            defaultSize_ = PHP_INT_SIZE << 3 - 1
        # end if
        if size_ < 1:
            #// @var int $size
            size_ = defaultSize_
        # end if
        #// @var int $size
        c_ = 0
        #// 
        #// Mask is either -1 or 0.
        #// 
        #// -1 in binary looks like 0x1111 ... 1111
        #// 0 in binary looks like 0x0000 ... 0000
        #// 
        #// @var int
        #//
        mask_ = -b_ >> php_int(defaultSize_) & 1
        #// 
        #// Ensure $b is a positive integer, without creating
        #// a branching side-channel
        #// 
        #// @var int $b
        #//
        b_ = b_ & (1 << (mask_).bit_length()) - 1 - mask_ | mask_ & -b_
        #// 
        #// Unless $size is provided:
        #// 
        #// This loop always runs 32 times when PHP_INT_SIZE is 4.
        #// This loop always runs 64 times when PHP_INT_SIZE is 8.
        #//
        i_ = size_
        while i_ >= 0:
            
            c_ += php_int(a_ & -b_ & 1)
            a_ <<= 1
            b_ >>= 1
            i_ -= 1
        # end while
        #// 
        #// If $b was negative, we then apply the same value to $c here.
        #// It doesn't matter much if $a was negative; the $c += above would
        #// have produced a negative integer to begin with. But a negative $b
        #// makes $b >>= 1 never return 0, so we would end up with incorrect
        #// results.
        #// 
        #// The end result is what we'd expect from integer multiplication.
        #//
        return php_int(c_ & (1 << (mask_).bit_length()) - 1 - mask_ | mask_ & -c_)
    # end def mul
    #// 
    #// Convert any arbitrary numbers into two 32-bit integers that represent
    #// a 64-bit integer.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int|float $num
    #// @return array<int, int>
    #//
    @classmethod
    def numericto64bitinteger(self, num_=None):
        
        
        high_ = 0
        #// @var int $low
        low_ = num_ & 4294967295
        if +abs(num_) >= 1:
            if num_ > 0:
                #// @var int $high
                high_ = php_min(+floor(num_ / 4294967296), 4294967295)
            else:
                #// @var int $high
                high_ = (1 << ((1 << (+ceil(num_ - +(1 << ((1 << (num_).bit_length()) - 1 - num_).bit_length()) - 1 - (1 << (num_).bit_length()) - 1 - num_ / 4294967296)).bit_length()) - 1 - +ceil(num_ - +(1 << ((1 << (num_).bit_length()) - 1 - num_).bit_length()) - 1 - (1 << (num_).bit_length()) - 1 - num_ / 4294967296)).bit_length()) - 1 - (1 << (+ceil(num_ - +(1 << ((1 << (num_).bit_length()) - 1 - num_).bit_length()) - 1 - (1 << (num_).bit_length()) - 1 - num_ / 4294967296)).bit_length()) - 1 - +ceil(num_ - +(1 << ((1 << (num_).bit_length()) - 1 - num_).bit_length()) - 1 - (1 << (num_).bit_length()) - 1 - num_ / 4294967296)
            # end if
        # end if
        return Array(php_int(high_), php_int(low_))
    # end def numericto64bitinteger
    #// 
    #// Store a 24-bit integer into a string, treating it as big-endian.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $int
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def store_3(self, int_=None):
        
        
        #// Type checks:
        if (not php_is_int(int_)):
            if php_is_numeric(int_):
                int_ = php_int(int_)
            else:
                raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be an integer, " + gettype(int_) + " given."))
            # end if
        # end if
        #// @var string $packed
        packed_ = pack("N", int_)
        return self.substr(packed_, 1, 3)
    # end def store_3
    #// 
    #// Store a 32-bit integer into a string, treating it as little-endian.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $int
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def store32_le(self, int_=None):
        
        
        #// Type checks:
        if (not php_is_int(int_)):
            if php_is_numeric(int_):
                int_ = php_int(int_)
            else:
                raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be an integer, " + gettype(int_) + " given."))
            # end if
        # end if
        #// @var string $packed
        packed_ = pack("V", int_)
        return packed_
    # end def store32_le
    #// 
    #// Store a 32-bit integer into a string, treating it as big-endian.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $int
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def store_4(self, int_=None):
        
        
        #// Type checks:
        if (not php_is_int(int_)):
            if php_is_numeric(int_):
                int_ = php_int(int_)
            else:
                raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be an integer, " + gettype(int_) + " given."))
            # end if
        # end if
        #// @var string $packed
        packed_ = pack("N", int_)
        return packed_
    # end def store_4
    #// 
    #// Stores a 64-bit integer as an string, treating it as little-endian.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $int
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def store64_le(self, int_=None):
        
        
        #// Type checks:
        if (not php_is_int(int_)):
            if php_is_numeric(int_):
                int_ = php_int(int_)
            else:
                raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be an integer, " + gettype(int_) + " given."))
            # end if
        # end if
        if PHP_INT_SIZE == 8:
            if PHP_VERSION_ID >= 50603:
                #// @var string $packed
                packed_ = pack("P", int_)
                return packed_
            # end if
            return self.inttochr(int_ & 255) + self.inttochr(int_ >> 8 & 255) + self.inttochr(int_ >> 16 & 255) + self.inttochr(int_ >> 24 & 255) + self.inttochr(int_ >> 32 & 255) + self.inttochr(int_ >> 40 & 255) + self.inttochr(int_ >> 48 & 255) + self.inttochr(int_ >> 56 & 255)
        # end if
        if int_ > PHP_INT_MAX:
            hiB_, int_ = self.numericto64bitinteger(int_)
        else:
            hiB_ = 0
        # end if
        return self.inttochr(int_ & 255) + self.inttochr(int_ >> 8 & 255) + self.inttochr(int_ >> 16 & 255) + self.inttochr(int_ >> 24 & 255) + self.inttochr(hiB_ & 255) + self.inttochr(hiB_ >> 8 & 255) + self.inttochr(hiB_ >> 16 & 255) + self.inttochr(hiB_ >> 24 & 255)
    # end def store64_le
    #// 
    #// Safe string length
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @ref mbstring.func_overload
    #// 
    #// @param string $str
    #// @return int
    #// @throws TypeError
    #//
    @classmethod
    def strlen(self, str_=None):
        
        
        #// Type checks:
        if (not php_is_string(str_)):
            raise php_new_class("TypeError", lambda : TypeError("String expected"))
        # end if
        return php_int(php_mb_strlen(str_, "8bit") if self.ismbstringoverride() else php_strlen(str_))
    # end def strlen
    #// 
    #// Turn a string into an array of integers
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $string
    #// @return array<int, int>
    #// @throws TypeError
    #//
    @classmethod
    def stringtointarray(self, string_=None):
        
        
        if (not php_is_string(string_)):
            raise php_new_class("TypeError", lambda : TypeError("String expected"))
        # end if
        #// 
        #// @var array<int, int>
        #//
        values_ = php_array_values(unpack("C*", string_))
        return values_
    # end def stringtointarray
    #// 
    #// Safe substring
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @ref mbstring.func_overload
    #// 
    #// @param string $str
    #// @param int $start
    #// @param int $length
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def substr(self, str_=None, start_=0, length_=None):
        if length_ is None:
            length_ = None
        # end if
        
        #// Type checks:
        if (not php_is_string(str_)):
            raise php_new_class("TypeError", lambda : TypeError("String expected"))
        # end if
        if length_ == 0:
            return ""
        # end if
        if self.ismbstringoverride():
            if PHP_VERSION_ID < 50400 and length_ == None:
                length_ = self.strlen(str_)
            # end if
            sub_ = php_str(php_mb_substr(str_, start_, length_, "8bit"))
        elif length_ == None:
            sub_ = php_str(php_substr(str_, start_))
        else:
            sub_ = php_str(php_substr(str_, start_, length_))
        # end if
        if sub_ != "":
            return sub_
        # end if
        return ""
    # end def substr
    #// 
    #// Compare a 16-character byte string in constant time.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $a
    #// @param string $b
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def verify_16(self, a_=None, b_=None):
        
        
        #// Type checks:
        if (not php_is_string(a_)):
            raise php_new_class("TypeError", lambda : TypeError("String expected"))
        # end if
        if (not php_is_string(b_)):
            raise php_new_class("TypeError", lambda : TypeError("String expected"))
        # end if
        return self.hashequals(self.substr(a_, 0, 16), self.substr(b_, 0, 16))
    # end def verify_16
    #// 
    #// Compare a 32-character byte string in constant time.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $a
    #// @param string $b
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def verify_32(self, a_=None, b_=None):
        
        
        #// Type checks:
        if (not php_is_string(a_)):
            raise php_new_class("TypeError", lambda : TypeError("String expected"))
        # end if
        if (not php_is_string(b_)):
            raise php_new_class("TypeError", lambda : TypeError("String expected"))
        # end if
        return self.hashequals(self.substr(a_, 0, 32), self.substr(b_, 0, 32))
    # end def verify_32
    #// 
    #// Calculate $a ^ $b for two strings.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $a
    #// @param string $b
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def xorstrings(self, a_=None, b_=None):
        
        
        #// Type checks:
        if (not php_is_string(a_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 1 must be a string"))
        # end if
        if (not php_is_string(b_)):
            raise php_new_class("TypeError", lambda : TypeError("Argument 2 must be a string"))
        # end if
        return php_str(a_ ^ b_)
    # end def xorstrings
    #// 
    #// Returns whether or not mbstring.func_overload is in effect.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return bool
    #//
    def ismbstringoverride(self):
        
        
        mbstring_ = None
        if mbstring_ == None:
            mbstring_ = php_extension_loaded("mbstring") and php_int(php_ini_get("mbstring.func_overload")) & MB_OVERLOAD_STRING
        # end if
        #// @var bool $mbstring
        return mbstring_
    # end def ismbstringoverride
# end class ParagonIE_Sodium_Core_Util
