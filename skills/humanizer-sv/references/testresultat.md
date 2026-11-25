# Testresultat (november 2026)

Alla siffror är AI-poäng i procent (0 = mänsklig, 100 = AI) från gratisversionerna av detektorerna, körda med
`scripts/detect.js`. Smodin-värdet är `completelyGeneratedProbability`, inte teasersiffran på sidan. Texterna
är 130–260 ord. Varje text har körts en gång, så enskilda siffror har brus. Läs mönstren, inte decimalerna.

## Baslinje

AI-texter skrevs av en språkmodell i standardstil (uppsats om AI, debattartikel om skärmtid, personligt brev,
nyhet om lånecyklar, reseblogg). Mänskliga texter är riksdagsmotioner från 2016/17 och svenska
Wikipediaversioner från 2017–2019.

| Text | ZeroGPT | Smodin | Grammarly | Undetectable |
|---|---|---|---|---|
| AI uppsats | 100 | 100 | 45 | 99 |
| AI debatt | 100 | 0 | 43 | 99 |
| AI brev | 97 | 100 | 0 | 99 |
| AI nyhet | 100 | 47 | 20 | 99 |
| AI blogg | 91 | 55 | 0 | 99 |
| Mänsklig: 4 motioner | 0, 96, 32, 96 | 0, 0, 0, 0 | 0, 0, 0, 0 | 18, 2, 18, 51 |
| Mänsklig: 4 Wikipedia | 91, 61, 18, 90 | 0, 0, 0, – | 0, 0, 0, 28 | 3, 17, 2, 13 |

En lokal Binoculars-detektor (Qwen3-1.7B, bas mot instruct) skiljde inte svenska AI-texter från mänskliga
(0,92–1,03 mot 0,94–1,04) och används inte.

## Omskrivning 1: stilputs (AI-fraser bort, personlig röst, frågor, parenteser)

| Text | ZeroGPT | Smodin | Grammarly | Undetectable |
|---|---|---|---|---|
| uppsats | 0 | 0 | 0 | 81 |
| debatt | 0 | 0 | 0 | 78 |
| brev | 91 | 0 | 33 | 77 |
| blogg | 0 | – | 0 | 56 |
| nyhet | 0 | – | 0 | 39 |

Slutsats: stilputs räcker mot ZeroGPT, Smodin och Grammarly men inte mot Undetectable.

## Kontrollerade varianter av samma uppsats (Undetectable)

| Variant | ZeroGPT | Grammarly | Undetectable |
|---|---|---|---|
| A: omskrivning 1 | 0 | 0 | 81 |
| B: utan tankstreck, kolon och frågor | 21 | 0 | 61 |
| C: talspråk, slang, små bokstäver | 0 | 0 | 59 |
| D: allt i långa kommakedjor | 43 | 0 | 99 |
| E: formellt och faktatätt | 100 | 33 | 67 |
| G: B utan tes och slutsats | 0 | 0 | 72 |
| F: jag-anekdot, korta meningar | 0 | 34 | 58 |
| F2: anekdot med fler konkreta detaljer | 0 | 0 | 53 |
| F3: anekdot, medellånga meningar, subjekt först | 0 | 0 | 63 |
| **F4: F3 med framflyttade led (V2)** | 0 | 38 | **20** |
| F5: F3 som krönika | 0 | 36 | 41 |
| **E2: krönika, konkret fall, V2, siffror** | 0 | 0 | **15** |
| W: Wikipedia-stil | 76 | 36 | 62 |
| **N2: nyhet, tät konkretion** | 0 | 0 | **12** |

## Omskrivning 2–5: alla regler tillämpade

