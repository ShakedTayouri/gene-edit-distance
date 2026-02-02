import csv
import os

import pandas as pd


class CsvWriter:
    def __init__(self, address):
        self.address = address

        # Check if the CSV file already exists, and create it if not
        if not os.path.exists(self.address):
            with open(self.address, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Write header row
                writer.writerow(['Query', 'Type', 'Current Date', 'Category', 'Score', 'Advanced Score', 'Running Time',
                                 'Cut Points',
                                 'Merged Queries'])

    def save_results_data(self, query, current_date, running_time, num_of_cut_points, num_of_merged_queries, score,
                          advanced_score):
        with open(self.address, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                [query, 'Restriction Enzyme Obfuscation', current_date, 'GED', score, advanced_score, running_time,
                 num_of_cut_points,
                 num_of_merged_queries])

    def save_classification_from_text(self, text_address):
        # Read the current exel file.
        panda_object = pd.read_excel(self.address)

        # Reset the score column.
        panda_object['Hit? [1=Yes, 0=No]'] = None

        with open(text_address, 'r') as file:
            for line in file:
                line = line.strip()
                if line:  # Skip empty lines
                    query, score = line.split("|")

                    # Add query and score to panda_object
                    self.update_data_frame_by_query(query, score, panda_object)

        # Write the DataFrame to an Excel file
        panda_object.to_excel(self.address, index=False)

    @staticmethod
    def update_data_frame_by_query(query, score, df):
        sequences = df['Sequence']
        matching_rows = df[sequences == query]

        if not matching_rows.empty:
            sequence_index = matching_rows.index[0]
            if float(score) > 100:
                classification = 1
            else:
                classification = 0
            df.loc[sequence_index, 'Hit? [1=Yes, 0=No]'] = classification

        else:
            print("the query " + str(query) + " not found!")
