#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filename: read_data.py
Description: Used to read and preprocess sample data from S3 data directory.
Author: Wei Zhang
Date: 7-7-2025

input: DataReader(file_path)
output: DataReader.path DataReader.data

Notice: the default path is in the Amazon S3

defaul path: s3://pr-home-datascience/Projects/AdHoc/InternProjects/2025/2025_Summer_AI_Property_Attributes/property_list_NJ_sample.csv
 

"""
import os
import pandas as pd
import boto3


class DataReader:
    """Class for reading and handling CSV data."""

    def __init__(self, path):
        """
        Initialize the DataReader with a file path.

        Args:
            path (str): Path to the CSV file.
        """
        self.path = path
        self.data = None # Will read the data using the private function _read()
        self._read()
        self._modify_zip5()

    def _read(self):
        """Reads the CSV file into a DataFrame."""

        try:
            self.data = pd.read_csv(self.path, sep=',', dtype=str, low_memory=False)
        except Exception as e:
            raise RuntimeError(f" Failed to read file: {e}")
    
    def _modify_zip5(self):
        """modify the variable zip5 to make it 5 digit zip code
            Must be called after self._read()
            return the same data structure with 5 digit zip code of zip5"""
        temp = '0' + self.data['zip5']
        self.data['zip5'] = temp

    def preview(self, n=5):
        """Print the first `n` rows of the data."""
        print(self.data.head(n))


# ---------------------------- Example Usage ---------------------------- #

if __name__ == "__main__":
    reader = DataReader("s3://pr-home-datascience/Projects/AdHoc/InternProjects/2025/2025_Summer_AI_Property_Attributes/property_list_NJ_sample.csv")
    print(reader.path)
    print(reader.preview())
    #temp = pd.read_csv(reader.path, sep = '\t', low_memory=False)
    #print(temp.head())



