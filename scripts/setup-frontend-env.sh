#!/bin/bash

# Setup script for frontend development environment

echo "🚀 Setting up frontend development environment..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Navigate to frontend directory
cd frontend || exit 1

echo "Installing frontend dependencies..."
npm install

# Install TypeScript type definitions
echo "Installing TypeScript type definitions..."
npm install --save-dev @types/react @types/react-dom @types/react-redux @types/material-ui @types/d3

# Create tsconfig.json if not exists
if [ ! -f tsconfig.json ]; then
    echo "Creating TypeScript configuration..."
    cat > tsconfig.json << 'EOL'
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"]
}
EOL
fi

# Create type definitions directory
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

echo "✅ Frontend environment setup complete!"
echo "You can now run: cd frontend && npm start"
