import pandas
from nlpandas.__keywords__ import key_words
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Span, Token
from spacy.strings import StringStore
class NPROCESSOR:
    def __init__(self , df):
        self.__df = df
        self.fields = [col for col in dict(df.dtypes)]
        self.avg_keys = [key for key in key_words['aggregation']['avarage']['keywords']]
        self.sum_keys = [key for key in key_words['aggregation']['sum']['keywords']]
        self.min_keys = [key for key in key_words['aggregation']['min']['keywords']]
        self.max_keys = [key for key in key_words['aggregation']['max']['keywords']]
       
        self.nlp = English()
      
        component_field = field_pipe(self.nlp , self.fields , "COL" , "is_field" , "has_field" , "has_field")  # initialise component
        component_avg = avg_pipe(self.nlp , self.avg_keys , "AVG" , "is_avarage" , "has_avarage" , "has_avarage")  # initialise component
        component_sum = sum_pipe(self.nlp, self.sum_keys , "SUM" , "is_sum" , "has_sum" , "has_sum")  # initialise component
        component_min = min_pipe(self.nlp, self.min_keys , "MIN" , "is_min" , "has_min" , "has_min")  # initialise component
        component_max = max_pipe(self.nlp, self.max_keys , "MAX" , "is_max" , "has_max" , "has_max")  # initialise component
        self.nlp.add_pipe(component_field, last=True)  # add last to the pipeline
        self.nlp.add_pipe(component_avg, last=True)  # add last to the pipeline
        self.nlp.add_pipe(component_sum, last=True)  # add last to the pipeline
        self.nlp.add_pipe(component_min, last=True)  # add last to the pipeline
        self.nlp.add_pipe(component_max, last=True)  # add last to the pipeline

    def nquery(self , statment=None):
        if statment == None:
            return _df
        self.__querydoc__ = self.nlp(statment)
        processed_chunks = []
        for token in self.__querydoc__:
            exec('print(token.text ,token._.is_keyword)')   
            # print(token.text , token._.is_field , token._.is_avarage, token._.is_sum, token._.is_min, token._.is_max)
            # print(token.text , token._.is_field , token._.is_avarage, token._.is_sum, token._.is_min, token._.is_max)
    


class key_word_recognizer(object):
    """Initialise the pipeline component. The shared nlp instance is used
    to initialise the matcher with the shared vocab, get the label ID and
    generate Doc objects as phrase match patterns.
    """
    def __init__(self , nlp , keywords , label , tokentag , doctag=None , spantag=None):
        nlp.vocab.strings.add(label)
        self.label = nlp.vocab.strings[label]
        self._token_tag = tokentag
        self._doctag = doctag
        self._spantag = spantag
        # Set up the PhraseMatcher – it can now take Doc objects as patterns,
        # so even if the list of companies is long, it's very efficient
        patterns = [nlp(key) for key in keywords]
        self.matcher = PhraseMatcher(nlp.vocab)
        self.matcher.add(self._token_tag, None, *patterns)

        # Register attribute on the Token. We'll be overwriting this based on
        # the matches, so we're only setting a default value, not a getter.
        Token.set_extension(self._token_tag, default=False)
        if not Token.has_extension("is_keyword"):
            Token.set_extension("is_keyword", default=False)
        # Register attributes on Doc and Span via a getter that checks if one of
        # the contained tokens is set to is_tech_org == True.
        Doc.set_extension(self._doctag, getter=lambda tokens: any([t._.get( self._token_tag) for t in tokens]))
        Span.set_extension(self._spantag, getter=lambda tokens: any([t._.get( self._token_tag) for t in tokens]))
    
    def __call__(self, doc):
        """Apply the pipeline component on a Doc object and modify it if matches
        are found. Return the Doc, so it can be processed by the next component
        in the pipeline, if available.
        """
        matches = self.matcher(doc)
        spans = []  # keep the spans for later so we can merge them afterwards
        for _, start, end in matches:
            # Generate Span representing the entity & set label
            entity = Span(doc, start, end, label=self.label)
            spans.append(entity)
            # Set custom attribute on each token of the entity
            for token in entity:
                token._.set( self._token_tag, True)
                if not token._.get("is_keyword"):
                    token._.set("is_keyword" , True)
            # Overwrite doc.ents and add entity – be careful not to replace!
            doc.ents = list(doc.ents) + [entity]
        for span in spans:
            # Iterate over all spans and merge them into one token. This is done
            # after setting the entities – otherwise, it would cause mismatched
            # indices!
            span.merge()
        return doc

class avg_pipe(key_word_recognizer):
    pass
class field_pipe(key_word_recognizer):
    pass
class sum_pipe(key_word_recognizer):
    pass
class min_pipe(key_word_recognizer):
    pass
class max_pipe(key_word_recognizer):
    pass
