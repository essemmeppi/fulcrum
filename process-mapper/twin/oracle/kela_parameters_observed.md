# Kela general housing allowance (yleinen asumistuki) – parameters observed on kela.fi

Observed 2026-11-01 (UTC). All quotes are verbatim from the pages fetched on that date. The oracle
calculator run is documented in `kela_calculator_results.json` in this directory.

## Sources

| Key | URL | Page date statement |
|---|---|---|
| FI-params | https://www.kela.fi/miten-tulot-ja-menot-vaikuttavat | "Sivu päivitetty 26.9.2026" |
| EN-params | https://www.kela.fi/housing-allowance-income-and-assets | "Last modified 26/9/2026" |
| FI-main | https://www.kela.fi/yleinen-asumistuki | "Sivu päivitetty 12.10.2026" |
| EN-main | https://www.kela.fi/general-housing-allowance | "Last modified 12/10/2026" |
| EN-news-2026 | https://www.kela.fi/news/changes-to-kela-benefits-in-2026 | published 19/12/2025 |
| Etuusohje | https://www.kela.fi/etti/Yleinenasumistuki.pdf (Kela benefit guideline, 84 pp.) | title page: "Yleinen asumistuki 29.10.2026" |
| Vero-2026 | https://vero.fi/syventavat-vero-ohjeet/paatokset/47380/verohallinnon-paatos-vuodelta-2026-toimitettavassa-verotuksessa-noudatettavista-luontoisetujen-laskentaperusteista/ | VH/6275/00.01.00/2025, issued 13.11.2025, in force 1.1.2026 |
| Calculator (FI) | https://laskurit.kela.fi/yleisen-asumistuen-laskuri | result shown "1.11.2026 alkaen" (no explicit parameter-year statement) |
| Calculator (EN) | https://laskurit.kela.fi/general-housing-allowance-calculator | same application, English UI |
| Calculator (SV) | https://laskurit.kela.fi/raknare-for-allmant-bostadsbidrag (linked from https://www.kela.fi/allmant-bostadsbidrag) | |
| Calculator index | https://www.kela.fi/laskurit | links "https://laskurit.kela.fi/yleisen-asumistuen-laskuri" |

Which year's parameters apply: EN-news-2026 says "There will be no index adjustments to the criteria for
determining the general housing allowance ... in 2026", "This means that the criteria for determining these
allowances will remain the same as in 2025", "no changes will be made to the heating and water costs or
maximum housing costs taken into account in the general housing allowance". The Etuusohje adds (basic
deductible, p. ~"Perusomavastuukaava"): "Vuosina 2024 -2027 kertoimiin ei tehdä indeksikorotuksia." So the
2025 and 2026 values are identical; the values below are the ones in force on 1.11.2026.

## 1. Compensation rate (korvausprosentti)

- FI-params: "Yleinen asumistuki on enintään 70 % hyväksyttävistä asumismenoista. Asumistuen määrä lasketaan kaavalla 0,7 x (hyväksyttävät asumismenot – perusomavastuu)."
- EN-params: "General housing allowance covers a maximum of 70% of your acceptable housing costs. The amount of housing allowance is calculated as follows: 0.7 x (acceptable housing costs – basic deductible)."
- Åland (FI-params): "Ahvenanmaalla asumistuki on enintään 80 % hyväksyttävistä asumismenoista. Asumistuen määrä lasketaan kaavalla 0,8 x (hyväksyttävät asumismenot – perusomavastuu)."
- Calculator result page: "Yleinen asumistuki on 70 prosenttia asumismenojen ja perusomavastuun erotuksesta."

## 2. Basic deductible (perusomavastuu)

