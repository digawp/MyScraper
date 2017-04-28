import sys, codecs

# Change the encoding if necessary
ENCODING = 'utf-16'

with codecs.open(sys.argv[1], 'r', ENCODING) as infile:
    with codecs.open(sys.argv[1] + '_cleaned', 'w', ENCODING) as outfile:
        for line in infile:
            extra_path_idx = line.find('/', 34) # return -1 if not found
            # For some reason [:-1] removes the newline, but it is good in this
            # case because if extra path is found, the newline will also be
            # stripped off, thus need to add newline on both cases
            clean_path = line[:extra_path_idx]+'\n'
            outfile.write(clean_path)
