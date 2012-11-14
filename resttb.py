#!/usr/bin/python
#
# Copyright (c) 2009 SZHC Inc. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#    * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#    * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# This tool is use to generate a table from a plant text.If you have some 
# document just like 
# h1:h2:h3:h4
# 1: col1  : col2 : col3
# 2: col11 : col22 : col33
# you can use this tool to generate a table use for restructText, just like
# +-----+---------+-------+-------+
# | 1   | col1    | col2  | col3  |
# | 2   | col11   | col22 | col33 |
# +-----+---------+-------+-------+

import sys;
import getopt
import fileinput
import io
from compiler.ast import Return

def usage():
    print("--input= -i input file")
    print("--output= -o output file")
    print("--sep= -s separate char")
    print("--help -h help")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hios", ["help", "input=", "output=", "sep="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output_file = None
    input_file = None
    sep = " "
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output_file = a
        elif o in ("-i", "--input"):
            input_file = a
        elif o in ("-s", "--sep"):
            sep = a
        else:
            assert False, "unhandled option"
            
    print("Begin")
    print("sep = " +  sep)
    content_table = []
    for line in fileinput.input(input_file):
        content_table.append(separate_row(line[:-1], sep))
    
    analyzed_result = analyze(content_table)
    
    out = open(output_file, 'w')
    out.write("\n".join(wrap_table(content_table, analyzed_result)))
    out.close()
    
    print("End")

def separate_row(text, sep):
    return text.split(sep)

def analyze(text_table):
    col_width = [];
    row = []
    col = []
    col_len = 0;
    for i in range(0, len(text_table)):
        row = text_table[i]
        if len(row) > len(col_width):
            col_width.extend([0] * (len(row) - len(col_width)))
        for j in range(0, len(row)):
            col = row[j]
            col_len = calculate_text_width(col) + 2
            if col_len  > col_width[j]:
                col_width[j] = col_len
    print("colum width", col_width)
    return col_width

def wrap_table(text_table, col_info, extra_width = 0):
    ret = []
    tmp_str = ""
    table_line = generate_table_line(col_info, extra_width)
    for row in text_table:
        ret.append(table_line)
        tmp_str = ""
        col_count = len(col_info)
        for i in range(0, col_count):
            row.extend([""] * (col_count - len(row)))
            tmp_str += ("| " + row[i] + (" " * (extra_width + col_info[i] - calculate_text_width(row[i] ) - 1)))
        ret.append(tmp_str + "|")
    ret.append(table_line)
    return ret;

def generate_table_line(col_info, extra_width = 0):
    col_count = len(col_info)
    ret = ""
    for i in range(0, col_count):
        ret += "+"
        ret += "-" * (col_info[i] + extra_width)
    return ret + "+";
    
def calculate_text_width(text):
    unicode_text = unicode(text, 'utf8')
    ret = 0;
    for c in unicode_text:
        if 0x2e80 <= ord(c)< 0x9fff:
            ret += 2
        else:
            ret += 1
    return ret

if __name__ == "__main__":
    main()
    
        
