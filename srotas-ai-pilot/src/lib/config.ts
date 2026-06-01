/**
 * Central AI provider configuration.
 * All values are read from environment variables – never hardcoded.
 *
 * To switch providers:
 *   1. Copy .env.example → .env.local
 *   2. Set LLM_PROVIDER and fill the matching API key
 *   3. Restart the dev server
 */

export type LLMProvider = 'openai' | 'gemini' | 'mock';

export interface AIConfig {
  llmProvider: LLMProvider;

  openai: {
    apiKey: string;
    model: string;
    maxTokens: number;
    temperature: number;
  };

  gemini: {
    apiKey: string;
    model: string;
    maxTokens: number;
    temperature: number;
  };
}

function getEnv(key: string, fallback: string): string {
  return process.env[key] ?? fallback;
}

export const aiConfig: AIConfig = {
  llmProvider: (getEnv('LLM_PROVIDER', 'mock') as LLMProvider),

  openai: {
    apiKey: getEnv('OPENAI_API_KEY', ''),
    model: getEnv('OPENAI_MODEL', 'gpt-4o-mini'),
    maxTokens: parseInt(getEnv('OPENAI_MAX_TOKENS', '300'), 10),
    temperature: parseFloat(getEnv('OPENAI_TEMPERATURE', '0.3')),
  },

  deepgram: {
    apiKey: getEnv('DEEPGRAM_API_KEY', ''),
  },

  elevenlabs: {
    apiKey: getEnv('ELEVENLABS_API_KEY', ''),
    voiceId: getEnv('ELEVENLABS_VOICE_ID', 'EXAVITQu4vr4xnSDxMaL'),
    agentId: getEnv('ELEVENLABS_AGENT_ID', ''),
  },

  voice: {
    sttProvider: getEnv('STT_PROVIDER', 'deepgram'),
    ttsProvider: getEnv('TTS_PROVIDER', 'elevenlabs'),
    mode: getEnv('VOICE_MODE', 'browser'), // 'browser' | 'provider'
    twilioPhoneNumber: getEnv('TWILIO_PHONE_NUMBER', ''),
  },

  gemini: {
    apiKey: getEnv('GEMINI_API_KEY', ''),
    model: getEnv('GEMINI_MODEL', 'gemini-2.5-flash'),
    maxTokens: parseInt(getEnv('GEMINI_MAX_TOKENS', '1000'), 10),
    temperature: parseFloat(getEnv('GEMINI_TEMPERATURE', '0.3')),
  },
};
