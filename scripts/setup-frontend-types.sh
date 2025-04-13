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
cat > src/types/index.d.ts << 'EOL'
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
EOL

echo "✅ Frontend type definitions setup complete!"
echo "Note: To install the actual type packages, run:"
echo "  cd frontend && npm install --save-dev @types/react @types/react-dom @types/react-redux @types/d3"
