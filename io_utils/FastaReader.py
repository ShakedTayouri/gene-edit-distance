from Bio.SeqIO import parse


class FastaReader:
    def __init__(self, address):
        self.address = address

    def load_queries(self) -> list:
        """
        read a string from a fasta file
        :param: address of the location of the fasta file
        :return: the string from the file
        """
        with open(self.address, 'r') as input_file:
            return list(map(lambda record: (record.seq, record.description), parse(input_file, "fasta")))