- FI-params: "Perusomavastuu = 0,5 x [T – (667 + 94 x A + 296 x L)]" and "Täyteen asumistukeen oikeuttavat 667 euron tulot, joihin lisätään 94 euroa jokaista ruokakuntaan kuuluvaa aikuista ja 296 euroa jokaista ruokakuntaan kuuluvaa lasta kohti. Luvut ovat sidoksissa kansaneläkeindeksiin (Tietoa Kelasta -osio)." (T = ruokakunnan yhteenlasketut tulot, A = aikuisten lukumäärä, L = lasten lukumäärä)
- EN-params: "Basic deductible = 0.5 x [T – (667 + 94 x A + 296 x L)]" and "The full rate of housing allowance is available on an income of EUR 667 plus EUR 94 for each adult and EUR 296 for each child in the household. These amounts are tied to the National Pensions Index (About Kela section)."
- Åland (FI-params): "0,42 x [T - (667 + 111 x A + 246 x L)]".
- Etuusohje history table ("Perusomavastuukaava"): "1.4.2024 alkaen  Perusomavastuu = 0,5 x (T – (667 + 94 x A + 296 x L)"; "1.1.- 31.3. 2024  Perusomavastuu = 0,42 x (T – (667 + 111 x A + 246 x L)"; "Vuosina 2024 -2027 kertoimiin ei tehdä indeksikorotuksia."
- Calculator check: 2 adults, T = 2000 → calculator shows "Tuloista ja ruokakunnan koosta määräytyvä asumismenojen perusomavastuu 572,50 e/kk" = 0.5 × (2000 − 667 − 2×94). 1 adult, T = 1100 → 169,50 = 0.5 × (1100 − 761). Consistent with the published formula and with NO earned-income deduction.

## 3. Maximum housing costs (enimmäisasumismenot) by municipality group

Note: the pages no longer use the labels "kuntaryhmä I–IV". There are three mainland groups plus Åland.
Group lists verbatim (FI-params, section "Asumistuen kuntakohtaiset ylärajat (enimmäisasumismenot)"):

- Group 1: "Espoo, Helsinki, Kauniainen ja Vantaa"
  "1 henkilö, asumismenoiksi hyväksytään enintään 563 e/kk / 2 henkilöä, asumismenoiksi hyväksytään enintään 808 e/kk / 3 henkilöä, asumismenoiksi hyväksytään enintään 1 019 e/kk / 4 henkilöä, asumismenoiksi hyväksytään enintään 1 188 e/kk / yli 4 henkilöä, asumismenoiksi hyväksytään enintään 1 188 e/kk + 148 e/kk jokaista seuraavaa henkilöä kohti."
- Group 2: "Hyvinkää, Hämeenlinna, Joensuu, Jyväskylä, Järvenpää, Kerava, Kirkkonummi, Kuopio, Lahti, Lohja, Nokia, Nurmijärvi, Oulu, Porvoo, Raisio, Riihimäki, Rovaniemi, Seinäjoki, Sipoo, Siuntio, Tampere, Turku, Tuusula ja Vihti"
  "1 henkilö, asumismenoiksi hyväksytään enintään 447 e/kk / 2 henkilöä ... 652 e/kk / 3 henkilöä ... 828 e/kk / 4 henkilöä ... 981 e/kk / yli 4 henkilöä, asumismenoiksi hyväksytään enintään 981 e/kk + 134 e/kk jokaista seuraavaa henkilöä kohti."
- Group 3: "Muut kunnat"
  "1 henkilö, asumismenoiksi hyväksytään enintään 394 e/kk / 2 henkilöä ... 574 e/kk / 3 henkilöä ... 734 e/kk / 4 henkilöä ... 875 e/kk / yli 4 henkilöä, asumismenoiksi hyväksytään enintään 875 e/kk + 129 e/kk jokaista seuraavaa henkilöä kohti."
