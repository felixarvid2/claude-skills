#!/usr/bin/env python3
"""Deterministisk kontroll av svenska AI-markörer. Ingen AI-detektor: den visar
det som går att räkna (ord, ordföljd, rytm, typografi) så att omskrivningen kan
riktas. Användning: python3 sv_check.py fil.txt [--json]"""
import json, re, sys
from statistics import mean

# Ord och fraser som AI-svenska överanvänder. Nivå 1 räcker ensamma; nivå 2 räknas först vid upprepning.
TIER1 = [
    r"i dagens (snabbrörliga|digitala|moderna|föränderliga)", r"i en (alltmer|allt mer) (digital|globaliserad|uppkopplad)",
    r"spelar en (avgörande|viktig|central|nyckel)roll", r"spelar en (avgörande|viktig|central) roll", r"en allt viktigare roll",
    r"sammanfattningsvis", r"avslutningsvis", r"det är (viktigt|värt) att (notera|understryka|komma ihåg|påpeka)",
    r"för det första", r"för det andra", r"för det tredje", r"när det kommer till", r"i slutändan", r"låt oss",
    r"djupdyk", r"mångfacetterad", r"banbrytande", r"sömlös", r"navigera (i|genom)", r"en resa (mot|genom)",
    r"(dra|dra full) nytta av (teknikens|dess) potential", r"fullt ut", r"inte bara .{1,60}? utan (även|också)",
    r"möjliggör", r"bidra till att", r"säkerställa att", r"på ett (ansvarsfullt|hållbart|effektivt) (och \w+ )?sätt",
    r"hitta (en|rätt) balans", r"driven(,| och)", r"lagspelare", r"många bollar i luften", r"lösningsorienterad",
    r"passion för", r"ser fram emot möjligheten", r"värdefull kompetens", r"dynamisk miljö",
    r"det handlar (i grunden|ytterst|i slutändan) om", r"är (inte|aldrig) (problemet|frågan)", r"det är dags att",
    r"kan man konstatera", r"en genomtänkt strategi", r"enorma möjligheter", r"betydande utmaningar",
]
TIER2 = ["avgörande", "dessutom", "därutöver", "vidare", "samtidigt", "tydligt", "centrala?", "innovativa?", "hållbar(t|a)?",
         "effektiv(t|a|isera)?", "potential", "utmaning(ar|en)?", "möjlighet(er|erna)?", "transparens", "främja", "aspekt(er)?",
         "faktorer", "avseende", "gällande", "bland annat", "olika", "viktig(t|a)?"]
SUBJ = {"jag", "vi", "du", "ni", "han", "hon", "den", "det", "de", "dom", "man", "detta", "denna", "dessa", "min", "mitt",
        "mina", "vår", "vårt", "våra", "många", "flera", "alla", "ingen", "inget", "några"}
FRONTED = {"i", "på", "när", "efter", "sedan", "under", "om", "för", "med", "till", "enligt", "trots", "eftersom", "innan",
           "medan", "därför", "då", "där", "här", "nu", "ändå", "redan", "också", "förra", "nästa", "varje", "hos", "från",
           "vid", "inom", "utan", "mot", "bland", "genom", "att", "varför", "hur", "vad", "vem", "vilken", "vilket", "först",
           "sist", "sen", "igår", "idag", "halvvägs", "uppför", "nedför", "ovanför", "inne", "ute", "hemma", "kanske", "ofta",
           "aldrig", "alltid", "sällan", "ibland", "mest", "helst", "så", "dessutom", "samtidigt", "däremot", "sedan"}
CONNECTOR_OPEN = {"dessutom", "samtidigt", "vidare", "därutöver", "slutligen", "avslutningsvis", "sammanfattningsvis",
                  "därför", "således", "följaktligen"}

def sentences(par):
    par = re.sub(r"\s+", " ", par.strip())
    parts = re.split(r"(?<=[.!?])\s+(?=[–—\-\"”A-ZÅÄÖ0-9])", par)
    return [p for p in parts if len(p.split()) >= 1]

