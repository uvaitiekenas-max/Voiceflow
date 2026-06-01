# ElevenLabs Conversational AI Agento Sąranka

Šis dokumentas paaiškina, kaip sukurti balso agentą "ElevenLabs" platformoje, įkelti automobilių duomenis ir integruoti jį į sukurtą demonstracinį web puslapį.

## 1. Agento Sukūrimas
1. Prisijunkite prie savo **ElevenLabs** paskyros.
2. Meniu kairėje pasirinkite **Conversational AI** (gali būti pavadinta "Agents" ar "Voice Agents").
3. Spauskite **Create Agent** (Sukurti agentą).
4. Suteikite jam pavadinimą, pvz., "Premium Auto Pardavėjas".
5. Pasirinkite tinkamą, profesionalų balsą (lietuvišką klonuotą balsą arba vieną iš standartinių, kurie gerai kalba lietuviškai).

## 2. Sistemos Instrukcija (System Prompt)
Agento nustatymuose raskite laukelį **System Prompt** (arba "Persona/Instructions") ir įklijuokite šį tekstą:

```text
Tu esi profesionalus, mandagus ir santūrus "Premium Auto" automobilių pardavimo asistentas.
Klientas tau skambina norėdamas pasiteirauti apie parduodamą automobilį.

Griežtos taisyklės:
1. Bendrauk TIK lietuvių kalba.
2. Tavo tonas turi būti dalykinis, ekspertinis ir profesionalus. Nenaudok šnekamosios kalbos žargonų.
3. Klientas dažniausiai paskambins dėl konkretaus automobilio (pvz., "Skambinu dėl BMW 530"). Iškart surask informaciją apie šį automobilį savo žinių bazėje (Knowledge Base) ir paklausk, kas konkrečiai jį domina.
4. Jei klientas klausia detalių, pateik jas aiškiai, remdamasis savininko aprašymu ir techniniais parametrais.
5. Niekada neišgalvok informacijos. Jei atsakymo nėra žinių bazėje, atsiprašyk ir pasakyk, kad šios informacijos šiuo metu neturi.
6. Neatsisveikink pirmas, leisk klientui baigti pokalbį.
```

## 3. Duomenų Bazės (Knowledge Base) Įkėlimas
Kad agentas žinotų apie jūsų automobilius:
1. Agento nustatymuose eikite į skiltį **Knowledge Base** (Žinių bazė).
2. Įkelkite failą `cars_database.csv`, kurį rasite šiame aplanke.
3. Palaukite, kol sistema apdoros duomenis. Dabar agentas gali skaityti visų 10 automobilių aprašymus.

## 4. Agento ID Integracija į Svetainę
Kad svetainėje veiktų skambučio mygtukas ir sujungtų su jūsų agentu:
1. ElevenLabs platformoje atidarykite savo agento nustatymus ir suraskite jo **Agent ID** (dažniausiai tai ilgas raidžių/skaičių kodas). Jį galite rasti "Embed", "Integration" arba "API" skiltyse.
2. Atsidarykite sukurtą `index.html` failą naudodami kodo redaktorių (pvz., VS Code ar Notepad).
3. Suraskite šią eilutę (apie 47 eilutę):
   `<elevenlabs-convai agent-id="JŪSŲ_ELEVENLABS_AGENT_ID"></elevenlabs-convai>`
4. Pakeiskite `JŪSŲ_ELEVENLABS_AGENT_ID` į tikrąjį savo kodą.
5. Išsaugokite `index.html` failą.

## 5. Išbandymas
- Naršyklėje atidarykite `index.html`.
- Prie bet kurio automobilio paspauskite **Skambinti**.
- Atsidariusiame lange paspauskite mikrofono ikonėlę ElevenLabs valdiklyje.
- Suteikite naršyklei leidimą naudoti mikrofoną.
- Pradėkite kalbėti! Pavyzdžiui: *"Sveiki, skambinu dėl BMW 530. Kokia jo rida ir būklė?"*
