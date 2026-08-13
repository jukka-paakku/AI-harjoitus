# Picture Matcher

Python 3 -komentorivityökalu, joka etsii valitusta kansiosta samankaltaisia kuvatiedostoja, tallentaa löydökset SQLite-tietokantaan ja voi siirtää löydetyt ehdokkaat erilliseen kansioon. Työkalu on turvallinen oletuksena: se vain raportoi ja tallentaa ehdokkaat; siirto vaatii erillisen `--move`-valinnan.

## Vaatimukset

- Python 3.11 tai uudempi
- Ei ulkoisia Python-riippuvuuksia

## Käyttö

Asenna projekti kehitettävänä pakettina:

```bash
python -m pip install -e .
```

Skannaa kansio ja tallenna tulokset oletusarvoiseen `data/images.db`-tietokantaan:

```bash
picture-matcher /polku/kuviin
```

Säädä samankaltaisuusrajaa (0–100):

```bash
picture-matcher /polku/kuviin --threshold 95
```

Siirrä löytyneet kopiot vasta tarkistuksen jälkeen:

```bash
picture-matcher /polku/kuviin --destination /polku/samantyyppisiin --move
```

Kohdekansio luodaan tarvittaessa käyttöoikeuksilla `750`. Kustakin kopiojoukosta ensimmäinen kuva jää lähdekansioon; muut, myös eri nimellä olevat kopiot, siirretään kohdekansioon. Jos kohdekansiossa on jo samanniminen tiedosto, siirto keskeytyy ennen yhtäkään siirtoa eikä tiedostoja ylikirjoiteta.

## Miten vertailu toimii

Tuetut muodot ovat vain JPG ja JPEG (kirjainkoko ei vaikuta). Vertailu muodostaa kustakin tiedostosta SHA-256-tiivisteen tiedoston alusta ja lopusta ja laskee tiivisteiden yhtä suurten bittien osuuden. Menetelmä on nopea lähtökohta tarkkojen tai lähes identtisten tiedostojen ryhmittelyyn, mutta ei vielä tulkitse kuvan visuaalista sisältöä. Seuraava kehitysaskel on korvata tämä perceptual hash- tai natiivilla C-algoritmilla.

Kun `--move` on annettu, ohjelma kokoaa ehdokaspareista kaikki yksilölliset lähde- ja kohdetiedostot. Näin samalla kuvalla voi olla eri nimiä ja kaikki löydetyt kopiot siirretään kerran kohdekansioon.

## Rakenne

```text
src/picture_matcher/
  cli.py          komentorivikäyttö
  scanner.py      kuvien haku ja samankaltaisuusvertailu
  database.py     SQLite-tallennus
  service.py      skannaus- ja siirtotyönkulku
  types/          jaetut tietotyypit
tests/            yksikkötestit
components/       SKILL.md:n kuvaama kuvavertailukomponentti
```

## Testit

```bash
python -m unittest discover -s tests
```

Projektin nykyinen `AGENTS.md` sisältää myös Next.js-, Tailwind-, shadcn/ui-, Vitest- ja Playwright-mainintoja. Ne ovat ristiriidassa saman tiedoston nykyisen Python 3 / Python -framework- ja kielivalintojen kanssa, joten tämä aloitusrunko noudattaa tuoreinta Python-määrittelyä eikä lisää verkkokehysriippuvuuksia.
