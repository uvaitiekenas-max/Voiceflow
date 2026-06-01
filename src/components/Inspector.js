import { h } from 'https://esm.sh/preact@10.19.6';
import htm from 'https://esm.sh/htm@3.1.1';

const html = htm.bind(h);

export default function Inspector({
  selectedNode,
  onChangeNodeData,
  onChangeNodeTitle,
  onDeleteNode
}) {
  if (!selectedNode) {
    return html`
      <div className="app-inspector">
        <div className="inspector-header">
          <div className="inspector-title">Properties</div>
        </div>
        <div className="variables-empty-state" style="padding: 24px;">
          <svg className="empty-state-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="width: 48px; height: 48px;">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
          </svg>
          <div style="font-weight: 600; color: var(--color-text-muted);">No Block Selected</div>
          <div style="font-size: 0.75rem; color: var(--color-text-dark); max-width: 180px;">Select a node card on the canvas to configure its settings.</div>
        </div>
      </div>
    `;
  }

  const handleTitleChange = (e) => {
    onChangeNodeTitle(selectedNode.id, e.target.value);
  };

  const handleDataChange = (key, value) => {
    onChangeNodeData(selectedNode.id, {
      ...selectedNode.data,
      [key]: value
    });
  };

  // Choice specific actions
  const handleChoiceChange = (index, value) => {
    const newChoices = [...(selectedNode.data.choices || [])];
    newChoices[index] = value;
    handleDataChange("choices", newChoices);
  };

  const handleAddChoice = () => {
    const newChoices = [...(selectedNode.data.choices || []), "New Choice"];
    handleDataChange("choices", newChoices);
  };

  const handleRemoveChoice = (index) => {
    const newChoices = (selectedNode.data.choices || []).filter((_, i) => i !== index);
    handleDataChange("choices", newChoices);
  };

  const renderContent = () => {
    switch (selectedNode.type) {
      case "start":
        return html`
          <div className="variables-empty-state" style="height: 120px;">
            <div style="font-size: 0.75rem; color: var(--color-text-muted);">The Start Block has no configuration. Connect it to your first conversational step to begin.</div>
          </div>
        `;
        
      case "speak":
        return html`
          <div className="inspector-field">
            <label className="field-label">Speak Text</label>
            <textarea
              className="textarea-input"
              value=${selectedNode.data.text || ""}
              onInput=${(e) => handleDataChange("text", e.target.value)}
              placeholder="What should the bot say? Supports variables like {user_name}"
            />
          </div>
        `;
        
      case "capture":
        return html`
          <div className="inspector-field">
            <label className="field-label">Question Prompt</label>
            <textarea
              className="textarea-input"
              value=${selectedNode.data.text || ""}
              onInput=${(e) => handleDataChange("text", e.target.value)}
              placeholder="E.g., What is your email address?"
            />
          </div>
          <div className="inspector-field">
            <label className="field-label">Store Response In Variable</label>
            <input
              type="text"
              className="input-text"
              value=${selectedNode.data.variable || ""}
              onInput=${(e) => handleDataChange("variable", e.target.value.replace(/[^a-zA-Z0-9_]/g, ""))}
              placeholder="e.g. user_email"
            />
            <span style="font-size: 0.65rem; color: var(--color-text-dark);">Variable name should be alphanumeric.</span>
          </div>
        `;
        
      case "set":
        return html`
          <div className="inspector-field">
            <label className="field-label">Variable Name</label>
            <input
              type="text"
              className="input-text"
              value=${selectedNode.data.variable || ""}
              onInput=${(e) => handleDataChange("variable", e.target.value.replace(/[^a-zA-Z0-9_\.]/g, ""))}
              placeholder="e.g. user_score"
            />
          </div>
          <div className="inspector-field">
            <label className="field-label">Expression / Value</label>
            <input
              type="text"
              className="input-text"
              value=${selectedNode.data.expression || ""}
              onInput=${(e) => handleDataChange("expression", e.target.value)}
              placeholder="e.g. 100 or true or Guest"
            />
            <span style="font-size: 0.65rem; color: var(--color-text-dark);">Can reference other variables like {name}.</span>
          </div>
        `;
        
      case "condition":
        return html`
          <div className="inspector-field">
            <label className="field-label">Variable to Evaluate</label>
            <input
              type="text"
              className="input-text"
              value=${selectedNode.data.variable || ""}
              onInput=${(e) => handleDataChange("variable", e.target.value)}
              placeholder="e.g. score or github_data.name"
            />
          </div>
          <div className="inspector-field">
            <label className="field-label">Operator</label>
            <select
              className="select-input"
              value=${selectedNode.data.operator || "equals"}
              onChange=${(e) => handleDataChange("operator", e.target.value)}
            >
              <option value="exists">Exists / Is Set</option>
              <option value="equals">Equals (==)</option>
              <option value="not_equals">Does Not Equal (!=)</option>
              <option value="contains">Contains Substring</option>
              <option value="greater_than">Greater Than (&gt;)</option>
              <option value="less_than">Less Than (&lt;)</option>
            </select>
          </div>
          
          ${selectedNode.data.operator !== "exists" && html`
            <div className="inspector-field">
              <label className="field-label">Comparison Value</label>
              <input
                type="text"
                className="input-text"
                value=${selectedNode.data.value || ""}
                onInput=${(e) => handleDataChange("value", e.target.value)}
                placeholder="e.g. 50 or Gold"
              />
            </div>
          `}
        `;
        
      case "api":
        return html`
          <div className="inspector-field">
            <label className="field-label">HTTP Method</label>
            <select
              className="select-input"
              value=${selectedNode.data.method || "GET"}
              onChange=${(e) => handleDataChange("method", e.target.value)}
            >
              <option value="GET">GET</option>
              <option value="POST">POST</option>
              <option value="PUT">PUT</option>
              <option value="DELETE">DELETE</option>
            </select>
          </div>
          <div className="inspector-field">
            <label className="field-label">Request URL</label>
            <input
              type="text"
              className="input-text"
              value=${selectedNode.data.url || ""}
              onInput=${(e) => handleDataChange("url", e.target.value)}
              placeholder="https://api.github.com/users/{username}"
            />
            <span style="font-size: 0.65rem; color: var(--color-text-dark);">Can interpolate variables using {var_name}.</span>
          </div>
          <div className="inspector-field">
            <label className="field-label">Save JSON Response To</label>
            <input
              type="text"
              className="input-text"
              value=${selectedNode.data.saveTo || ""}
              onInput=${(e) => handleDataChange("saveTo", e.target.value.replace(/[^a-zA-Z0-9_]/g, ""))}
              placeholder="e.g. api_data"
            />
          </div>
        `;
        
      case "ai":
        return html`
          <div className="inspector-field">
            <label className="field-label">System / User Prompt Template</label>
            <textarea
              className="textarea-input"
              style="min-height: 120px;"
              value=${selectedNode.data.prompt || ""}
              onInput=${(e) => handleDataChange("prompt", e.target.value)}
              placeholder="e.g. Write a paragraph summarizing {api_data.bio} in the voice of a pirate."
            />
          </div>
          <div className="inspector-field">
            <label className="field-label">Save AI Text Response To</label>
            <input
              type="text"
              className="input-text"
              value=${selectedNode.data.saveTo || ""}
              onInput=${(e) => handleDataChange("saveTo", e.target.value.replace(/[^a-zA-Z0-9_]/g, ""))}
              placeholder="e.g. ai_summary"
            />
          </div>
        `;
        
      case "choice":
        return html`
          <div className="inspector-field">
            <label className="field-label">Choice Question Prompt</label>
            <input
              type="text"
              className="input-text"
              value=${selectedNode.data.text || ""}
              onInput=${(e) => handleDataChange("text", e.target.value)}
              placeholder="Choose a path below:"
            />
          </div>
          <div className="inspector-field">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <label className="field-label" style="margin: 0;">Paths / Choices</label>
              <button 
                className="btn btn-accent" 
                style="padding: 4px 8px; font-size: 0.7rem; border-radius: 4px;"
                onClick=${handleAddChoice}
              >
                + Add
              </button>
            </div>
            <div className="choices-editor-list">
              ${(selectedNode.data.choices || []).map((choice, idx) => html`
                <div key=${idx} className="choice-editor-item">
                  <input
                    type="text"
                    className="input-text"
                    style="flex: 1; padding: 6px 10px; font-size: 0.8rem;"
                    value=${choice}
                    onInput=${(e) => handleChoiceChange(idx, e.target.value)}
                  />
                  <button 
                    className="btn btn-outline-danger" 
                    style="padding: 6px; border-radius: 6px;"
                    onClick=${() => handleRemoveChoice(idx)}
                    title="Remove choice"
                  >
                    <svg width="12" height="12" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6" />
                    </svg>
                  </button>
                </div>
              `)}
            </div>
          </div>
        `;
        
      default:
        return null;
    }
  };

  return html`
    <div className="app-inspector">
      <div className="inspector-header">
        <div className="inspector-title" style="display: flex; align-items: center; gap: 8px;">
          <span>Block Config</span>
          <span className="node-header-badge" style="font-size: 0.6rem;">${selectedNode.type}</span>
        </div>
        <button 
          className="btn btn-outline-danger" 
          style="padding: 6px;"
          onClick=${() => onDeleteNode(selectedNode.id)}
          title="Delete selected block"
        >
          <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6M4 7h16" />
          </svg>
        </button>
      </div>

      <div className="inspector-body">
        <div className="inspector-field">
          <label className="field-label">Block Name</label>
          <input
            type="text"
            className="input-text"
            value=${selectedNode.title || ""}
            onInput=${handleTitleChange}
            placeholder="e.g. Intro Prompt"
          />
        </div>
        
        <hr style="border: 0; border-top: 1px solid var(--border-light); margin: 4px 0;" />

        ${renderContent()}
      </div>
    </div>
  `;
}
