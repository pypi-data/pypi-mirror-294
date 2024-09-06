# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv


import pandas as pd
from sklearn.model_selection import train_test_split

# Data processing functions
def load_data(source_filepath):
    logger = logging.getLogger(__name__)
    logger.info(f"Loading data from {source_filepath}...")
    df = pd.read_csv(source_filepath)
    return df

def save_data(df, destination_filepath):
    logger = logging.getLogger(__name__)
    logger.info(f"Saving data to {destination_filepath}...")
    df.to_csv(destination_filepath, index=False)

def basic_cleaning(df):
    logger = logging.getLogger(__name__)
    logger.info("Performing basic cleaning...")
    df = df.drop(columns=['unnecessary_column'], errors='ignore')
    return df

def split_data(df, train_size=0.8):
    logger = logging.getLogger(__name__)
    logger.info(f"Splitting data into training ({train_size*100}%) and test ({(1-train_size)*100}%) sets...")
    train_df, test_df = train_test_split(df, train_size=train_size, random_state=42)
    return train_df, test_df

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('Making final data set from raw data')

    # Load and clean the data
    df = load_data(input_filepath)
    df = basic_cleaning(df)
    
    # Split the data into train and test sets
    train_df, test_df = split_data(df)
    
    # Save the cleaned and split data
    train_output_path = Path(output_filepath) / 'train.csv'
    test_output_path = Path(output_filepath) / 'test.csv'
    save_data(train_df, train_output_path)
    save_data(test_df, test_output_path)

    logger.info('Dataset creation completed.')

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    project_dir = Path(__file__).resolve().parents[2]

    load_dotenv(find_dotenv())

    main()