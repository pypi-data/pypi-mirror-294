import pyodbc
import pandas as pd
#from tests import test_deffined_connection

from scr.config import SERVER,DATABASE,USERNAME,PASSWORD


class GlobalDataPlatformTools():
    """
    This package will support you in accessing, and working with data from the GDP. 
    It's functional requirements are:
    - Accessing data on GDP Base/CIM/Warehouse 
    - Accessing data in temp storage (LAB)
    - Querying that data in SQL
    - utlising that data as a Python/PySpark DataFrame
    - Storing processed data to the temp storage space (LAB)    
    """

    def __init__(self,):

        self.SERVER = SERVER
        self.DATABASE = DATABASE # Location of Synapse
        self.USERNAME = USERNAME # load from config
        self.PASSWORD = PASSWORD # load from config
        self.AUTH = 'ActiveDirectoryInteractive' #aka Azure Active Directory - Universal with MFA # using sbaadminuk and setting this auth method results in a connection timeout

        # deffine connectors
        self.setup_odbc_connection()

    def setup_odbc_connection(self,):
        #https://learn.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver16
        #https://github.com/mkleehammer/pyodbc/wiki/The-pyodbc-Module#connect
        #https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-connect-overview

        # Setup connection using ODBC Driver
        connectionString = f'''
                             DRIVER={{ODBC Driver 18 for SQL Server}};
                             SERVER=tcp:{self.SERVER};
                             DATABASE={self.DATABASE};
                             UID={self.USERNAME};
                             PWD={self.PASSWORD};
                             Encrypt=yes;
                             TrustServerCertificate=no;
                             Connection Timeout=30;
                            '''
        
        #SQL Server Native Client 11.0
        try:
            self.conn = pyodbc.connect(connectionString)
            print("Connected Successfully") 
        except Exception as e:
            print("Connection failed: ", e )

    def query_gdp_to_pd(self,sql_query: str):
        """
        Input: user enters a SQL query as a string
        Output: returns a python dataframe
        """
        
        # test if connection is deffined
        #test_deffined_connection(self.conn)

        return pd.read_sql(sql_query, self.conn)