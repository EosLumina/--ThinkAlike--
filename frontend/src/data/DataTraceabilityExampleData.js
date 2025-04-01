const dataFlow = {
  nodes: [
    { id: 'node1', label: 'User Input', group: 1, value: "User data input" },
    { id: 'node2', label: 'AI Agent', group: 4, isAI: true, value: "AI processing node" },
    { id: 'node3', label: 'Database', group: 3, value: "Persistent data storage" },
    { id: 'node4', label: 'Response', group: 2, value: "Response to the user" }
  ],
  edges: [
    { from: 'node1', to: 'node2', value: "User data" },
    { from: 'node2', to: 'node3', value: "AI processed data" },
    { from: 'node3', to: 'node4', value: "Data for response" },
  ]
};

export default dataFlow;
