import { NextRequest, NextResponse } from 'next/server';
import { saveLeadToStore, getLeads } from '@/lib/store';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { name, phone, carInfo, productId, notes } = body;

    if (!name || !phone || !productId) {
      return NextResponse.json(
        { error: 'name, phone, productId yra privalomi' },
        { status: 400 }
      );
    }

    const lead = saveLeadToStore({ name, phone, carInfo: carInfo || '', productId, notes: notes || '' });
    return NextResponse.json({ success: true, lead });
  } catch (err) {
    console.error('[/api/leads] Error:', err);
    return NextResponse.json({ error: 'Serverio klaida' }, { status: 500 });
  }
}

export async function GET() {
  return NextResponse.json({ leads: getLeads() });
}
