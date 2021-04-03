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

text = u""" promin, ale já jsem fakt měla pocit, že jsi to pochopil už v ten večer, když jsi mi volal. víš, že jsem ti dostatečně vysvětlila, jak jsem se celý ty týdny psaní diplomky těšila na to, až ji dopíšu a budu ze sebe mít dobrej pocit, že jsem to zvládla a že jsi mi ho totálně, totálně zkazil, že jsem místo radosti po odevzdání diplomky brečela, ne kvůli tomu, že je to špatný, ale že jsi mi to pokazil, že jsem po tolika týdnech měla příležitost cítit se dobře a ty jsi mi ji vzal a já vlastně vůbec nevím proč? jako že to byla snaha o vtip? nebo já fakt nevím. bylo to hrozný, bylo to v návaznosti na to, že jsem se musela vyrovnat s pro mě dost neskutečnou situací, že se na mě vysral jakub, člověk mi nejbližší, s věcí, kterou mi slíbil a já jsem neměla důvod o tom pochybovat a pak se na to vysral bez omluvy a nějakýho studu a nepřemýšlel nad tím, že je to blbě, ok, já jsem poslední hodiny psaní diplomky trávila s pocitem, že to musím zvládnout dokončit, nedělat místo toho scénu na téma, jak ses na mě mohl takhle vykašlat, opakovala jsem si, že mám na hlavě vlastní máslo a že to zvládnu, i když tu slíbenou věc udělá, musela jsem se přes tohle přenést a psát a dokončit to. A já jsem tu práci dokončila a fakt jsem na sebe byla moc pyšná. a ty to asi nevidíš, víš, ale prostě ta práce není tak špatná, těm hodnotitelům se líbila a v porovnání s mými spolužáky prostě fakt není špatná. nevím, prostě mi přišlo, že mám právo na to mít z toho radost a že jsem ti dala dost jasně najevo, jak mi tvoje reakce na tu práci ublížila a že už nechci, abys to dělal. takže mě ted fakt dost sejmula ta tvoje naprosto bezpředmětná a nesouvislá poznámka v reakci na to, že děda je účetní. jako fakt wtf, to bylo potřeba? přišlo mi, že tím, že píšu, že na to nechci myslet ti dávám celkem příležitost, že tu poznámku přejdeme. no a ta ironická, hloupá a nesouvislá poznámka, že jsi zapomněl, že na chyby se zapomíná a nepoučuje se z nich... wow. jestli ti přijde, že jsme si z toho psaní diplomky nic nevzala, tak ok, asi ještě jednou zmíním, že si jsem vědomá toho, že je tam spousta chyb, že jsme to věděla už při odevzdání, že mě to nemírně mrzí, že jsem to prostě začala dělat pozdě a nebyl na to čas. myslela jsem, že tomu třeba napovědělo i to, že jsem ti už v tom telefonu říkala, že mám vybrané téma diplomky a chci ho napsat vedoucí, kterou jsem si vybrala. nevím, no, přijde mi to jako celkem dost zodpovědný a hodně pochybuju o tom, že tohle dělají lidi v prvním semestru studia. takže napsat mi zrovna k tématu diplomka, že jsem se nepoučila. no, zkrátka je to bolestivé. jako klidně mi nadávej za to, že jsem debilní ve vztahových záležitostech, že tam jsem se z ničeho nepoučila, ale zrovna u té diplomky je to od tebe fakt drsný a myslím, že si to nezasloužím. toš tak """.lower()

stopwords = {'z', 'o', 'a', 'v', 's', 'že', 'do', 'se', 'na', 've', 'nananana', 'ze'}

# with open("C:/Users/Lamanchy/Downloads/stopwords-cs.txt", "r", encoding='utf8') as f:
#     stopwords = set([i.strip() for i in f.readlines()])

wordcloud = WordCloud(
    stopwords=stopwords,
    max_words=100000,
    min_font_size=10,
    relative_scaling=0.1,
    min_word_length=2,
    normalize_plurals=False,
    repeat=True,
    width=1080,
    height=1080,
    collocations=False,
    include_numbers=True,
    # colormap="Pastel2",
    font_path="C:/Users/Lamanchy/PycharmProjects/songbook/pil_quality_pdf/fonts/DejaVuSansMono.ttf",
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
