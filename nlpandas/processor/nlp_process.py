import pandas
import spacy
from nlpandas.__keywords__ import key_words
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Span, Token
from spacy.strings import StringStore
class NPROCESSOR:
    def __init__(self , df):
        self.df = df
        self.fields = [col for col in dict(df.dtypes)]
        self.avg_keys = [key for key in key_words['aggregation']['avarage']['keywords']]
        self.count_keys = [key for key in key_words['aggregation']['count']['keywords']]
        self.sum_keys = [key for key in key_words['aggregation']['sum']['keywords']]
        self.min_keys = [key for key in key_words['aggregation']['min']['keywords']]
        self.max_keys = [key for key in key_words['aggregation']['max']['keywords']]
       
        self.nlp = spacy.load("en_core_web_sm")
      
        component_field = field_pipe(self.nlp , self.fields , "COL" , "is_field" , "has_field" , "has_field")  # initialise component
        component_avg = avg_pipe(self.nlp , self.avg_keys , "AVG" , "is_avarage" , "has_avarage" , "has_avarage")  # initialise component
        component_sum = sum_pipe(self.nlp, self.sum_keys , "SUM" , "is_sum" , "has_sum" , "has_sum")  # initialise component
        component_min = min_pipe(self.nlp, self.min_keys , "MIN" , "is_min" , "has_min" , "has_min")  # initialise component
        component_max = max_pipe(self.nlp, self.max_keys , "MAX" , "is_max" , "has_max" , "has_max")  # initialise component
        component_count = count_pipe(self.nlp, self.count_keys , "COUNT" , "is_count" , "has_count" , "has_count")  # initialise component
        removeEnts = RemoveEnts()
        self.nlp.add_pipe(removeEnts , last=True)
        self.nlp.add_pipe(component_field, last=True)  # add last to the pipeline
        self.nlp.add_pipe(component_avg, last=True)  # add last to the pipeline
        self.nlp.add_pipe(component_sum, last=True)  # add last to the pipeline
        self.nlp.add_pipe(component_min, last=True)  # add last to the pipeline
        self.nlp.add_pipe(component_max, last=True)  # add last to the pipeline
        self.nlp.add_pipe(component_count, last=True)  # add last to the pipeline

    
    def nquery(self , statment=None):
        if statment == None:
            return _df
        self.__querydoc__ = self.nlp(statment)
        processed_chunks = []
        #print(list(self.__querydoc__.ents))
        #print(self.__querydoc__.to_json())
         
        for t in self.__querydoc__:
            if t._.is_keyword:
                c = chunk(t)
                processed_chunks.append(c)
                print(c.__str__())
        
        return self.get_dep(processed_chunks)
        
    def get_dep(self, processed_chunk):
        result_str = 'self.df'
        for c in processed_chunk:
            if c.ent._.is_field and c.headlabel != None:
                if c.headlabel == "SUM":
                    print(self.df)
                    return self.df[c.text].sum()
            
class chunk(object):
    def __init__(self , ent):
        self.text = ent.text
        self.label = ent._.label_
        self.dep = ent.dep_
        self.head = ent.head.text
        self.ent = ent
        self.headlabel = ent.head._.label_
    
    def __str__(self):
        return '{{ "text" : {self.text} , "label" : {self.label} ,"dep" : {self.dep} ,"head" : {self.head} ,"headlabel" : {self.headlabel} }}'.format(self=self)
    


class key_word_recognizer(object):
    """Initialise the pipeline component. The shared nlp instance is used
    to initialise the matcher with the shared vocab, get the label ID and
    generate Doc objects as phrase match patterns.
    """
    def __init__(self , nlp , keywords , label , tokentag , doctag=None , spantag=None):
        nlp.vocab.strings.add(label)
        self.label = nlp.vocab.strings[label]
        self._label_str = label
        self._token_tag = tokentag
        self._doctag = doctag
        self._spantag = spantag
        self._keywordtag = "is_keyword"
        self._labeltag = "label_"
        # Set up the PhraseMatcher – it can now take Doc objects as patterns,
        # so even if the list of companies is long, it's very efficient
        patterns = [nlp(key) for key in keywords]
        self.matcher = PhraseMatcher(nlp.vocab)
        self.matcher.add(self._token_tag, None, *patterns)

        # Register attribute on the Token. We'll be overwriting this based on
        # the matches, so we're only setting a default value, not a getter.
        Token.set_extension(self._token_tag, default=False)
        if not Token.has_extension(self._keywordtag):
            Token.set_extension(self._keywordtag, default=False)
            Token.set_extension(self._labeltag, default=None)
        # Register attributes on Doc and Span via a getter that checks if one of
        # the contained tokens is set to is_tech_org == True.
        Doc.set_extension(self._doctag, getter=lambda tokens: any([t._.get( self._token_tag) for t in tokens]))
        Span.set_extension(self._spantag, getter=lambda tokens: any([t._.get( self._token_tag) for t in tokens]))
        if not Span.has_extension("dep_"):
            Span.set_extension("dep_" , default="")
            Span.set_extension("head_" , default=None)
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
                token._.set( self._labeltag, self._label_str)
                entity._.set("dep_" , token.dep_)
                entity._.set("head_" , {"text" : token.head.text , "index" : token.head.i})
                
                if not token._.get(self._keywordtag):
                    token._.set(self._keywordtag , True)
            # Overwrite doc.ents and add entity – be careful not to replace!
            # print(doc.ents)
            # print(entity)
            if not entity in list(doc.ents):
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
class count_pipe(key_word_recognizer):
    pass

class RemoveEnts(object):
    def __init__(self):
        pass
    def __call__(self , doc):
        doc.ents = []
        return doc
