import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { useSelector } from 'react-redux';
import { ConnectionType, EntityNode, ViewMode } from '../../types/family-tree';
import { RootState } from '../../store';
import { Typography, Box, Slider, ToggleButtonGroup, ToggleButton } from '@material-ui/core';
import { DataTraceability } from '../ui_components/DataTraceability';

interface UnityInDiversityViewProps {
  width: number;
  height: number;
  zoomLevel: number;
  onZoomChange: (level: number) => void;
  viewMode: ViewMode;
  onViewModeChange: (mode: ViewMode) => void;
}

/**
 * UnityInDiversityView - A visualization component that renders the family tree
 * in a way that reveals both our interconnectedness and our uniqueness.
 *
 * This component represents our philosophical approach that we are both
 * "one" (a unified collective) and "many" (sovereign individuals).
 */
const UnityInDiversityView: React.FC<UnityInDiversityViewProps> = ({
  width,
  height,
  zoomLevel,
  onZoomChange,
  viewMode,
  onViewModeChange
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const nodes = useSelector((state: RootState) => state.familyTree.nodes);
  const connections = useSelector((state: RootState) => state.familyTree.connections);
  const currentUser = useSelector((state: RootState) => state.auth.user);

  // Force simulation setup for the network diagram
  useEffect(() => {
    if (!svgRef.current || !nodes.length) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    // Create different visualizations based on view mode
    switch(viewMode) {
      case 'unity':
        renderUnityView(svg, nodes, connections, zoomLevel);
        break;
      case 'diversity':
        renderDiversityView(svg, nodes, connections, zoomLevel);
        break;
      case 'fractal':
        renderFractalView(svg, nodes, connections, zoomLevel);
        break;
      default:
        renderBalancedView(svg, nodes, connections, zoomLevel);
    }

    // Add legend explaining the visualization
    addLegend(svg, viewMode);

  }, [nodes, connections, zoomLevel, viewMode, width, height]);

  /**
   * Unity View emphasizes our collective wholeness by visualizing the network
   * as an interconnected web where individual nodes blend into the greater pattern.
   */
  const renderUnityView = (svg: any, nodes: EntityNode[], connections: any[], zoom: number) => {
    // Implementation using d3 force layout with strong attractive forces
    // and emergent pattern visualization that shows the whole as greater than parts
    // ...existing code...
  };

  /**
   * Diversity View emphasizes individual sovereignty by showing each node's
   * unique attributes while still maintaining connection context.
   */
  const renderDiversityView = (svg: any, nodes: EntityNode[], connections: any[], zoom: number) => {
    // Implementation with greater emphasis on node attributes, personal achievements,
    // and individual contributions to the whole
    // ...existing code...
  };

  /**
   * Fractal View shows how the same patterns repeat at different scales,
   * revealing how individuals, families, and communities mirror each other.
   */
  const renderFractalView = (svg: any, nodes: EntityNode[], connections: any[], zoom: number) => {
    // Implementation using recursive patterns that show self-similarity
    // across different scales of connection
    // ...existing code...
  };

  /**
   * Balanced View shows both unity and diversity simultaneously,
   * the default visualization that balances collective and individual focus.
   */
  const renderBalancedView = (svg: any, nodes: EntityNode[], connections: any[], zoom: number) => {
    // Implementation that balances collective patterns with individual uniqueness
    // ...existing code...
  };

  return (
    <Box className="family-tree-container" data-testid="unity-in-diversity-view">
      <Box className="view-controls">
        <Typography variant="h6">Perspective</Typography>
        <ToggleButtonGroup
          value={viewMode}
          exclusive
          onChange={(_, newMode) => onViewModeChange(newMode)}
        >
          <ToggleButton value="unity" aria-label="Unity view">
            One Whole
          </ToggleButton>
          <ToggleButton value="diversity" aria-label="Diversity view">
            Many Parts
          </ToggleButton>
          <ToggleButton value="fractal" aria-label="Fractal view">
            Fractal Patterns
          </ToggleButton>
          <ToggleButton value="balanced" aria-label="Balanced view">
            Unity in Diversity
          </ToggleButton>
        </ToggleButtonGroup>

        <Typography variant="subtitle2">
          Zoom: {zoomLevel === 1 ? 'Individual' : zoomLevel === 10 ? 'Collective' : 'Relational'}
        </Typography>
        <Slider
          value={zoomLevel}
          min={1}
          max={10}
          step={1}
          onChange={(_, value) => onZoomChange(value as number)}
          aria-labelledby="zoom-slider"
        />
      </Box>

      <svg
        ref={svgRef}
        width={width}
        height={height}
        className="family-tree-svg"
        aria-label="Family tree visualization showing unity in diversity"
      />

      <DataTraceability
        dataSource="family-tree-connections"
        processingSteps={["raw-data", "privacy-filtering", "visualization-transformation"]}
        lastUpdated={new Date().toISOString()}
      />
    </Box>
  );
};

export default UnityInDiversityView;
