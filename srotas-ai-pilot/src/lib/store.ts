export interface Lead {
  id: string;
  name: string;
  phone: string;
  carInfo: string;
  productId: string;
  notes: string;
  createdAt: string;
}

export type CompatibilityRisk = 'low' | 'medium' | 'high' | 'needs human verification';

export interface ConversationTurn {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  source?: 'text' | 'voice';
  sttProvider?: string;
  ttsProvider?: string;
  sttConfidence?: number;
  sttDuration?: number;
  sttCost?: number;
  ttsCost?: number;
  llmCost?: number;
  error?: string;
}

export interface ConversationLog {
  id: string;
  productId: string;
  productName: string;
  turns: ConversationTurn[];
  leadCaptured: boolean;
  startedAt: string;
  endedAt?: string;
  estimatedDurationSec: number;
  estimatedCostEur: number;
  compatibilityRisk: CompatibilityRisk;
}

// In-memory stores (reset on page reload – replace with DB/Redis in production)
const leads: Lead[] = [];
const conversationLogs: ConversationLog[] = [];

// ---- Leads ----
export function saveLeadToStore(lead: Omit<Lead, 'id' | 'createdAt'>): Lead {
  const record: Lead = {
    ...lead,
    id: `LEAD-${Date.now()}`,
    createdAt: new Date().toISOString(),
  };
  leads.push(record);
  return record;
}

export function getLeads(): Lead[] {
  return [...leads];
}

// ---- Conversation Logs ----
export function saveConversationLog(
  log: Omit<ConversationLog, 'id' | 'estimatedCostEur' | 'compatibilityRisk'>
): ConversationLog {
  const turnCount = log.turns.length;
  // Rough cost estimate: $0.002 per 1K tokens, ~20 tokens/turn
  const estimatedTokens = turnCount * 20;
  const estimatedCostEur = parseFloat(((estimatedTokens / 1000) * 0.002).toFixed(4));

  // 2. Compatibility Risk Heuristic
  let risk: CompatibilityRisk = 'needs human verification';
  const allText = log.turns.map(t => t.content.toLowerCase()).join(' ');
  const aiText = log.turns.filter(t => t.role === 'assistant').map(t => t.content.toLowerCase()).join(' ');

  if (aiText.includes('nesutampa') || aiText.includes('netiks') || aiText.includes('kitam automobiliui')) {
    risk = 'high';
  } else if (aiText.includes('sutampa') || aiText.includes('identiškas') || aiText.includes('tikrai tinka')) {
    risk = 'low';
  } else if (aiText.includes('neaišku') || aiText.includes('nežinau') || aiText.includes('patikrinti') || aiText.includes('saugiausia')) {
    risk = 'medium';
  }

  const record: ConversationLog = {
    ...log,
    id: `CONV-${Date.now()}`,
    estimatedCostEur,
    compatibilityRisk: risk,
  };
  conversationLogs.push(record);
  return record;
}

export function getConversationLogs(): ConversationLog[] {
  return [...conversationLogs];
}
