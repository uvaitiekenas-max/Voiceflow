import { h } from 'https://esm.sh/preact@10.19.6';
import { useState, useEffect, useRef } from 'https://esm.sh/preact/hooks@10.19.6';
import htm from 'https://esm.sh/htm@3.1.1';

const html = htm.bind(h);

export default function Simulator({
  isOpen,
  onClose,
  messages,
  variables,
  currentChoiceNode,
  currentCaptureNode,
  isExecuting,
  onChoiceSelect,
  onCaptureSubmit,
  onReset,
  executingNodeTitle
}) {
  const [activeTab, setActiveTab] = useState("chat"); // 'chat' | 'vars'
  const [inputText, setInputText] = useState("");
  const messagesEndRef = useRef(null);

  // Auto-scroll messages list to bottom
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isExecuting]);

  const handleSendCapture = (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;
    onCaptureSubmit(inputText.trim());
    setInputText("");
  };

  // Convert nested variables object into flat rows for debugging table
  const getFlatVariables = (obj, prefix = "") => {
    let rows = [];
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        const path = prefix ? `${prefix}.${key}` : key;
        if (typeof obj[key] === 'object' && obj[key] !== null) {
          // If it's a simple flat-like object or array, show JSON preview, else recurse
          rows.push({
            name: path,
            value: JSON.stringify(obj[key])
          });
          // Also recurse for granular tracking
          rows = rows.concat(getFlatVariables(obj[key], path));
        } else {
          rows.push({
            name: path,
            value: String(obj[key])
          });
        }
      }
    }
    return rows;
  };

  const flatVars = getFlatVariables(variables);

  return html`
    <div className="simulator-panel ${isOpen ? '' : 'collapsed'}">
      <div className="simulator-header">
        <div className="simulator-header-title">
          <div style="width: 8px; height: 8px; border-radius: 50%; background-color: ${isExecuting ? 'var(--color-accent-cyan)' : 'var(--color-text-dark)'}; animation: ${isExecuting ? 'active-glow 1s infinite alternate' : 'none'};"></div>
          <span>Agent Simulator</span>
        </div>
        
        <div className="simulator-tabs">
          <button className="tab-btn ${activeTab === 'chat' ? 'active' : ''}" onClick=${() => setActiveTab("chat")}>
            Chat
          </button>
          <button className="tab-btn ${activeTab === 'vars' ? 'active' : ''}" onClick=${() => setActiveTab("vars")}>
            Variables
          </button>
        </div>

        <div style="display: flex; gap: 8px; align-items: center;">
          <button 
            className="btn btn-outline-danger" 
            style="padding: 4px 8px; font-size: 0.7rem;"
            onClick=${onReset}
            title="Restart conversation"
          >
            Reset
          </button>
          <button 
            className="control-btn" 
            style="width: 24px; height: 24px;"
            onClick=${onClose}
            title="Minimize"
          >
            <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
      </div>

      <div style="background: rgba(139, 92, 246, 0.08); border-bottom: 1px solid var(--border-light); padding: 8px 20px; font-size: 0.7rem; display: flex; justify-content: space-between; align-items: center;">
        <span style="color: var(--color-text-muted);">Executing Block:</span>
        <span style="font-weight: 700; color: var(--color-primary);">${executingNodeTitle || "None (Idle)"}</span>
      </div>

      <div className="simulator-body">
        ${activeTab === "chat" && html`
          <div className="chat-messages-container">
            <div style="text-align: center; color: var(--color-text-dark); font-size: 0.7rem; margin-bottom: 8px;">
              Session started. Active nodes highlight in cyan on the canvas.
            </div>

            ${messages.map((msg, index) => html`
              <div key=${index} className="chat-bubble ${msg.sender}">
                <div style="white-space: pre-wrap;">${msg.text}</div>
                <div style="font-size: 0.55rem; color: var(--color-text-dark); margin-top: 4px; text-align: right;">
                  ${msg.timestamp}
                </div>
              </div>
            `)}

            ${isExecuting && html`
              <div className="chat-bubble bot" style="width: 60px; padding: 10px 14px;">
                <div className="typing-dots">
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                </div>
              </div>
            `}
            
            <div ref=${messagesEndRef}></div>
          </div>

          ${!isExecuting && currentChoiceNode && html`
            <div className="chat-choices-container">
              <div style="font-size: 0.7rem; color: var(--color-text-dark); font-weight: 700; text-transform: uppercase; margin-bottom: 4px; letter-spacing: 0.5px;">User Choices:</div>
              ${(currentChoiceNode.data.choices || []).map((choice, index) => html`
                <button 
                  key=${index} 
                  className="chat-choice-btn"
                  onClick=${() => onChoiceSelect(index, choice)}
                >
                  ${choice}
                </button>
              `)}
            </div>
          `}

          ${!isExecuting && currentCaptureNode && html`
            <form className="chat-input-container" onSubmit=${handleSendCapture}>
              <input
                type="text"
                className="chat-input"
                value=${inputText}
                onInput=${(e) => setInputText(e.target.value)}
                placeholder="Type your response..."
                autoFocus
              />
              <button type="submit" className="btn btn-primary" style="padding: 12px 18px;">
                Send
              </button>
            </form>
          `}
        `}

        ${activeTab === "vars" && html`
          <div className="variables-container">
            ${flatVars.length === 0 ? html`
              <div className="variables-empty-state">
                <svg className="empty-state-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="width: 40px; height: 40px;">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                </svg>
                <div style="font-weight: 600;">No Variables Active</div>
                <div style="font-size: 0.75rem; max-width: 200px;">Capture user inputs, set variables, or fetch endpoints to populate state variables here.</div>
              </div>
            ` : html`
              <table className="variables-table">
                <thead>
                  <tr>
                    <th>Variable</th>
                    <th>Runtime Value</th>
                  </tr>
                </thead>
                <tbody>
                  ${flatVars.map(row => html`
                    <tr key=${row.name}>
                      <td className="var-name">{${row.name}}</td>
                      <td className="var-val">
                        <div style="max-height: 80px; overflow-y: auto; white-space: pre-wrap; font-size: 0.75rem;">
                          ${row.value}
                        </div>
                      </td>
                    </tr>
                  `)}
                </tbody>
              </table>
            `}
          </div>
        `}
      </div>
    </div>
  `;
}
