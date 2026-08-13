# AGENTS.md

## Projektin kuvaus
search picture files from specific folder and compare each other then mark and move 
similar pictures to another folder

## Tech Stack
- Framework: Next.js 15 (App Router)
- Kieli: C language
- Tietokanta: lite SQL
- Tyylitys: Tailwind CSS + shadcn/ui

## Koodauskäytännöt
- Käytä funktionaalisia komponentteja (ei class-komponentteja)
- Kirjoita tyypit erilliseen types-kansioon
- Käytä server actions tietokantaoperaatioihin

## Testaus
- Yksikkötestit: Vitest
- E2E-testit: Playwright
- Testikattavuustavoite: 80 %

## Rajoitteet
- Älä käytä any-tyyppiä
- Älä lisää uusia riippuvuuksia ilman persearch 
