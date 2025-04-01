import React, { useState, useEffect, useRef } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
// import ReactTooltip from 'react-tooltip'; // Remove or comment out if unused

function DataTraceabilityGraph({
  apiEndpoint = '',
  method = 'GET',
  requestData = {},
  responseData = {},
  statusCode = 0,
  status = 'idle', // idle, loading, success, error
  validationPassed = true,
  validationMessage = '',
  title = 'Data Flow Traceability'
}) {
  const fgRef = useRef();
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [expandedNode, setExpandedNode] = useState(null);
  const [animationTime, setAnimationTime] = useState(0);
  const [currentStage, setCurrentStage] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setAnimationTime((prev) => prev + 1);
    }, 30);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const nodes = [
      {
        id: 'user-action',
        label: 'User Action',
        group: 1,
        stage: 1,
        active: true,
        details: 'User initiated API request'
      },
      {
        id: 'api-request',
        label: 'API Request Sent',
        group: 2,
        stage: 2,
        active: status !== 'idle',
        details: { endpoint: apiEndpoint, method, requestData }
      },
      {
        id: 'api-processing',
        label: 'API Processing',
        group: 2,
        stage: 3,
        active: status === 'loading' || status === 'success' || status === 'error',
        isAI: true,
        details: 'Server processing request'
      },
      {
        id: 'api-response',
        label: 'API Response Received',
        group: 2,
        stage: 4,
        active: status === 'success' || status === 'error',
        error: status === 'error',
        details: { statusCode, responseData }
      },
      {
        id: 'data-validation',
        label: 'Data Validation',
        group: 3,
        stage: 5,
        active: status === 'success',
        error: !validationPassed && status === 'success',
        details: validationPassed ? 'Validation passed' : validationMessage
      },
      {
        id: 'ui-update',
        label: 'UI Updated',
        group: 3,
        stage: 6,
        active: status === 'success' && validationPassed,
        details: 'UI updated with validated data'
      }
    ];

    const links = [
      { source: 'user-action', target: 'api-request', active: status !== 'idle' },
      {
        source: 'api-request',
        target: 'api-processing',
        active: status === 'loading' || status === 'success' || status === 'error'
      },
      {
        source: 'api-processing',
        target: 'api-response',
        active: status === 'success' || status === 'error'
      },
      {
        source: 'api-response',
        target: 'data-validation',
        active: status === 'success'
      },
      {
        source: 'data-validation',
        target: 'ui-update',
        active: status === 'success' && validationPassed
      }
    ];

    if (status === 'idle') setCurrentStage(1);
    else if (status === 'loading') setCurrentStage(3);
    else if (status === 'success') setCurrentStage(validationPassed ? 6 : 5);
    else if (status === 'error') setCurrentStage(4);

    setGraphData({ nodes, links });

    if (fgRef.current && fgRef.current.zoomToFit) {
      setTimeout(() => {
        fgRef.current.zoomToFit(400);
      }, 500);
    }
  }, [
    apiEndpoint,
    method,
    requestData,
    responseData,
    status,
    statusCode,
    validationPassed,
    validationMessage
  ]);

  const nodeColors = {
    1: '#FFC300',
    2: '#F86B03',
    3: '#800000'
  };

  const getNodeTooltip = (node) => {
    let tooltip = '<div style="padding: 10px; background: rgba(0,0,0,0.8); color: white; border-radius: 4px; max-width: 250px;">';
    tooltip += '<div style="font-weight: bold; margin-bottom: 5px; color: ' + (nodeColors[node.group] || '#CCCCCC') + ';">' + node.label + '</div>';

    if (typeof node.details === 'object') {
      if (node.id === 'api-request') {
        tooltip += '<div>Endpoint: ' + node.details.endpoint + '</div>';
        tooltip += '<div>Method: ' + node.details.method + '</div>';
        tooltip += '<div>Click to view request data</div>';
      } else if (node.id === 'api-response') {
        tooltip += '<div>Status Code: ' + (node.details.statusCode || 'N/A') + '</div>';
        tooltip += '<div>Click to view response data</div>';
      } else {
        tooltip += '<div>' + JSON.stringify(node.details) + '</div>';
      }
    } else {
      tooltip += '<div>' + node.details + '</div>';
    }

    tooltip += '</div>';
    return tooltip;
  };

  const handleNodeClick = (node) => {
    if (expandedNode === node.id) {
      setExpandedNode(null);
    } else {
      setExpandedNode(node.id);
    }
  };

  const renderExpandedDetails = () => {
    if (!expandedNode) return null;
    const node = graphData.nodes.find((n) => n.id === expandedNode);
    if (!node) return null;

    let content = null;

    if (node.id === 'api-request') {
      content = (
        <div>
          <h3 style={{ color: '#FFC300', marginTop: 0, marginBottom: '15px' }}>API Request Details</h3>
          <p><strong>Endpoint:</strong> {apiEndpoint}</p>
          <p><strong>Method:</strong> {method}</p>
          <h4 style={{ color: '#FFC300', marginTop: '15px', marginBottom: '10px' }}>Request Data:</h4>
          <div
            style={{
              background: '#1e1e1e',
              padding: '10px',
              borderRadius: '4px',
              overflowX: 'auto',
              fontFamily: 'monospace',
              fontSize: '14px'
            }}
          >
            <pre style={{ color: '#e6e6e6' }}>{JSON.stringify(requestData, null, 2)}</pre>
          </div>
        </div>
      );
    } else if (node.id === 'api-response') {
      content = (
        <div>
          <h3 style={{ color: '#FFC300', marginTop: 0, marginBottom: '15px' }}>API Response Details</h3>
          <p><strong>Status Code:</strong> {statusCode}</p>
          <h4 style={{ color: '#FFC300', marginTop: '15px', marginBottom: '10px' }}>Response Data:</h4>
          <div
            style={{
              background: '#1e1e1e',
              padding: '10px',
              borderRadius: '4px',
              overflowX: 'auto',
              fontFamily: 'monospace',
              fontSize: '14px'
            }}
          >
            <pre style={{ color: '#e6e6e6' }}>{JSON.stringify(responseData, null, 2)}</pre>
          </div>
        </div>
      );
    } else {
      content = (
        <div>
          <h3 style={{ color: '#FFC300', marginTop: 0, marginBottom: '15px' }}>{node.label} Details</h3>
          <p>{typeof node.details === 'string' ? node.details : JSON.stringify(node.details, null, 2)}</p>
        </div>
      );
    }

    return (
      <div
        style={{
          background: '#222',
          border: '1px solid #444',
          borderRadius: '8px',
          padding: '20px',
          position: 'relative',
          marginTop: '20px',
          overflow: 'auto',
          maxHeight: '400px'
        }}
      >
        <button
          onClick={() => setExpandedNode(null)}
          style={{
            position: 'absolute',
            top: '10px',
            right: '10px',
            background: '#333',
            color: 'white',
            border: '1px solid #444',
            borderRadius: '4px',
            width: '30px',
            height: '30px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            fontSize: '20px'
          }}
        >
          ×
        </button>
        {content}
      </div>
    );
  };

  return (
    <div
      style={{
        width: '100%',
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '20px',
        backgroundColor: '#111',
        color: 'white',
        fontFamily: 'Arial, sans-serif',
        borderRadius: '8px',
        border: '1px solid #444'
      }}
    >
      <h2
        style={{
          color: '#F86B03',
          fontSize: '2em',
          textAlign: 'center',
          marginBottom: '20px',
          fontWeight: 'bold',
          textTransform: 'uppercase',
          letterSpacing: '1px'
        }}
      >
        {title}
      </h2>

      <div
        data-tooltip-id="graph-tooltip"
        style={{
          border: '1px solid #444',
          borderRadius: '8px',
          background: '#111',
          height: '400px',
          marginBottom: '20px',
          position: 'relative'
        }}
      >
        <ForceGraph2D
          ref={fgRef}
          graphData={graphData}
          nodeLabel={null}
          linkDirectionalArrowLength={3.5}
          linkDirectionalArrowRelPos={1}
          linkWidth={(link) => (link.active ? 2 : 1)}
          linkColor={(link) => (link.active ? '#FFFFFF' : '#555')}
          linkDirectionalParticles={(link) => (link.active ? 3 : 0)}
          linkDirectionalParticleSpeed={0.01}
          cooldownTicks={100}
          d3AlphaDecay={0.01}
          d3VelocityDecay={0.3}
          nodeCanvasObject={(node, ctx, globalScale) => {
            const label = node.label;
            const fontSize = 12 / globalScale;
            const baseNodeSize = 8 / globalScale;
            const pulsateFactor = Math.sin(animationTime * 0.1) * 0.5 + 1;
            let finalNodeSize;

            if (node.isAI || node.stage === currentStage) {
              finalNodeSize = baseNodeSize * (node.isAI ? 1.5 : 1) * pulsateFactor;
            } else {
              finalNodeSize = baseNodeSize;
            }

            ctx.shadowBlur = 0;
            if (node.isAI || node.stage === currentStage) {
              ctx.shadowBlur = 15;
              ctx.shadowColor = node.isAI ? 'orange' : nodeColors[node.group];
            }

            if (node.isAI) {
              const ratio = pulsateFactor - 0.5;
              const clampedRatio = Math.max(0, Math.min(1, ratio));
              const orange = [255, 165, 0];
              const yellow = [255, 215, 0];
              const r = Math.round(orange[0] * (1 - clampedRatio) + yellow[0] * clampedRatio);
              const g = Math.round(orange[1] * (1 - clampedRatio) + yellow[1] * clampedRatio);
              const b = Math.round(orange[2] * (1 - clampedRatio) + yellow[2] * clampedRatio);
              ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
            } else if (node.error) {
              ctx.fillStyle = '#F44336';
            } else if (!node.active) {
              ctx.fillStyle = '#555';
            } else {
              ctx.fillStyle = nodeColors[node.group] || '#CCCCCC';
            }

            ctx.beginPath();
            ctx.arc(node.x, node.y, finalNodeSize, 0, 2 * Math.PI, false);
            ctx.fill();

            if (node.active) {
              ctx.strokeStyle = 'rgba(255, 255, 255, 0.7)';
              ctx.lineWidth = 1 / globalScale;
              ctx.stroke();
            }

            ctx.shadowBlur = 0;
            let labelY =
              node.id === 'api-processing'
                ? node.y - finalNodeSize - fontSize * 0.8
                : node.y + finalNodeSize + fontSize * 0.8;

            ctx.fillStyle = node.active ? 'white' : '#999';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.font = `${fontSize}px Arial`;
            ctx.fillText(label, node.x, labelY);

            node.__rd3t_tooltip = getNodeTooltip(node);
          }}
          onNodeClick={handleNodeClick}
          onNodeHover={(node) => {
            document.body.style.cursor = node ? 'pointer' : 'default';
          }}
          onLinkHover={(link) => {
            document.body.style.cursor = link ? 'pointer' : 'default';
          }}
          dagMode="lr"
          dagLevelDistance={100}
        />
      </div>
      {renderExpandedDetails()}
    </div>
  );
}

export default DataTraceabilityGraph;
