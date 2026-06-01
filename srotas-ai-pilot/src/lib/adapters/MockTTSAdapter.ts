import type { TTSAdapter } from './types';

/**
 * MockTTSAdapter – uses the browser's Web Speech API (SpeechSynthesis) in Lithuanian.
 * Falls back to console.log if the API is unavailable.
 * Replace with ElevenLabsTTSAdapter in production.
 */
export class MockTTSAdapter implements TTSAdapter {
  private utterance: SpeechSynthesisUtterance | null = null;
  private speaking = false;

  async speak(text: string): Promise<void> {
    return new Promise((resolve) => {
      if (typeof window === 'undefined' || !window.speechSynthesis) {
        console.log('[MockTTS] SpeechSynthesis not available. Text:', text);
        setTimeout(resolve, 1000);
        return;
      }

      this.stop();

      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'lt-LT';
      utterance.rate = 1.0;
      utterance.pitch = 1.0;

      // Try to find a Lithuanian voice
      const voices = window.speechSynthesis.getVoices();
      const ltVoice = voices.find((v) => v.lang.startsWith('lt'));
      if (ltVoice) utterance.voice = ltVoice;

      utterance.onstart = () => {
        this.speaking = true;
      };
      utterance.onend = () => {
        this.speaking = false;
        resolve();
      };
      utterance.onerror = () => {
        this.speaking = false;
        resolve();
      };

      this.utterance = utterance;
      window.speechSynthesis.speak(utterance);
    });
  }

  stop(): void {
    if (typeof window !== 'undefined' && window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    this.speaking = false;
    this.utterance = null;
  }

  isSpeaking(): boolean {
    return this.speaking;
  }
}
