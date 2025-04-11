export interface ValueDimension {
  id: string;
  name: string;
  description: string;
  position: number;      // User's position (-1.0 to 1.0)
  importance: number;    // User-assigned importance (0.0-1.0)
  confidence: number;    // System confidence in this value
}

export interface ValueProfile {
  userId: string;
  dimensions: Record<string, ValueDimension>;
  lastUpdated: string;
  confidenceScore: number;

  // Visual representation data for celestial UI
  spectralSignature?: number[];
  dominantHue?: string;
  luminosity?: number;
}

export interface OrbitRelationship {
  userId1: string;
  userId2: string;
  resonanceScore: number;      // Overall compatibility (0.0-1.0)
  complementaryValues: string[]; // Dimensions where users complement each other
  sharedValues: string[];      // Dimensions with strong agreement
  tensionPoints: string[];     // Potential areas of value conflict
  orbitalStability: number;    // Predicted relationship stability
}
