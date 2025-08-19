from csv import DictWriter
import dateparser
from httpx import get
from parsel import Selector


def letra(url: str) -> str:
    response = get(url)
    s = Selector(response.text)
    return '\n'.join(s.css('[data-lyrics-container]::text').getall())


def faixas(url: str) -> list[tuple[str, str]]:
    response = get(url)
    s = Selector(response.text)

    musicas = s.css('div.chart_row-content')

    return [
        (musica.css('h3::text').get().strip(), musica.css('a').attrib['href'])
        for musica in musicas
    ]


def discos(url: str) -> list[tuple[str | None, ...]]:
    response = get(url)
    s = Selector(response.text)

    discos = s.css('.ddfKcW')

    resultado = []

    for disco in discos:
        disco_url = disco.css('.jsXEqK').attrib['href']
        disco_nome = disco.css('.gSnatN::text').get()
        disco_ano = disco.css('.ixmAQP::text').get()

        resultado.append((disco_url, disco_nome, disco_ano))

    return resultado

url = 'https://genius.com/artists/Dead-fish/albums'

with open('deadfish.csv', 'w') as f:
    writer = DictWriter(f, ['album', 'data', 'musica', 'letra'])
    writer.writeheader()
    for disco in discos(url):
        for faixa in faixas(disco[0]):
            row = {
                'album': disco[1],
                'data': dateparser.parse(disco[2]),
                'musica': faixa[0],
                'letra': letra(faixa[1])
            }
            writer.writerow(row)
