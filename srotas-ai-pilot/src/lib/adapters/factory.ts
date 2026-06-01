import type { LLMAdapter } from './types';
import { aiConfig } from '../config';

/**
 * getLLMAdapter – resolves the correct LLM backend at runtime based on LLM_PROVIDER env var.
 *
 * Providers:
 *   "gemini"  → GeminiLLMAdapter  (requires GEMINI_API_KEY)
 *   "openai"  → OpenAILLMAdapter  (requires OPENAI_API_KEY)
 *   "mock"    → MockLLMAdapter    (no keys needed, built-in Lithuanian simulator)
 *
 *
 * Falls back to MockLLMAdapter if the API key is missing or the adapter fails to init.
 * Calls are wrapped in a SafeAdapter to handle runtime failures (like quotas).
 */
class SafeAdapter implements LLMAdapter {
  constructor(private primary: LLMAdapter, private fallback: LLMAdapter) {}

  async chat(messages: LLMMessage[]): Promise<string> {
    try {
      return await this.primary.chat(messages);
    } catch (err) {
      console.error('[SafeAdapter] Primary adapter failed, using fallback:', err);
      return await this.fallback.chat(messages);
    }
  }

  async chatStream?(
    messages: LLMMessage[],
    onChunk: (chunk: string) => void,
    onDone: () => void
  ): Promise<void> {
    if (this.primary.chatStream) {
      try {
        return await this.primary.chatStream(messages, onChunk, onDone);
      } catch (err) {
        console.error('[SafeAdapter] Primary stream failed, using fallback:', err);
        if (this.fallback.chatStream) {
          return await this.fallback.chatStream(messages, onChunk, onDone);
        }
      }
    }
    // Simple fallback if no streaming available on fallback
    const response = await this.fallback.chat(messages);
    onChunk(response);
    onDone();
  }
}

export function getLLMAdapter(): LLMAdapter {
  const provider = aiConfig.llmProvider;

  if (provider === 'gemini') {
    if (!aiConfig.gemini.apiKey) {
      console.warn(
        '[getLLMAdapter] LLM_PROVIDER=gemini but GEMINI_API_KEY is missing. ' +
          'Falling back to MockLLMAdapter.'
      );
      return makeMock();
    }
    try {
      const { GeminiLLMAdapter } = require('./GeminiLLMAdapter');
      console.log(`[getLLMAdapter] Using Gemini (model: ${aiConfig.gemini.model})`);
      return new SafeAdapter(new GeminiLLMAdapter(), makeMock());
    } catch (err) {
      console.error('[getLLMAdapter] Failed to init GeminiLLMAdapter:', err);
      return makeMock();
    }
  }

  if (provider === 'openai') {
    if (!aiConfig.openai.apiKey) {
      console.warn(
        '[getLLMAdapter] LLM_PROVIDER=openai but OPENAI_API_KEY is missing. ' +
          'Falling back to MockLLMAdapter.'
      );
      return makeMock();
    }
    try {
      const { OpenAILLMAdapter } = require('./OpenAILLMAdapter');
      console.log(`[getLLMAdapter] Using OpenAI (model: ${aiConfig.openai.model})`);
      return new SafeAdapter(new OpenAILLMAdapter(), makeMock());
    } catch (err) {
      console.error('[getLLMAdapter] Failed to init OpenAILLMAdapter:', err);
      return makeMock();
    }
  }

  // Default: mock
  return makeMock();
}

function makeMock(): LLMAdapter {
  console.log('[getLLMAdapter] Using MockLLMAdapter');
  const { MockLLMAdapter } = require('./MockLLMAdapter');
  return new MockLLMAdapter();
}