- Åland: "Ahvenanmaan kunnat" — "1 henkilö ... 470 e/kk / 2 henkilöä ... 687 e/kk / 3 henkilöä ... 871 e/kk / 4 henkilöä ... 1 032 e/kk / yli 4 henkilöä, asumismenoiksi hyväksytään enintään 1 032 e/kk + 141 e/kk jokaista seuraavaa henkilöä kohti."
- Extra-space rule (all groups): "Jos ruokakuntaan kuuluu vammainen henkilö, joka tarvitsee apuvälineiden tai hoitajan vuoksi erityisen paljon tilaa, hyväksymme asumismenot yhtä henkilöä suuremman henkilömäärän mukaan."
- EN-params gives the same numbers: "1 person, a maximum of EUR 563 per month is accepted as housing costs" ... "more than 4 persons, a maximum of EUR 1,188 is accepted as housing costs + EUR 148 per month for each additional person." / "... EUR 447 ... 652 ... 1,019→(group 2: 828) ... 981 + EUR 134" / "... EUR 394 ... 574 ... 734 ... 875 + EUR 129".
- FI-params also states: "Asuntosi koko ei vaikuta tukeen." (dwelling size does not affect the allowance) — but see §6 on electricity: the calculator asks floor area when electricity is included in the rent.
- Calculator check: Helsinki 2 persons → "Enimmäisasumismenot 808,00 e/kk"; Rovaniemi 1 person → "447,00 e/kk"; Helsinki 1 person → "563,00 e/kk".

Summary table (€/month):

| persons | Espoo/Helsinki/Kauniainen/Vantaa | 24 listed cities (Turku, Tampere, Oulu, Rovaniemi, …) | Muut kunnat (e.g. Pori, Kemi) | Åland |
|---|---|---|---|---|
| 1 | 563 | 447 | 394 | 470 |
| 2 | 808 | 652 | 574 | 687 |
| 3 | 1019 | 828 | 734 | 871 |
| 4 | 1188 | 981 | 875 | 1032 |
| each additional | +148 | +134 | +129 | +141 |

## 4. Flat rates for separately paid water and heating

- Water (FI-params): "Vesimaksuksi hyväksytään 20 e/kk henkilöä kohti." EN-params: "Up to EUR 20 per person and per month is accepted."
- Heating (FI-params): "Jos ruokakunnassa on 1 henkilö, lämmityskuluiksi hyväksytään 46 e/kk. Jos ruokakuntaan kuuluu useampi henkilö, lämmityskuluihin lisätään 16 e/kk jokaista seuraavaa henkilöä kohti."
  "Etelä-Savon, Pohjois-Savon ja Pohjois-Karjalan maakunnissa hyväksytään lämmityskuluiksi 1 henkilön ruokakunnassa 48 e /kk ja jokaista seuraavaa henkilöä kohti 17 e/kk."
  "Pohjois-Pohjanmaan, Kainuun ja Lapin maakunnissa hyväksytään lämmityskuluiksi 1 henkilön ruokakunnassa 50 e/kk ja jokaista seuraavaa henkilöä kohti 17 e/kk."
- EN-params: "For one-person households, the amount of heating charges accepted is EUR 46 per month. If the household consists of more than one person, EUR 16 per month is added for each additional person." / "In Etelä-Savo, Pohjois-Savo and Pohjois-Karjala, up to EUR 48 per month ... EUR 17 per month is added for each additional person." / "In Pohjois-Pohjanmaa, Kainuu and Lapland, up to EUR 50 per month ... EUR 17 per month is added for each additional person."
- Calculator check: Rovaniemi (Lapland), 1 person, heating paid separately → "Erilliset lämmityskustannukset 50,00 e/kk". The calculator never asks for the actual water/heating amount; it only asks Kyllä/Ei and applies the flat rate.

## 5. Minimum payable amount

- FI-main: "Jos asumistuen määrä on alle 15 e/kk, sitä ei makseta."
- EN-main: "If your housing allowance is less than EUR 15 per month, it is not paid out."
- Etuusohje: "Yleistä asumistukea ei makseta, jos asumistuen määrä on alle 15 euroa."
- Calculator result page (zero case): "Asumistukea ei makseta, kun sen määrä on alle 15 e/kk." and the headline shows "0,00 e/kk".

## 6. Electricity included in rent (not in the task list, but it changes the oracle inputs)

