import type { LLMAdapter, LLMMessage } from './types';

interface ProductContext {
  name: string;
  category: string;
  make: string;
  model: string;
  yearFrom: number;
  yearTo: number;
  oemCode: string;
  condition: string;
  price: number;
  currency: string;
  description: string;
}

interface ConversationState {
  requestedPart?: string;
  carMake?: string;
  carModel?: string;
  year?: number;
  engine?: string;
  oemCode?: string;
}

/**
 * Enhanced MockLLMAdapter – simulates a professional Lithuanian sales consultant.
 * Features:
 * - Product context awareness (notices when user asks for a different part/car)
 * - State tracking (remembers provided info)
 * - Compatibility logic (checks make/model/year)
 * - Tone control (short, professional, Lithuanian)
 */
export class MockLLMAdapter implements LLMAdapter {
  async chat(messages: LLMMessage[]): Promise<string> {
    // Simulate network latency
    await new Promise((r) => setTimeout(r, 900 + Math.random() * 400));

    const systemMsg = messages.find((m) => m.role === 'system')?.content || '';
    // All non-system messages make up the real conversation
    const conversationMsgs = messages.filter((m) => m.role !== 'system');
    const userMessages = messages.filter((m) => m.role === 'user');
    const lastUserMsg = userMessages[userMessages.length - 1]?.content || '';

    const product = this.parseProductContext(systemMsg);
    // Pass the full conversation (user + assistant) so state extraction
    // can read what has already been discussed
    const state = this.extractConversationState(conversationMsgs);

    // Greeting fires only when there is no prior assistant turn at all
    const hasAssistantTurn = conversationMsgs.some((m) => m.role === 'assistant');

    return this.generateResponse(lastUserMsg, product, state, conversationMsgs, hasAssistantTurn);
  }

  private parseProductContext(systemMsg: string): ProductContext {
    const extract = (label: string) => {
      const match = systemMsg.match(new RegExp(`- ${label}: (.*)`));
      return match ? match[1].trim() : '';
    };

    const makeModelStr = extract('Markė / Modelis');
    const [make, ...rest] = makeModelStr.split(' ');
    const model = rest.join(' ').split('(')[0].trim();
    const yearsMatch = makeModelStr.match(/\((\d{4})–(\d{4})\)/);

    return {
      name: extract('Pavadinimas'),
      category: extract('Kategorija').toLowerCase(),
      make: make || '',
      model: model || '',
      yearFrom: yearsMatch ? parseInt(yearsMatch[1]) : 0,
      yearTo: yearsMatch ? parseInt(yearsMatch[2]) : 0,
      oemCode: extract('OEM kodas'),
      condition: extract('Būklė'),
      price: parseFloat(extract('Kaina')),
      currency: extract('Kaina').split(' ')[1] || 'EUR',
      description: extract('Aprašymas'),
    };
  }

  private extractConversationState(history: LLMMessage[]): ConversationState {
    const state: ConversationState = {};
    // Only look at user messages for state — assistant text can contain car names
    // that shouldn't be treated as the user's car
    const userText = history
      .filter((m) => m.role === 'user')
      .map((m) => m.content.toLowerCase())
      .join(' ');

    // Detect car make mentioned by user
    const makes = ['bmw', 'audi', 'vw', 'volkswagen', 'mercedes', 'toyota', 'ford', 'opel', 'peugeot', 'honda', 'skoda'];
    for (const m of makes) {
      if (userText.includes(m)) {
        state.carMake = m;
        break;
      }
    }

    // Detect common models mentioned by user
    const models = ['e46', 'a4', 'b8', 'golf', 'astra', 'focus', 'w211', 'corolla', '307', 'civic', 'octavia'];
    for (const m of models) {
      if (userText.includes(m)) {
        state.carModel = m;
        break;
      }
    }

    // Detect years
    const yearMatch = userText.match(/\b(19|20)\d{2}\b/g);
    if (yearMatch) state.year = parseInt(yearMatch[yearMatch.length - 1]);

    // Detect OEM code – must be all-caps alphanumeric 8–14 chars (avoid catching common words)
    const oemMatch = userText.match(/\b[A-Z0-9]{8,14}\b/);
    if (oemMatch) state.oemCode = oemMatch[0];

    // Detect engine
    if (/dyzelis|tdi|hdi|cdti|tdci/.test(userText)) state.engine = 'dyzelis';
    if (/benzinas|tsi|tfsi/.test(userText)) state.engine = 'benzinas';

    return state;
  }

