import glob
import pandas as pd

from more import pandas_helper


class Data:
    """
    type: Allowed values are 'csv', 'web', 'folder_csv', 'pandas'
    link: If type = web, then weblink, if type = csv, then location of csv
    file on local computer, if folder_csv, then folder location on computer
    data: Pandas Dataframe (applicable only if type = 'pandas')
    """

    def __init__(self, name, file_type, link=None, data=None, fillna=None):
        self.name = name
        self.type = file_type
        self.link = link
        self.fillna = fillna
        self._validate()
        self.set_data(data)

    def _validate(self):
        if (self.type != 'csv' and
            self.type != 'xls' and
            self.type != 'web' and
            self.type != 'folder_csv' and
                self.type != 'pandas'):
            # Check if initialized correctly
            raise TypeError(
                "Type must be one of 'csv', 'web' or 'folder_csv. "
                "You provided " + self.type)

    def get_name(self):
        return(self.name)

    def get_col_names(self):
        return(self.data.columns)

    def set_data(self, data=None):
        if self.type == 'csv':
            self.data = pd.read_csv(self.link)
        elif (self.type == 'xls'):
            self.data = pd.read_excel(self.link)
        elif self.type == 'web':
            pass
        elif self.type == 'folder_csv':
            filenames = glob.glob(self.link + "/*.csv")
            dfs = []
            for filename in filenames:
                dfs.append(pd.read_csv(filename))
            # Concatenate all data into one DataFrame
            self.data = pd.concat(dfs, ignore_index=True)
        elif self.type == 'pandas':
            self.data = data

        # Fill NA values
        if self.fillna is not None:
            self.data = self.data.fillna(value=self.fillna)

    def get_data(self):
        return(self.data)

    def overwrite_data(self, data):
        self.data = data

    def map_columns(self, mapping):
        self.data.helper.map_columns(mapping)

    def add_columns(self, names, value=""):
        self.data.helper.add_columns(names, value)

    def drop_columns(self, names, inplace=True):
        # self.data.drop([name],axis=1,inplace=True)
        self.data.helper.drop_columns(names, inplace=inplace)

    def filter_delete(self, col_name, col_values):
        """
        col_name: Column to delete observations from
        col_value: If the value of the delColumn in an observation
        (row) is equal to this value then that observation is deleted
        from the dataset.
        """
        self.data = self.data.helper.filter_delete(col_name, col_values)

    def filter_change(self, filter_col, filter_value,
                      change_col, change_value):
        """
        filter_col: Column name to filter by
        filter_value: value to filter
        change_col: Column to change values
        change_value: Value to change to in the changeCol column
        """
        self.data = self.data.helper.filter_change(
            filter_col, filter_value,
            change_col, change_value)

    def filter_change_to_col(self, filter_col, filter_value,
                             change_col, change_value_colname):
        """
        filter_col: Column name to filter by
        filter_value: value to filter
        change_col: Column to change values
        change_value_colname: Column from where to pick new value
        """
        self.data = self.data.helper.filter_change_to_col(
            filter_col, filter_value,
            change_col, change_value_colname)

    def concat_columns(self, new_col_name,
                       concat_list, concat_by=" "):
        self.data = self.data.helper.concat_columns(
            new_col_name, concat_list, concat_by)

    def strip_columns(self, names):
        """
        names: column names to strip of leading and trailing whitespaces
        """
        self.data = self.data.helper.strip_columns(names)

    def title_case(self, names):
        """
        names: column names to convert to title case
        """
        self.data = self.data.helper.title_case(names)

    def upper_case(self, names):
        """
        names: column names to convert to upper case
        """
        self.data = self.data.helper.upper_case(names)

    def to_datetime(self, names):
        """
        names: column names to convert to datetime
        """
        self.data = self.data.helper.to_datetime(names)
