import { NextRequest, NextResponse } from 'next/server';
import { getLLMAdapter } from '@/lib/adapters/factory';
import type { LLMMessage } from '@/lib/adapters/types';

// Resolve adapter once at module load (server-side singleton per worker)
const llm = getLLMAdapter();

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const messages: LLMMessage[] = body.messages;

    if (!Array.isArray(messages) || messages.length === 0) {
      return NextResponse.json({ error: 'messages array required' }, { status: 400 });
    }

    const response = await llm.chat(messages);
    return NextResponse.json({ response });
  } catch (err) {
    console.error('[/api/chat] Error:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
