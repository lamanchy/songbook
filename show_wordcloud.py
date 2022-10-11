import os
import sys

from PIL import Image
from wordcloud import WordCloud

from scripts.chord import Chord

path = sys.argv[1]

with open(path, "r", encoding="utf8") as f:
    raw = f.read()

text = []
for word in raw.split():
    word = word.strip()
    if Chord.is_chord(word):
        continue
    if word.startswith('['):
        continue
    text.append(word)

for i in range(10):
    text.append(os.path.splitext(os.path.basename(path))[0])

text = ' '.join(text).lower()

text = u"""Mezi nebem a zemí, přibližně v půli cesty,
mezi magickou krajinou a dusivými městy;
Odhalí se v pravou chvíli
samého vědomí hranice.
A dá se po ní tiše přejít,
skrz bílou linku ve světle měsíce
radno je dobrých mravů dbáti, neboť stává se nejednou, 
že si vlídné Přízraky na kus řeči přisednou.
Slušností je přivítat a nabídnout cigaretu, 
při tom vzácném prolnutí
jindy uzavřených světů.
Do stromových domků vstoupit smí se 
i bez pozvání, 
třeba je ale rozloučit se hbitě,
jakmile ozve se za zády klepání.
Někdy v brzkém odpoledni k procházce přizve lesní pěšina, 
běda však těm, kdo zapomenou, kde končí a kde začíná.
Stává se totiž nepozorným dobrodruhům,  
že zabloudí v mlze k vílám, 
vyhne se ale hříbky lemovaným kruhům, ten, komu je duše jeho milá;
Bytosti tajemného hvozdu omamnou melodii pějí, 
místy znepokojivou, jako chvění prasklé struny

V prazvláštním tichu okolí ty tóny dlouze znějí,
tu nad hlavou, tu zas pod nohama zjevují se runy.
Na kopci v místě čtyř živlů smíření
se ve stínu kříže poodhalí Znamení,
zjeví se kudlanka, můra či netopýr,
zapsal jsem jejich poselství na papír;
A jako důkaz na místě činu 
zanechám předmět doličný,
obálku pod listím břečťanu 
kdesi v Šentvidu pri Stični""".lower()

stopwords = {'z', 'o', 'a', 'v', 's', 'že', 'do', 'se', 'na', 've', 'nananana', 'ze'}

# with open("C:/Users/Lamanchy/Downloads/stopwords-cs.txt", "r", encoding='utf8') as f:
#     stopwords = set([i.strip() for i in f.readlines()])

wordcloud = WordCloud(
    stopwords=stopwords,
    max_words=10000000,
    min_font_size=10,
    relative_scaling=0.1,
    min_word_length=2,
    normalize_plurals=False,
    repeat=True,
    width=int(105/25.4*300),
    height=int(148/25.4*300),
    collocations=True,
    include_numbers=True,
    # colormap="Pastel2",
    font_path="C:/Users/Lamanchy/PycharmProjects/songbook/pil_quality_pdf/fonts/calibri.ttf",
).generate(text)

wordcloud.to_file("test.png")
img = Image.open('test.png')
img.show()

# import matplotlib as mpl
# import matplotlib.pyplot as plt
#
# def plot_colorMaps(cmap):
#
#     fig, ax = plt.subplots(figsize=(4,0.4))
#     col_map = plt.get_cmap(cmap)
#     mpl.colorbar.ColorbarBase(ax, cmap=col_map, orientation = 'horizontal')
#
#     plt.show()
#
#
# for cmap_id in plt.colormaps():
#     print(cmap_id)
#     plot_colorMaps(cmap_id)

# Pastel1 Pastel2 Wistia
