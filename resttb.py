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
        if 0x4e00 <= ord(c)< 0x9fa6:
            ret += 2
        else:
            ret += 1
    return ret

if __name__ == "__main__":
    main()
    
        