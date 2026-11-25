# Svenska AI-markörer

Listan bygger på egna detektortester (se `testresultat.md`), Erigo, Scribill, Realtid (rekryterare om
personliga brev) och erfarenheter från humanizer-skills på andra språk (engelska blader/humanizer, tyska
humanizer-de, franska humaniseur-fr, kinesiska Humanizer-zh, koreanska im-not-ai). Regeln från de bästa av dem
gäller här också: en enstaka markör bevisar ingenting. Leta efter kluster.

## Nivå 1: stryk eller skriv om alltid

| Markör | Gör i stället |
|---|---|
| I dagens snabbrörliga / digitala / moderna värld | Börja i sakfrågan: en siffra, ett beslut, en händelse |
| I en alltmer digitaliserad / globaliserad värld | Stryk |
| X har blivit en allt viktigare / avgörande del av vårt samhälle | Säg var och hur: `Swedbanks chattbot svarar på…` |
| spelar en avgörande / viktig / central roll / nyckelroll | Säg vad X gör |
| Det är viktigt att notera / understryka / komma ihåg att | Stryk inledningen, behåll påståendet om det bär information |
| För det första … För det andra … | Inga uppräkningsord. Låt styckena bära ordningen |
| Dessutom / Samtidigt / Vidare / Därutöver först i mening | Stryk, eller flytta in i meningen |
| Sammanfattningsvis / Avslutningsvis / Sammantaget | Inget sammanfattande slutstycke |
| när det kommer till (anglicism) | `när det gäller`, eller bara `i`, `om` |
| i slutändan (at the end of the day) | Stryk |
| inte bara … utan även / också | Säg båda sakerna rakt |
| inte X utan Y / X är inte problemet, problemet är Y | Säg Y |
| navigera, en resa, utforska, landskap (bildligt) | Det konkreta verbet |
| djupdykning, mångfacetterad, banbrytande, sömlös, robust | Stryk eller konkretisera |
| möjliggör, bidrar till att, säkerställa att | Vad händer? `gör att`, `så att`, eller omformulera |
| på ett ansvarsfullt / hållbart / effektivt sätt | Hur? Säg det, eller stryk |
| hitta en balans | Vilken gräns, för vem? |
| dra nytta av teknikens fulla potential | Stryk |
| enorma möjligheter, betydande utmaningar | Vilka? |
| Det handlar i grunden / ytterst om | Stryk |
| Det är dags att vi tar detta på allvar | Ett krav med adressat och datum |
| Låt oss … | Stryk |
| kan man konstatera att | Stryk |

### Personliga brev (rekryterare känner igen dessa)

| Markör | Gör i stället |
|---|---|
| driven, strukturerad och lösningsorienterad | Ett exempel som visar en av dem |
| lagspelare, trivs i en dynamisk miljö | Vad du gör i gruppen |
| håller många bollar i luften | `har tre till fem projekt igång samtidigt` |
| med stort intresse för tjänsten | Börja med något ur annonsen |
| passion för, brinner för | Stryk |
| värdefull kompetens till ert team | Vad du kan göra från dag ett |
| Jag ser fram emot möjligheten att diskutera | `En intervju passar bra…` eller stryk |
| Med vänliga hälsningar, (komma efter) | `Vänliga hälsningar` utan komma |
| Er / Ni med versal | Gemener |

## Nivå 2: bara ett av varje per text

avgörande, dessutom, samtidigt, tydligt/tydlig, central, innovativ, hållbar, effektiv(isera), potential,
utmaning, möjlighet, transparens, främja, aspekt, faktorer, avseende, gällande, bland annat, olika, viktig.

## Struktur

- Tes → fördelar → risker → balanserad slutsats → uppmaning. Det är den vanligaste AI-dispositionen på
  svenska oavsett ämne.
- Alla stycken ungefär lika långa (35–45 ord) och alla med 3–4 meningar.
- Trepunktslistor i löptext (`integritet, transparens och ansvar`), ofta abstrakta substantiv.
- Synonymrotation för samma sak (`tekniken`, `AI-lösningarna`, `systemen`, `verktygen` i varannan mening).
- Samma abstraktionsnivå rakt igenom. Människor växlar mellan detalj och helhet.
- Varje fråga besvaras, inga lösa trådar.
- Slutstycke med moral eller uppmaning (`Det är dags att…`, `Tillsammans kan vi…`).

## Ordföljd

- Subjekt först i nästan varje mening (`Jag har…`, `Det finns…`, `Tekniken medför…`). Svenska är V2: tid,
  plats, objekt, bisats och predikativ kan stå först. I testet sjönk Undetectable från 63 till 20 % av enbart
  den ändringen.
- `Det är … som`-satser i rad.
- Engelska -ing-svansar översatta till `vilket …` eller `något som …` i slutet av varje mening.
- Substantivkedjor (`genomförandet av implementeringen av`) och många s-passiv.

## Typografi

| AI/engelsk | Svensk |
|---|---|
| `—` (långt tankstreck utan mellanslag) | ` – ` |
| `"citat"` eller `“citat”` | `”citat”` |
| `25%` | `25 %` |
| `1,000` | `1 000` |
| `EUs`, `AIs` | `EU:s`, `AI:s` |
| `Så Här Skriver Man Rubriker` | `Så här skriver man rubriker` |
| `äpplen, päron, och bananer` | `äpplen, päron och bananer` |
| `Hej Anna,` följt av versal | `Hej Anna!` eller `Hej,` följt av gemen |

## Vad som saknas i AI-svenska

- Konkreta namn, platser, årtal och siffror (se konkretionsmåttet i `sv_check.py`).
- Lösa trådar, en sidokommentar i parentes, en mening som går tillbaka till något tidigare.
- Ett tydligt ställningstagande som väger över åt ett håll.
- Variation i abstraktionsnivå.

## Vad som inte ska läggas till

Slang för att verka ung, stavfel, särskrivningar, "haha", små bokstäver i meningsbörjan, emojis, eller
tankstreck och frågor i varje stycke. Inget av det sänkte poängen i testerna mot den starka detektorn, och
texten blev sämre.
