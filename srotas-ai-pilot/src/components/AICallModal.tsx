'use client';

import { useState, useRef, useEffect, useCallback } from 'react';
import { useConversation } from '@elevenlabs/react';
import type { Product } from '@/types/product';
import type { LLMMessage } from '@/lib/adapters/types';

// ---- Types ----
type CallStatus = 'idle' | 'active' | 'thinking' | 'speaking' | 'ended';

interface TranscriptMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  source: 'text' | 'voice';
  sttProvider?: string;
  ttsProvider?: string;
  sttConfidence?: number;
  error?: string;
}

interface LeadForm {
  name: string;
  phone: string;
  carInfo: string;
  notes: string;
}

interface Props {
  product: Product;
  onClose: () => void;
}

const STATUS_LABELS: Record<CallStatus, string> = {
  idle: 'Nepradėta',
  active: 'Pokalbis aktyvus',
  thinking: 'AI mąsto...',
  speaking: 'AI kalba...',
  ended: 'Pokalbis baigtas',
};

const CATEGORY_EMOJI: Record<string, string> = {
  Veidrodėlis: '🪞',
  Žibintas: '💡',
  Bamperis: '🚗',
  Turbo: '⚡',
  Inžektorius: '⛽',
  Sparnas: '🛡️',
  Durys: '🚪',
  'Greičių dėžė': '⚙️',
  'Galinis žibintas': '🔴',
  Radiatorius: '🌡️',
};