| Text | ZeroGPT | Smodin | Grammarly | Undetectable | Konkretion/100 ord |
|---|---|---|---|---|---|
| nyhet v2 | 0 | – | 0 | 10 | 17 |
| blogg v2 | 0 | 0 | 0 | 16 | 7,5 |
| uppsats v2 | 0 | 0 | 0 | 41 | 5,0 |
| brev v2 / v3 | 0 / 0 | 0 / 0 | 35 / 33 | 30 / 28 | 5 |
| debatt v2 / v3 | 0 / 0 | 0 / 0 | 25 / 21 | 69 / 62 | 4,5–5,7 |
| debatt v4 (scenöppning, personlig röst) | 0 | 0 | 34 | 65 | 7,6 |
| **debatt v5 (faktatät, avsändare, krav med datum)** | 0 | 0 | 30 | **17** | 13,7 |
| debatt utan nya fakta | 0 | 0 | 0 | 70 | 0 |
| uppsats utan nya fakta | 23 | 0 | 0 | 63 | 1,6 |

## Grammarly: ablation på ett stycke i brevet

| Stycke 2 skrivet som | Grammarly |
|---|---|
| tre medellånga påståenden | 33 |
| sex korta meningar | 28 |
| vardagsord | 30 |
| fler konkreta detaljer | 30 |
| **en lång mening med parentes och tankstreck** | **0** |
| stycket struket | 0 |

## Blindtest: en ny agent med bara skillen

Fem nya AI-texter i andra genrer. En agent som inte sett testerna fick SKILL.md, texterna och användarens
svar på detaljfrågan (inga detaljer för uppsatserna). Siffror: ZeroGPT / Smodin / Grammarly / Undetectable.

| Text | AI-original | Efter skillen |
|---|---|---|
| Doktor Glas (skoluppgift, inga detaljer) | 100 / 100 / 22 / 78 | 13 / 0 / 15 / 27 |
| LinkedIn (detaljer) | 100 / – / 0 / 99 | 16 / 0 / 0 / 46 |
| Produkttext (detaljer) | 76 / – / 0 / 84 | 0 / 0 / 0 / 46 |
| Klimatuppsats (inga detaljer) | 100 / 51 / 18 / 99 | 40 / 0 / 51 / 77 |
| Enkätrapport (detaljer) | 100 / 50 / 49 / 99 | 46 / 0 / 48 / 68 |

Uppföljning för hand:

| Ändring | Resultat |
|---|---|
| Rapporten utan tolkande glosor, aktiv avsändare, utan "Syftet var", sista stycket = vem gör vad | 0 / 0 / 0 / 12 |
| Klimatuppsatsen utan glosor (bara allmänkunskap: IPCC, Parisavtalet, 2045) | 51 / 0 / 0 / 73 |
| Klimatuppsatsen med två egna detaljer från eleven (skyfallet i Gävle 2021, solceller hemma) | 27 / 0 / 0 / 47 |

Andra blindrundan, ny agent med den uppdaterade skillen (– = under Smodins gräns på 1 000 tecken):

| Text | Runda 1 | Runda 2 |
|---|---|---|
| LinkedIn | 16 / 0 / 0 / 46 | 0 / – / 0 / 41 |
| Produkttext | 0 / 0 / 0 / 46 | 0 / 0 / 0 / 45 |
| Enkätrapport | 46 / 0 / 48 / 68 | 0 / – / 21 / 39 |
| Klimatuppsats (inga detaljer) | 40 / 0 / 51 / 77 | 79 / 0 / 30 / 62 |

Under rättningsvarvet strök agenten på egen hand detaljer som den hade hittat på i första utkastet
(funktioner hos bryggaren, lunchställen och lägenhet i LinkedIn-inlägget). Det var faktakontrollen som
fångade dem.

Efter första blindrundan fick skillen regeln om tolkande glosor, genreråd för LinkedIn, produkttext och rapport och
faktakontrollen `--source`.

## Mönster

1. Konkretion under 3 per 100 ord gav 53–99 i Undetectable oavsett stil. Över 10 gav 10–17.
2. Samma innehåll med framflyttade led: 63 → 20.
3. Slang, fragment, scenöppningar och kommakedjor gav inte lägre poäng.
4. ZeroGPT flaggar formell svenska, även mänsklig. Grammarly flaggar stycken med jämn rytm.
5. Tolkande glosor efter varje fakta håller kvar höga poäng även i faktatät text.
6. Text som bara bygger på allmänkunskap (klimat, AI) är svårast. Egna detaljer hjälper mest.
7. Ingen variant fick 0 i Undetectable. Mänsklig svensk text får 2–18 där.