- FI-params: "Jos vuokraan sisältyy sähkö, vähennämme vuokrasta sähkön osuuden. Asumistukea ei voi saada sähkömaksuihin."
- EN-params: "If the rent includes electricity, we will deduct the electricity charge from the rent. In other words, the housing allowance does not cover the amount you pay for electricity."
- Etuusohje ("Asumismenoista vähennetään"): "sähkön käyttöoikeuden raha-arvon mukainen määrä, jos sähkö sisältyy vuokraan – vähennys tehdään pääsääntöisesti (myös soluasunnoissa) rajoittamattoman raha-arvon mukaan. – Katso: Luontoisetujen raha-arvot."
- Vero-2026 §5: "Asuntoetuun liittyvän rajoittamattoman sähkönkäyttöoikeuden arvo on 0,86 euroa neliömetriltä kuukaudessa."
- Calculator check: when "Vuokran lisäksi erillinen sähkölasku tai -maksu" = Ei, the calculator adds a mandatory field "Ruokakunnan käytössä oleva asuinpinta-ala * m²" and shows "Vuokraan sisältyvä käyttösähkö −30,10 e/kk" for 35 m², −43,00 for 50 m², −60,20 for 70 m² (= 0,86 €/m²). When the answer is Kyllä (tenant pays own electricity bill), no floor area is asked and no deduction is made.

## 7. Asset rules

- FI-params: "Omaisuutesi vaikuttaa asumistukeen, jos asut yhden aikuisen ruokakunnassa ja sinulla on omaisuutta yli 10 000 euroa / asut kahden tai useamman aikuisen ruokakunnassa ja ruokakunnallasi on omaisuutta yhteensä yli 20 000 euroa." "Jos ruokakuntasi omaisuus ylittää 10 000 tai 20 000 euron rajan, otamme rajan ylittävästä osasta tuloksi huomioon 20 %." "Jos ruokakunnallasi on omaisuutta 50 000 euroa tai enemmän, asumistukea ei makseta lainkaan. Omaisuudesta vähennetään kuitenkin ensin pitkäaikaiset velat kuten asunto- tai opintolaina."
- Deposit disregard (FI-params): "Talletukset. Tilillä olevista talletuksista tehdään kuitenkin 2 000 euron käyttövaravähennys, joka ei vaikuta yleiseen asumistukeen. Vähennys on henkilökohtainen, eli se tehdään jokaisen ruokakunnan jäsenen tilitalletuksista."
- Published example (FI-params): "Pekalle lasketaan 5 000 euron omaisuudesta tuloa 20 % eli 1 000 euroa. Pekan omaisuudesta yleiseen asumistukeen vaikuttaa siis 1 000 euroa vuodessa eli 83,33 euroa kuukaudessa." → 20 % of the excess is an ANNUAL amount, divided by 12 for the monthly income.
- EN-params: "If your household's assets exceed the above limits of EUR 10,000 or EUR 20,000, we will take 20% of the excess into account as income." "If your household has assets of EUR 50,000 or more, no housing allowance is paid at all." "Deposits. However, a deduction of EUR 2,000 for disposable income is made from account deposits."
- Etuusohje ("Omaisuusrajat"): "Omaisuus otetaan huomioon, jos ruokakunnan omaisuus käyttövaravähennyksen ja velkojen vähentämisen jälkeen ylittää • yhden aikuisen ruokakunnassa 10 000 euroa ja • kahden tai useamman aikuisen ruokakunnassa 20 000 euroa. Jos ruokakunnan omaisuus käyttövaravähennyksen ja velkojen vähentämisen jälkeen on vähintään 50 000 euroa, yleiseen asumistukeen ei ole oikeutta lainkaan."
- Calculator step 3 text: "Omaisuus otetaan huomioon siten, että tuloihin lisätään 20 prosenttia siitä omaisuuden osasta, joka ylittää omaisuusrajan (yhden aikuisen ruokakunnassa 10 000 euroa ja kahden tai useamman aikuisen ruokakunnassa 20 000 euroa).Velat puolestaan vähentävät huomioon otettavan omaisuuden määrää." Deposit field help: "Ennen ilmoittamista vähennä talletusten määrästä 2 000 euroa käyttövaroina." (the calculator expects the user to subtract the €2,000 disregard before entering deposits).
- Also from FI-params: capital income from book-entry shares counts only "jos ne ovat suuremmat kuin 12,02 e/kk".

