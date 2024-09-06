from sqlalchemy import create_engine, exc
import pandas as pd
import os.path

class NsysEvent:

    class MissingDatabaseFile(Exception):
        def __init__(self, filename):
            super().__init__(f'Database file {filename} does not exist.')

    class InvalidDatabaseFile(Exception):
        def __init__(self, filename):
            super().__init__(f'Database file {filename} could not be opened and appears to be invalid.')

    class InvalidSQL(Exception):
        def __init__(self, sql):
            super().__init__(f'Bad SQL statement: {sql}')

    query = "SELECT 1 AS 'ONE'"

    def __init__(self, report) -> None:
        self._dbcon = None
        self._dbfile = f"{os.path.splitext(report)[0]}.sqlite"
        self._df = pd.DataFrame()

        if not os.path.exists(self._dbfile):
            raise self.MissingDatabaseFile(self._dbfile)

        try:
            self._dbcon = create_engine(f"sqlite:///{self._dbfile}")
        except exc.SQLAlchemyError:
            self._dbcon = None
            raise self.InvalidDatabaseFile(self._dbfile)

    def Setup(self):
        pass

    def preprocess(self):
        pass

    def postprocess(self):
        pass

    def load_data(self):
        try:
            pd.read_sql_query(self.query, self._dbcon)
        except pd.errors.DatabaseError:
            self.InvalidSQL(self.query)

    def apply_process_model(self, threads=pd.DataFrame, streams=pd.DataFrame):
        self.df["thread"] = self.df["Tid"].map(threads.set_index('Tid')["thread"])
        self.df["task"] = self.df["Tid"].map(threads.set_index('Tid')["task"])
        if 'Rank' in threads.columns:
            self.df["Rank"] = self.df["Tid"].map(threads.set_index('Tid')["Rank"])
        pass

    def get_threads(self):
        return self._df[['Pid', 'Tid']].drop_duplicates()