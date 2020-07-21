import pandas #import pandas library
from nlpandas.processor.nlp_process import NPROCESSOR #
class NLDataFrame:
    def __init__(self , df):
        self._df = df
        self._nlp = NPROCESSOR(self._df )
    
    def nlq(self , statement=None):
        return self._nlp.nquery(statement)