  private generateResponse(
    msg: string,
    product: ProductContext,
    state: ConversationState,
    history: LLMMessage[],
    hasAssistantTurn: boolean
  ): string {
    const text = msg.toLowerCase();

    // 1. Initial greeting – only when no assistant has spoken yet
    if (!hasAssistantTurn) {
      return `Sveiki! Čia Rokas iš Srotas.lt. Matau, kad domitės ${product.name}. Kuo galėčiau padėti?`;
    }

    // 2. Intent: Different part detection
    const parts: Record<string, string> = {
      'radiatorius': 'radiatorių',
      'veidrodėlis': 'veidrodėlį',
      'veidrodis': 'veidrodėlį',
      'bamperis': 'bamperį',
      'žibintas': 'žibintą',
      'fara': 'žibintą',
      'stopas': 'galinį žibintą',
      'turbo': 'turbiną',
      'inžektorius': 'purkštuką',
      'purkštukas': 'purkštuką',
      'sparnas': 'sparną',
      'durys': 'duris',
      'dėžė': 'greičių dėžę'
    };
    
    let requestedPartKey = '';
    for (const p of Object.keys(parts)) {
      if (text.includes(p)) {
        requestedPartKey = p;
        break;
      }
    }
    
    if (requestedPartKey && !product.category.toLowerCase().includes(requestedPartKey)) {
      return `Šiuo metu esate ${product.name} puslapyje. Ar kalbame apie šią prekę, ar norite, kad padėčiau surasti ${parts[requestedPartKey]} kitam automobiliui?`;
    }

    // Different make/model detection
    if (state.carMake && state.carMake !== product.make.toLowerCase() && !text.includes(product.make.toLowerCase())) {
      return `Pastebėjau, kad klausiate apie ${state.carMake.toUpperCase()}, tačiau ši dalis skirta ${product.make}. Ar norėtumėte paieškoti dalies kitam automobiliui?`;
    }

    // 3. Intent: Compatibility / uncertainty
    if (/tik|tinka|suderinam|ar ši|ar šitas|ar tiks|ar gali|nezinau|nežinau/.test(text)) {
      // If we have zero car info, ask for everything at once
      if (!state.carMake && !state.carModel && !state.year) {
        return `Supratau. Kad galėčiau įvertinti, ar ši dalis gali tikti, pasakykite automobilio markę, modelį ir metus. Jei žinote – dar kėbulo tipą arba senos detalės OEM kodą.`;
      }
      // Have some info but missing pieces
      if (!state.carMake) {
        return `Kokios markės automobilis? Tai padės patikrinti suderinamumą su ${product.name}.`;
      }
      if (!state.carModel) {
        return `Koks jūsų ${state.carMake.toUpperCase()} modelis?`;
      }
      if (!state.year) {
        return `Kokie pagaminimo metai?`;
      }

      // Have make + model + year – check against product specs
      const yearInRange = state.year >= product.yearFrom && state.year <= product.yearTo;
      const modelMatches =
        product.model.toLowerCase().includes(state.carModel) ||
        state.carModel.includes(product.model.toLowerCase());

      if (yearInRange && modelMatches) {
        // Body type check
        const isBodyPart = /veidrodėlis|žibintas|durys|sparnas|bamperis/.test(product.category.toLowerCase());
        const bodyTypeMismatch = text.includes('kabrio') || text.includes('universal') || text.includes('kupė') || text.includes('coupe');

        if (bodyTypeMismatch && isBodyPart) {
          return `Kadangi jūsų automobilis yra kitokio kėbulo tipo nei nurodyta prekės aprašyme, negaliu garantuoti, kad tiks. Tokios dalys kaip veidrodėliai ar žibintai dažnai skiriasi. Saugiausia būtų sutikrinti OEM kodą arba palikti kontaktą.`;
        }

        return `Pagal metus (${state.year}) ir modelį dalis turėtų tikti, tačiau 100% garantuoti negaliu be OEM kodo. Ar turite senos detalės kodą palyginimui? Galite palikti kontaktą, kad patikrintume tiksliau.`;
      } else {
        return `Ši dalis skirta ${product.make} ${product.model} (${product.yearFrom}–${product.yearTo}). Jūsų automobiliui gali nesutapti. Atsiųskite senos detalės kodą arba palikite kontaktą – patikrinsime.`;
      }
    }


    // 4. Intent: OEM code
    if (text.includes('oem') || text.includes('kodas') || text.includes('numeris')) {
      if (state.oemCode) {
        if (state.oemCode === product.oemCode.toUpperCase()) {
          return `Sutampa! OEM kodas ${state.oemCode} yra identiškas. Ši dalis tikrai tinka jūsų automobiliui. Ar rezervuoti?`;
        } else {
          return `Apgailestauju, jūsų kodas ${state.oemCode} nesutampa su šios detalės kodu ${product.oemCode}. Ši dalis greičiausiai netiks.`;
        }
      }
      return `Originalus kodas šiai detalei yra ${product.oemCode}. Jei ant jūsų senos detalės kodas toks pat – dalis tiks idealiai.`;
    }

    // 5. Intent: Price / Condition / Delivery
    if (text.includes('kaina') || text.includes('eur')) {
      return `Šios detalės kaina yra ${product.price} ${product.currency}. Ar kaina jums tinka?`;
    }
    if (text.includes('bukle') || text.includes('būklė') || text.includes('defektas')) {
      return `Detalės būklė: ${product.condition}. ${product.description.slice(0, 100)}... Ar norėtumėte gauti daugiau nuotraukų?`;
    }
    if (text.includes('siuntimas') || text.includes('pristatymas') || text.includes('kurjeris')) {
      return `Pristatymas visoje Lietuvoje trunka 1-2 darbo dienas. Galime išsiųsti dar šiandien. Ar domina?`;
    }

    // 6. Intent: Lead Generation / Purchase
    if (text.includes('pirkti') || text.includes('uzsakyti') || text.includes('užsakyti') || text.includes('noriu')) {
      return `Puiku! Palikite savo vardą ir telefono numerį – mūsų konsultantas susisieks per 15 minučių ir suderins apmokėjimą bei siuntimą.`;
    }

    // 7. Generic data gathering if unknown
    if (!state.carMake) return `Supratau. Priminkite, kokios markės automobiliui ieškote detalės?`;
    if (!state.carModel) return `Koks jūsų ${state.carMake.toUpperCase()} modelis? Tai padės patikrinti suderinamumą.`;
    if (!state.year) return `Kokie jūsų automobilio pagaminimo metai?`;

    return `Supratau. Ar turite dar klausimų apie šį ${product.name}, ar norėtumėte, kad susisiektume dėl pirkimo?`;
  }

