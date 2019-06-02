# Ondřej Lomič's songbook

Songs to add: 
```
Moravská - Tomas Kočko
bodláky ve vlasech
kde domov můj
bláznivá markéta
pl9hal kdz6 prsi
holubi dum in 5/6 taktu
show must go on
jan hodný
nezmaři růže
Red Hot Chili Peppers - Can't Stop
Frank Sinatra Fly Me To The Moon
Joan Jett & the Blackhearts - I Love Rock N Roll
The Lumineers - Classy Girls
The Lumineers - Flowers In Your Hair
Bad Romance - Vintage 1920's Gatsby 
```

Ok, I suppose, that my family will read it, so: Czech.

Ahojte rodino, známí. Tohle je zárodek nového zpěvníku, který bude mít
tu výhodu, že bude centralizovaný, zálohovaný a verzovaný.

## Základ

Hele, funguje to takhle: ve složce výše jsou songy, v jednoduchém formátu
.txt. Relativně čitelný i tak, ALE ještě je k tomu pár skriptů v pythonu,
které všechny songy přegenerují do PDF na tisk. Parametry půjde měnit,
tatínek může chtít větší písmo oproti ségře, která ocení kompaktnější verzi.

Vše ale bude vždy vygenerováno ze stejného (doufám kvalitního :D) základu
výše. Git navíc poskytuje spoustu nástrojů, jak sledovat změny a třeba i
spojovat změny, pokud více lidí pracuje na zpěvníku zároveň.

## Chci pomoci!

Máš v zásadě tři možnosti:

1. Jsem lenoch, tak Ondrovi pošlu jen název písničky, on to tam nějak přidá.

2. Chci jednorázově pomoci, takže když najdu nějakou super písničku, upravím
ji do formátu, co najdu popsaný níže (nebo vyčtu z jiných songů) a pošli ji
Ondrovi. On ji tam jen nakopíruje a zkotroluje, super!

3. Chci dlouhodobě přidávat písničky, takže ti Ondra někdy na návštěvě
nainstaluje GIT, tím pádem budeš mít všechny songy u sebe na počítači,
budeš je moci upravovat (a opravovat a přidávat) dle libosti, a jednou
za čas s Ondrou uděláš commit, fetch, merge a push, aby si tvé změny mohli
užívat všichni ostatní. Děkujeme

## Formát songů

### Název souboru
Název souboru musí vypadat takto:

`<Název songu> - <Název autora>.txt`

S tím, že jak název songu, tak název autora musí být uvedeny, nesmí mít
na začátku či konci mezeru a první znak musí být velký. Separátor ` - ` 
musí být v názvu souboru pouze jeden. Ani název ani autor nesmí 
obsahovat dvě mezery vedle sebe.

Správně je tedy: `Hurt - Johnny Cash.txt`

Či: `If I ever leave this world alive - P.S. I love you.txt`

Či: `E8ds d sad51de qqwe55 - AdwdD-5dš2.das-d8šš.txt`

Špatně je:

```
hurt - Johnny Cash.txt
Hurt - johnny Cash.txt
Hurt  - Johnny Cash.txt
Hurt - Johnny Cash .txt
Hurt-Johnny Cash.txt
Hurt - Johnny - Cash.txt
Hurt - Johnny  Cash.txt
```

Btw, nebojte, nekontroluji to já, ale script v pythonu.

### Struktura songu

Tady už skript jen nekontroluje, ale i opravuje. Mohl by to dělat i výše,
u názvů souborů, ale (příšerný řev o tom, že windows je case insensitive
a kurva namrdat na lidi, co to vymýšleli), EHM, no nechce se mi to řešit.

Tedy ačkoli lecco schroustá, hlavně si pořádně dejte pozor na správnost
a umístění akordů.

#### k textu

- čistý text je preferován

- řádek začíná velkým písmenem
 
- nikdy nekončí interpunkcí

- dvojté mezery jsou mazády

