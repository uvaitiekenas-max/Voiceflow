import { h } from 'https://esm.sh/preact@10.19.6';
import { useState, useEffect, useRef } from 'https://esm.sh/preact/hooks@10.19.6';
import htm from 'https://esm.sh/htm@3.1.1';
import Canvas from './components/Canvas.js';
import Sidebar from './components/Sidebar.js';
import Inspector from './components/Inspector.js';
import Simulator from './components/Simulator.js';
import { templates } from './utils/templates.js';
import { interpolate, setDeepVariable, evaluateCondition, executeApiCall, executeAiCall } from './utils/flowExecutor.js';

const html = htm.bind(h);

// Helper to generate unique IDs
const generateId = (prefix) => `${prefix}-${Math.random().toString(36).substr(2, 9)}`;

export default function App() {
  // Canvas State: Nodes and connections
  const [nodes, setNodes] = useState([]);
  const [connections, setConnections] = useState([]);
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  
  // Connection drag indicators
  const [activePort, setActivePort] = useState(null);
  const [hoveredPort, setHoveredPort] = useState(null);

  // Simulator Runtime State
  const [simulatorOpen, setSimulatorOpen] = useState(true);
  const [isSimulating, setIsSimulating] = useState(false); // Typing loader
  const [activeNodeId, setActiveNodeId] = useState(null);
  const [variables, setVariables] = useState({});
  const [messages, setMessages] = useState([]);
  
  // Ref to keep track of variables inside async simulation loop
  const variablesRef = useRef({});
  useEffect(() => {
    variablesRef.current = variables;
  }, [variables]);

  // Load from local storage or default to Survey template
  useEffect(() => {
    const saved = localStorage.getItem('voiceflow_project');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setNodes(parsed.nodes || []);
        setConnections(parsed.connections || []);
      } catch (e) {
        loadTemplate("survey");
      }
    } else {
      loadTemplate("survey");
    }
  }, []);

  // Save to local storage on changes
  const saveWorkspace = () => {
    localStorage.setItem('voiceflow_project', JSON.stringify({ nodes, connections }));
  };

  useEffect(() => {
    if (nodes.length > 0) {
      saveWorkspace();
    }
  }, [nodes, connections]);

  // Template loader
  const loadTemplate = (templateKey) => {
    const template = templates[templateKey];
    if (template) {
      setNodes(JSON.parse(JSON.stringify(template.nodes)));
      setConnections(JSON.parse(JSON.stringify(template.connections)));
      setSelectedNodeId(null);
      resetSimulation();
      
      // Auto open simulator for immediate demonstration
      setSimulatorOpen(true);
    }
  };

  const clearWorkspace = () => {
    if (confirm("Are you sure you want to clear the entire canvas?")) {
      setNodes([]);
      setConnections([]);
      setSelectedNodeId(null);
      resetSimulation();
      localStorage.removeItem('voiceflow_project');
    }
  };

  // Node operations
  const handleAddNode = (type) => {
    const id = generateId(`node-${type}`);
    const nameMap = {
      start: "Start Node",
      speak: "Speak Prompt",
      choice: "Multi Branch",
      capture: "User Capture",
      set: "Set Variable",
      condition: "Evaluate logic",
      api: "External API Call",
      ai: "AI Prompt Generator"
    };

    const defaultData = {
      start: {},
      speak: { text: "Hello there! How can I assist you today? 🌟" },
      choice: { text: "Please select an option:", choices: ["Option A", "Option B"] },
      capture: { text: "Please enter your response:", variable: "user_input" },
      set: { variable: "score", expression: "10" },
      condition: { variable: "score", operator: "equals", value: "10" },
      api: { url: "https://api.github.com/users/uvaitiekenas-max", method: "GET", saveTo: "api_response" },
      ai: { prompt: "Generate a summary based on user details: {user_input}", saveTo: "ai_output" }
    };

    const newNode = {
      id,
      type,
      x: 150 + Math.random() * 50,
      y: 150 + Math.random() * 50,
      title: nameMap[type] || "New Step",
      data: defaultData[type] || {}
    };

    // If adding a Start block and one already exists, warn user
    if (type === "start" && nodes.some(n => n.type === "start")) {
      alert("A Start Block already exists! Only one entry point is allowed per conversational agent.");
      return;
    }

    setNodes(prev => [...prev, newNode]);
    setSelectedNodeId(newNode.id);
  };

  const handleMoveNode = (id, x, y) => {
    setNodes(prev => prev.map(n => n.id === id ? { ...n, x, y } : n));
  };

  const handleDeleteNode = (id) => {
    setNodes(prev => prev.filter(n => n.id !== id));
    // Clean up related connections
    setConnections(prev => prev.filter(c => c.fromNodeId !== id && c.toNodeId !== id));
    if (selectedNodeId === id) {
      setSelectedNodeId(null);
    }
    // If active simulating node gets deleted, reset simulation
    if (activeNodeId === id) {
      resetSimulation();
    }
  };

  const handleChangeNodeTitle = (id, title) => {
    setNodes(prev => prev.map(n => n.id === id ? { ...n, title } : n));
  };

  const handleChangeNodeData = (id, data) => {
    setNodes(prev => prev.map(n => {
      if (n.id === id) {
        // Handle choice removals: delete redundant connections
        if (n.type === "choice" && n.data.choices && data.choices) {
          const oldLen = n.data.choices.length;
          const newLen = data.choices.length;
          if (newLen < oldLen) {
            // Choices were removed, clean up ports
            setConnections(curr => curr.filter(c => {
              if (c.fromNodeId === id && c.fromPortId.startsWith("choice-")) {
                const choiceIdx = parseInt(c.fromPortId.replace("choice-", ""));
                return choiceIdx < newLen;
              }
              return true;
            }));
          }
        }
        return { ...n, data };
      }
      return n;
    }));
  };

  // Connection operations
  const handleAddConnection = (conn) => {
    const id = generateId("conn");
    const newConn = { id, ...conn };
    
    // Rule check: Output port can only have ONE outgoing line.
    // If connection exists from the same fromNodeId + fromPortId, remove it.
    setConnections(prev => {
      const filtered = prev.filter(c => !(c.fromNodeId === conn.fromNodeId && c.fromPortId === conn.fromPortId));
      return [...filtered, newConn];
    });
  };

  const handleRemoveConnection = (connId) => {
    setConnections(prev => prev.filter(c => c.id !== connId));
  };

  // Export flow as JSON file
  const exportFlow = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({ nodes, connections }, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `voiceflow_agent_${new Date().toISOString().slice(0, 10)}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  // Import flow from JSON file
  const importFlow = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const parsed = JSON.parse(event.target.result);
        if (Array.isArray(parsed.nodes) && Array.isArray(parsed.connections)) {
          setNodes(parsed.nodes);
          setConnections(parsed.connections);
          setSelectedNodeId(null);
          resetSimulation();
          alert("Flow imported successfully!");
        } else {
          alert("Invalid flow format: file must contain 'nodes' and 'connections' arrays.");
        }
      } catch (err) {
        alert("Failed to parse file: Make sure it's valid JSON.");
      }
    };
    reader.readAsText(file);
    e.target.value = null; // Reset input element
  };

  // --- SIMULATOR EXECUTION CONTROLLER ---
  const addMessage = (text, sender) => {
    const now = new Date();
    const timestamp = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    setMessages(prev => [...prev, { text, sender, timestamp }]);
  };

  const resetSimulation = () => {
    setVariables({});
    setMessages([]);
    setActiveNodeId(null);
    setIsSimulating(false);
  };

  const startSimulation = () => {
    resetSimulation();
    const startNode = nodes.find(n => n.type === "start");
    if (!startNode) {
      alert("Cannot start simulation: Place a Start Block on the canvas first!");
      return;
    }
    
    // Add greetings log
    addMessage("Simulator session started.", "bot");
    executeNode(startNode.id, {});
  };

  // Execute individual Node logic
  const executeNode = async (nodeId, currentVars) => {
    const node = nodes.find(n => n.id === nodeId);
    if (!node) {
      setIsSimulating(false);
      addMessage("Conversation finished. No further blocks linked.", "bot");
      setActiveNodeId(null);
      return;
    }

    setActiveNodeId(nodeId);
    setIsSimulating(true);
    
    // Delay to simulate typing & network calls naturally
    const sleep = (ms) => new Promise(res => setTimeout(res, ms));

    try {
      if (node.type === "start") {
        await sleep(400);
        // Find default connection from start node
        const conn = connections.find(c => c.fromNodeId === nodeId);
        if (conn) {
          executeNode(conn.toNodeId, currentVars);
        } else {
          setIsSimulating(false);
          addMessage("Start block has no outgoing connection.", "bot");
        }
      } 
      
      else if (node.type === "speak") {
        await sleep(800);
        const resolvedText = interpolate(node.data.text || "", currentVars);
        addMessage(resolvedText, "bot");
        
        setIsSimulating(false);
        // Move to next node
        const conn = connections.find(c => c.fromNodeId === nodeId && c.fromPortId === "default");
        if (conn) {
          executeNode(conn.toNodeId, currentVars);
        } else {
          addMessage("End of path.", "bot");
          setActiveNodeId(null);
        }
      } 
      
      else if (node.type === "capture") {
        await sleep(600);
        const resolvedText = interpolate(node.data.text || "Please reply:", currentVars);
        addMessage(resolvedText, "bot");
        setIsSimulating(false);
        // Pause and wait for user text input.
        // Simulator.js will capture user reply, call onCaptureSubmit, which resumes.
      } 
      
      else if (node.type === "set") {
        await sleep(300);
        const interpolatedExpr = interpolate(node.data.expression || "", currentVars);
        const newVars = { ...currentVars };
        setDeepVariable(newVars, node.data.variable || "var", interpolatedExpr);
        setVariables(newVars);
        
        // Immediate transition
        const conn = connections.find(c => c.fromNodeId === nodeId && c.fromPortId === "default");
        if (conn) {
          executeNode(conn.toNodeId, newVars);
        } else {
          setIsSimulating(false);
          addMessage("Variables set. End of path.", "bot");
          setActiveNodeId(null);
        }
      } 
      
      else if (node.type === "condition") {
        await sleep(600);
        const outcome = evaluateCondition(node.data, currentVars);
        const portId = outcome ? "true" : "false";
        
        const conn = connections.find(c => c.fromNodeId === nodeId && c.fromPortId === portId);
        if (conn) {
          executeNode(conn.toNodeId, currentVars);
        } else {
          setIsSimulating(false);
          addMessage(`Logic evaluated to: ${portId.toUpperCase()}. No block is linked to the ${portId} output.`, "bot");
          setActiveNodeId(null);
        }
      } 
      
      else if (node.type === "api") {
        await sleep(1000); // Simulate API call latency
        addMessage(`🔗 Connecting to endpoint API...`, "bot");
        const apiResponse = await executeApiCall(node.data, currentVars);
        
        const newVars = { ...currentVars };
        setDeepVariable(newVars, node.data.saveTo || "api_response", apiResponse);
        setVariables(newVars);
        
        addMessage(`✅ Response successfully saved to {${node.data.saveTo || "api_response"}}.`, "bot");
        
        const conn = connections.find(c => c.fromNodeId === nodeId && c.fromPortId === "default");
        if (conn) {
          executeNode(conn.toNodeId, newVars);
        } else {
          setIsSimulating(false);
          setActiveNodeId(null);
        }
      } 
      
      else if (node.type === "ai") {
        await sleep(1200); // Simulate AI generation wait
        addMessage(`✨ Thinking... Prompting LLM Model`, "bot");
        const generatedText = executeAiCall(node.data, currentVars);
        
        const newVars = { ...currentVars };
        setDeepVariable(newVars, node.data.saveTo || "ai_output", generatedText);
        setVariables(newVars);
        
        addMessage(`✍️ AI response generated and stored.`, "bot");
        
        const conn = connections.find(c => c.fromNodeId === nodeId && c.fromPortId === "default");
        if (conn) {
          executeNode(conn.toNodeId, newVars);
        } else {
          setIsSimulating(false);
          setActiveNodeId(null);
        }
      } 
      
      else if (node.type === "choice") {
        await sleep(600);
        if (node.data.text) {
          addMessage(interpolate(node.data.text, currentVars), "bot");
        }
        setIsSimulating(false);
        // Pause and wait for choice selection.
        // Simulator.js will render buttons, clicking calling onChoiceSelect, which resumes.
      }
    } catch (err) {
      console.error(err);
      setIsSimulating(false);
      addMessage(`⚠️ Execution error at block "${node.title}": ${err.message}`, "bot");
      setActiveNodeId(null);
    }
  };

  // Submit User Capture (textbox input)
  const handleCaptureSubmit = (text) => {
    const node = nodes.find(n => n.id === activeNodeId);
    if (!node || node.type !== "capture") return;

    addMessage(text, "user");
    
    // Save to variable
    const varName = node.data.variable || "user_input";
    const newVars = { ...variables };
    setDeepVariable(newVars, varName, text);
    setVariables(newVars);

    // Proceed to next node
    const conn = connections.find(c => c.fromNodeId === activeNodeId && c.fromPortId === "default");
    if (conn) {
      executeNode(conn.toNodeId, newVars);
    } else {
      addMessage("End of path.", "bot");
      setActiveNodeId(null);
    }
  };

  // Select User Choice Option (button click)
  const handleChoiceSelect = (choiceIndex, choiceText) => {
    const node = nodes.find(n => n.id === activeNodeId);
    if (!node || node.type !== "choice") return;

    addMessage(choiceText, "user");

    // Proceed to node connected to selected choice port
    const portId = `choice-${choiceIndex}`;
    const conn = connections.find(c => c.fromNodeId === activeNodeId && c.fromPortId === portId);
    
    if (conn) {
      executeNode(conn.toNodeId, variables);
    } else {
      addMessage(`No block connected to choice "${choiceText}". Path ended.`, "bot");
      setActiveNodeId(null);
    }
  };

  // Retrieve current active nodes for simulator component
  const currentChoiceNode = activeNodeId ? nodes.find(n => n.id === activeNodeId && n.type === "choice") : null;
  const currentCaptureNode = activeNodeId ? nodes.find(n => n.id === activeNodeId && n.type === "capture") : null;
  const executingNode = activeNodeId ? nodes.find(n => n.id === activeNodeId) : null;
  const selectedNode = selectedNodeId ? nodes.find(n => n.id === selectedNodeId) : null;

  return html`
    <div style="display: flex; flex-direction: column; height: 100vh; overflow: hidden; background-color: var(--bg-deep);">
      <header className="app-header">
        <div className="logo-container">
          <svg className="logo-icon" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            <line x1="12" x2="12" y1="19" y2="22"></line>
          </svg>
          <span className="logo-text">Voiceflow Visual Builder</span>
          <span className="node-header-badge" style="background: rgba(139, 92, 246, 0.15); color: var(--color-primary); font-size: 0.65rem; border: 1px solid var(--border-glow);">
            PRO CANVAS
          </span>
        </div>
        
        <div className="header-actions">
          <label className="btn" style="cursor: pointer;">
            <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            Import JSON
            <input type="file" accept=".json" onChange=${importFlow} style="display: none;" />
          </label>
          
          <button className="btn" onClick=${exportFlow} title="Export workspace flow as JSON file">
            <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Export JSON
          </button>

          <button className="btn btn-primary" onClick=${startSimulation}>
            <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
            Play Agent
          </button>
        </div>
      </header>

      <div className="app-container">
        <${Sidebar}
          onAddNodeClick=${handleAddNode}
          onLoadTemplate=${loadTemplate}
          onClearCanvas=${clearWorkspace}
        />

        <${Canvas}
          nodes=${nodes}
          connections=${connections}
          selectedNodeId=${selectedNodeId}
          executingNodeId=${activeNodeId}
          onSelectNode=${setSelectedNodeId}
          onAddConnection=${handleAddConnection}
          onRemoveConnection=${handleRemoveConnection}
          onMoveNode=${handleMoveNode}
          onDblClickCanvas=${(x, y) => {
            const id = generateId("node-speak");
            const newNode = {
              id,
              type: "speak",
              x,
              y,
              title: "Speak Prompt",
              data: { text: "Double click to write response text..." }
            };
            setNodes(prev => [...prev, newNode]);
            setSelectedNodeId(id);
          }}
          activePort=${activePort}
          setActivePort=${setActivePort}
          hoveredPort=${hoveredPort}
          setHoveredPort=${setHoveredPort}
        />

        <${Inspector}
          selectedNode=${selectedNode}
          onChangeNodeData=${handleChangeNodeData}
          onChangeNodeTitle=${handleChangeNodeTitle}
          onDeleteNode=${handleDeleteNode}
        />

        <${Simulator}
          isOpen=${simulatorOpen}
          onClose=${() => setSimulatorOpen(false)}
          messages=${messages}
          variables=${variables}
          currentChoiceNode=${currentChoiceNode}
          currentCaptureNode=${currentCaptureNode}
          isExecuting=${isSimulating}
          onChoiceSelect=${handleChoiceSelect}
          onCaptureSubmit=${handleCaptureSubmit}
          onReset=${startSimulation}
          executingNodeTitle=${executingNode ? executingNode.title : ""}
        />

        <button 
          className="simulator-toggle-fab ${simulatorOpen ? 'active' : ''}"
          onClick=${() => setSimulatorOpen(true)}
          title="Open testing console"
        >
          <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </button>
      </div>
    </div>
  `;
}

