# AI-detektorer och svenska (läget november 2026)

## Vilka som spelar roll

| Detektor | Svenska | Åtkomst | Kommentar |
|---|---|---|---|
| Copyleaks | Ja, officiellt (`sv`) | Webb: Cloudflare-captcha. API: konto, betalt | Bäst oberoende siffror: 95 % träffsäkerhet på 800 svenska texter, 0 falska positiva (Landberg, Chalmers 2024). Testa för hand på copyleaks.com/ai-content-detector |
| Pangram | Ja, officiellt (24 språk) | Konto krävs (även gratis). API betalt | Inspera Originality är svenska lärosätens nationella textmatchningstjänst från 1 nov 2025 (SUNET) och har ett samarbete med Pangram. Stockholms universitet har inte aktiverat AI-detektionen |
| Undetectable (XLM-detektor) | Ja i praktiken | Gratis webb, inget konto | Bäst separation av de gratis: AI 99 %, mänskligt 2–18 % (en motion 51 %). Visar röda och gröna meningar. Bra stand-in för de starka klassificerarna |
| Smodin | Påstått | Gratis webb, minst 1 000 tecken | Den stora siffran på sidan ("AI-genererad 75–93 %") är en säljteaser som visas även för mänsklig text. Läs `completelyGeneratedProbability` i svaret (`detect.js` gör det): mänskligt 0, AI 47–100 |
| ZeroGPT | Ospecificerat | Gratis webb | Brusig på formell svenska: riksdagsmotioner från 2016 fick 32–96 %, Wikipedia från 2017 18–91 %. Mäter i praktiken formell, opersonlig stil |
| Grammarly | Inte officiellt | Gratis webb | Svag på svenska (AI-texter 0–45 %). Markerar stycken med tre jämnlånga påståenden i rad |
| GPTZero | Nej (en, es, fr, de, pt, zh) | Gratis webb; körs inte headless här | Varnar själv för att svenska bara stöds delvis. Chalmers: 0 % AI på alla svenska GPT-3.5-texter |
| Originality.ai | Ja (Multi Language) | 3 gratis skanningar om dagen med konto | Aggressiv: flaggade en mänsklig svensk text som 100 % AI i AIMagasinets test |
| Turnitin | Nej | Via lärosäte | AI-detektion bara på engelska, spanska, japanska, arabiska, nederländska, tyska och turkiska |
| Winston AI | Nej | – | Svenska saknas bland 23 språk |
| isgen.ai | Påstått | reCAPTCHA | Svenskt gränssnitt |
| aidetector.se | Påstått | Google-inloggning | Påstår 99,2 % utan metod |

Skolverket säger att det saknas tillförlitliga verktyg. KTH, Lund och Uppsala avråder från detektorer.

## Hur poängen ska läsas

- **Undetectable:** procenten är sannolikheten för AI. Under ungefär 45 står "human written". Mänsklig svensk
  text låg på 2–18 %, så under 20 är ett rimligt mål. Röda meningar visar var den reagerar, men markeringen
  följer textfönster och delar ibland meningar mitt itu. Läs den som en ungefärlig karta, inte som en dom
  över enskilda meningar.
- **Smodin:** använd bara `completelyGeneratedProbability`. Under 1 000 tecken körs ingen analys.
- **ZeroGPT:** 0 är lätt att nå för vardaglig text men svårt för formella rapporter, eftersom den även
  flaggar mänsklig formell svenska. Ett högt värde på en formell text säger lite.
- **Grammarly:** ett markerat stycke ger 20–45 %. Dela upp stycket eller variera längden på meningarna.

## Webbåtkomst

`scripts/detect.js` använder sidorna som en vanlig besökare: en text i taget, ingen captcha, inga konton.
Sidorna ändras ofta. Om en detektor slutar svara, öppna sidan med Playwright, ta en skärmdump och uppdatera
selektorn. Lägg inte in kringgåenden av captcha eller Cloudflare.

## Källor

- Landberg 2024, *AI-Wolf in Sheep's Clothing*, Chalmers: https://odr.chalmers.se/items/916af05a-e9e5-4718-96c4-f6a51215b722
- Copyleaks språk: https://docs.copyleaks.com/reference/actions/miscellaneous/ai-detection-supported-languages
- Pangram språk: https://www.pangram.com/knowledge-hub/what-languages-does-pangram-work-on
- Inspera och Pangram: https://www.fenews.co.uk/education/inspera-and-pangram-launch-a-new-partnership/
- SU om Inspera Originality: https://medarbetare.su.se/en/our-su/staff-information/staff-news/news-archive/2025-09-25-ai-detection-in-inspera-originality-will-not-be-activated
- GPTZero språk: https://support.gptzero.me/articles/1682612063-what-languages-does-gptzero-support
- Winston språk: https://help.gowinston.ai/article/which-languages-does-winston-ai-work-with
- AIMagasinet test: https://aimagasinet.se/fungerar-ai-detektorer-pa-svenska/
- AIKompassen om GPTZero: https://aikompassen.com/artiklar/ai-detektorer-gptzero-guide/
