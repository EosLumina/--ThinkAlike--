#!/bin/bash

# Check if we're in the frontend directory
if [ $(basename "$PWD") == "frontend" ]; then
  echo "⚠️ This script should be run from the repository root."
  echo "Navigating to repository root and running the setup script there..."
  cd ..

  # Check if the script exists in the scripts directory
  if [ -f "scripts/setup-frontend-types.sh" ]; then
    chmod +x scripts/setup-frontend-types.sh
    ./scripts/setup-frontend-types.sh
  else
    # The script is missing from the scripts directory, let's create it
    mkdir -p scripts

    cat > scripts/setup-frontend-types.sh << 'EOL'
#!/bin/bash

# Setup script for frontend development environment
# Must be run from the repository root

echo "🚀 Setting up frontend TypeScript definitions..."

# Navigate to frontend directory
cd frontend || exit 1

# Create types directory if it doesn't exist
mkdir -p src/types

# Create type declarations file
echo "Creating custom type declarations..."
cat > src/types/index.d.ts << 'EOF'
// Global type declarations for ThinkAlike project

// Declare modules without type definitions
declare module '../../store' {
  export const store: any;
  export type RootState = any;
}

declare module '../../store/actions/familyTree' {
  export const selectConnection: (id: string) => any;
}

declare module '../../types/family-tree' {
  export interface Connection {
    id: string;
    type: string;
    sourceId: string;
    targetId: string;
    strength: number;
    qualities: string[];
    createdAt: string;
  }

  export interface Person {
    id: string;
    name: string;
  }
}

declare module '../ui_components/CoreValuesValidator' {
  export interface CoreValuesValidatorProps {
    data: any;
    type: string;
    onValidationComplete?: (isValid: boolean) => void;
  }

  export default function CoreValuesValidator(props: CoreValuesValidatorProps): JSX.Element;
}

declare module '../ui_components/DataTraceability' {
  export interface DataTraceabilityProps {
    data: any;
    showDetails?: boolean;
  }

  export default function DataTraceability(props: DataTraceabilityProps): JSX.Element;
}
EOF

echo "✅ Frontend type definitions setup complete!"
echo "Note: To install the actual type packages, run:"
echo "  cd frontend && npm install --save-dev @types/react @types/react-dom @types/react-redux @types/d3"
EOL

    chmod +x scripts/setup-frontend-types.sh
    ./scripts/setup-frontend-types.sh
  fi
else
  echo "Error: This script must be run from the frontend directory."
  exit 1
fi
