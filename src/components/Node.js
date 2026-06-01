import { h } from 'https://esm.sh/preact@10.19.6';
import htm from 'https://esm.sh/htm@3.1.1';

const html = htm.bind(h);

// Inline SVG Icon dictionary for premium styling without network dependency
export const NodeIcons = {
  start: html`
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <polygon points="6 3 20 12 6 21 6 3"></polygon>
    </svg>
  `,
  speak: html`
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
    </svg>
  `,
  choice: html`
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="18" cy="18" r="3"></circle>
      <circle cx="6" cy="6" r="3"></circle>
      <path d="M6 9a9 9 0 0 0 9 9"></path>
    </svg>
  `,
  capture: html`
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
      <polyline points="14 2 14 8 20 8"></polyline>
      <line x1="6" y1="13" x2="18" y2="13"></line>
      <line x1="6" y1="17" x2="18" y2="17"></line>
      <line x1="6" y1="9" x2="10" y2="9"></line>
    </svg>
  `,
  set: html`
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
    </svg>
  `,
  condition: html`
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <line x1="6" y1="3" x2="6" y2="15"></line>
      <circle cx="6" cy="18" r="3"></circle>
      <path d="M18 3v6a4 4 0 0 1-4 4H6"></path>
      <circle cx="18" cy="18" r="3"></circle>
    </svg>
  `,
  api: html`
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="10"></circle>
      <line x1="2" y1="12" x2="22" y2="12"></line>
      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
    </svg>
  `,
  ai: html`
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"></path>
      <path d="m5 3 1 2.5L8.5 6 6 7 5 9.5 4 7 1.5 6 4 5.5z"></path>
      <path d="m19 17 1 2.5 2.5.5-2.5 1-1 2.5-1-2.5-2.5-1 2.5-1z"></path>
    </svg>
  `
};

export const NodeColors = {
  start: "color-start",
  speak: "color-speak",
  choice: "color-choice",
  capture: "color-capture",
  set: "color-set",
  condition: "color-condition",
  api: "color-api",
  ai: "color-ai"
};

// Fixed Port offsets inside nodes to draw SVG lines correctly
export function getNodePortCoordinates(node) {
  const width = 250;
  let height = 96;
  const ports = {};

  if (node.type === "start") {
    height = 48;
    ports["default"] = { x: node.x + width, y: node.y + height / 2 };
  } else if (node.type === "speak") {
    height = 96;
    ports["input"] = { x: node.x, y: node.y + height / 2 };
    ports["default"] = { x: node.x + width, y: node.y + height / 2 };
  } else if (node.type === "capture") {
    height = 96;
    ports["input"] = { x: node.x, y: node.y + height / 2 };
    ports["default"] = { x: node.x + width, y: node.y + height / 2 };
  } else if (node.type === "set") {
    height = 86;
    ports["input"] = { x: node.x, y: node.y + height / 2 };
    ports["default"] = { x: node.x + width, y: node.y + height / 2 };
  } else if (node.type === "api") {
    height = 110;
    ports["input"] = { x: node.x, y: node.y + height / 2 };
    ports["default"] = { x: node.x + width, y: node.y + height / 2 };
  } else if (node.type === "ai") {
    height = 110;
    ports["input"] = { x: node.x, y: node.y + height / 2 };
    ports["default"] = { x: node.x + width, y: node.y + height / 2 };
  } else if (node.type === "condition") {
    height = 112;
    ports["input"] = { x: node.x, y: node.y + height / 2 };
    ports["true"] = { x: node.x + width, y: node.y + 54 };
    ports["false"] = { x: node.x + width, y: node.y + 90 };
  } else if (node.type === "choice") {
    const choicesCount = (node.data.choices && node.data.choices.length) || 0;
    height = 82 + choicesCount * 36;
    ports["input"] = { x: node.x, y: node.y + height / 2 };
    for (let i = 0; i < choicesCount; i++) {
      ports[`choice-${i}`] = { x: node.x + width, y: node.y + 74 + i * 36 };
    }
  }

  return { height, ports };
}