- max. jeden volný řádek mezi texty

- před prvním refrénem `[chorus]`

- místo druhého stejného značka `[chorus]`

- povoleny značky jako [verse], [solo], [bridge], ovšem jen tam, kde to nejde
poznat z akordů / přirozené struktury textu

- používejte opakování, tj. na konci řádku umístěte třeba `[2x]`
(viz drunken sailor)

- dodržuje pravidla DRY a KISS (viz google)

- inspirujte se hotovými songy ;)

#### zápis akordů

Dvě nejdůležitější pravidla:

!!! první znak je vždy jeden z: CDEFGABH

!!! vedle akrdů může být počet opakování (3x, 5x), ale NIC jiného

všechny tvary akordů:

```
Akord začíná primou, tón je jeden z: cdefgabh
C je dur, c je moll
Za primou může být:
    křížek: # is (tedy například F# Fis)
    béčko b s es (tedy například Eb Es Des)

durový akort může být kormě velikosti písmene označen:
dur, maj, △ (toto má přednost před velikostí písmene, tedy c△ bude C ne Cm

molový akord může být označen:
m, min, mol, mi

preferovaný zápis (a zápis, na který jsou akordy převáděny) je:
C, Cm, Cb Cbm, C#, C#m

Další možné tvary akordů (ne nutně všechny):
(vždy: název - alerernativní názvy - tóny daného akordu
C CMaj C△ Cdur, C - E - G
Cm Cmin, C - Eb - G
C7, C - E - G - Bb
Cm7, C - Eb - G - Bb
Cmaj7, C - E - G - B
Cminmaj CmM7, C - Eb - G - B
C6, C - E - G - A
Cm6 Cmin6, C - Eb - G - A
C6add9 C6/9, C - E - G - A - D
C5 Cno3, C - G
C9, C - E - G - Bb - D
Cm9 Cmin9, C - Eb - G - Bb - D
Cmaj9, C - E - G - B - D
C11, C - E - G - Bb - D - F
Cm11, C - Eb - G - Bb - D - F
C13, C - E - G - Bb - D - F - A
Cm13, C - Eb - G - Bb - D - F - A
Cadd9 Cadd2, C - E - G - D
C7b5 C7-5, C - E - Gb - Bb
Caug7 C7+5 C7#5, C - E - G# - Bb
Csus4, C - F - G
Csus2, C - D - G
Cdim C°, C - Eb - Gb
Cdim7 C°7, C - Eb - Gb - A
Cm7b5 Cø, C - Eb - Gb - Bb
Caug C+ C(#5), C - E - G#

za akordem může být /BASS, třeba D/F#

Pozor, řídíme se českou notací, tedy: A B H C, ne A Bb B C
Bb je transformováno na A, stejně jako třeba H# na C
```

#### umístění akordů

Textový soubor, pokud je otevřen třeba třeba v notepadu, má výchozí font
monospaced, tzn. každý znak je stejně široký. Všechny akordy tedy mohou být
umístěny přesně nad to místo, kde mají znít. Jako ukázku první sloka z 
`Wish you were here`:

```
C                              D/F#
 So, so you think you can tell
                 Am/E                  G
Heaven from Hell, blue skies from pain
                          D/F#               C                    Am
Can you tell a green field from a cold steel rail, a smile from a veil,
                           G
Do you think you can tell?
```
Pár poznámek:

- První `C` začíná před zpěvem, v tom případě (a jen v tom případě)
je řádek s textem odsunut jednou mezerou (při renderování bude posunut akord
, ne text ;))

- Druhý akord `D/F#` zní až po slově `tell`, je tedy až za slovem (přesně
o dvě mezery dál než poslední `l`)

- Třetí akord je mezi slovy, tedy opět znak před tím následujícím

- Například druhé `C` zní přesně se znakem `r`

Mnohé z písniček jsou mnohem přímočarejší, i tak prosím pozor na správné
umístění akordů