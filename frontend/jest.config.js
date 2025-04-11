module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  moduleNameMapper: {
    "\\.(jpg|jpeg|png|gif|svg)$": "<rootDir>/__mocks__/fileMock.js",
    "\\.(css|less|scss|sass)$": "<rootDir>/__mocks__/styleMock.js",
    "^@components/(.*)$": "<rootDir>/src/components/$1",
    "^@pages/(.*)$": "<rootDir>/src/pages/$1",
    "^@services/(.*)$": "<rootDir>/src/services/$1",
    "^@utils/(.*)$": "<rootDir>/src/utils/$1",
    "^@hooks/(.*)$": "<rootDir>/src/hooks/$1",
    "^@contexts/(.*)$": "<rootDir>/src/contexts/$1",
    "^@styles/(.*)$": "<rootDir>/src/styles/$1",
    "^@types/(.*)$": "<rootDir>/src/types/$1",
    "^@constants/(.*)$": "<rootDir>/src/constants/$1",
    "^@assets/(.*)$": "<rootDir>/src/assets/$1"
  },
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
  testMatch: [
    "<rootDir>/src/**/__tests__/**/*.{js,jsx,ts,tsx}",
    "<rootDir>/src/**/*.{spec,test}.{js,jsx,ts,tsx}"
  ],
  collectCoverageFrom: [
    "src/**/*.{js,jsx,ts,tsx}",
    "!src/**/*.d.ts"
  ],
  coverageThreshold: {
    global: {
      statements: 80,
      branches: 80,
      functions: 80,
      lines: 80
    }
  },
  transform: {
    "^.+\\.(ts|tsx)$": "ts-jest"
  }
};
