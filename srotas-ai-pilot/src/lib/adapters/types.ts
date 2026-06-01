// ============================================================
// STT (Speech-to-Text) Adapter Interface
// ============================================================
export interface STTAdapter {
  /**
   * Starts listening for speech input.
   * Returns a cleanup function to stop listening.
   */
  startListening(onTranscript: (text: string, isFinal: boolean) => void): Promise<() => void>;

  /** Stops listening */
  stopListening(): Promise<void>;

  /** Returns true if currently listening */
  isListening(): boolean;
}

// ============================================================
// LLM (Large Language Model) Adapter Interface
// ============================================================
export interface LLMMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface LLMAdapter {
  /**
   * Sends a conversation history and returns the AI response.
   */
  chat(messages: LLMMessage[]): Promise<string>;

  /**
   * Streaming variant – calls onChunk for each token/chunk.
   */
  chatStream?(
    messages: LLMMessage[],
    onChunk: (chunk: string) => void,
    onDone: () => void
  ): Promise<void>;
}

// ============================================================
// TTS (Text-to-Speech) Adapter Interface
// ============================================================
export interface TTSAdapter {
  /**
   * Speaks the given text aloud.
   * Returns a promise that resolves when speech is done.
   */
  speak(text: string): Promise<void>;

  /** Stops current speech playback */
  stop(): void;

  /** Returns true if currently speaking */
  isSpeaking(): boolean;
}
