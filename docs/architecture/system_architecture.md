# ThinkAlike: Architecture of Digital Liberation

## Core Principles Embodied in Architecture

- **User Sovereignty**: All data belongs to users, with clear boundaries and consent
- **Radical Transparency**: System designed for visibility and auditability
- **Decentralized Control**: Avoiding central points of control or failure

## Component Architecture

### Backend (FastAPI)
- Clean separation between API, business logic, and data access
- Explicit consent mechanisms for all data operations
- Transparent data flow with tracing capabilities

### Frontend (React)
- UI as a validation framework - visualizing data sovereignty
- Component architecture mirroring our values
- Clear user control over all data sharing and usage

import React, { useState, useEffect, useRef } from 'react';
import { Box, Heading, Tag, Flex, Button, Text, Tooltip, useColorModeValue } from '@chakra-ui/react';
import { motion } from 'framer-motion';
import { useSwarmContext } from '../../../contexts/SwarmContext';
import { TaskCard } from './TaskCard';
import { SwarmVisualization } from './SwarmVisualization';
import { ConsentToggle } from '../../sovereignty/ConsentToggle';
import * as d3 from 'd3';

export const SwarmRoadmap: React.FC = () => {
  const { swarms, activeTasks, joinSwarm, createSwarm, userSwarms } = useSwarmContext();
  const [view, setView] = useState<'list' | 'visualization'>('visualization');
  const [userPreference, setUserPreference] = useState({
    showCompleted: false,
    priorityFilter: 'all',
    categoryFilter: 'all',
  });
  
  // Background gradient embodying the collective energy
  const bgGradient = useColorModeValue(
    'linear(to-br, purple.50, blue.50, teal.50)',
    'linear(to-br, purple.900, blue.900, teal.900)'
  );
  
  return (
    <Box 
      as={motion.div}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      p={6}
      borderRadius="lg"
      bgGradient={bgGradient}
      boxShadow="lg"
    >
      <Flex justifyContent="space-between" alignItems="center" mb={6}>
        <Heading as="h2" size="xl">Collective Liberation Tasks</Heading>
        <Flex>
          <Button 
            variant={view === 'list' ? 'solid' : 'outline'} 
            onClick={() => setView('list')}
            mr={2}
          >
            List View
          </Button>
          <Button 
            variant={view === 'visualization' ? 'solid' : 'outline'} 
            onClick={() => setView('visualization')}
          >
            Swarm Visualization
          </Button>
        </Flex>
      </Flex>
      
      <Flex mb={6} flexWrap="wrap" gap={2}>
        <ConsentToggle 
          label="Show Completed Tasks"
          isChecked={userPreference.showCompleted}
          onChange={() => setUserPreference({...userPreference, showCompleted: !userPreference.showCompleted})}
          tooltipText="Control what information you see"
        />
        {/* Additional filters would go here */}
      </Flex>
      
      {view === 'visualization' ? (
        <SwarmVisualization 
          swarms={swarms} 
          userSwarms={userSwarms}
          onJoinSwarm={joinSwarm}
        />
      ) : (
        <Flex direction="column" gap={4}>
          {swarms.map(swarm => (
            <Box key={swarm.id} p={4} borderRadius="md" borderWidth="1px">
              <Flex justifyContent="space-between" alignItems="center" mb={3}>
                <Heading as="h3" size="md">{swarm.name}</Heading>
                <Tag colorScheme={swarm.category === 'frontend' ? 'purple' : swarm.category === 'backend' ? 'blue' : 'green'}>
                  {swarm.category}
                </Tag>
              </Flex>
              <Text mb={3}>{swarm.description}</Text>
              <Flex gap={2} mb={3}>
                <Tag size="sm">Members: {swarm.memberCount}</Tag>
                <Tag size="sm">Tasks: {swarm.tasks.length}</Tag>
                <Tag size="sm" colorScheme={swarm.progress < 30 ? 'red' : swarm.progress < 70 ? 'yellow' : 'green'}>
                  Progress: {swarm.progress}%
                </Tag>
              </Flex>
              <Flex gap={2}>
                {userSwarms.includes(swarm.id) ? (
                  <Button size="sm" variant="outline">Already Joined</Button>
                ) : (
                  <Button size="sm" colorScheme="blue" onClick={() => joinSwarm(swarm.id)}>Join Swarm</Button>
                )}
                <Button size="sm" variant="ghost">View Details</Button>
              </Flex>
            </Box>
          ))}
          <Button mt={4} leftIcon={<>+</>} onClick={() => createSwarm()} colorScheme="purple">
            Propose New Liberation Swarm
          </Button>
        </Flex>
      )}
    </Box>




























































































































































































};  );    </Box>      </Text>        Click on a swarm to join • Drag nodes to explore connections      <Text position="absolute" bottom="5" right="5" fontSize="xs" opacity={0.7}>      <svg ref={svgRef} width="100%" height="100%"></svg>    <Box w="100%" h="600px" position="relative">  return (    }, [svgRef, swarms, userSwarms, nodeColor, linkColor, textColor, onJoinSwarm]);        }      d.fy = null;      d.fx = null;      if (!event.active) simulation.alphaTarget(0);    function dragended(event, d) {        }      d.fy = event.y;      d.fx = event.x;    function dragged(event, d) {        }      d.fy = d.y;      d.fx = d.x;      if (!event.active) simulation.alphaTarget(0.3).restart();    function dragstarted(event, d) {    // Drag functions        });      node.attr("transform", d => `translate(${d.x},${d.y})`);              .attr("y2", d => d.target.y);        .attr("x2", d => d.target.x)        .attr("y1", d => d.source.y)        .attr("x1", d => d.source.x)      link    simulation.on("tick", () => {    // Update simulation on tick          .attr("font-size", "10px");      .attr("fill", textColor)      .text(d => d.name)      .attr("text-anchor", "middle")      .attr("dy", 35)      .append("text")    node.filter(d => d.type === 'swarm')    // Add text labels to swarm nodes only          .text(d => `${d.name} (${d.type})`);    node.append("title")    // Add hover labels          });        }          onJoinSwarm(d.id.replace('swarm-', ''));        if (d.type === 'swarm' && !d.joined) {      .on("click", (event, d) => {      .attr("stroke-width", d => d.joined ? 3 : 1)      .attr("stroke", d => d.joined ? "#FC8181" : "white")      })        }          return '#F6AD55';          // Contributors        else {        }                 '#718096';                 d.status === 'completed' ? '#38A169' :          return d.status === 'in_progress' ? '#DD6B20' :          // Color based on status        else if (d.type === 'task') {        }                 '#38A169';                 d.category === 'backend' ? '#3182CE' :           return d.category === 'frontend' ? '#805AD5' :           // Color based on category        if (d.type === 'swarm') {      .attr("fill", d => {      .attr("r", d => d.radius)    node.append("circle")    // Add circles to nodes            .on("end", dragended));        .on("drag", dragged)        .on("start", dragstarted)      .call(d3.drag()      .attr("class", "node")      .enter().append("g")      .data(nodes)      .selectAll(".node")    const node = svg.append("g")    // Create node groups          .attr("stroke-width", d => Math.sqrt(d.value));      .attr("stroke-opacity", 0.6)      .attr("stroke", linkColor)      .enter().append("line")      .data(links)      .selectAll("line")    const link = svg.append("g")    // Create links          .force("collide", d3.forceCollide().radius(d => d.radius * 1.5));      .force("center", d3.forceCenter(width / 2, height / 2))      .force("charge", d3.forceManyBody().strength(-300))      .force("link", d3.forceLink(links).id(d => d.id).distance(100))    const simulation = d3.forceSimulation(nodes)    // Create force simulation        });      });        });          });            value: 1            target: contributorId,            source: `task-${task.id}`,          links.push({                    }            });              radius: 10              type: 'contributor',              name: contributor.username,              id: contributorId,            nodes.push({          if (!nodes.some(n => n.id === contributorId)) {          // Check if contributor node already exists                    const contributorId = `contributor-${contributor.id}`;        task.contributors.forEach(contributor => {        // Add contributor nodes and links to tasks                });          value: 1          target: `task-${task.id}`,          source: `swarm-${swarm.id}`,        links.push({                });          priority: task.priority          status: task.status,          radius: 15,          type: 'task',          name: task.title,          id: `task-${task.id}`,        nodes.push({      swarm.tasks.forEach(task => {      // Add task nodes and links to swarm            });        joined: userSwarms.includes(swarm.id)        category: swarm.category,        progress: swarm.progress,        radius: 25,        type: 'swarm',        name: swarm.name,        id: `swarm-${swarm.id}`,      nodes.push({    swarms.forEach(swarm => {    // Add swarm nodes        const links = [];    const nodes = [];    // Create data structure for visualization          .attr("height", height);      .attr("width", width)    const svg = d3.select(svgRef.current)    // Create SVG        d3.select(svgRef.current).selectAll("*").remove();    // Clear previous visualization        const height = 600;    const width = svgRef.current.clientWidth;        if (!svgRef.current || !swarms.length) return;  useEffect(() => {    const textColor = useColorModeValue('#1A202C', '#E2E8F0');  const linkColor = useColorModeValue('#3182CE', '#90CDF4'); // Blue  const nodeColor = useColorModeValue('#553C9A', '#B794F4'); // Purple  const svgRef = useRef(null);export const SwarmVisualization = ({ swarms, userSwarms, onJoinSwarm }) => {};  );};

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.swarm import Swarm, SwarmMember, Task, TaskContributor
from app.schemas.swarm import (
    SwarmCreate, SwarmUpdate, SwarmResponse, 
    TaskCreate, TaskUpdate, TaskResponse,
    SwarmMemberCreate
)
from app.services.traceability_service import TraceabilityService

router = APIRouter()

@router.get("/swarms", response_model=List[SwarmResponse])
def get_swarms(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
):
    """
    Get all active swarms with their tasks and contributors.
    
    This endpoint embodies our radical transparency principle by making
    all collective work visible to all participants.
    """
    # Start with base query
    query = db.query(Swarm)
    
    # Apply category filter if provided
    if category:
        query = query.filter(Swarm.category == category)
    
    # Get swarms with pagination
    swarms = query.offset(skip).limit(limit).all()
    
    # Record this data access for transparency
    traceability = TraceabilityService(db)
    traceability.record_data_access(
        user_id=current_user.id,
        data_type="swarm_list",
        purpose="view_roadmap"
    )
    
    return swarms

@router.post("/swarms", response_model=SwarmResponse)
def create_swarm(
    swarm: SwarmCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new swarm for collaborative work on a specific focus area.
    
    This embodies our principle of decentralized control, allowing any user
    to initiate collective action on important areas.
    """
    # Create new swarm
    db_swarm = Swarm(
        name=swarm.name,
        description=swarm.description,
        category=swarm.category,
        created_by=current_user.id
    )
    db.add(db_swarm)
    db.commit()
    db.refresh(db_swarm)
    
    # Automatically add creator as a member
    db_member = SwarmMember(
        swarm_id=db_swarm.id,
        user_id=current_user.id,
        role="coordinator"
    )
    db.add(db_member)
    db.commit()
    
    # Record this action for transparency
    traceability = TraceabilityService(db)
    traceability.record_data_creation(
        user_id=current_user.id,
        data_type="swarm",
        data_id=str(db_swarm.id),
        purpose="create_collaboration"
    )
    
    return db_swarm

@router.post("/swarms/{swarm_id}/join", response_model=SwarmResponse)
def join_swarm(
    swarm_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Join an existing swarm to contribute to its tasks.
    
    This endpoint embodies our user sovereignty principle by giving users
    explicit control over which collaborative efforts they participate in.
    """
    # Check if swarm exists
    swarm = db.query(Swarm).filter(Swarm.id == swarm_id).first()
    if not swarm:
        raise HTTPException(status_code=404, detail="Swarm not found")
    
    # Check if already a member
    existing_member = db.query(SwarmMember).filter(
        SwarmMember.swarm_id == swarm_id,
        SwarmMember.user_id == current_user.id
    ).first()
    
    if existing_member:
        raise HTTPException(status_code=400, detail="Already a member of this swarm")
    
    # Add user as member
    db_member = SwarmMember(
        swarm_id=swarm_id,
        user_id=current_user.id,
        role="contributor"
    )
    db.add(db_member)
    db.commit()
    
    # Record this action for transparency
    traceability = TraceabilityService(db)
    traceability.record_data_update(
        user_id=current_user.id,
        data_type="swarm_membership",
        data_id=str(swarm_id),
        purpose="join_collaboration"
    )
    
    return swarm

@router.post("/swarms/{swarm_id}/tasks", response_model=TaskResponse)
def create_task(
    swarm_id: UUID,
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new task within a swarm.
    
    This endpoint embodies both decentralized control (anyone in a swarm can propose tasks)
    and radical transparency (all tasks are visible to all participants).
    """
    # Check if swarm exists
    swarm = db.query(Swarm).filter(Swarm.id == swarm_id).first()
    if not swarm:
        raise HTTPException(status_code=404, detail="Swarm not found")
    
    # Check if user is a member of the swarm
    is_member = db.query(SwarmMember).filter(
        SwarmMember.swarm_id == swarm_id,
        SwarmMember.user_id == current_user.id
    ).first()
    
    if not is_member:
        raise HTTPException(
            status_code=403, 
            detail="You must be a member of the swarm to create tasks"
        )
    
    # Create new task
    db_task = Task(
        swarm_id=swarm_id,
        title=task.title,
        description=task.description,
        status="open",
        priority=task.priority,
        created_by=current_user.id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Record this action for transparency
    traceability = TraceabilityService(db)
    traceability.record_data_creation(
        user_id=current_user.id,
        data_type="task",
        data_id=str(db_task.id),
        purpose="propose_contribution"
    )
    
    return db_task

# Additional endpoints for task assignment, completion, etc. would follow the same pattern
# of enforcing our core principles of sovereignty, transparency, and decentralization

from sqlalchemy import Column, String, ForeignKey, Enum, Text, DateTime, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.db.base_class import Base

class Swarm(Base):
    __tablename__ = "swarms"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String, nullable=False)  # frontend, backend, documentation, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    members = relationship("SwarmMember", back_populates="swarm")
    tasks = relationship("Task", back_populates="swarm")
    creator = relationship("User", foreign_keys=[created_by])

class SwarmMember(Base):
    __tablename__ = "swarm_members"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    swarm_id = Column(UUID(as_uuid=True), ForeignKey("swarms.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False)  # coordinator, contributor
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    swarm = relationship("Swarm", back_populates="members")
    user = relationship("User")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    swarm_id = Column(UUID(as_uuid=True), ForeignKey("swarms.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum("open", "in_progress", "review", "completed", name="task_status"), nullable=False)
    priority = Column(Integer, default=3)  # 1-5, higher is more important
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    swarm = relationship("Swarm", back_populates="tasks")
    contributors = relationship("TaskContributor", back_populates="task")
    creator = relationship("User", foreign_keys=[created_by])

class TaskContributor(Base):
    __tablename__ = "task_contributors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    task = relationship("Task", back_populates="contributors")
    user = relationship("User")