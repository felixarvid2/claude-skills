---
name: humanizer-sv
description: Skriv om svensk text så att den låter skriven av en människa och får låga poäng i AI-detektorer (ZeroGPT, Smodin, Grammarly, Undetectable, Copyleaks, Pangram, GPTZero). Tar bort svenska AI-markörer (ord, mallar, ordföljd, rytm, typografi), bygger upp konkretion med riktiga detaljer och mäter resultatet med ett kontrollskript och valfritt mot detektorerna. Använd när någon vill "avAI:a", humanisera, få bort AI-tonen eller sänka AI-poängen på en svensk text, eller när du själv skriver svensk text som inte ska låta som AI. Svenska regler, inte översatta engelska.
---

# Humanizer för svenska

Målet är svensk text som en svensk läsare och en AI-detektor båda läser som mänsklig. Reglerna nedan är
**uppmätta**: varje påstående om vad som sänker en poäng kommer från tester mot riktiga detektorer på svenska
texter (se `references/testresultat.md`). Engelska humanizer-regler fungerar bara delvis på svenska.

## Det viktigaste först (uppmätt)

1. **Stilputs räcker mot de svaga detektorerna, inte mot de starka.** Om man tar bort AI-fraser, mallen och
   typografin går ZeroGPT, Smodin och Grammarly till 0. Undetectable (flerspråkig XLM-klassificerare, samma
   klass som Copyleaks och Pangram) låg kvar på 60–80 % så länge innehållet var generiskt.
2. **Konkretion är den största spaken mot starka detektorer.** Samma debattartikel gick från 65 till 17 % när
   allmänna påståenden ersattes med namn, siffror, platser och datum. Nyhetstext med tät konkretion fick 10 %.
   Mänskliga svenska texter från före 2020 får 2–18 % i samma detektor.
3. **Svensk ordföljd (V2) sänker mycket.** Exakt samma innehåll gick från 63 till 20 % när meningarna fick
   börja med tid, plats, objekt eller bisats i stället för subjektet (`Sju minuter tog samtalet`,
   `På Sahlgrenska läser…`). AI-svenska är engelsk SVO i svenska ord.
4. **Stryk tolkande glosor.** AI förklarar varje fakta (`vilket tyder på att…`, `har förvaltningen alltså en
   stabil grund att bygga vidare på`, `Bakom den siffran finns…`). Det var den största skillnaden mellan en
   rapport på 68 % och samma rapport på 12 % (och 0 i de andra tre detektorerna).
5. **Det som "låter mänskligt" enligt engelska humanizers fungerar inte.** Slang och slarv (59 %), korta
   hackiga fragment, scenöppningar ("Klockan var tjugo i tolv…") och jag-anekdoter med subjektet först
   (53–65 %) flaggades. Långa kommakedjor gav 99 %.
6. **Hitta aldrig på fakta.** Konkretionen måste vara sann: ur källtexten, ur användarens egna uppgifter
   eller ur källor du har kontrollerat. Saknas detaljer: fråga (steg 1).

## Arbetsgång

### 0. Läs av uppdraget
Ta reda på genre (skoluppsats, debattartikel, personligt brev, nyhet, blogg, rapport, mejl, inlägg), mottagare
och vem som "skriver". Finns ett eget textprov från användaren: matcha dess meningslängd, ordval och
skiljetecken. Behåll registret (en formell rapport ska inte bli talspråk). Kör kontrollen på originalet:

```bash
python3 scripts/sv_check.py original.txt
```

### 1. Samla konkretion (gör detta innan du skriver om)
Lista allt konkret som redan finns i texten: namn, platser, siffror, datum, institutioner, titlar, citat,
egna erfarenheter. Räkna `konkretion_per_100_ord` i kontrollen. Under 5 betyder att starka detektorer kommer
att flagga texten hur väl den än är skriven.

Om texten är generisk, **fråga användaren** efter 3–6 riktiga detaljer som passar genren, till exempel:
- personligt brev: arbetsgivare, ort, årtal, verktyg, ett konkret resultat, något från annonsen
- skoluppsats/debatt: källan eller undersökningen med namn och år, en plats, ett exempel ur egen vardag
- blogg: datum, platser, priser, namn på ställen, vad som gick snett
- rapport: tabellvärden, metod, urval, årtal

Kan användaren inte svara: skriv om ändå med det som finns och med fakta du säkert vet (en roman, en
rapport från IPCC, ett riksdagsbeslut). Lista sedan i ditt svar, inte i den färdiga texten, var detaljer
skulle göra mest nytta (`ett eget exempel i stycke 2`, `källa med år i stycke 3`). Säg rakt ut att starka
detektorer troligen ger högt utslag utan dem. I testet låg en klimatuppsats byggd på allmänkunskap kvar på
73 %. Med två egna detaljer från eleven sjönk den till 47 %.