def words(s): return re.findall(r"[\wåäöÅÄÖéÉ\-]+", s)

def check(text):
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    body = [p for p in paras if len(words(p)) >= 8]  # hoppa över hälsningsfraser och namnrader
    sents = [s for p in body for s in sentences(p)]
    low = text.lower()
    issues = []
    t1 = {}
    for pat in TIER1:
        n = len(re.findall(pat, low))
        if n: t1[pat] = n
    t2 = {}
    for w in TIER2:
        n = len(re.findall(r"\b" + w + r"\b", low))
        if n >= 2: t2[w] = n
    # Ordföljd: hur många meningar börjar med subjekt resp. framflyttat led
    starts = []
    for s in sents:
        w = [x.lower() for x in words(s)]
        if not w: continue
        if s.lstrip().startswith(("–", "—", "-")): continue  # repliker
        starts.append(w[0])
    n_s = len(starts) or 1
    subj_first = sum(1 for w in starts if w in SUBJ) / n_s
    fronted = sum(1 for w in starts if w in FRONTED) / n_s
    conn_open = [w for w in starts if w in CONNECTOR_OPEN]
    det_start = sum(1 for s in sents if re.match(r"\s*Det (är|finns|handlar|krävs|gäller)\b", s)) / n_s
    # Rytm: tre eller fler meningar i rad inom ±4 ord
    runs = []
    for p in body:
        L = [len(words(s)) for s in sentences(p)]
        i = 0
        while i < len(L) - 2:
            j = i
            while j + 1 < len(L) and abs(L[j + 1] - L[i]) <= 4: j += 1
            if j - i >= 2: runs.append((L[i:j + 1], sentences(p)[i][:60])); i = j + 1
            else: i += 1
    lens = [len(words(s)) for s in sents]
    short_frag = sum(1 for x in lens if x <= 4)
    long_chain = sum(1 for s in sents if len(words(s)) >= 40 and s.count(",") >= 4)
    # Negativ kontrast
    negc = len(re.findall(r"\binte\b[^.!?]{0,80}\b(utan|däremot)\b", low)) + len(re.findall(r"är inte [^.!?]{1,40}\. (problemet|det|frågan)", low))
    # Typografi
    typo = {}
    if "—" in text: typo["långt tankstreck — (svenska använder – med mellanslag)"] = text.count("—")
    if re.search(r"\w-\s|\s-\s", text): typo["bindestreck som tankstreck"] = len(re.findall(r"\s-\s", text))
    if re.search(r"[“\"]", text): typo["engelska citattecken (svenska: ” ”)"] = len(re.findall(r"[“\"]", text))
    if re.search(r"\d%", text): typo["procent utan mellanslag (svenska: 25 %)"] = len(re.findall(r"\d%", text))
    if re.search(r"\b\d{1,3},\d{3}\b", text): typo["tusentalskomma (svenska: 1 000)"] = 1
    if re.search(r"\b[A-ZÅÄÖ]{2,}s\b", text): typo["genitiv utan kolon (EU:s, AI:s)"] = len(re.findall(r"\b[A-ZÅÄÖ]{2,}s\b", text))
    heads = [l for l in text.splitlines() if l.strip() and len(l.split()) <= 8 and not l.strip().endswith((".", "!", "?", ","))]
    tc = [h for h in heads if sum(1 for w in h.split()[1:] if w[:1].isupper()) >= 2]
    if tc: typo["Versaler I Rubriker (engelsk stil)"] = len(tc)
    colons = len(re.findall(r":\s+[a-zåäö]", text))
    qs = sum(1 for s in sents if s.endswith("?"))
    paren = text.count("(")
    plens = [len(words(p)) for p in body]
    # Konkretion: siffror, egennamn mitt i meningen, månader/veckodagar, enheter. Mäter inte sanning, bara täthet.
    conc = 0
    for s_ in sents:
        toks = s_.split()
        conc += sum(1 for t in toks[1:] if re.match(r"[A-ZÅÄÖ][a-zåäöé]+", t) and t.rstrip(".,;:)!?") not in ("AI", "Jag", "Det"))
        conc += sum(1 for t in toks[1:] if re.match(r"[A-ZÅÄÖ]{2,}", t))
    conc += len(re.findall(r"\b\d+([,.]\d+)?\b", text))
    conc += len(re.findall(r"\b(januari|februari|mars|april|maj|juni|juli|augusti|september|oktober|november|december|måndag|tisdag|onsdag|torsdag|fredag|lördag|söndag)\w*", low))
    conc_rate = round(100 * conc / max(1, len(words(text))), 1)
    res = {
        "ord": len(words(text)), "meningar": len(sents), "stycken": len(body),
        "nivå1_fraser": t1, "nivå2_upprepade": t2,
        "andel_subjekt_först": round(subj_first, 2), "andel_framflyttat_led": round(fronted, 2),
        "andel_Det_är/finns-start": round(det_start, 2), "sambandsord_först_i_mening": conn_open,
        "negativ_kontrast": negc, "likformiga_meningsserier": runs,
        "meningslängd_medel": round(mean(lens), 1) if lens else 0,
        "meningslängd_min_max": [min(lens), max(lens)] if lens else [],
        "korta_fragment(<=4 ord)": short_frag, "kommakedjor(>=40 ord)": long_chain,
        "styckelängder": plens, "kolon_inledning": colons, "frågor": qs, "parenteser": paren,
        "typografi": typo, "konkretion_per_100_ord": conc_rate,
    }
    # Bedömning (trösklar kalibrerade på testkorpusen, se references/testresultat.md)
    if t1: issues.append(f"{sum(t1.values())} nivå 1-fraser: skriv om dem")
    if t2: issues.append("upprepade nivå 2-ord: " + ", ".join(f"{k}×{v}" for k, v in t2.items()))
    if subj_first > 0.55: issues.append(f"{subj_first:.0%} av meningarna börjar med subjektet: flytta fram tid, plats, objekt eller bisats (mål ≤ 50 %)")
    if conn_open: issues.append("meningar som börjar med sambandsord: " + ", ".join(conn_open))
    if negc: issues.append(f"{negc} negativa kontraster (inte X utan Y / X är inte problemet)")
    if runs: issues.append(f"{len(runs)} serier med 3+ lika långa meningar: slå ihop eller dela")
    if short_frag >= 3: issues.append(f"{short_frag} korta fragment: humaniseringsstil som detektorer känner igen")
    if long_chain: issues.append(f"{long_chain} kommakedjor: dela upp")
    if typo: issues.append("typografi: " + "; ".join(typo))
    if len(plens) >= 4:
        m = mean(plens); cv = (sum((x - m) ** 2 for x in plens) / len(plens)) ** 0.5 / m
        if cv < 0.15: issues.append(f"alla stycken är nästan lika långa ({plens}): låt minst ett vara tydligt kortare eller längre")
    if conc_rate < 5: issues.append(f"konkretion {conc_rate} per 100 ord: för lite namn, siffror, platser och datum. Starka detektorer (Undetectable, Copyleaks, Pangram) flaggar generiskt innehåll oavsett stil. Använd detaljer ur källan eller be användaren om riktiga detaljer (mål ≥ 7)")
    res["åtgärder"] = issues
    return res

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for f in args:
        r = check(open(f, encoding="utf-8").read())
        if "--json" in sys.argv: print(json.dumps({"fil": f, **r}, ensure_ascii=False)); continue
        print(f"== {f}: {r['ord']} ord, {r['meningar']} meningar, subjekt först {r['andel_subjekt_först']:.0%}, framflyttat {r['andel_framflyttat_led']:.0%}, konkretion {r['konkretion_per_100_ord']}, stycken {r['styckelängder']}")
        for i in r["åtgärder"] or ["inga räknebara markörer kvar"]: print("  -", i)
