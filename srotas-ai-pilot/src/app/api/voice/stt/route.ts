import { NextRequest, NextResponse } from 'next/server';
import { aiConfig } from '@/lib/config';

export async function POST(req: NextRequest) {
  try {
    const apiKey = aiConfig.deepgram.apiKey;
    if (!apiKey) {
      return NextResponse.json({ error: 'Deepgram API key not configured' }, { status: 500 });
    }

    const formData = await req.formData();
    const audioFile = formData.get('audio') as Blob;

    if (!audioFile) {
      return NextResponse.json({ error: 'No audio file provided' }, { status: 400 });
    }

    // Convert blob to ArrayBuffer for Deepgram
    const arrayBuffer = await audioFile.arrayBuffer();

    // Call Deepgram API
    // Lithuanian support in Deepgram often requires 'lt' language tag and 'nova-2' or similar model
    const response = await fetch(
      'https://api.deepgram.com/v1/listen?language=lt&model=nova-2&smart_format=true',
      {
        method: 'POST',
        headers: {
          'Authorization': `Token ${apiKey}`,
          'Content-Type': audioFile.type || 'audio/wav',
        },
        body: arrayBuffer,
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      console.error('[Deepgram] Error:', errorData);
      return NextResponse.json(
        { error: 'Apgailestaujame, nepavyko atpažinti kalbos per Deepgram.' },
        { status: response.status }
      );
    }

    const data = await response.json();
    const transcript = data.results?.channels[0]?.alternatives[0]?.transcript || '';
    const confidence = data.results?.channels[0]?.alternatives[0]?.confidence || 0;

    return NextResponse.json({
      transcript,
      confidence,
      provider: 'deepgram',
      durationSeconds: data.metadata?.duration || 0,
      estimatedCost: 0.005, // Placeholder for logging
    });
  } catch (err) {
    console.error('[/api/voice/stt] Error:', err);
    return NextResponse.json(
      { error: 'Serverio klaida atpažįstant kalbą.' },
      { status: 500 }
    );
  }
}