## 8. Earned-income deduction (ansiotulovähennys)

- Not mentioned on FI-params or EN-params at all (the only deductions described are the basic deductible and the asset rules).
- Etuusohje ("Vähennykset / Ansiotulovähennys"): "Ansiotulovähennystä koskeva yleisen asumistuen pykälä oli voimassa 1.9.2015 - 31.3.2024." "Ansiotulovähennyksen määrä oli 300 euroa kuukaudessa." Section heading: "Ansiotulovähennyksen poistuminen 1.4.2024 alkaen".
- Conclusion: the €300/month earned-income deduction no longer exists (abolished 1.4.2024). The calculator's basic deductible for a 1200 € wage (219,50 = 0.5 × (1200 − 761)) confirms no deduction is applied.

## 9. Income limits published (derived from the above; useful for sanity checks)

FI-params "Tulorajat" (rounded to nearest euro), e.g. "Espoo, Helsinki, Kauniainen ja Vantaa ... 1 aikuinen, tuloraja on 1 844 e/kk ... 2 aikuista, tuloraja on 2 428 e/kk ... 3 aikuista, tuloraja on 2 944 e/kk"; 24-city group "1 aikuinen, tuloraja on 1 612 e/kk ... 2 aikuista, tuloraja on 2 116 e/kk"; "Muut kunnat ... 1 aikuinen, tuloraja on 1 506 e/kk ... 2 aikuista, tuloraja on 1 960 e/kk".
Check: Helsinki 1 adult: allowance 0 when 0.5(T−761) ≥ 563 → T ≥ 1887; the published 1 844 is the income at which the allowance drops below the 15 € minimum: 0.7(563 − 0.5(T−761)) < 15 ⇒ T > 1843.6. So the published "tulorajat" already include the 15 € minimum rule.

## 10. Published worked examples (FI-params / EN-params)

- "Eino asuu puolisonsa Elisan kanssa Turussa vuokra-asunnossa. Heidän yhteenlasketut tulonsa ovat 1 800 euroa. ... asumismenoja on yhteensä 950 euroa. Turussa kahden aikuisen asumismenoiksi hyväksytään kuitenkin enintään 652 e/kk ... perusomavastuun määrä on 472,50 euroa. ... 0,7 x (652 euroa – 472,50 euroa) = 125,65 euroa."
- "Maija asuu yksin vuokra-asunnossa Helsingissä. Hän maksaa vuokraa 800 e/kk. Yksin asuvan asumismenoiksi voidaan Helsingissä hyväksyä enintään 563 e/kk."
- "Tommi ja Pauliina asuvat kahdestaan vuokra-asunnossa Turussa. He maksavat vuokraa 750 e/kk. ... enintään 652 e/kk."
- "Pia ja Eero asuvat vuokra-asunnossa Porissa. He maksavat vuokraa 650 e/kk. ... enintään 574 e/kk."
- "Pekka ... vakuutussijoitus, jonka arvo on 15 000 euroa ... 83,33 euroa kuukaudessa."

## 11. Differences between the Finnish and English pages

- No numeric differences found: compensation rate, deductible formula and constants, all four max-cost tables, water/heating flat rates, asset thresholds, €2,000 deposit disregard, 12,02 € capital-income threshold, 15 € minimum, income limits and the worked examples are identical.
- Both pages carry the same update date (26.9.2026 / 26/9/2026 for the parameter pages; 12.10.2026 / 12/10/2026 for the main pages).
- Wording only: the EN page says amounts are "rounded up to the nearest euro" where FI says "pyöristetty lähimpään euroon" (rounded to the nearest euro). EN page keeps one Finnish-style decimal comma in "0,7 x (EUR 652 – EUR 472.50)".
- The English calculator UI (https://laskurit.kela.fi/general-housing-allowance-calculator) is the same application; its step 1 still shows one untranslated label "Päivämäärä, josta alkaen asumistuki lasketaan".
- Neither language page gives the per-m² electricity deduction; it comes only via the Etuusohje reference to the Tax Administration's in-kind benefit values (0,86 €/m²/month for 2026).
