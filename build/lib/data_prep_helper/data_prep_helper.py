import pandas as pd
from .data import Data
import warnings


class DataPrepHelper:
    """
    type: Allowed values are 'csv', 'web', 'folder_csv'
    link: If type = web, then weblink, if type = csv, then location of csv
    file on local computer, if folder_csv, then folder location on computer
    """

    def __init__(self, data_dict, allowed_cols=None):
        self.data_dict = data_dict
        self.all_data = {}  # Empty Dictionary
        self.set_data_info()
        self.allowed_cols = allowed_cols

    def set_data_info(self):
        for name in self.data_dict.keys():
            if self.data_dict[name]['file_type'] != 'pandas':
                single_data_object = Data(
                        name=name,
                        file_type=self.data_dict[name]['file_type'],
                        link=self.data_dict[name]['link'],
                        fillna=self.data_dict[name]['fillna'])
            else:  # Pandas Data Type
                single_data_object = Data(
                        name=name,
                        file_type=self.data_dict[name]['file_type'],
                        data=self.data_dict[name]['data'],
                        fillna=self.data_dict[name]['fillna'])
            self.all_data.update({name: single_data_object})

    def update_data_info(self, data_dict):
        """
        Updates the data dictionaty and internal data object with a new sources
        """
        self.data_dict.update(data_dict)
        for name in data_dict.keys():
            # single_data_object = Data(name,
            #                          self.data_dict[name]['file_type'],
            #                          self.data_dict[name]['link'],
            #                          self.data_dict[name]['fillna'])
            if self.data_dict[name]['file_type'] != 'pandas':
                single_data_object = Data(
                        name=name,
                        file_type=self.data_dict[name]['file_type'],
                        link=self.data_dict[name]['link'],
                        fillna=self.data_dict[name]['fillna'])
            else:  # Pandas Data Type
                single_data_object = Data(
                        name=name,
                        file_type=self.data_dict[name]['file_type'],
                        data=self.data_dict[name]['data'],
                        fillna=self.data_dict[name]['fillna'])
            self.all_data.update({name: single_data_object})

    def set_allowed_cols(self, allowed_cols):
        self.allowed_cols = allowed_cols

    def get_all_names(self):
        return(self.all_data.keys())

    def get_col_names(self, name):
        """
        name: Name of the dataset to get column names for
        """
        return(self.all_data[name].get_col_names())

    def get_data(self, name):
        """
        name: Name of the dataset to return
        """
        return(self.all_data[name].get_data())

    def overwrite_data(self, name, data):
        """
        name: Name of the dataset to set
        data: data to use to overwrite
        """
        self.all_data[name].overwrite_data(data)

    def head():
        pass  # Need to define

    def map_columns(self, name, mapping):
        self.all_data[name].map_columns(mapping)

    def get_extra_cols(self, name):
        """
        Compares the columns in data 'name' with the allowed columns list
        Returns the columns that are present in the data but not allowed
        as per the allowed columns list
        """
        data_cols = self.get_col_names(name)
        extra = list(set(data_cols).difference(self.allowed_cols))
        extra.sort()
        return(extra)

    def get_missing_cols(self, name):
        """
        Compares the columns in data 'name' with the allowed columns list
        Returns the columns that are missing in the data but should be present
        as per the allowed columns list
        """
        data_cols = self.get_col_names(name)
        missing = list(set(self.allowed_cols).difference(data_cols))
        missing.sort()
        return(missing)

    def check_clenliness(self, name, force=False):
        """
        Check if the columns are in the allowed list
        Check if there are missing columns in the data that are in the
        allowed list
        Check if there extra columns in the data that are not in the
        allowed list
        force: If True, the run will fail if data is not clean
        """
        if (not force):
            print("Additional columns in data:", self.get_extra_cols(name))
            print('-'*50)
            print("Missing columns in data:", self.get_missing_cols(name))

        if (force):
            assert(len(self.get_extra_cols(name)) == 0)
            assert(len(self.get_missing_cols(name)) == 0)
            print("Data has the right columns and none are missing")

    def check_clenliness_all(self):
        pass

    def add_columns(self, name, col_names, col_value=""):
        """
        name: name of data set to add the columns to
        col_names: list of column names to add
        col_values: value to use for each row of these new columns. Note that
        the same value will be assigned to each row. This is useful when we
        want to add a dumy column before merging 2 data sources.
        """
        self.all_data[name].add_columns(names=col_names, value=col_value)

    def drop_columns(self, name, col_names):
        """
        name: name of data set to drop columns from (always inplace)
        col_names: list of column names to drop
        """
        self.all_data[name].drop_columns(names=col_names, inplace=True)

    def filter_delete(self, name, col_name, col_values):
        """
        name: name of data set to drop columns from (always inplace)
        col_name: Column to delete observations from
        col_values: If the value of the col_name in an observation (row) is
        equal to any value in col_values then that observation is deleted from
        the dataset.
        """
        self.all_data[name].filter_delete(col_name, col_values)

    def filter_change(self, name, filter_col, filter_value,
                      change_col, change_value):
        """
        NOTE: This changes the value to a fixed value
        name: name of data set to modify (always inplace)
        filter_col: Column name to filter by
        filter_value: value to filter
        change_col: Column to change values
        change_value: Value to change to in the changeCol column
        """
        self.all_data[name].filter_change(
            filter_col, filter_value,
            change_col, change_value)

    def filter_change_to_col(self, name, filter_col, filter_value,
                             change_col, change_value_colname):
        """
        NOTE: This changes the value to that of another column in the same row
        name: name of data set to modify (always inplace)
        filter_col: Column name to filter by
        filter_value: value to filter
        change_col: Column to change values
        change_value_colname: Column from where to pick new value
        """
        self.all_data[name].filter_change_to_col(
            filter_col, filter_value,
            change_col, change_value_colname)

    def concat_columns(self, name, new_col_name, concat_list, concatBy=" "):
        """
        name: name of data set to use to concate columns
        new_col_name: New Column name after concatenation
        concat_list: List of columns to concatenate
        """
        self.all_data[name].concat_columns(
            new_col_name, concat_list, concatBy)

    def strip_columns(self, name, col_names=None):
        """
        name: name of data set to use to strip columns
        cols_to_strip: List of columns to strip.
        If None, it will strip all columns of object type
        """
        if (col_names is None):
            col_names = self.all_data[name].get_data().select_dtypes(
                include='object').columns
        self.all_data[name].strip_columns(col_names)

    def title_case(self, name, col_names=None):
        """
        name: name of data set to use for conversino to title case
        col_names: List of columns to make title case.
        If None, it will strip all columns of object type
        """
        if (col_names is None):
            col_names = self.all_data[name].get_data().select_dtypes(
                include='object').columns
        self.all_data[name].title_case(col_names)

    def upper_case(self, name, col_names=None):
        """
        name: name of data set to use for conversion to upper case
        col_names: List of columns to make upper case.
        If None, it will strip all columns of object type
        """
        if (col_names is None):
            col_names = self.all_data[name].get_data().select_dtypes(
                include='object').columns
        self.all_data[name].upper_case(col_names)

    def to_datetime(self, name, col_names=None):
        """
        name: name of data set to use for conversion to datetime
        col_names: List of columns to convert to datetime
        """
        if (col_names is None):
            warnings.warn("Column name not specified. No action will be taken")
        else:
            self.all_data[name].to_datetime(col_names)

    def combine_all_data_sources(self, source_col_name='Source'):
        """
        Combined Data is stored as a Data class object with name = 'combined'
        """
        frames = []
        for name in self.all_data.keys():
            if (name != 'combined'):
                frames.append(self.all_data[name].get_data())

        data = pd.concat(frames, sort=True).reset_index(drop=True)
        update_data_dict = {'combined': {'file_type': "pandas",
                                         'data': data,
                                         'fillna': None}}
        self.update_data_info(update_data_dict)

    def get_combined_data(self):
        """
        Returns the combined data
        """
        if 'combined' in self.all_data.keys():
            return(self.get_data('combined'))
        else:
            warnings.warn(
                "Data has not been merged yet. Nothing will be retuened")
