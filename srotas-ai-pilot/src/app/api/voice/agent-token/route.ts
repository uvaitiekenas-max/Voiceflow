import { NextResponse } from 'next/server';
import { aiConfig } from '@/lib/config';

/**
 * POST /api/voice/agent-token
 * Generates a signed URL for the ElevenLabs Conversational AI Agent.
 */
export async function POST(req: Request) {
  try {
    const { productInfo } = await req.json().catch(() => ({}));
    const apiKey = aiConfig.elevenlabs.apiKey;
    const agentId = aiConfig.elevenlabs.agentId;

    if (!apiKey || !agentId) {
      return NextResponse.json(
        { error: 'ElevenLabs API key or Agent ID not configured' },
        { status: 500 }
      );
    }

    // Get signed URL from ElevenLabs (Must be GET)
    const response = await fetch(
      `https://api.elevenlabs.io/v1/convai/conversation/get-signed-url?agent_id=${agentId}`,
      {
        method: 'GET',
        headers: {
          'xi-api-key': apiKey,
        },
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      console.error('[ElevenLabs Agent] Token Error:', errorData);
      return NextResponse.json(
        { error: 'Nepavyko gauti prisijungimo rakto agentui.' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json({ signedUrl: data.signed_url });
  } catch (err) {
    console.error('[/api/voice/agent-token] Error:', err);
    return NextResponse.json(
      { error: 'Serverio klaida generuojant agento raktą.' },
      { status: 500 }
    );
  }
}
