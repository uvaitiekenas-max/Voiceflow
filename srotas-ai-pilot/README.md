## 🚀 Quick Start

```bash
cd srotas-ai-pilot
npm install

# Copy env template and configure
cp .env.example .env.local

npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

---

## ⚙️ Environment Configuration

Copy `.env.example` → `.env.local` and set your values:

```bash
# Use mock AI (no API key needed) – default
LLM_PROVIDER=mock

# Use real OpenAI GPT
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini       # or gpt-4o for higher quality
OPENAI_MAX_TOKENS=300
OPENAI_TEMPERATURE=0.3
```

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `mock` | `mock` or `openai` |
| `OPENAI_API_KEY` | – | Required when `LLM_PROVIDER=openai` |
| `OPENAI_MODEL` | `gpt-4o-mini` | Any OpenAI chat model |
| `OPENAI_MAX_TOKENS` | `300` | Max tokens per reply (keep low for phone-style answers) |
| `VOICE_MODE` | `browser` | `browser` (WebSpeech) or `provider` (Deepgram/ElevenLabs) |
| `DEEPGRAM_API_KEY` | – | Required for `VOICE_MODE=provider` |
| `ELEVENLABS_API_KEY` | – | Required for `VOICE_MODE=provider` |
| `ELEVENLABS_VOICE_ID` | `EXAVITQu4vr4xnSDxMaL` | Your ElevenLabs voice ID |

---

## 🎙️ Professional Voice Setup

To enable professional STT and TTS (instead of browser defaults):

1. **Get Deepgram API Key**:
   - Go to [Deepgram](https://console.deepgram.com/)
   - Create a project and an API Key
   - Set `DEEPGRAM_API_KEY` in `.env.local`

2. **Get ElevenLabs API Key**:
   - Go to [ElevenLabs](https://elevenlabs.io/)
   - Copy your API Key from Profile Settings
   - Choose a voice and copy its **Voice ID**
   - Set `ELEVENLABS_API_KEY` and `ELEVENLABS_VOICE_ID` in `.env.local`

3. **Enable Provider Mode**:
   - Set `VOICE_MODE=provider` in `.env.local`
   - Restart the dev server

The system will now use **Deepgram** for high-accuracy Lithuanian transcription and **ElevenLabs** for natural-sounding Lithuanian speech.
| `OPENAI_TEMPERATURE` | `0.3` | 0 = deterministic, 1 = creative |

> **Fallback safety**: If `LLM_PROVIDER=openai` but `OPENAI_API_KEY` is missing or the adapter fails to init, the server automatically falls back to `MockLLMAdapter` and logs a warning.

---

## 🏗️ Project Structure

```
srotas-ai-pilot/
├── .env.example                        # Template – safe to commit
├── .env.local                          # Your secrets – gitignored
├── src/
│   ├── app/
│   │   ├── page.tsx                    # Homepage – product catalog
│   │   ├── layout.tsx
│   │   ├── globals.css                 # Full design system (dark theme)
│   │   ├── products/[slug]/
│   │   │   ├── page.tsx                # Product detail (server)
│   │   │   └── ProductDetailClient.tsx # Product detail (client, modal trigger)
│   │   ├── admin/
│   │   │   └── page.tsx                # Admin: provider status + conversations + leads
│   │   └── api/
│   │       ├── chat/route.ts           # POST /api/chat  ← uses getLLMAdapter()
│   │       ├── config/route.ts         # GET  /api/config (safe provider info)
│   │       ├── leads/route.ts          # GET/POST /api/leads
│   │       └── conversations/route.ts  # GET/POST /api/conversations
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── ProductCard.tsx
│   │   └── AICallModal.tsx             # Full call UX + system prompt builder
│   ├── data/
│   │   └── products.json               # 10 mock car parts
│   ├── lib/
│   │   ├── config.ts                   # Central env-var config (LLM_PROVIDER etc.)
│   │   ├── adapters/
│   │   │   ├── types.ts                # STTAdapter, LLMAdapter, TTSAdapter interfaces
│   │   │   ├── factory.ts              # getLLMAdapter() – picks provider from config
│   │   │   ├── MockLLMAdapter.ts       # Built-in Lithuanian sales simulator
│   │   │   ├── OpenAILLMAdapter.ts     # ✅ OpenAI GPT (gpt-4o-mini / gpt-4o)
│   │   │   ├── MockSTTAdapter.ts       # → replace with DeepgramSTTAdapter
│   │   │   └── MockTTSAdapter.ts       # → replace with ElevenLabsTTSAdapter
│   │   └── store.ts                    # In-memory leads + conversation logs
│   └── types/
│       └── product.ts
└── README.md
```

---

## 🤖 Adapter Architecture

All AI integrations are behind clean interfaces. To connect real APIs, create a new class implementing the interface and swap the import in the relevant file.

### STTAdapter (`src/lib/adapters/types.ts`)
```typescript
interface STTAdapter {
  startListening(onTranscript: (text: string, isFinal: boolean) => void): Promise<() => void>;
  stopListening(): Promise<void>;
  isListening(): boolean;
}
```
**Current**: `MockSTTAdapter` (text input fallback)  
**Next step**: `DeepgramSTTAdapter` or `WebSpeechSTTAdapter`

### LLMAdapter
```typescript
interface LLMAdapter {
  chat(messages: LLMMessage[]): Promise<string>;
  chatStream?(messages, onChunk, onDone): Promise<void>;
}
```
**Current**: `MockLLMAdapter` (pre-scripted Lithuanian responses)  
**Next step**: `OpenAILLMAdapter` (GPT-4o with system prompt in Lithuanian)

### TTSAdapter
```typescript
interface TTSAdapter {
  speak(text: string): Promise<void>;
  stop(): void;
  isSpeaking(): boolean;
}
```
**Current**: `MockTTSAdapter` (browser Web Speech API, Lithuanian)  
**Next step**: `ElevenLabsTTSAdapter` (realistic Lithuanian voice)

---

## 📦 Mock Data

10 used car parts in `src/data/products.json`:

| ID | Part | Make | Model |
|----|------|------|-------|
| PRD-001 | Dešinysis veidrodėlis | BMW | E46 |
| PRD-002 | Kairysis žibintas | Audi | A4 B8 |
| PRD-003 | Priekinis bamperis | Volkswagen | Golf VI |
| PRD-004 | Turbokompresoriius | Opel | Astra H |
| PRD-005 | Dyzelio inžektorius | Ford | Focus MK2 |
| PRD-006 | Kairysis sparnas | Mercedes-Benz | W211 |
| PRD-007 | Dešiniosios galinės durys | Toyota | Corolla E12 |
| PRD-008 | Mechaninė greičių dėžė | Peugeot | 307 |
| PRD-009 | Kairysis galinis žibintas | Honda | Civic MK8 |
| PRD-010 | Aušinimo radiatorius | Škoda | Octavia II |

---

## 🛣️ Pages

| Route | Description |
|-------|-------------|
| `/` | Product catalog grid |
| `/products/[slug]` | Product detail + AI call button |
| `/admin` | Conversations + lead log dashboard |

---

## 🔌 API Routes

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | Send conversation to LLM adapter |
| `/api/leads` | GET / POST | Retrieve / save lead |
| `/api/conversations` | GET / POST | Retrieve / save conversation log |

---

## 🔮 Roadmap – Connecting Real APIs

### Phase 1: Real LLM (OpenAI GPT-4o)
```bash
npm install openai
```
Create `src/lib/adapters/OpenAILLMAdapter.ts`, implement `LLMAdapter`, swap import in `/api/chat/route.ts`.

### Phase 2: Real TTS (ElevenLabs)
```bash
npm install elevenlabs
```
Create `ElevenLabsTTSAdapter.ts`, swap in `AICallModal.tsx`.

### Phase 3: Real STT (Deepgram)
```bash
npm install @deepgram/sdk
```
Create `DeepgramSTTAdapter.ts`, swap in `AICallModal.tsx`.

### Phase 4: Real-time voice (Twilio / WebRTC)
Use Twilio Media Streams or WebRTC to replace the text input fallback with actual microphone audio.

---

## 🧪 AI Consultant Behaviour

The mock AI (Rokas) follows these rules:
- ✅ Always responds in **Lithuanian**
- ✅ Collects: make, model, year, engine, body type, OEM code
- ✅ **Never guarantees compatibility** without full OEM/fitment data
- ✅ Guides user toward purchase or leaving contact details
- ✅ Short, professional, friendly responses (1–4 sentences)

---

## 📋 Requirements

- Node.js 18+
- npm 9+

No external API keys required for mock mode.

---

## 🏢 About

Built as a pilot demo for the **Srotas** used car parts platform. All data is mocked; no real purchases, payments, or API calls are made.
