import spacy
import polars as pl

nlp = spacy.load('pt_core_news_lg')

def tokens(text: str) -> int:
    """Quantidade de tokens em um texto"""
    doc = nlp(text)
    return len([t.text for t in doc if not t.is_punct])

def types(text: str) -> int:
    """Quantidade de types em um texto"""
    doc = nlp(text)
    return len(set([t.text for t in doc if not t.is_punct]))

def ttr(cols) -> float:
    """type-token ratio"""
    types = cols.get('types')
    tokens = cols.get('tokens')
    if types is None or tokens is None or tokens == 0:
        return 0.0
    return (types / tokens) * 100

def lemmas(text: str) -> int:
    """Quantidade de lemmas em um texto"""
    doc = nlp(text)
    return len(set([t.lemma_ for t in doc if not t.is_punct]))
    
    

df = pl.read_csv('deadfish_cleaned.csv')

new_df = df.with_columns(
    pl.col('letra')
    .map_elements(tokens, return_dtype=int)
    .alias('tokens'),
    pl.col('letra')
    .map_elements(types, return_dtype=int)
    .alias('types'),
    pl.col('letra')
    .map_elements(lemmas, return_dtype=int)
    .alias('lemmas'),
).with_columns(
    (
        pl.struct(
        ['types', 'tokens']
        ).map_elements(ttr, return_dtype=float)
        .alias('ttr')
    ),
    (
        pl.struct(
        ['lemmas', 'tokens']
        ).map_elements(lambda cols: (
            0.0
            if cols['lemmas'] is None or cols['tokens'] is None or cols['tokens'] == 0
            else (cols['lemmas'] / cols['tokens']) * 100
        ), return_dtype=float)
        .alias('ltor')
    ),
)

new_df.write_csv('deadfish_stats.csv')