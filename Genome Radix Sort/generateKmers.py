"""
@author: Sol Jennings 26356015
@created: 2016-04-17
@description:

Converts a given file with a single long string to file called kmers in the format
kmer    int_kmer    offset


Usage:
python generateKmers.py [window size] [input filename] [output filename]

outputfile name will default to kmers.txt


"""

import sys

"""
The alphabet of the string file.
"""
ALPHABET = ['A', 'C', 'G', 'T']


class GenerateKmers:
    def __init__(self, window_size):
        """
        Initialise the generate kmers object with a window size
        :param window_size: the window size of the kmers
        """
        if window_size < 16 or window_size > 32:
            raise ValueError("Window must be an integer between 16 and 32 inclusive")
        self.window_size = window_size

    def convert_file(self, infile, outfile):
        """
        Convert the input file over the alphabet into a kmer string, kmer int and offset
        and write it to the output file
        :param infile: the input file
        :param outfile: the output file
        """
        # open output file for writing
        outfile = open(outfile, 'w')

        with open(infile) as f:
            position = 1
            # read in an initial window of window_size -1 characters
            window = f.read(self.window_size - 1)
            while True:
                # read in 1 character
                c = f.read(1)
                # if the character is not in the alphabet, finish reading in
                if not c or c not in ALPHABET:
                    break
                # add 1 character to the current window
                window += c
                # convert the kmer string to base
                int_enc_kmer = self.string_to_base(window)
                # convert kmer to integer base 10
                int_enc_kmer = int(int_enc_kmer, len(ALPHABET))
                # convert to a string for writing
                int_enc_kmer = str(int_enc_kmer)
                if len(int_enc_kmer):
                    outfile.write(window + "\t" + int_enc_kmer + "\t" + str(position) + "\n")
                # remove 1 character from front of the window
                window = window[1:]
                position += 1

    def string_to_base(self, string):
        """
        Convert a string over the alphabet into an integer
        a base of the alphabet size will be used

        :param string:
        :return:
        """
        # initialise an empty string
        integer = ""
        for i in string:
            if i in ALPHABET:
                # append alphabet position to end of string
                integer += str(ALPHABET.index(i))
        return integer


if __name__ == "__main__":
    """
    Take file as input from the user and process kmer file for it
    """
    if len(sys.argv) < 3:
        print("Not enough arguments")
        print("Must be of form:")
        print("generateKmers.py [window] [infile] [outfile]")
        exit()

    input_file = sys.argv[2]
    output_file = "kmers.txt"
    window_size = 0

    if len(sys.argv) == 4:
        output_file = sys.argv[3]
    try:
        window_size = int(sys.argv[1])
    except ValueError:
        print("Window is not an integer")
        exit()
    try:
        gk = GenerateKmers(window_size)
        print("Generating from " + input_file + " with window size " + str(window_size) + "...")
        gk.convert_file(input_file, output_file)
        print("kmer file " + output_file + " created!")
    except IOError:
        print("Unable to open input or output file")
    except (ValueError) as e:
        print(e)
