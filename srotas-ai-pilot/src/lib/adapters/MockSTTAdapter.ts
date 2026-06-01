import type { STTAdapter } from './types';

/**
 * MockSTTAdapter – simulates speech-to-text by accepting typed text.
 * Replace with DeepgramSTTAdapter or WebSpeechSTTAdapter in production.
 */
export class MockSTTAdapter implements STTAdapter {
  private listening = false;

  async startListening(
    _onTranscript: (text: string, isFinal: boolean) => void
  ): Promise<() => void> {
    this.listening = true;
    console.log('[MockSTT] Listening started (mock – use text input fallback)');
    return () => {
      this.listening = false;
    };
  }

  async stopListening(): Promise<void> {
    this.listening = false;
    console.log('[MockSTT] Listening stopped');
  }

  isListening(): boolean {
    return this.listening;
  }
}
