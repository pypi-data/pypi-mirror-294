from pandas import read_sql

def fetch_data_from_sql(query, connection):
    return read_sql(query, connection)

