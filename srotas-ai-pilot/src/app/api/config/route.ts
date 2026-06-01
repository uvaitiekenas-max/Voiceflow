import { NextResponse } from 'next/server';
import { aiConfig } from '@/lib/config';

/**
 * GET /api/config
 * Returns the current AI provider configuration (safe subset – no secret values).
 */
export async function GET() {
  return NextResponse.json({
    llmProvider: aiConfig.llmProvider,
    openai: {
      model: aiConfig.openai.model,
      maxTokens: aiConfig.openai.maxTokens,
      temperature: aiConfig.openai.temperature,
      apiKeySet: Boolean(aiConfig.openai.apiKey),
    },
    gemini: {
      model: aiConfig.gemini.model,
      maxTokens: aiConfig.gemini.maxTokens,
      temperature: aiConfig.gemini.temperature,
      apiKeySet: Boolean(aiConfig.gemini.apiKey),
    },
    voice: {
      sttProvider: aiConfig.voice.sttProvider,
      ttsProvider: aiConfig.voice.ttsProvider,
      mode: aiConfig.voice.mode,
      twilioPhoneNumber: aiConfig.voice.twilioPhoneNumber,
    }
  });
}
