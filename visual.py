import polars as pl
import matplotlib.pyplot as plt

df = pl.read_csv('deadfish_stats.csv')

"""
Contagem de faixas por disco
"""

#counter = df.group_by('album').len().sort('len')
#fig, ax = plt.subplots()
#ax.barh(counter['album'], counter['len'])
#plt.show()

"""
Estadísticas gerais por album
"""

#for album in df.sort('data').partition_by('album'):
#    album = album.sort('tokens')

#    mean = album['ttr'].mean()

#    fg, ax = plt.subplots()
    
#    ax.barh(album['musica'], album['tokens'])
#    ax.barh(album['musica'], album['types'])
#    ax.barh(album['musica'], album['ttr'])
#    ax.axvline(mean)

#    ax.set_title(album['album'][0])
#    ax.set_xlabel('Estatísticas de texto')
#    ax.set_ylabel('Nome da música')
#    ax.legend(
#        (
#            'Média de ttr ',
#            'Tokens (N): Quantidade de palavras', 
#            'Types (N): Quantidade de palavras únicas', 
#            'TTR (%): Razão entre Tokens e Types'
#        )
#    )
    
#   plt.show()

"""
Estadísticas gerais por target
"""
boxes = {}
target = 'types'
for album in df.sort('data').partition_by('album'):
    boxes |= {
        album['album'][0]: album[target].drop_nulls()
    }

mean = df[target].mean()

    
fig, ax = plt.subplots()

ax.boxplot(boxes.values())
ax.set_xticklabels(boxes.keys())
ax.axhline(y=mean)
plt.show()