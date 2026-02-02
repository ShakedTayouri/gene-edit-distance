import configparser
import os
import tempfile

from Bio import SearchIO
from Bio.Blast.Applications import NcbiblastnCommandline
from io_utils.FastaWriter import FastaWriter

BLAST_XML_FORMAT = 5


class BlastRunner:
    def __init__(self, config_path: str):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        # Temp files
        query_tmp = tempfile.NamedTemporaryFile(
            prefix="temp_query_",
            suffix=".fasta",
            delete=False
        )
        result_tmp = tempfile.NamedTemporaryFile(
            prefix="temp_result_",
            suffix=".xml",
            delete=False
        )

        # Close immediately — BLAST will open them itself
        query_tmp.close()
        result_tmp.close()

        self.temp_query_path = query_tmp.name
        self.temp_result_path = result_tmp.name

        self.blastn = NcbiblastnCommandline(
            query=self.temp_query_path,
            out=self.temp_result_path,
            outfmt=BLAST_XML_FORMAT,
            db=self.config['blast_parameters']['db'],
            cmd=self.config['blast_paths']['blastn_path'],
            evalue=self.config['blast_parameters']['evalue'],
            task='blastn-short'
        )

    def run_blast(self, query):
        """
        Run BLAST for a given query.
        :param query: list of sequences
        :return: SearchIO blast record
        """
        FastaWriter(self.temp_query_path).save_queries(query)
        self.blastn()

        with open(self.temp_result_path) as result_file:
            return SearchIO.read(result_file, "blast-xml")

    def cleanup(self):
        if os.path.exists(self.temp_query_path):
            os.remove(self.temp_query_path)
        if os.path.exists(self.temp_result_path):
            os.remove(self.temp_result_path)

    def __del__(self):
        self.cleanup()
