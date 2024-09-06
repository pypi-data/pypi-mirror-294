
class DataSource:
    '''
    This is to fetch current and reference datasets using snowflake session
    params:
        session: snowflake session,
        dataset_details : dict, contains the details of the dataset names
        dataset_type : pandas dataframe or snowflake dataframe
    output:
        current, reference: pandas or snowflake dataframe depending on the dataset_type
    '''

    def __init__(self, session, dataset_details: dict, dataset_type: str):
        self.session = session
        self.dataset_details = dataset_details
        self.dataset_type = dataset_type


    def load_snowflake_datasets(self):
        sf_current = self.session.table(self.dataset_details['current_dataset']).dropna()
        sf_reference = self.session.table(self.dataset_details['reference_dataset']).dropna()
        return sf_current, sf_reference

    def load_pandas_datasets(self):
        sf_current, sf_reference = self.load_snowflake_datasets()
        current = sf_current.to_pandas()
        reference = sf_reference.to_pandas()
        return current, reference