### 2. Bryt mallen (struktur)
AI-svenska följer samma disposition oavsett ämne: tes ("X har blivit en allt viktigare del av…") →
fördelar → risker → "Sammanfattningsvis… både möjligheter och utmaningar" → uppmaning. Gör så här:
- Börja i materialet: en siffra, ett beslut, en iakttagelse. Inte i en allmän bakgrund.
- Stryk meningar som inte bär information ("Det är viktigt att komma ihåg att varje situation är unik").
  Att stryka höjer konkretionen utan att något hittas på.
- Ingen balanserad för/emot-symmetri om inte genren kräver den. Låt en sida väga tyngre.
- **Inga tolkande glosor.** Efter en siffra eller ett faktum: lägg inte till vad det "visar", "tyder på",
  "innebär" eller "säger om". Stryk `alltså`, `vilket ger`, `något som understryker`, `en god grund att bygga
  vidare på`, `Ett enstaka X bevisar inget, men…`. Står tolkningen för något nytt, skriv den som ett eget
  påstående med eget innehåll.
- Inget sammanfattande slutstycke. Sluta på en konkret punkt, ett krav med adressat och datum, eller en
  sista iakttagelse.
- Stycken av olika längd. Ett stycke kan vara en enda mening.

### 3. Meningar (ordföljd och rytm)
- **Variera fundamentet.** Högst hälften av meningarna ska börja med subjektet, särskilt i text med få
  fakta (nyhetstext med tät konkretion klarade sig med hälften). Flytta fram tid
  (`I tisdags`, `Sedan hösten 2021`), plats (`På röntgen på Sahlgrenska`), objekt (`Torrfisken provade jag en
  gång`), bisats (`När leveransen börjar glida…`) eller predikativ (`Svårare är frågan om…`). Gör det där det
  låter naturligt, inte i varje mening.
- **Ingen negativ kontrast.** `inte X utan Y`, `X är inte problemet, problemet är Y`, `Förbud tror vi inte
  på. Däremot…` är den starkaste AI-markören i alla språk som har mätts. Säg Y direkt.
- **Inga sambandsord först i meningen** (`Dessutom`, `Samtidigt`, `Vidare`, `Därför`). Högst ett per stycke,
  helst inne i meningen.
- **Rytm per stycke.** Aldrig tre meningar i rad med ungefär samma längd. Blanda en mening på 6–10 ord med en
  på 20–35. Grammarly markerar just stycken med tre jämnlånga, `och`-bundna påståenden. En lång mening med
  en parentes eller ett tankstreck klarade sig, där tre korta inte gjorde det.
- **Inga fragment** av typen `Ingen människa alltså.` eller `Vissa mer än andra.` och inga meningar på 40+
  ord som är kommakedjor. Båda ger höga poäng.
- Retoriska frågor och kolon som "avslöjar" något: högst en per text.

### 4. Ord
Se `references/ai-markorer.md` för hela listan i nivåer. Kort version:
- **Nivå 1 (stryk alltid):** `i dagens snabbrörliga/digitala värld`, `spelar en avgörande/viktig roll`,
  `Sammanfattningsvis`, `Avslutningsvis`, `Det är viktigt att notera/komma ihåg`, `För det första/andra`,
  `när det kommer till`, `i slutändan`, `inte bara … utan även`, `navigera`, `en resa`, `djupdykning`,
  `möjliggöra`, `säkerställa`, `på ett hållbart och ansvarsfullt sätt`, `hitta en balans`, `dra nytta av
  potentialen`, `enorma möjligheter`, `betydande utmaningar`. I personliga brev även: `driven`,
  `lagspelare`, `många bollar i luften`, `lösningsorienterad`, `passion för`, `värdefull kompetens`,
  `ser fram emot möjligheten`.
- **Nivå 2 (bara ett av varje per text):** `avgörande`, `dessutom`, `samtidigt`, `tydligt`, `central`,
  `innovativ`, `hållbar`, `effektiv`, `potential`, `utmaning`, `möjlighet`, `transparens`, `främja`, `aspekt`.
- Byt inte bara synonym. Skriv det som faktiskt menas (`frigöra tid för mer kreativa uppgifter` → vad
  gör man med tiden?).
- Behåll vanliga svenska småord där de hör hemma (`ju`, `väl`, `nog`, `ändå`), men strö inte ut dem för
  effekt.

### 5. Typografi (svensk, inte engelsk)
- Tankstreck: ` – ` (kort, med mellanslag), aldrig `—`. Repliker i nyhetstext börjar med `– `.
- Citattecken: `”så här”`, inte `“så här”` eller `"så här"`.
- `25 %` (mellanslag), `1 000` (mellanslag), `EU:s`, `AI:s` (kolon vid genitiv av förkortning).
- Rubriker med versal bara i första ordet och i egennamn.
- Ingen Oxford-komma före `och`.

### 6. Kontrollera
```bash
python3 scripts/sv_check.py omskriven.txt
```
Åtgärda allt i listan `åtgärder`. Målen: inga nivå 1-fraser, inga tolkande glosor, inga negativa
kontraster, inga serier av jämnlånga meningar, högst 50 % subjekt först i faktafattig text, konkretion minst 5
och helst 7 per 100 ord (bara med sanna detaljer).

