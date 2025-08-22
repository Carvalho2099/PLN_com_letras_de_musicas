import matplotlib.pyplot as plt
from wordcloud import WordCloud
import polars as pl
from collections import Counter
import spacy

nlp = spacy.load('pt_core_news_lg')

df = pl.read_csv('deadfish_stats.csv')
wc = WordCloud(
                width=1280, 
                height=720, 
                background_color='white',
            )

for album in df.sort('data').partition_by('album'):
    palavras = nlp(''.join(album['letra'].drop_nulls()))

    contador = Counter(
        palavra.text for palavra in palavras
        if not palavra.is_punct
        )
    
    
    img = wc.generate_from_frequencies(contador)

    fig, ax = plt.subplots()

    ax.set_title(album['album'][0])
    ax.imshow(img)
    ax.axis('off')
    plt.show()