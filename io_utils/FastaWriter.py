class FastaWriter:
    def __init__(self, address):
        self.address = address

    def save_queries(self, string):
        """
        write a string from to a fasta file
        :param: address of the location of the fasta file and the string from the file
        """
        with open(self.address, 'w') as output_file:
            output_file.write(string)
