# IMPORTS
from sqlalchemy import create_engine, Engine
import pandas as pd

class Org:
    # Constructor
    def __init__(self, user, password, host="127.0.0.1", port=5432, db="galigeo"):
        # Infos
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._db = db
        # Engine
        self._is_valid = False
        self._engine = self._get_engine()
        self._is_valid = self._check_validity()
    
    # Getters and setters
    @property
    def engine(self): return self._engine
    @property
    def is_valid(self): return self._is_valid

    # Private Methods
    def _get_engine(self) -> Engine:
        return create_engine(f'postgresql://{self._user}:{self._password}@{self._host}:{self._port}/{self._db}')

    def _check_validity(self)->bool:
        # Check connection
        try:
            self._engine.connect()
            return True
        except Exception as e:
            return False
    
    # Public Methods
    def getNetworksList(self)->pd.DataFrame:
        # Query
        query = "SELECT * FROM ggo_network"
        # Get data from query
        df = pd.read_sql(query, self._engine)
        # return df
        return df

