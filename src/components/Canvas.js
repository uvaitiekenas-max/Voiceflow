import { h } from 'https://esm.sh/preact@10.19.6';
import { useState, useRef, useEffect } from 'https://esm.sh/preact/hooks@10.19.6';
import htm from 'https://esm.sh/htm@3.1.1';
import Node, { getNodePortCoordinates } from './Node.js';

const html = htm.bind(h);

// Bezier Curve calculation for connection lines
function getBezierPath(x1, y1, x2, y2) {
  const dx = Math.abs(x2 - x1);
  // Control points horizontal offset
  const cx1 = x1 + Math.max(dx * 0.5, 40);
  const cx2 = x2 - Math.max(dx * 0.5, 40);
  return `M ${x1} ${y1} C ${cx1} ${y1}, ${cx2} ${y2}, ${x2} ${y2}`;
}

export default function Canvas({
  nodes,
  connections,
  selectedNodeId,
  executingNodeId,
  onSelectNode,
  onAddConnection,
  onRemoveConnection,
  onMoveNode,
  onDblClickCanvas,
  activePort,
  setActivePort,
  hoveredPort,
  setHoveredPort
}) {
  const canvasRef = useRef(null);
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 100, y: 50 }); // Start with a nice offset
  const [isPanning, setIsPanning] = useState(false);
  const [draggedNodeId, setDraggedNodeId] = useState(null);
  
  // Ref to track latest drag offsets
  const dragOffsetRef = useRef({ x: 0, y: 0 });
  const panStartRef = useRef({ x: 0, y: 0 });
  const mousePosRef = useRef({ x: 0, y: 0 }); // In client space
  
  // Track temporary connection drag
  const [tempLineEnd, setTempLineEnd] = useState(null);

  // Zoom handlers
  const handleWheel = (e) => {
    e.preventDefault();
    const zoomFactor = 0.05;
    let newZoom = zoom;
    if (e.deltaY < 0) {
      newZoom = Math.min(zoom + zoomFactor, 2);
    } else {
      newZoom = Math.max(zoom - zoomFactor, 0.4);
    }
    
    // Zoom centered on mouse pointer
    if (canvasRef.current) {
      const rect = canvasRef.current.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;
      
      const canvasMouseX = (mouseX - pan.x) / zoom;
      const canvasMouseY = (mouseY - pan.y) / zoom;
      
      setPan({
        x: mouseX - canvasMouseX * newZoom,
        y: mouseY - canvasMouseY * newZoom
      });
      setZoom(newZoom);
    }
  };

  // Reset zoom & pan
  const resetViewport = () => {
    setZoom(1);
    setPan({ x: 100, y: 50 });
  };

  const zoomIn = () => {
    setZoom(prev => Math.min(prev + 0.1, 2));
  };

  const zoomOut = () => {
    setZoom(prev => Math.max(prev - 0.1, 0.4));
  };

  // Node Drag Handlers
  const handleNodeDragStart = (e, nodeId) => {
    e.stopPropagation();
    const node = nodes.find(n => n.id === nodeId);
    if (!node) return;

    if (canvasRef.current) {
      const rect = canvasRef.current.getBoundingClientRect();
      // Get pointer position in canvas space
      const canvasX = (e.clientX - rect.left - pan.x) / zoom;
      const canvasY = (e.clientY - rect.top - pan.y) / zoom;
      
      dragOffsetRef.current = {
        x: canvasX - node.x,
        y: canvasY - node.y
      };
      setDraggedNodeId(nodeId);
    }
  };

  // Port Mouse down starts line drag
  const handlePortMouseDown = (e, nodeId, portId, isInput) => {
    e.stopPropagation();
    setActivePort({ nodeId, portId, isInput });
    
    // Set initial mouse pos in canvas space
    if (canvasRef.current) {
      const rect = canvasRef.current.getBoundingClientRect();
      const canvasX = (e.clientX - rect.left - pan.x) / zoom;
      const canvasY = (e.clientY - rect.top - pan.y) / zoom;
      setTempLineEnd({ x: canvasX, y: canvasY });
    }
  };

  // Mouse Move Orchestrator (Canvas Panning, Node Dragging, Connection Drawing)
  const handleMouseMove = (e) => {
    if (canvasRef.current) {
      const rect = canvasRef.current.getBoundingClientRect();
      const canvasX = (e.clientX - rect.left - pan.x) / zoom;
      const canvasY = (e.clientY - rect.top - pan.y) / zoom;
      
      mousePosRef.current = { x: e.clientX, y: e.clientY };

      if (isPanning) {
        setPan({
          x: e.clientX - panStartRef.current.x,
          y: e.clientY - panStartRef.current.y
        });
      } else if (draggedNodeId) {
        // Compute new coordinates with simple grid snapping (12px)
        const snap = 12;
        const newRawX = canvasX - dragOffsetRef.current.x;
        const newRawY = canvasY - dragOffsetRef.current.y;
        
        const newX = Math.round(newRawX / snap) * snap;
        const newY = Math.round(newRawY / snap) * snap;
        
        onMoveNode(draggedNodeId, newX, newY);
      } else if (activePort) {
        setTempLineEnd({ x: canvasX, y: canvasY });
      }
    }
  };

  // Mouse Up Orchestrator
  const handleMouseUp = (e) => {
    if (isPanning) {
      setIsPanning(false);
    }
    
    if (draggedNodeId) {
      setDraggedNodeId(null);
    }
    
    if (activePort) {
      // Connect if released over a valid target port
      if (hoveredPort && hoveredPort.nodeId !== activePort.nodeId) {
        // Ensure connection goes from Output to Input
        const source = activePort.isInput ? hoveredPort : activePort;
        const target = activePort.isInput ? activePort : hoveredPort;
        
        if (!source.isInput && target.isInput) {
          onAddConnection({
            fromNodeId: source.nodeId,
            fromPortId: source.portId,
            toNodeId: target.nodeId,
            toPortId: target.portId
          });
        }
      }
      setActivePort(null);
      setTempLineEnd(null);
    }
  };

  // Start Canvas Pan
  const handleMouseDown = (e) => {
    // Left click on empty canvas starts panning
    if (e.button === 0 && e.target.classList.contains('grid-bg')) {
      setIsPanning(true);
      panStartRef.current = {
        x: e.clientX - pan.x,
        y: e.clientY - pan.y
      };
      onSelectNode(null); // Deselect
    }
  };

  // Double click canvas to add a new Node
  const handleDblClick = (e) => {
    if (e.target.classList.contains('grid-bg') && canvasRef.current) {
      const rect = canvasRef.current.getBoundingClientRect();
      const canvasX = (e.clientX - rect.left - pan.x) / zoom;
      const canvasY = (e.clientY - rect.top - pan.y) / zoom;
      onDblClickCanvas(canvasX - 125, canvasY - 50); // Center the node card (250px wide, ~100px high)
    }
  };

  // Compute actual coordinates of ports on canvas
  const getPortCoords = (nodeId, portId) => {
    const node = nodes.find(n => n.id === nodeId);
    if (!node) return { x: 0, y: 0 };
    
    const { ports } = getNodePortCoordinates(node);
    return ports[portId] || { x: node.x, y: node.y };
  };

  // Connect port hover listeners for reliable targeting
  useEffect(() => {
    const handleMouseOverPort = (e) => {
      const portEl = e.target.closest('.port');
      if (portEl && activePort) {
        // Find which node and port this belongs to
        const nodeEl = portEl.closest('.node-element');
        if (nodeEl) {
          const domId = nodeEl.id; // dom-node-id
          const nodeId = domId.replace('dom-', '');
          const isInput = portEl.classList.contains('port-input');
          
          // Determine portId
          let portId = "default";
          if (isInput) {
            portId = "input";
          } else if (portEl.classList.contains('choice-port')) {
            // Find choice index
            const rows = Array.from(nodeEl.querySelectorAll('.choice-port-row'));
            const rowIndex = rows.findIndex(row => row.contains(portEl));
            if (rowIndex !== -1) {
              portId = `choice-${rowIndex}`;
            }
          } else {
            // Check condition ports
            const styleTop = portEl.style.top;
            if (styleTop === "54px") portId = "true";
            else if (styleTop === "90px") portId = "false";
          }
          
          setHoveredPort({ nodeId, portId, isInput });
        }
      }
    };

    const handleMouseLeavePort = (e) => {
      if (e.target.closest('.port')) {
        setHoveredPort(null);
      }
    };

    document.addEventListener('mouseover', handleMouseOverPort);
    document.addEventListener('mouseout', handleMouseLeavePort);
    
    return () => {
      document.removeEventListener('mouseover', handleMouseOverPort);
      document.removeEventListener('mouseout', handleMouseLeavePort);
    };
  }, [activePort]);

  return html`
    <div 
      className="canvas-container"
      ref=${canvasRef}
      onWheel=${handleWheel}
      onMouseMove=${handleMouseMove}
      onMouseDown=${handleMouseDown}
      onMouseUp=${handleMouseUp}
      onDblClick=${handleDblClick}
    >
      <div 
        className="canvas-grid"
        style="transform: translate(${pan.x}px, ${pan.y}px) scale(${zoom});"
      >
        <div className="grid-bg"></div>

        <svg className="svg-connections-overlay">
          <defs>
            <linearGradient id="gradient-primary" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#8b5cf6" />
              <stop offset="100%" stop-color="#06b6d4" />
            </linearGradient>
            <linearGradient id="gradient-executing" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.8" />
              <stop offset="100%" stop-color="#ec4899" stop-opacity="0.8" />
            </linearGradient>
          </defs>

          ${connections.map(conn => {
            const start = getPortCoords(conn.fromNodeId, conn.fromPortId);
            const end = getPortCoords(conn.toNodeId, conn.toPortId);
            const pathData = getBezierPath(start.x, start.y, end.x, end.y);
            
            const isExecutingPath = executingNodeId === conn.fromNodeId;
            const isSelectedNodePath = selectedNodeId === conn.fromNodeId || selectedNodeId === conn.toNodeId;

            return html`
              <g key=${conn.id} className="connection-group">
                <path
                  d=${pathData}
                  fill="none"
                  stroke="transparent"
                  strokeWidth="14"
                  style="cursor: pointer; pointer-events: stroke;"
                  onDblClick=${(e) => {
                    e.stopPropagation();
                    onRemoveConnection(conn.id);
                  }}
                  title="Double click line to delete"
                />
                
                <path
                  d=${pathData}
                  className="connection-path ${isSelectedNodePath ? 'active' : ''} ${isExecutingPath ? 'executing' : ''}"
                />
                
                ${(isExecutingPath || isSelectedNodePath) && html`
                  <path
                    d=${pathData}
                    className="connection-pulse"
                  />
                `}
              </g>
            `;
          })}

          ${activePort && tempLineEnd && (() => {
            const start = getPortCoords(activePort.nodeId, activePort.portId);
            const p1 = activePort.isInput ? tempLineEnd : start;
            const p2 = activePort.isInput ? start : tempLineEnd;
            const pathData = getBezierPath(p1.x, p1.y, p2.x, p2.y);
            
            return html`
              <path
                d=${pathData}
                fill="none"
                stroke="var(--color-primary)"
                stroke-width="3"
                stroke-dasharray="6,4"
                style="opacity: 0.8"
              />
            `;
          })()}
        </svg>

        ${nodes.length === 0 && html`
          <div className="canvas-empty-state">
            <svg className="empty-state-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div className="empty-state-title">Empty Canvas</div>
            <div className="empty-state-desc">
              Drag nodes from the left sidebar palette or double-click anywhere to spawn steps.
            </div>
          </div>
        `}

        ${nodes.map(node => html`
          <${Node}
            key=${node.id}
            node=${node}
            isSelected=${selectedNodeId === node.id}
            isExecuting=${executingNodeId === node.id}
            onSelect=${onSelectNode}
            onNodeDragStart=${handleNodeDragStart}
            onPortMouseDown=${handlePortMouseDown}
          />
        `)}
      </div>

      <div className="canvas-controls">
        <button className="control-btn" onClick=${zoomIn} title="Zoom In">
          <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg>
        </button>
        <span className="control-zoom-indicator">${Math.round(zoom * 100)}%</span>
        <button className="control-btn" onClick=${zoomOut} title="Zoom Out">
          <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14"/></svg>
        </button>
        <button className="control-btn" onClick=${resetViewport} title="Reset Viewport">
          <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>
        </button>
      </div>
    </div>
  `;
}

