import OpenAI from 'openai';
import type { LLMAdapter, LLMMessage } from './types';
import { aiConfig } from '../config';

/**
 * OpenAILLMAdapter – production LLM backend using the OpenAI Chat Completions API.
 *
 * Swap in by setting:
 *   LLM_PROVIDER=openai
 *   OPENAI_API_KEY=sk-...
 *   OPENAI_MODEL=gpt-4o-mini   (or gpt-4o for best quality)
 *
 * The system prompt is injected by AICallModal / buildSystemPrompt()
 * and contains the full product context + Lithuanian sales consultant rules.
 */
export class OpenAILLMAdapter implements LLMAdapter {
  private client: OpenAI;

  constructor() {
    if (!aiConfig.openai.apiKey) {
      throw new Error(
        '[OpenAILLMAdapter] OPENAI_API_KEY is not set. ' +
          'Add it to .env.local or set LLM_PROVIDER=mock to use the mock adapter.'
      );
    }

    this.client = new OpenAI({
      apiKey: aiConfig.openai.apiKey,
    });
  }

  async chat(messages: LLMMessage[]): Promise<string> {
    const response = await this.client.chat.completions.create({
      model: aiConfig.openai.model,
      messages: messages.map((m) => ({
        role: m.role,
        content: m.content,
      })),
      max_tokens: aiConfig.openai.maxTokens,
      temperature: aiConfig.openai.temperature,
    });

    const content = response.choices[0]?.message?.content;
    if (!content) throw new Error('[OpenAILLMAdapter] Empty response from OpenAI');
    return content.trim();
  }

  async chatStream(
    messages: LLMMessage[],
    onChunk: (chunk: string) => void,
    onDone: () => void
  ): Promise<void> {
    const stream = await this.client.chat.completions.create({
      model: aiConfig.openai.model,
      messages: messages.map((m) => ({
        role: m.role,
        content: m.content,
      })),
      max_tokens: aiConfig.openai.maxTokens,
      temperature: aiConfig.openai.temperature,
      stream: true,
    });

    for await (const chunk of stream) {
      const delta = chunk.choices[0]?.delta?.content;
      if (delta) onChunk(delta);
    }
    onDone();
  }
}