export default function AICallModal({ product, onClose }: Props) {
  const [status, setStatus] = useState<CallStatus>('idle');
  const [messages, setMessages] = useState<TranscriptMessage[]>([]);
  const [userInput, setUserInput] = useState('');
  const [showLeadForm, setShowLeadForm] = useState(false);
  const [leadForm, setLeadForm] = useState<LeadForm>({ name: '', phone: '', carInfo: '', notes: '' });
  const [leadSubmitted, setLeadSubmitted] = useState(false);
  const [startTime, setStartTime] = useState<Date | null>(null);
  const transcriptRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const conversationHistory = useRef<LLMMessage[]>([]);
  
  // Voice states
  const [isRecording, setIsRecording] = useState(false);
  const [voiceEnabled, setVoiceEnabled] = useState(true); // Default to true for voice demo
  const [recognitionSupport, setRecognitionSupport] = useState(false);
  const [voiceMode, setVoiceMode] = useState<'browser' | 'provider'>('browser');
  const [voiceStatus, setVoiceStatus] = useState<string>('');
  const [isProcessingVoice, setIsProcessingVoice] = useState(false);
  const [isContinuous, setIsContinuous] = useState(true);
  const [twilioNumber, setTwilioNumber] = useState('');
  
  const addMessage = useCallback((role: 'user' | 'assistant', content: string, source: 'text' | 'voice' = 'text', metadata?: Partial<TranscriptMessage>) => {
    setMessages((prev) => [...prev, { role, content, timestamp: new Date(), source, ...metadata }]);
    conversationHistory.current.push({ role, content });
  }, []);

  // ElevenLabs Agent Integration
  const conversation = useConversation({
    onConnect: useCallback(() => {
      setVoiceStatus('Agentas prisijungė');
      setIsRecording(true);
    }, []),
    onDisconnect: useCallback(() => {
      setVoiceStatus('Agentas atsijungė');
      setIsRecording(false);
    }, []),
    onMessage: useCallback((message: any) => {
      // Clean non-verbal metadata (e.g., [warmly], (English translations), etc.)
      const cleanContent = (text: string) => {
        return text
          .replace(/\[.*?\]/g, '') // Remove [tags]
          .replace(/\(.*?\)/g, '') // Remove (parentheses) - often used for translations
          .replace(/\s+/g, ' ')    // Normalize whitespace
          .trim();
      };

      const text = cleanContent(message.message);
      if (!text) return;

      // Sync messages to our UI
      if (message.source === 'user') {
        addMessage('user', text, 'voice');
      } else {
        addMessage('assistant', text, 'voice', {
          ttsProvider: 'eleven-agent'
        });
      }
    }, [addMessage]),
    onError: useCallback((error: any) => {
      console.error('[ElevenLabs Agent] Error:', error);
      setVoiceStatus('Agento klaida');
    }, [])
  });

  const recognitionRef = useRef<any>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  // Fetch config
  useEffect(() => {
    fetch('/api/config')
      .then((res) => res.json())
      .then((data) => {
        if (data.voice) {
          setVoiceMode(data.voice.mode || 'browser');
          if (data.voice.twilioPhoneNumber) {
            setTwilioNumber(data.voice.twilioPhoneNumber);
          }
        }
      });
  }, []);

  // Scroll transcript to bottom
  useEffect(() => {
    if (transcriptRef.current) {
      transcriptRef.current.scrollTop = transcriptRef.current.scrollHeight;
    }
  }, [messages]);

  const speak = useCallback((text: string) => {
    if (!voiceEnabled || !window.speechSynthesis) return;
    // Don't use manual TTS if we are in a live Agent session
    if (conversation.status === 'connected') return;

    if (voiceMode === 'provider') {
      providerSpeak(text);
      return;
    }
    
    // Stop current speech
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'lt-LT';
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    // Browser voices are loaded asynchronously
    const voices = window.speechSynthesis.getVoices();
    const ltVoice = voices.find(v => v.lang.includes('lt-LT') || v.lang.includes('lt_LT') || v.lang === 'lt');
    
    if (ltVoice) {
      utterance.voice = ltVoice;
    }

    window.speechSynthesis.speak(utterance);
  }, [voiceEnabled, voiceMode]);

  const providerSpeak = useCallback(async (text: string) => {
    if (!voiceEnabled) return;
    setVoiceStatus('Generuojamas balsas...');
    
    try {
      const res = await fetch('/api/voice/tts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      if (!res.ok) throw new Error('TTS failed');

      const audioBlob = await res.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      
      if (audioRef.current) {
        audioRef.current.src = audioUrl;
        audioRef.current.onplay = () => setVoiceStatus('AI atsako balsu');
        audioRef.current.onended = () => setVoiceStatus('');
        audioRef.current.play();
      }
    } catch (err) {
      console.error('[TTS] Error:', err);
      setVoiceStatus('TTS Klaida');
    }
  }, [voiceEnabled]);

  const sendToAI = useCallback(
    async (userText: string, source: 'text' | 'voice' = 'text', voiceMetadata?: any) => {
      if (!userText.trim()) return;

      addMessage('user', userText, source, {
        sttProvider: voiceMetadata?.provider,
        sttConfidence: voiceMetadata?.confidence,
      });
      
      setStatus('thinking');
      setVoiceStatus('AI galvoja...');

      try {
        const apiMessages: LLMMessage[] = [
          { role: 'system', content: buildSystemPrompt(product) },
          ...conversationHistory.current,
        ];

        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ messages: apiMessages }),
        });

        const data = await res.json();
        const aiText: string = data.response || 'Atsiprašau, įvyko klaida.';

        setStatus('speaking');
        addMessage('assistant', aiText, 'text', {
          ttsProvider: voiceMode === 'provider' ? 'elevenlabs' : 'browser'
        });
        speak(aiText);

        // Short speaking animation delay (not proportional to text length)
        await new Promise((r) => setTimeout(r, 600));
        setStatus('active');

        // Auto-suggest lead form after 4+ turns
        const turnCount = conversationHistory.current.filter((m) => m.role === 'user').length;
        if (turnCount >= 3 && !leadSubmitted && !showLeadForm) {
          const contactKeywords = /kontakt|skambin|pirkti|užsakyti|palikti/i;
          if (contactKeywords.test(aiText)) {
            setShowLeadForm(true);
          }
        }
      } catch {
        addMessage('assistant', 'Atsiprašau, įvyko techninė klaida. Bandykite dar kartą.');
        setStatus('active');
      }
    },
    [addMessage, product, leadSubmitted, showLeadForm, voiceMode, speak]
  );

  const unlockAudio = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.play().catch(() => {});
      audioRef.current.pause();
    }
  }, []);

  const handleStart = useCallback(async () => {
    unlockAudio();
    
    if (voiceMode === 'provider') {
      // For Agent mode, we start the session instead of calling Gemini greeting
      startRecording();
      setStartTime(new Date());
      setStatus('active');
      return;
    }

    setStatus('thinking');
    setStartTime(new Date());
    // Start with a clean slate
    conversationHistory.current = [];

    try {
      // Seed history with the user greeting so the LLM responds to it
      addMessage('user', 'Sveiki');
      
      const greetingMessages: LLMMessage[] = [
        { role: 'system', content: buildSystemPrompt(product) },
        { role: 'user', content: 'Sveiki' },
      ];

      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: greetingMessages }),
      });
      const data = await res.json();
      const greeting = data.response || 'Sveiki! Čia Rokas iš Srotas.lt. Matau, kad domitės šia detale. Kuo galiu padėti?';

      // The response from AI is the assistant message
      addMessage('assistant', greeting, 'text', {
        ttsProvider: voiceMode === 'provider' ? 'elevenlabs' : 'browser'
      });
      speak(greeting);

      setStatus('speaking');
      // Short fixed delay – just enough for the animation to be visible
      await new Promise((r) => setTimeout(r, 600));
      setStatus('active');
    } catch {
      addMessage('assistant', 'Labas! Kuo galiu padėti su šia detale?', 'text');
      setStatus('active');
    }

    inputRef.current?.focus();
  }, [addMessage, product, voiceMode, speak, unlockAudio]);

  const handleSend = useCallback(() => {
    if (!userInput.trim() || status === 'thinking' || status === 'speaking') return;
    unlockAudio();
    const text = userInput.trim();
    setUserInput('');
    sendToAI(text);
  }, [userInput, status, sendToAI]);

  const handleEnd = useCallback(async () => {
    // End the ElevenLabs session if active
    if (conversation.status === 'connected') {
      await conversation.endSession();
    }
    
    setStatus('ended');
    const endTime = new Date();

    // Save conversation log
    try {
      await fetch('/api/conversations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          productId: product.id,
          productName: product.name,
          turns: messages.map(m => ({
            role: m.role,
            content: m.content,
            timestamp: m.timestamp.toISOString(),
            source: m.source,
            sttProvider: m.sttProvider,
            ttsProvider: m.ttsProvider,
            sttConfidence: m.sttConfidence,
            error: m.error
          })),
          leadCaptured: leadSubmitted,
          startedAt: startTime?.toISOString(),
          endedAt: endTime.toISOString(),
        }),
      });
    } catch {
      console.error('Failed to save conversation log');
    }
  }, [product, leadSubmitted, startTime]);

  const handleLeadSubmit = useCallback(async () => {
    if (!leadForm.name || !leadForm.phone) return;

    try {
      await fetch('/api/leads', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...leadForm,
          productId: product.id,
        }),
      });
      setLeadSubmitted(true);
      setShowLeadForm(false);
      addMessage('assistant', `Ačiū, ${leadForm.name}! Jūsų kontaktai išsaugoti. Susisieksime su jumis artimiausiu metu! 🎉`);
    } catch {
      console.error('Lead save failed');
    }
  }, [leadForm, product.id, addMessage]);

  // Initialize Speech Recognition (only for browser mode)
  useEffect(() => {
    if (voiceMode !== 'browser') return;

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      setRecognitionSupport(true);
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'lt-LT';

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        if (transcript) {
          sendToAI(transcript, 'voice');
        }
        setIsRecording(false);
      };

      recognition.onerror = () => setIsRecording(false);
      recognition.onend = () => setIsRecording(false);

      recognitionRef.current = recognition;
    }

    if (window.speechSynthesis) {
      window.speechSynthesis.getVoices();
    }
  }, [voiceMode, sendToAI]);

  // Cleanup on unmount - use a ref to avoid re-triggering on every render
  const convRef = useRef(conversation);
  useEffect(() => {
    convRef.current = conversation;
  }, [conversation]);

  useEffect(() => {
    return () => {
      if (convRef.current.status === 'connected') {
        convRef.current.endSession();
      }
      window.speechSynthesis.cancel();
    };
  }, []); // Empty array = only on unmount

  const startRecording = useCallback(async () => {
    unlockAudio();

    if (voiceMode === 'provider') {
      if (conversation.status === 'connected' || conversation.status === 'connecting') return;
      
      try {
        const tokenRes = await fetch('/api/voice/agent-token', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            productInfo: `${product.name} (${product.category}, ${product.price}€). OEM: ${product.oem || 'nėra'}.`
          })
        });
        const { signedUrl } = await tokenRes.json();
        
        if (!signedUrl) throw new Error('No signed URL');

        await conversation.startSession({ signedUrl });
      } catch (err) {
        console.error('[Agent] Init error:', err);
        setVoiceStatus('Nepavyko paleisti agento');
      }
      return;
    }

    if (recognitionRef.current && !isRecording) {
      window.speechSynthesis.cancel();
      recognitionRef.current.start();
      setIsRecording(true);
      setVoiceEnabled(true);
    }
  }, [isRecording, voiceMode, conversation, unlockAudio]);

  const stopRecording = useCallback(async () => {
    if (conversation.status === 'connected') {
      await conversation.endSession();
      return;
    }

    if (recognitionRef.current && isRecording) {
      recognitionRef.current.stop();
      setIsRecording(false);
    }
  }, [isRecording, conversation]);

  const processAudio = async (blob: Blob) => {
    setIsProcessingVoice(true);
    try {
      const formData = new FormData();
      formData.append('audio', blob, 'query.webm');

      const res = await fetch('/api/voice/stt', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) throw new Error('STT failed');

      const data = await res.json();
      if (data.transcript) {
        setVoiceStatus('Kalba atpažinta');
        sendToAI(data.transcript, 'voice', data);
      } else {
        setVoiceStatus('Nepavyko atpažinti kalbos');
      }
    } catch (err) {
      console.error('[processAudio] Error:', err);
      setVoiceStatus('Klaida atpažįstant kalbą');
    } finally {
      setIsProcessingVoice(false);
    }
  };

  const emoji = CATEGORY_EMOJI[product.category] || '🔧';

  return (
    <div className="modal-overlay" onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div className="modal" role="dialog" aria-modal="true" aria-label="AI Konsultantas">
        {/* Header */}
        <div className="modal-header">
          <div className="flex items-center gap-2">
            <span style={{ fontSize: '1.4rem' }}>{emoji}</span>
            <div>
              <div className="modal-title">AI Konsultantas – Rokas</div>
              <div className="text-small text-muted">{product.name}</div>
            </div>
          </div>
          <button className="modal-close" onClick={onClose} aria-label="Uždaryti">
            ✕
          </button>
        </div>

        {/* Status bar */}
        <div className="call-status-bar">
          <div className={`status-dot ${status}`} />
          <span style={{ color: statusColor(status) }}>{STATUS_LABELS[status]}</span>
          {status !== 'idle' && status !== 'ended' && startTime && (
            <div className="flex items-center gap-2" style={{ marginLeft: 'auto' }}>
              {isRecording && <div className="recording-pulse" />}
              {voiceStatus && <span className="text-small" style={{ color: 'var(--color-accent)' }}>{voiceStatus}</span>}
              <CallTimer startTime={startTime} />
            </div>
          )}
        </div>
        
        <audio ref={audioRef} style={{ display: 'none' }} />

        {/* Transcript */}
        <div className="transcript-area" ref={transcriptRef}>
          {messages.length === 0 ? (
            <div className="transcript-empty">
              <div className="transcript-empty-icon">🎙️</div>
              <p>Paspauskite „Pradėti pokalbį" norėdami kalbėti su AI konsultantu</p>
              <p className="text-small">Rokas padės rasti tinkamą detalę ir atsakys į klausimus</p>
            </div>
          ) : (
            messages.map((msg, i) => (
              <div key={i} className={`message-bubble ${msg.role}`}>
                <div className={`message-avatar ${msg.role === 'assistant' ? 'ai' : 'user'}`}>
                  {msg.role === 'assistant' ? '🤖' : '👤'}
                </div>
                <div className="message-content">{msg.content}</div>
              </div>
            ))
          )}
          {status === 'thinking' && (
            <div className="message-bubble">
              <div className="message-avatar ai">🤖</div>
              <div className="message-content typing">
                <div className="typing-dot" />
                <div className="typing-dot" />
                <div className="typing-dot" />
              </div>
            </div>
          )}
        </div>

        {/* Input area */}
        <div className="modal-input-area">
          {/* Lead capture panel */}
          {showLeadForm && !leadSubmitted && (
            <div className="lead-panel mb-3">
              <div className="lead-panel-title">📞 Palikite kontaktus – susisieksime!</div>
              <div className="lead-form-grid">
                <div className="form-group">
                  <label className="form-label">Vardas</label>
                  <input
                    className="form-input"
                    placeholder="Jūsų vardas"
                    value={leadForm.name}
                    onChange={(e) => setLeadForm((f) => ({ ...f, name: e.target.value }))}
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Telefonas</label>
                  <input
                    className="form-input"
                    placeholder="+370 ..."
                    value={leadForm.phone}
                    onChange={(e) => setLeadForm((f) => ({ ...f, phone: e.target.value }))}
                  />
                </div>
              </div>
              <div className="form-group mb-2">
                <label className="form-label">Automobilis</label>
                <input
                  className="form-input"
                  placeholder="pvz. BMW E46 2003, 2.0d"
                  value={leadForm.carInfo}
                  onChange={(e) => setLeadForm((f) => ({ ...f, carInfo: e.target.value }))}
                />
              </div>
              <div className="form-group mb-3">
                <label className="form-label">Pastabos</label>
                <input
                  className="form-input"
                  placeholder="Papildomos pastabos..."
                  value={leadForm.notes}
                  onChange={(e) => setLeadForm((f) => ({ ...f, notes: e.target.value }))}
                />
              </div>
              <div className="flex gap-2">
                <button
                  className="btn btn-primary btn-sm"
                  onClick={handleLeadSubmit}
                  disabled={!leadForm.name || !leadForm.phone}
                >
                  ✉️ Išsiųsti
                </button>
                <button
                  className="btn btn-ghost btn-sm"
                  onClick={() => setShowLeadForm(false)}
                >
                  Vėliau
                </button>
              </div>
            </div>
          )}

          {/* Message input */}
          {status !== 'ended' && (
            <div className="modal-input-row">
              <input
                ref={inputRef}
                className="form-input"
                placeholder={
                  status === 'idle'
                    ? 'Pirmiausia pradėkite pokalbį...'
                    : status === 'thinking' || status === 'speaking'
                    ? 'AI atsako...'
                    : 'Įveskite žinutę...'
                }
                value={userInput}
                disabled={status === 'idle' || status === 'thinking' || status === 'speaking'}
                onChange={(e) => setUserInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              />
              <button
                className="btn btn-primary"
                onClick={handleSend}
                disabled={status === 'idle' || status === 'thinking' || status === 'speaking' || !userInput.trim()}
              >
                ➤
              </button>
              {recognitionSupport ? (
                <button
                  className={`btn ${isRecording ? 'btn-danger' : 'btn-ghost'}`}
                  onClick={isRecording ? stopRecording : startRecording}
                  disabled={status === 'idle' || status === 'thinking' || status === 'speaking'}
                  title={isRecording ? 'Stabdyti įrašymą' : 'Kalbėti balsu'}
                >
                  {isRecording ? '🛑' : '🎤'}
                </button>
              ) : (
                <button
                  className="btn btn-ghost"
                  disabled
                  title="Ši naršyklė nepalaiko balso atpažinimo. Kol kas naudokite tekstinį režimą."
                >
                  🚫🎤
                </button>
              )}
            </div>
          )}

          {/* Voice Output Toggle */}
          {status !== 'ended' && status !== 'idle' && (
            <div className="flex items-center gap-2 mb-3 px-1">
              <input
                type="checkbox"
                id="toggle-voice"
                checked={voiceEnabled}
                onChange={(e) => setVoiceEnabled(e.target.checked)}
                style={{ cursor: 'pointer' }}
              />
              <label htmlFor="toggle-voice" className="text-small text-muted" style={{ cursor: 'pointer' }}>
                Skaityti atsakymus balsu
              </label>
            </div>
          )}

          {/* Action buttons */}
          <div className="modal-actions">
            {status === 'idle' && (
              <button id="btn-start-call" className="btn btn-primary" style={{ flex: 1 }} onClick={handleStart}>
                🎙️ Pradėti pokalbį
              </button>
            )}
            {status !== 'idle' && status !== 'ended' && (
              <>
                {!showLeadForm && !leadSubmitted && (
                  <button className="btn btn-ghost btn-sm" onClick={() => setShowLeadForm(true)}>
                    📞 Palikti kontaktus
                  </button>
                )}
                {isRecording ? (
                  <button className="btn btn-danger btn-sm" onClick={stopRecording}>
                    📵 Baigti skambutį
                  </button>
                ) : (
                  <div className="flex gap-2" style={{ flex: 1 }}>
                    <button className="btn btn-primary btn-sm" style={{ flex: 1 }} onClick={startRecording} disabled={status === 'thinking' || status === 'speaking' || isProcessingVoice}>
                      🎙️ Kalbėti naršyklėje
                    </button>
                    {twilioNumber && (
                      <a href={`tel:${twilioNumber}`} className="btn btn-ghost btn-sm" style={{ border: '1px solid var(--color-border)' }}>
                        📞 Skambinti telefonu
                      </a>
                    )}
                  </div>
                )}
                {voiceMode === 'provider' && messages.length > 0 && messages[messages.length - 1].role === 'assistant' && (
                  <button className="btn btn-ghost btn-sm" onClick={() => speak(messages[messages.length - 1].content)}>
                    🔊 Pakartoti
                  </button>
                )}
                <button className="btn btn-danger btn-sm" style={{ marginLeft: 'auto' }} onClick={handleEnd}>
                  ❌ Uždaryti
                </button>
              </>
            )}
            {status === 'ended' && (
              <div style={{ display: 'flex', gap: 8, width: '100%' }}>
                <button className="btn btn-ghost" style={{ flex: 1 }} onClick={onClose}>
                  Uždaryti
                </button>
                {!leadSubmitted && (
                  <button className="btn btn-primary" style={{ flex: 1 }} onClick={() => setShowLeadForm(true)}>
                    📞 Palikti kontaktus
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// ---- Helpers ----

function buildSystemPrompt(product: Product): string {
  return `Tu esi profesionalus naudotų automobilių dalių pardavimo konsultantas vardu Rokas.
Dirbi "Srotas.lt" platformoje – didžiausiame Lietuvos auto dalių portale.

ŠIUO METU APTARIAMA DETALĖ (Tavo prekė):
- Pavadinimas: ${product.name}
- Kategorija: ${product.category}
- Markė / Modelis: ${product.make} ${product.model} (${product.yearFrom}–${product.yearTo})
- OEM kodas: ${product.oemCode}
- Būklė: ${product.condition}
- Kaina: ${product.price} ${product.currency}
- Sandėlyje: ${product.stock} vnt.
- Aprašymas: ${product.description}

TAVO BAZINĖS TAISYKLĖS:
1. PASISVEIKINIMAS: Visada pasisveikink pilnu sakiniu. Pvz.: "Sveiki! Čia Rokas iš Srotas.lt. Matau, kad domitės ${product.name}. Kuo galiu padėti?"
2. SUDERINAMUMAS: Klausk markės, modelio, metų, variklio ir kėbulo tipo.
3. OEM SAUGA (GRIEŽTA): 
   - NIEKADA nesakyk "OEM kodai nesutampa", nebent vartotojas nurodė savo detalės kodą ir jis skiriasi nuo prekės kodo (${product.oemCode}).
   - Jei vartotojas nepateikė kodo, klausk: "Gal turite senos detalės OEM kodą?"
4. KĖBULO TIPAS: Jei tavo prekė skirta sedanui, o vartotojas turi kabrioletą/universalą/kupė – sakyk, kad suderinamumas neaiškus. Paaiškink: "Veidrodėliai, žibintai, durys ir kėbulo dalys dažnai skiriasi pagal kėbulo tipą."
5. JOKIŲ GARANTIJŲ: Negarantuok tinkamumo ("tikrai tiks"), nebent OEM kodai sutampa identiškai.
6. JOKIŲ IŠGALVOJIMŲ: Jei nežinai ar tiks – sakyk "nežinau" arba "reikia tikrinti".

STILIUS IR PABAIGA:
- Trumpi, pardavėjiški atsakymai (1-2 sakiniai).
- Kalba: Tik lietuvių.
- Pabaiga neaiškiais atvejais: Baik vienu iš: "Galite palikti kontaktą", "Atsiųskite senos detalės kodą", arba "Reikėtų patikrinti pagal jungtį ir tvirtinimą".

PIRMASIS ATSAKYMAS:
Vartotojas pasisveikino ("Sveiki"). Tavo atsakymas turi būti pilnas pasisveikinimas, prisistatymas ir pasiūlymas padėti dėl konkrečios prekės (${product.name}).`;
}

function statusColor(status: CallStatus): string {
  const colors: Record<CallStatus, string> = {
    idle: 'var(--color-text-muted)',
    active: 'var(--color-success)',
    thinking: 'var(--color-warning)',
    speaking: 'var(--color-accent)',
    ended: 'var(--color-danger)',
  };
  return colors[status];
}

function CallTimer({ startTime }: { startTime: Date }) {
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setElapsed(Math.floor((Date.now() - startTime.getTime()) / 1000));
    }, 1000);
    return () => clearInterval(id);
  }, [startTime]);

  const mm = String(Math.floor(elapsed / 60)).padStart(2, '0');
  const ss = String(elapsed % 60).padStart(2, '0');

  return (
    <span style={{ marginLeft: 'auto', color: 'var(--color-text-muted)', fontVariantNumeric: 'tabular-nums' }}>
      {mm}:{ss}
    </span>
  );
}
