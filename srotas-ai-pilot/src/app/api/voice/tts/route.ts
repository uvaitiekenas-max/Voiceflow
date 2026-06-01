import { NextRequest, NextResponse } from 'next/server';
import { aiConfig } from '@/lib/config';

export async function POST(req: NextRequest) {
  try {
    const { text } = await req.json();
    const apiKey = aiConfig.elevenlabs.apiKey;
    const voiceId = aiConfig.elevenlabs.voiceId;

    if (!text) {
      return NextResponse.json({ error: 'No text provided' }, { status: 400 });
    }

    if (!apiKey) {
      return NextResponse.json({ error: 'ElevenLabs API key not configured' }, { status: 500 });
    }

    const response = await fetch(
      `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`,
      {
        method: 'POST',
        headers: {
          'xi-api-key': apiKey,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text,
          model_id: 'eleven_multilingual_v2',
          voice_settings: {
            stability: 0.5,
            similarity_boost: 0.75,
          },
        }),
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      console.error('[ElevenLabs] Error:', errorData);
      return NextResponse.json(
        { error: 'Nepavyko sugeneruoti balso atsakymo per ElevenLabs.' },
        { status: response.status }
      );
    }

    const audioBlob = await response.blob();

    // Return the audio stream with appropriate headers
    return new NextResponse(audioBlob, {
      headers: {
        'Content-Type': 'audio/mpeg',
        'X-Provider': 'elevenlabs',
        'X-Text-Length': text.length.toString(),
      },
    });
  } catch (err) {
    console.error('[/api/voice/tts] Error:', err);
    return NextResponse.json(
      { error: 'Serverio klaida generuojant balsą.' },
      { status: 500 }
    );
  }
}
