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
