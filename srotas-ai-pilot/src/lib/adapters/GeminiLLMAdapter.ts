import { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } from '@google/generative-ai';
import type { LLMAdapter, LLMMessage } from './types';
import { aiConfig } from '../config';

/**
 * GeminiLLMAdapter – production LLM backend using Google Gemini API.
 *
 * Swap in by setting:
 *   LLM_PROVIDER=gemini
 *   GEMINI_API_KEY=AIza...
 *   GEMINI_MODEL=gemini-2.5-flash   (or gemini-1.5-pro)
 *
 * The system prompt is injected from AICallModal/buildSystemPrompt()
 * and contains the full product context + Lithuanian sales consultant rules.
 *
 * Note: Gemini uses a different message format than OpenAI –
 * system instructions are passed separately, and roles are "user"/"model".
 */
export class GeminiLLMAdapter implements LLMAdapter {
  private client: GoogleGenerativeAI;

  constructor() {
    if (!aiConfig.gemini.apiKey) {
      throw new Error(
        '[GeminiLLMAdapter] GEMINI_API_KEY is not set. ' +
          'Add it to .env.local or set LLM_PROVIDER=mock to use the mock adapter.'
      );
    }
    this.client = new GoogleGenerativeAI(aiConfig.gemini.apiKey);
  }

  async chat(messages: LLMMessage[]): Promise<string> {
    const { systemInstruction, history, lastUserMsg } = this.splitMessages(messages);

    const model = this.client.getGenerativeModel({
      model: aiConfig.gemini.model,
      systemInstruction,
      safetySettings: [
        { category: HarmCategory.HARM_CATEGORY_HARASSMENT,        threshold: HarmBlockThreshold.BLOCK_NONE },
        { category: HarmCategory.HARM_CATEGORY_HATE_SPEECH,       threshold: HarmBlockThreshold.BLOCK_NONE },
        { category: HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold: HarmBlockThreshold.BLOCK_NONE },
        { category: HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold: HarmBlockThreshold.BLOCK_NONE },
      ],
      generationConfig: {
        maxOutputTokens: aiConfig.gemini.maxTokens,
        temperature: aiConfig.gemini.temperature,
      },
    });

    const chat = model.startChat({ history });
    const result = await chat.sendMessage(lastUserMsg);
    const text = result.response.text();
    if (!text) throw new Error('[GeminiLLMAdapter] Empty response from Gemini');
    return text.trim();
  }

  async chatStream(
    messages: LLMMessage[],
    onChunk: (chunk: string) => void,
    onDone: () => void
  ): Promise<void> {
    const { systemInstruction, history, lastUserMsg } = this.splitMessages(messages);

    const model = this.client.getGenerativeModel({
      model: aiConfig.gemini.model,
      systemInstruction,
      generationConfig: {
        maxOutputTokens: aiConfig.gemini.maxTokens,
        temperature: aiConfig.gemini.temperature,
      },
    });

    const chat = model.startChat({ history });
    const result = await chat.sendMessageStream(lastUserMsg);

    for await (const chunk of result.stream) {
      const text = chunk.text();
      if (text) onChunk(text);
    }
    onDone();
  }

  /**
   * Converts OpenAI-style messages (system/user/assistant)
   * into Gemini format (systemInstruction + history[] + lastUserMsg).
   *
   * Gemini roles: "user" | "model"  (not "assistant")
   * System message must be passed as systemInstruction, not in history.
   */
  private splitMessages(messages: LLMMessage[]): {
    systemInstruction: string;
    history: { role: 'user' | 'model'; parts: { text: string }[] }[];
    lastUserMsg: string;
  } {
    const systemMsg = messages.find((m) => m.role === 'system')?.content ?? '';
    const conversation = messages.filter((m) => m.role !== 'system');

    // The last message must be a user turn (sent separately via sendMessage)
    const lastUserMsg = conversation.filter((m) => m.role === 'user').at(-1)?.content ?? '';

    // Everything except the final user message goes into history
    const historyMsgs = conversation.slice(0, -1);
    const history = historyMsgs.map((m) => ({
      role: m.role === 'assistant' ? ('model' as const) : ('user' as const),
      parts: [{ text: m.content }],
    }));

    // Gemini requirement: History must start with a 'user' turn.
    // If our history starts with the AI greeting (model), prepend a synthetic user message.
    if (history.length > 0 && history[0].role === 'model') {
      history.unshift({
        role: 'user',
        parts: [{ text: 'Sveiki' }],
      });
    }

    return { systemInstruction: systemMsg, history, lastUserMsg };
  }
}