Kör också faktakontrollen mot källorna (originalet och det användaren har skrivit):
```bash
python3 scripts/sv_check.py omskriven.txt --source original.txt,uppgifter.txt
```
Den listar siffror och namn som inte finns i källorna. Varje sådan detalj måste vara något du säkert vet,
annars stryker du den. Lätt att glida på: produkttexter (funktioner som inte finns), LinkedIn
(teamritualer, kollegors namn) och rapporter (årtal som bara är gissade).

Läs sedan texten som en svensk läsare: låter något översatt? Finns det en mening som bara finns för att låta
bra? Stryk den. Arbetet är **ett** omskrivningsutkast plus **ett** rättningsvarv. Fler varv slätar ut texten
igen.

### 7. Mät mot detektorerna (valfritt)
```bash
cd scripts && npm i playwright@1 && node detect.js omskriven.txt
```
Kör ZeroGPT, Smodin, Grammarly och Undetectable via deras gratis webbsidor (som en vanlig besökare, en text i
taget, minst 1 000 tecken för Smodin). Tolkning och kända fel: `references/detektorer.md`. Copyleaks,
Pangram, GPTZero och Originality kräver konto eller captcha och får kontrolleras för hand.

Rimliga mål: 0 på ZeroGPT, Smodin och Grammarly. Under 20 % på Undetectable, vilket är samma nivå som
mänskliga svenska texter. Att alltid få exakt 0 i alla detektorer går inte att lova: mänskliga texter får
också utslag, och ZeroGPT ger formell mänsklig svenska upp till 96 %.

## Det här fungerade inte (uppmätt, gör inte så)
| Åtgärd | Undetectable före → efter |
|---|---|
| Talspråk, slang, små bokstäver, "haha" | 81 → 59 |
| Allt i långa kommakedjor | 81 → 99 |
| Korta fragment och jag-anekdot med subjekt först | 53–63 |
| Scenöppning med klockslag och barnets namn | 62 → 65 |
| Wikipedia-stil med fakta men allmänna inledningsmeningar | 62 (ZeroGPT 76) |
| Stilputs utan nya detaljer | 63–70 |

Lägg inte heller in stavfel, särskrivningar eller osynliga tecken: andra humanizer-projekt har mätt att det
inte hjälper, och det försämrar texten.

## Genrer i korthet
- **Nyhet:** tätast konkretion, korta stycken, replik med `– `, siffror och partibeteckningar. Gav lägst poäng.
- **Krönika/debatt:** argumentera från ett konkret fall eller en siffra, avsändare med namn och ort under
  texten, kravet med adressat och datum. Inga "Det är dags att…".
- **Personligt brev:** arbetsgivare, ort, år, verktyg och ett resultat. En egen iakttagelse om annonsen.
  Inga egenskapslistor (`driven, strukturerad och lösningsorienterad`).
- **Skoluppsats:** egen tes tidigt, källor med namn och år, ett eget exempel. Undvik den balanserade
  "både och"-slutsatsen.
- **Blogg:** datum, platser, priser, vad som gick snett. Inga "Tips:"-listor i slutet i AI-stil.
- **Formell rapport:** behåll sakligheten men med aktiv avsändare (`Förvaltningen skickade ut…`, inte `En
  undersökning genomfördes`). Stryk `Syftet med denna rapport är att`, `Mot bakgrund av`, `rekommenderas
  att` och alla tolkningar av siffrorna. Låt tabellvärden, datum och antal bära. Sluta med vem som gör vad
  och när. Det gav 0 / 0 / 0 / 12 i testet. ZeroGPT flaggar även mänsklig formell svenska, så räkna med
  några procent där.
- **LinkedIn-inlägg:** inga `otroligt glad och stolt`, `fantastiska kollegor`, `min resa`, `nu kör vi!` och
  inga raketemojis. Börja med fakta (datum, företag, roll), en sak du faktiskt gjorde med ett resultat, ett
  tack som säger vad kollegorna lärde dig.
- **Produkttext:** mått, effekt, material, pris, garanti och vad som *inte* ingår. Inga `Upptäck`,
  `perfekta kombinationen`, `den ultimata upplevelsen`, `Beställ i dag och upptäck skillnaden!`. Lägg inte
  till funktioner som tillverkaren inte har uppgett.

## Filer
- `scripts/sv_check.py` räknar markörer, ordföljd, rytm, typografi, glosor och konkretion, och listar
  med `--source` detaljer som saknas i källorna. Ingen nätåtkomst.
- `scripts/detect.js` kör de fyra gratisdetektorerna med Playwright.
- `references/ai-markorer.md` innehåller hela listan med svenska AI-markörer och ersättningar.
- `references/detektorer.md` beskriver vilka detektorer som spelar roll för svenska, hur de beter sig och hur
  man läser deras siffror.
- `references/testresultat.md` innehåller alla mätningar bakom reglerna.
