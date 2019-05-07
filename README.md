# Ondřej Lomič's songbook

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

- před prvním refrénem `®:`

- místo druhého stejného značka `®`

- povoleny značky jako [verse], [solo], [bridge], ovšem jen tam, kde to nejde
poznat z akordů / přirozené struktury textu

- používejte opakování, tj. na konci řádku umístěte třeba `2x`
(viz drunken sailor)

- dodržuje pravidla DRY a KISS (viz google)

- inspirujte se hotovými songy ;)

#### zápis akordů

```
první znak je vždy jeden z: CDEFGABH !!!
A - dur
Am - mol
A# - ais dur
As - as dur
Ab - as dur
Abm - as mol
Asus - asus
Adim - adim
A9
A9# - a se zvýšenou devítkou...
H je H a B je B, Bb je A
A/C - a s tónem C v basu
AC/DC - to je kapela, ne akord
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
umístění akordů. 