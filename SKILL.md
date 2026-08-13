--
name: component-generator
description: Luo uusi kansio joka annetaam parametrinä jonne kuvien kopiot siirretään. Käytä kun pyydetään kuva vertailua.
---

# Component Generator

## Milloin tätä käytetään
Kun käyttäjä pyytää uutta kuvien vertailua

## Tarvittava konteksti
- Kansion nimi
- Mihin tiedostot sijoitetaan

## Vaiheet
1. Luo annettu kansio
2. Anna kansiolle riittävät oikeudet
3. Tee vertailu ja siirrä kopiot kansioon
4. Luo vastaava testitiedosto

## Lopputulos
- Komponenttitiedosto (.txt)
- Testitiedosto (.test.tsx)
- alkuperäinen kansio sisältää vain yksilöllisiä kuvia
- kopio kansiossa on kuvien kopiot 
