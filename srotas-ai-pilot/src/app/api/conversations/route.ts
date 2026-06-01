import { NextRequest, NextResponse } from 'next/server';
import { saveConversationLog, getConversationLogs } from '@/lib/store';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { productId, productName, turns, leadCaptured, startedAt, endedAt } = body;

    if (!productId || !Array.isArray(turns)) {
      return NextResponse.json({ error: 'productId ir turns yra privalomi' }, { status: 400 });
    }

    const startMs = new Date(startedAt).getTime();
    const endMs = endedAt ? new Date(endedAt).getTime() : Date.now();
    const estimatedDurationSec = Math.round((endMs - startMs) / 1000);

    const log = saveConversationLog({
      productId,
      productName: productName || '',
      turns,
      leadCaptured: !!leadCaptured,
      startedAt,
      endedAt: endedAt || new Date().toISOString(),
      estimatedDurationSec,
    });

    return NextResponse.json({ success: true, log });
  } catch (err) {
    console.error('[/api/conversations] Error:', err);
    return NextResponse.json({ error: 'Serverio klaida' }, { status: 500 });
  }
}

export async function GET() {
  return NextResponse.json({ conversations: getConversationLogs() });
}
