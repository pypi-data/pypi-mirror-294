from nsys_event import NsysEvent
import os.path
from mpi_event_encoding import *

class MPIP2PSemantic(NsysEvent):
    def __init__(self, report) -> None:
        super().__init__(report)
    
    def Setup(self):
        with open(os.path.join(os.path.dirname(__file__), '../scripts/mpi_p2p.sql'), 'r') as query:
            self.query = query

class MPICollSemantic(NsysEvent):
    def __init__(self, report) -> None:
        super().__init__(report)
    
    def Setup(self):
        with open(os.path.join(os.path.dirname(__file__), '../scripts/mpi_coll.sql'), 'r') as query:
            self.query = query
    
    def preprocess(self):
        self._df = self._df.drop(self._df[self._df["Event"].str.contains("File") ].index)

class MPIOtherSemantic(NsysEvent):
    def __init__(self, report) -> None:
        super().__init__(report)
    
    def Setup(self):
        with open(os.path.join(os.path.dirname(__file__), '../scripts/mpi_other.sql'), 'r') as query:
            self.query = query
    
    def preprocess(self):
        self._df = self._df.drop(self._df[self._df["Event"].str.contains("File") ].index)
        self._df = self._df.drop(self._df[self._df["Event"].str.contains("Win|MPI_Get|MPI_Put|Accumulate") ].index)

class MPIRMASemantic(NsysEvent):
    def __init__(self, report) -> None:
        super().__init__(report)
    
    def Setup(self):
        with open(os.path.join(os.path.dirname(__file__), '../scripts/mpi_other.sql'), 'r') as query:
            self.query = query
    
    def preprocess(self):
        self._df = self._df[self._df["Event"].str.contains("Win|MPI_Get|MPI_Put|Accumulate")]

class MPIIOPSemantic(NsysEvent):
    def __init__(self, report) -> None:
        super().__init__(report)
    
    def Setup(self):
        with open(os.path.join(os.path.dirname(__file__), '../scripts/mpi_io.sql'), 'r') as query:
            self.query = query
    
    def preprocess(self):
        self._df = self._df[self._df["Event"].str.contains("File")]