export default function Node({
  node,
  isSelected,
  isExecuting,
  onSelect,
  onNodeDragStart,
  onPortMouseDown
}) {
  const { height } = getNodePortCoordinates(node);
  const colorClass = NodeColors[node.type] || "color-speak";
  const icon = NodeIcons[node.type];

  const handleMouseDown = (e) => {
    // Prevent dragging node if clicking on a port
    if (e.target.closest('.port')) return;
    
    e.stopPropagation();
    onSelect(node.id);
    onNodeDragStart(e, node.id);
  };

  const renderBodyContent = () => {
    switch (node.type) {
      case "start":
        return null;
      case "speak":
        return html`
          <div className="node-body">
            <div style="font-weight: 500; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;">
              ${node.data.text || "Says something..."}
            </div>
          </div>
        `;
      case "capture":
        return html`
          <div className="node-body">
            <div style="color: var(--color-text-main); font-weight: 500; margin-bottom: 6px;">
              ${node.data.text || "Type query..."}
            </div>
            <div>Capture response to: <span style="font-family: monospace; color: var(--color-accent-pink); font-weight: 700;">{${node.data.variable || "variable"}}</span></div>
          </div>
        `;
      case "set":
        return html`
          <div className="node-body">
            <div>Set <span style="font-family: monospace; color: var(--color-accent-pink); font-weight: 700;">{${node.data.variable || "var"}}</span></div>
            <div style="color: var(--color-accent-cyan); font-family: monospace; font-weight: 600; margin-top: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
              = ${node.data.expression || "value"}
            </div>
          </div>
        `;
      case "condition":
        return html`
          <div className="node-body" style="display: flex; flex-direction: column; gap: 8px;">
            <div style="font-size: 0.7rem; color: var(--color-text-dark); text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Condition Check</div>
            <div style="font-family: monospace; font-weight: 600; color: var(--color-accent-pink); overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
              {${node.data.variable || "var"}}
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.7rem;">
              <span style="color: var(--color-text-muted);">${node.data.operator || "equals"}</span>
              <span style="color: var(--color-accent-cyan); font-family: monospace; font-weight: 600;">${node.data.value || "exists"}</span>
            </div>
          </div>
        `;
      case "api":
        return html`
          <div className="node-body">
            <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
              <span className="node-header-badge" style="background: rgba(16, 185, 129, 0.15); color: var(--color-accent-green); font-size: 0.6rem;">
                ${node.data.method || "GET"}
              </span>
              <span style="font-family: monospace; font-size: 0.65rem; color: var(--color-text-muted); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1;">
                ${node.data.url || "https://api.com"}
              </span>
            </div>
            <div style="font-size: 0.7rem;">Save response to: <span style="font-family: monospace; color: var(--color-accent-pink); font-weight: 700;">{${node.data.saveTo || "api_response"}}</span></div>
          </div>
        `;
      case "ai":
        return html`
          <div className="node-body">
            <div style="color: var(--color-accent-pink); font-weight: 700; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">LLM Prompt</div>
            <div style="font-weight: 500; font-size: 0.7rem; color: var(--color-text-main); overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; margin-bottom: 6px;">
              ${node.data.prompt || "Ask AI something..."}
            </div>
            <div style="font-size: 0.65rem; color: var(--color-text-dark);">Save text to: <span style="font-family: monospace; color: var(--color-accent-cyan); font-weight: 700;">{${node.data.saveTo || "ai_result"}}</span></div>
          </div>
        `;
      case "choice":
        return html`
          <div className="node-body" style="display: flex; flex-direction: column; gap: 6px; padding-top: 6px;">
            <div style="font-weight: 600; font-size: 0.75rem; color: var(--color-text-main); margin-bottom: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
              ${node.data.text || "Choose path:"}
            </div>
            ${(node.data.choices || []).map((choice, index) => html`
              <div key=${index} className="choice-port-row">
                <div className="choice-text">${choice}</div>
                <div 
                  className="port choice-port port-output"
                  onMouseDown=${(e) => {
                    e.stopPropagation();
                    onPortMouseDown(e, node.id, `choice-${index}`, false);
                  }}
                ></div>
              </div>
            `)}
          </div>
        `;
      default:
        return null;
    }
  };

  return html`
    <div 
      className="node-element ${isSelected ? 'selected' : ''} ${isExecuting ? 'executing-active' : ''}"
      style="left: ${node.x}px; top: ${node.y}px; height: ${height}px;"
      onMouseDown=${handleMouseDown}
      id=${`dom-${node.id}`}
    >
      ${node.type !== "start" && html`
        <div 
          className="port port-input"
          onMouseDown=${(e) => {
            e.stopPropagation();
            onPortMouseDown(e, node.id, "input", true);
          }}
        ></div>
      `}
      
      <div className="node-header">
        <div className="node-header-icon ${colorClass}">
          ${icon}
        </div>
        <div className="node-header-title">${node.title}</div>
        <span className="node-header-badge">${node.type}</span>
      </div>

      ${renderBodyContent()}

      ${node.type !== "choice" && node.type !== "condition" && html`
        <div 
          className="port port-output"
          onMouseDown=${(e) => {
            e.stopPropagation();
            onPortMouseDown(e, node.id, "default", false);
          }}
        ></div>
      `}

      ${node.type === "condition" && html`
        <div 
          className="port port-output" 
          style="top: 54px; right: -7px; border-color: var(--color-accent-green);"
          onMouseDown=${(e) => {
            e.stopPropagation();
            onPortMouseDown(e, node.id, "true", false);
          }}
        >
          <span style="position: absolute; right: 14px; top: -3px; font-size: 0.6rem; font-weight: 800; color: var(--color-accent-green);">TRUE</span>
        </div>
        <div 
          className="port port-output" 
          style="top: 90px; right: -7px; border-color: #ef4444;"
          onMouseDown=${(e) => {
            e.stopPropagation();
            onPortMouseDown(e, node.id, "false", false);
          }}
        >
          <span style="position: absolute; right: 14px; top: -3px; font-size: 0.6rem; font-weight: 800; color: #ef4444;">FALSE</span>
        </div>
      `}
    </div>
  `;
}
