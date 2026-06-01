import { h } from 'https://esm.sh/preact@10.19.6';
import htm from 'https://esm.sh/htm@3.1.1';
import { NodeIcons, NodeColors } from './Node.js';

const html = htm.bind(h);

const PALETTE_ITEMS = [
  {
    type: "speak",
    title: "Speak Block",
    desc: "Make the bot speak text"
  },
  {
    type: "choice",
    title: "Choice Block",
    desc: "Define routing options"
  },
  {
    type: "capture",
    title: "Capture Block",
    desc: "Collect user input into a var"
  },
  {
    type: "set",
    title: "Set Block",
    desc: "Define/modify state variables"
  },
  {
    type: "condition",
    title: "Condition Block",
    desc: "If/Else branching routes"
  },
  {
    type: "api",
    title: "API Block",
    desc: "Perform external HTTP queries"
  },
  {
    type: "ai",
    title: "AI Prompt Block",
    desc: "Generate dynamic text with LLM"
  }
];

export default function Sidebar({
  onAddNodeClick,
  onLoadTemplate,
  onClearCanvas
}) {
  return html`
    <div className="app-sidebar">
      <div className="sidebar-section" style="flex: 1; overflow-y: auto;">
        <div className="sidebar-section-title">Step Library</div>
        <div className="node-palette-list">
          <div 
            className="palette-node-item" 
            onClick=${() => onAddNodeClick("start")}
            title="Click to add Start Node to canvas"
          >
            <div className="node-icon-wrapper color-start">
              ${NodeIcons.start}
            </div>
            <div>
              <div className="palette-node-title">Start Block</div>
              <div className="palette-node-desc">Flow entry point</div>
            </div>
          </div>

          ${PALETTE_ITEMS.map(item => {
            const colorClass = NodeColors[item.type];
            const icon = NodeIcons[item.type];
            return html`
              <div 
                key=${item.type}
                className="palette-node-item"
                onClick=${() => onAddNodeClick(item.type)}
                title="Click to add to canvas"
              >
                <div className="node-icon-wrapper ${colorClass}">
                  ${icon}
                </div>
                <div>
                  <div className="palette-node-title">${item.title}</div>
                  <div className="palette-node-desc">${item.desc}</div>
                </div>
              </div>
            `;
          })}
        </div>
      </div>

      <div className="sidebar-section" style="background: rgba(0,0,0,0.1); border-top: 1px solid var(--border-light);">
        <div className="sidebar-section-title">Agent Templates</div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          <button 
            className="btn btn-accent" 
            style="width: 100%; justify-content: flex-start;"
            onClick=${() => onLoadTemplate("survey")}
          >
            <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
            Lead Survey Bot
          </button>
          
          <button 
            className="btn btn-accent" 
            style="width: 100%; justify-content: flex-start;"
            onClick=${() => onLoadTemplate("ai_bot")}
          >
            <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 9.172V5L8 4z" />
            </svg>
            AI Support Bot
          </button>
        </div>
      </div>

      <div className="sidebar-section" style="padding: 16px 20px;">
        <button 
          className="btn btn-outline-danger" 
          style="width: 100%; justify-content: center;"
          onClick=${onClearCanvas}
        >
          <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          Clear Workspace
        </button>
      </div>
    </div>
  `;
}
