'use client';

import { useState, useEffect, useCallback } from 'react';
import Navbar from '@/components/Navbar';
import type { Lead, ConversationLog } from '@/lib/store';

type Tab = 'conversations' | 'leads';

interface ProviderConfig {
  llmProvider: string;
  openai: { model: string; maxTokens: number; temperature: number; apiKeySet: boolean };
  gemini: { model: string; maxTokens: number; temperature: number; apiKeySet: boolean };
}

export default function AdminPage() {
  const [tab, setTab] = useState<Tab>('conversations');
  const [conversations, setConversations] = useState<ConversationLog[]>([]);
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(false);
  const [providerConfig, setProviderConfig] = useState<ProviderConfig | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const [convRes, leadsRes, configRes] = await Promise.all([
        fetch('/api/conversations'),
        fetch('/api/leads'),
        fetch('/api/config'),
      ]);
      const convData = await convRes.json();
      const leadsData = await leadsRes.json();
      const configData = await configRes.json();
      setConversations(convData.conversations || []);
      setLeads(leadsData.leads || []);
      setProviderConfig(configData);
    } catch (err) {
      console.error('Failed to fetch admin data', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const totalLeads = leads.length;
  const totalConversations = conversations.length;
  const avgDuration =
    conversations.length > 0
      ? Math.round(
          conversations.reduce((sum, c) => sum + c.estimatedDurationSec, 0) /
            conversations.length
        )
      : 0;
  const totalCost = conversations.reduce((sum, c) => sum + c.estimatedCostEur, 0).toFixed(4);

  function formatDuration(sec: number): string {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${m}:${String(s).padStart(2, '0')}`;
  }

  function formatDate(iso: string): string {
    return new Date(iso).toLocaleString('lt-LT');
  }

  return (
    <>
      <Navbar />
      <main>
        <div className="container">
          <div className="page-header">
            <div className="page-tag">⚙️ Administravimas</div>
            <h1 className="page-title">
              Pokalbių ir <span>lead'ų</span> žurnalas
            </h1>
            <p className="page-subtitle">
              Visų AI konsultanto pokalbių ir surinktų kontaktų apžvalga.
            </p>
          </div>

          {/* Provider status banner */}
          {providerConfig && (
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 12,
                padding: '12px 16px',
                marginBottom: 24,
                background: 'var(--color-surface)',
                border: '1px solid var(--color-border)',
                borderRadius: 'var(--radius-md)',
                fontSize: '0.82rem',
              }}
            >
              <span style={{ color: 'var(--color-text-secondary)' }}>🤖 LLM:</span>
              {providerConfig.llmProvider === 'openai' ? (
                <>
                  <span className="badge badge-success">OpenAI</span>
                  <span style={{ color: 'var(--color-text-secondary)' }}>
                    {providerConfig.openai.model}
                  </span>
                  <span className="badge badge-primary">t={providerConfig.openai.temperature}</span>
                  <span className="badge badge-primary">max={providerConfig.openai.maxTokens} tok</span>
                  {!providerConfig.openai.apiKeySet && (
                    <span className="badge badge-warning">⚠️ API key missing</span>
                  )}
                </>
              ) : providerConfig.llmProvider === 'gemini' ? (
                <>
                  <span className="badge badge-success" style={{ background: 'var(--color-accent)', color: 'white' }}>Gemini</span>
                  <span style={{ color: 'var(--color-text-secondary)' }}>
                    {providerConfig.gemini.model}
                  </span>
                  <span className="badge badge-primary">t={providerConfig.gemini.temperature}</span>
                  <span className="badge badge-primary">max={providerConfig.gemini.maxTokens} tok</span>
                  {!providerConfig.gemini.apiKeySet && (
                    <span className="badge badge-warning">⚠️ API key missing</span>
                  )}
                </>
              ) : (
                <span className="badge badge-neutral">Mock (simuliacija)</span>
              )}
            </div>
          )}

          {/* Stats */}
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-value">{totalConversations}</div>
              <div className="stat-label">Pokalbių iš viso</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{totalLeads}</div>
              <div className="stat-label">Surinktų kontaktų</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{formatDuration(avgDuration)}</div>
              <div className="stat-label">Vid. pokalbio trukmė</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">€{totalCost}</div>
              <div className="stat-label">
                Est. sąnaudos
                {providerConfig?.llmProvider === 'openai' ? ' (OpenAI)' : providerConfig?.llmProvider === 'gemini' ? ' (Gemini)' : ' (mock)'}
              </div>
            </div>
          </div>

          {/* Tabs */}
          <div className="admin-tabs">
            <button
              id="tab-conversations"
              className={`admin-tab ${tab === 'conversations' ? 'active' : ''}`}
              onClick={() => setTab('conversations')}
            >
              💬 Pokalbiai ({totalConversations})
            </button>
            <button
              id="tab-leads"
              className={`admin-tab ${tab === 'leads' ? 'active' : ''}`}
              onClick={() => setTab('leads')}
            >
              📞 Kontaktai ({totalLeads})
            </button>
          </div>

          {/* Refresh */}
          <div className="flex items-center justify-between mb-4">
            <span className="text-small text-muted">
              {loading ? 'Kraunama...' : 'Duomenys atnaujinti'}
            </span>
            <button className="btn btn-ghost btn-sm" onClick={fetchData} disabled={loading}>
              🔄 Atnaujinti
            </button>
          </div>

          {/* Conversations Tab */}
          {tab === 'conversations' && (
            <div className="card" style={{ overflow: 'auto' }}>
              {conversations.length === 0 ? (
                <div className="empty-state">
                  <div className="empty-state-icon">💬</div>
                  <p className="empty-state-text">
                    Pokalbių dar nėra. Pradėkite pokalbį su AI konsultantu produkto puslapyje.
                  </p>
                </div>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Detalė</th>
                      <th>Žinutės</th>
                      <th>Trukmė</th>
                      <th>Kaina</th>
                      <th>Rizika</th>
                      <th>Kontaktas</th>
                      <th>Data</th>
                    </tr>
                  </thead>
                  <tbody>
                    {conversations.map((conv) => (
                      <ConversationRow key={conv.id} conv={conv} formatDuration={formatDuration} formatDate={formatDate} />
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}

          {/* Leads Tab */}
          {tab === 'leads' && (
            <div className="card" style={{ overflow: 'auto' }}>
              {leads.length === 0 ? (
                <div className="empty-state">
                  <div className="empty-state-icon">📞</div>
                  <p className="empty-state-text">
                    Kontaktų dar nėra. Klientai gali palikti kontaktus per AI pokalbį.
                  </p>
                </div>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Vardas</th>
                      <th>Telefonas</th>
                      <th>Automobilis</th>
                      <th>Detalės ID</th>
                      <th>Pastabos</th>
                      <th>Data</th>
                    </tr>
                  </thead>
                  <tbody>
                    {leads.map((lead) => (
                      <LeadRow key={lead.id} lead={lead} formatDate={formatDate} />
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}
        </div>
      </main>
    </>
  );
}

function ConversationRow({
  conv,
  formatDuration,
  formatDate,
}: {
  conv: ConversationLog;
  formatDuration: (s: number) => string;
  formatDate: (s: string) => string;
}) {
  const [expanded, setExpanded] = useState(false);

  return (
    <>
      <tr style={{ cursor: 'pointer' }} onClick={() => setExpanded((v) => !v)}>
        <td>
          <code style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
            {conv.id}
          </code>
        </td>
        <td style={{ maxWidth: 180, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          {conv.productName}
        </td>
        <td>{conv.turns.length}</td>
        <td>{formatDuration(conv.estimatedDurationSec)}</td>
        <td>€{conv.estimatedCostEur}</td>
        <td>
          <CompatibilityRiskBadge risk={conv.compatibilityRisk} />
        </td>
        <td>
          {conv.leadCaptured ? (
            <span className="badge badge-success">✅</span>
          ) : (
            <span className="badge badge-neutral">–</span>
          )}
        </td>
        <td className="text-small text-muted">{formatDate(conv.startedAt)}</td>
      </tr>
      {expanded && (
        <tr>
          <td colSpan={8} style={{ padding: '0 16px 16px' }}>
            <div
              style={{
                background: 'var(--color-surface-2)',
                borderRadius: 'var(--radius-sm)',
                padding: '12px',
                fontSize: '0.82rem',
                lineHeight: 1.6,
                maxHeight: 300,
                overflowY: 'auto',
              }}
            >
              {conv.turns.map((turn, i) => (
                <div key={i} style={{ marginBottom: 8 }}>
                  <span
                    style={{
                      fontWeight: 700,
                      color:
                        turn.role === 'assistant'
                          ? 'var(--color-primary)'
                          : 'var(--color-accent)',
                      marginRight: 8,
                    }}
                  >
                    {turn.role === 'assistant' ? '🤖 Rokas' : '👤 Klientas'}
                    {turn.source === 'voice' && (
                      <span style={{ fontWeight: 400, fontSize: '0.7rem', opacity: 0.7, marginLeft: 4 }}>
                        (balsu 🎤 {turn.sttProvider && `STT: ${turn.sttProvider}`} {turn.ttsProvider && `TTS: ${turn.ttsProvider}`})
                      </span>
                    )}
                    :
                  </span>
                  {turn.content}
                  {turn.error && (
                    <div style={{ color: 'var(--color-danger)', fontSize: '0.75rem', marginTop: 4 }}>
                      ⚠️ {turn.error}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </td>
        </tr>
      )}
    </>
  );
}

function CompatibilityRiskBadge({ risk }: { risk: string }) {
  const styles: Record<string, { bg: string; color: string; label: string }> = {
    low: { bg: 'rgba(34, 197, 94, 0.1)', color: 'rgb(34, 197, 94)', label: 'Low' },
    medium: { bg: 'rgba(234, 179, 8, 0.1)', color: 'rgb(234, 179, 8)', label: 'Medium' },
    high: { bg: 'rgba(239, 68, 68, 0.1)', color: 'rgb(239, 68, 68)', label: 'High' },
    'needs human verification': {
      bg: 'rgba(107, 114, 128, 0.1)',
      color: 'rgb(107, 114, 128)',
      label: 'Manual',
    },
  };

  const style = styles[risk] || styles['needs human verification'];

  return (
    <span
      style={{
        padding: '2px 8px',
        borderRadius: '12px',
        fontSize: '0.7rem',
        fontWeight: 600,
        textTransform: 'uppercase',
        backgroundColor: style.bg,
        color: style.color,
        border: `1px solid ${style.color}`,
        whiteSpace: 'nowrap',
      }}
    >
      {style.label}
    </span>
  );
}

function LeadRow({
  lead,
  formatDate,
}: {
  lead: Lead;
  formatDate: (s: string) => string;
}) {
  return (
    <tr>
      <td>
        <code style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>{lead.id}</code>
      </td>
      <td style={{ fontWeight: 600 }}>{lead.name}</td>
      <td>
        <a href={`tel:${lead.phone}`} style={{ color: 'var(--color-primary)' }}>
          {lead.phone}
        </a>
      </td>
      <td className="text-small">{lead.carInfo || '–'}</td>
      <td>
        <code style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
          {lead.productId}
        </code>
      </td>
      <td className="text-small text-muted">{lead.notes || '–'}</td>
      <td className="text-small text-muted">{formatDate(lead.createdAt)}</td>
    </tr>
  );
}
