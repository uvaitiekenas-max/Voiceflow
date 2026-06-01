import { NextResponse } from 'next/server';
import { aiConfig } from '@/lib/config';

/**
 * POST /api/voice/twilio/inbound
 * This is the webhook Twilio calls when a phone call is received.
 * It returns TwiML that connects the call to ElevenLabs Media Stream.
 */
export async function POST() {
  const agentId = process.env.ELEVENLABS_AGENT_ID;

  if (!agentId) {
    return new NextResponse(
      `<?xml version="1.0" encoding="UTF-8"?>
      <Response>
        <Say language="lt-LT">Atsiprašome, sistema nėra sukonfigūruota.</Say>
      </Response>`,
      { headers: { 'Content-Type': 'text/xml' } }
    );
  }

  try {
    // 1. Get a signed URL from ElevenLabs for the stream
    const apiKey = process.env.ELEVENLABS_API_KEY;
    const response = await fetch(
      `https://api.elevenlabs.io/v1/convai/conversation/get-signed-url?agent_id=${agentId}`,
      {
        method: 'GET',
        headers: { 'xi-api-key': apiKey || '' },
      }
    );

    if (!response.ok) throw new Error('Failed to get signed URL');
    const { signed_url } = await response.json();

    // 2. Return TwiML with the signed ElevenLabs stream URL
    // The Twilio stream URL for ElevenLabs
    const streamUrl = `wss://api.elevenlabs.io/v1/convai/conversation/twilio-stream?agent_id=${agentId}`;

    const twiml = `<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <Stream url="${streamUrl}">
      <Parameter name="signed_url" value="${signed_url}" />
    </Stream>
  </Connect>
</Response>`;

    return new NextResponse(twiml, {
      headers: { 'Content-Type': 'text/xml' },
    });
  } catch (err) {
    console.error('[Twilio Inbound] Error:', err);
    return new NextResponse(
      `<?xml version="1.0" encoding="UTF-8"?>
      <Response>
        <Say language="lt-LT">Atsiprašome, įvyko ryšio klaida su balso agentu.</Say>
      </Response>`,
      { headers: { 'Content-Type': 'text/xml' } }
    );
  }
}
