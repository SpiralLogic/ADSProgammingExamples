"""
@author: Sol Jennings 26356015
@created: 2016-04-17
@description:

Uses LSD radix sort to sort a kmer file and writes it to the file "kmers_sorted.txt"

Usage:
python radixLSD.py [filename]

"""
import sys
import math

# radix size to sort over, must be a multiple of the alphabet size
RADIX_BITS = 8


class KmerLine:
    def __init__(self, kmer_str, kmer_int, pos):
        """
        Initialise the Kmer line with 3 pieces of information

        :param kmer_str: the kmer string
        :param kmer_int: the kmer integer
        :param pos: the offset/position of the line
        """
        self.kmer_str = kmer_str
        self.kmer_int = int(kmer_int)
        self.pos = pos


class RadixLSD:
    def __init__(self):
        """
        Initialise the radix sort
        """
        # list of items to be sorted
        self.kmers = []
        # length of the base4, needed to do 8 bits at a time
        self.base4_size = None

    def read_file(self, filename):
        """
        Reads in the kmer file
        :param filename: kmer file to read in
        """
        with open(filename, "r") as file:
            # for each line in the file split by whitespace
            for line in file:
                line = line.split()
                # if this is the first line, work out the size needed for the base 4 to have 8 bits
                # per iteration. This can be worked out from the kmer string
                if self.base4_size is None:
                    self.base4_size = len(line[0])
                # initialise the line as a KmerLine, storing the string, int and offset
                # could be faster if done as a tuple, but not much faster
                newline = KmerLine(line[0], line[1], line[2])
                self.kmers.append(newline)

    def sort(self):
        """
        sort the kmers that have been read in
        """
        # create a bitmask from the radix size
        bitmask = (2 ** RADIX_BITS) - 1

        # the number of bits per base4 needed
        bits_per_base4 = (RADIX_BITS // 2)

        # the number of passes required
        passes = math.ceil(self.base4_size / bits_per_base4)

        print("Sorting with window size: ", self.base4_size)
        # process RADIX_SIZE bits at a time from the kmer
        for i in range(passes, 0, -1):
            print("Sorting pass: " + str(i))

            # initialise buckets to move each kmer into for this iteration
            # we need 2^RADIX_SIZE buckets to do RADIX_SIZE bits at a time of a base4 kmer
            buckets = [[] for _ in range(2 ** RADIX_BITS)]

            # Move each of it's kmers into the correct bucket based on the RADIX_SIZE bits
            # being processed. If the buckets are implemented as a linked list
            # then appending each kmer is done in O(1) time
            for j in range(len(self.kmers)):
                # extract the current bits needed using the bit mask
                bucket_index = self.kmers[j].kmer_int & bitmask
                # remove the trailing zeros to get the correct bucket
                bucket_index >>= (passes - i) * RADIX_BITS
                # convert the base4 to an integer to put in the correct bucket
                # append to the bucket for stability
                buckets[bucket_index].append(self.kmers[j])

            # right shift the bit mask across the size of the radix
            bitmask <<= RADIX_BITS

            # rejoin all of the buckets into a single array. We are assuming that the array is
            # implemented as a linked list which would allow O(1) joining.
            # the arrays are appended to each other to maintain stability
            self.kmers = []
            for bucket in buckets:
                self.kmers += bucket

    def write_file(self, output_file):
        """
        Writes the sorted kmers to a file
        :param output_file:
        """
        outfile = open(output_file, 'w')
        for i in self.kmers:
            outfile.write(
                i.kmer_str + "\t" + str(i.kmer_int) + "\t" + str(i.pos) + "\n")
        outfile.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No kmer file given")
        exit()

    # read the input file name
    input_file = sys.argv[1]
    output_file = "kmers_sorted.txt"
    try:
        rlsd = RadixLSD()
        print("Reading in kmer file")
        rlsd.read_file(input_file)
        print("Sorting kmer file using radix LSD sort...")
        rlsd.sort()
        print("Creating sorted kmer file")
        rlsd.write_file(output_file)
        print("kmer file " + output_file + " created!")
    except IOError:
        print("Unable to open input file")
    except (ValueError) as e:
        print(e)
