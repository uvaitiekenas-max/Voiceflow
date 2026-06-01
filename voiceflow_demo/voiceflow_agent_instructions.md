# Voiceflow Agento Konfigūracijos Instrukcija

Šis dokumentas skirtas greitai ir sklandžiai sukonfigūruoti "Voiceflow" agentą jūsų kuriamo produkto demo pilotui. Ši konfigūracija pritaikyta integruoti su "ElevenLabs" balsais bei naudoti paruoštą automobilių duomenų bazę (`cars_database.csv`).

---

## 1. Knowledge Base (Duomenų Bazės) Įkėlimas

1. Prisijunkite prie savo "Voiceflow" paskyros ir atidarykite projektą.
2. Eikite į **Knowledge Base** skiltį (kairiajame meniu).
3. Spauskite **Add Data Source** -> **Upload Document**.
4. Įkelkite šalia esantį `cars_database.csv` failą.
5. Palaukite, kol "Voiceflow" apdoros failą ir pavers jį vektorine duomenų baze.

---

## 2. System Prompt (Sistemos Instrukcija Agentui)

Norint užtikrinti, kad agentas bendrautų profesionaliai, santūriai ir nenaudotų emojijų, nukopijuokite šį tekstą į savo AI agento "System Prompt" (arba "Persona" / "Instructions" nustatymus):

```text
Esate profesionalus, mandagus ir santūrus automobilių pardavimo asistentas. 
Jūsų tikslas – padėti klientams rasti tinkamą automobilį, remiantis jūsų turimais duomenimis (Knowledge Base).

Griežtos taisyklės:
1. Bendraukite TIK lietuvių kalba.
2. Jūsų tonas turi būti dalykinis, ekspertinis ir profesionalus. Nenaudokite šnekamosios kalbos žargonų.
3. GRIEŽTAI DRAUDŽIAMA naudoti bet kokius emoji (šypsenėles, automobilių ikonėles ir pan.). Jūsų atsakymai turi būti tik tekstiniai.
4. Atsakykite trumpai, aiškiai ir tiksliai. Jei klientas prašo išsamesnės informacijos, pateikite ją struktūruotai.
5. Jei klientas teiraujasi apie automobilį, visada paminėkite markę, modelį, metus, ridą, variklį, kainą ir įtraukite esminius punktus iš savininko aprašymo.
6. Jei klientas užduoda klausimą, į kurį atsakymo nėra jūsų duomenų bazėje, atsiprašykite ir profesionaliai paaiškinkite, kad šiuo metu tokios informacijos neturite.
7. Niekada neišgalvokite informacijos apie automobilius – remkitės tik "Knowledge Base" duomenimis.
```

---

## 3. ElevenLabs Integracija (Balsas)

Norint įgalinti "ElevenLabs" balsą jūsų Voiceflow agente:

1. "Voiceflow" projekte atidarykite nustatymus (Settings) arba **Integrations** skiltį.
2. Suraskite "ElevenLabs" integraciją (arba API skambučio bloką).
3. Įveskite savo **ElevenLabs API Key** (jį rasite ElevenLabs paskyros nustatymuose).
4. Pasirinkite balsą (Voice ID). 
   *Rekomendacija: Pasirinkite profesionalų, ramų, žemesnio tembro vyrišką arba moterišką balsą (pavyzdžiui, standartiniai "Antoni" arba "Rachel", jei palaiko kalbą, arba jūsų pačių klonuotas lietuviškas balsas).*
5. Agentui atsakinėjant, konfigūruokite bloką atlikti "Speak" veiksmą naudodami ElevenLabs API, siunčiant sugeneruotą tekstinį atsakymą.

---

## 4. Testavimas

1. Paspauskite **Run** arba **Test** mygtuką Voiceflow platformoje.
2. Išbandykite šias užklausas:
   - "Kokių automobilių turite iki 20000 eurų?"
   - "Papasakokite apie parduodamą BMW 530."
   - "Ar turite hibridinių automobilių su mažesne nei 100 tūkst. rida?"
3. Įsitikinkite, kad agentas atsako be jokių emojijų ir kalba santūriu tonu.