  async chatStream(
    messages: LLMMessage[],
    onChunk: (chunk: string) => void,
    onDone: () => void
  ): Promise<void> {
    const response = await this.chat(messages);
    const words = response.split(' ');
    for (const word of words) {
      await new Promise((r) => setTimeout(r, 40));
      onChunk(word + ' ');
    }
    onDone();
  }
}

/**
 * TEST EXAMPLES:
 * 
 * 1. User asks for radiator while on injector page:
 *    Context: Ford Focus 2 Injector
 *    User: "reiktu radiatoriaus skodai"
 *    Response: "Šiuo metu esate Dešinysis galinio vaizdo veidrodėlis puslapyje. Ar kalbame apie šią prekę, ar norite, kad padėčiau surasti radiatorius kitam automobiliui?"
 * 
 * 2. User asks if Ford injector fits Audi:
 *    Context: Ford Focus 2 Injector
 *    User: "Ar šitas purkštukas tiks Audi A4?"
 *    Response: "Pastebėjau, kad klausiate apie AUDI, tačiau ši dalis skirta Ford. Ar norėtumėte paieškoti dalies kitam automobiliui?"
 * 
 * 3. User asks about OEM code:
 *    User: "koks oem kodas?"
 *    Response: "Originalus kodas šiai detalei yra [OEM]. Jei ant jūsų senos detalės kodas toks pat – dalis tiks idealiai."
 * 
 * 4. User provides car info:
 *    User: "Mano BMW E46 2003m"
 *    Response: "Pagal metus ir modelį dalis turėtų tikti, tačiau 100% garantuoti negaliu. Ar turite senos detalės OEM kodą palyginimui?"
 */

