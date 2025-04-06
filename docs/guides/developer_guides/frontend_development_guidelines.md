# Frontend Development Guidelines

---

## 1. Introduction

This document outlines ThinkAlike's frontend development standards and best practices. These guidelines ensure consistent, maintainable, and high-quality user interfaces across our applications.

---

## 2. Project Structure

### 2.1 Directory Structure

```typescript
src/
├── assets/          # Static assets (images, fonts, etc.)
├── components/      # Reusable UI components
│   ├── common/     # Shared components
│   ├── features/   # Feature-specific components
│   └── layouts/    # Layout components
├── hooks/          # Custom React hooks
├── pages/          # Route components
├── services/       # API and external service integrations
├── store/          # State management
├── styles/         # Global styles and theme
├── types/          # TypeScript type definitions
└── utils/          # Utility functions
```

### 2.2 Component Structure

```typescript
// filepath: src/components/features/UserProfile/UserProfile.tsx
import React from 'react';
import { useUser } from '@/hooks/useUser';
import { UserAvatar } from '@/components/common/UserAvatar';
import styles from './UserProfile.module.css';

interface UserProfileProps {
  userId: string;
  showSettings?: boolean;
}

export const UserProfile: React.FC<UserProfileProps> = ({
  userId,
  showSettings = false
}) => {
  const { user, isLoading, error } = useUser(userId);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className={styles.profile}>
      <UserAvatar src={user.avatarUrl} size="large" />
      <h2>{user.name}</h2>
      {showSettings && <SettingsPanel userId={userId} />}
    </div>
  );
};
```

---

## 3. State Management

### 3.1 React Query Configuration

```typescript
// filepath: src/lib/react-query.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 30 * 60 * 1000, // 30 minutes
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000)
    }
  }
});
```

### 3.2 Zustand Store Example

```typescript
// filepath: src/store/useAuthStore.ts
import create from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  token: string | null;
  user: User | null;
  setToken: (token: string) => void;
  setUser: (user: User) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      setToken: (token) => set({ token }),
      setUser: (user) => set({ user }),
      logout: () => set({ token: null, user: null })
    }),
    {
      name: 'auth-storage'
    }
  )
);
```

---

## 4. Styling Guidelines

### 4.1 CSS Modules Configuration

```typescript
// filepath: src/styles/theme.css
:root {
  --color-primary: #007AFF;
  --color-secondary: #5856D6;
  --color-success: #34C759;
  --color-warning: #FF9500;
  --color-error: #FF3B30;

  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  --font-size-xs: 12px;
  --font-size-sm: 14px;
  --font-size-md: 16px;
  --font-size-lg: 20px;
  --font-size-xl: 24px;
}
```

### 4.2 Component Styling

```typescript
// filepath: src/components/common/Button/Button.module.css
.button {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: 4px;
  font-size: var(--font-size-md);
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.primary {
  background-color: var(--color-primary);
  color: white;
}

.secondary {
  background-color: var(--color-secondary);
  color: white;
}

.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

---

## 5. Testing Strategy

### 5.1 Component Testing

```typescript
// filepath: src/components/common/Button/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByText('Click me')).toBeDisabled();
  });
});
```

### 5.2 Integration Testing

```typescript
// filepath: src/features/auth/Login.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Login } from './Login';
import { useAuthStore } from '@/store/useAuthStore';

describe('Login', () => {
  it('handles successful login', async () => {
    render(<Login />);

    await userEvent.type(
      screen.getByLabelText(/email/i),
      'test@example.com'
    );
    await userEvent.type(
      screen.getByLabelText(/password/i),
      'password123'
    );

    await userEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(useAuthStore.getState().token).toBeTruthy();
    });
  });
});
```

---

## 6. Performance Optimization

### 6.1 Code Splitting

```typescript
// filepath: src/pages/routes.tsx
import { lazy, Suspense } from 'react';
import { Loading } from '@/components/common/Loading';

const Dashboard = lazy(() => import('./Dashboard'));
const UserProfile = lazy(() => import('./UserProfile'));
const Settings = lazy(() => import('./Settings'));

export const Routes = () => (
  <Suspense fallback={<Loading />}>
    <Switch>
      <Route path="/dashboard" component={Dashboard} />
      <Route path="/profile" component={UserProfile} />
      <Route path="/settings" component={Settings} />
    </Switch>
  </Suspense>
);
```

### 6.2 Performance Monitoring

```typescript
// filepath: src/utils/performance.ts
export const measurePerformance = (componentName: string) => {
  const start = performance.now();

  return () => {
    const duration = performance.now() - start;
    if (duration > 100) {
      console.warn(`Slow render detected in ${componentName}: ${duration}ms`);
    }
  };
};
```

---

By following these frontend development guidelines, ThinkAlike ensures consistent, maintainable, and high-quality user interfaces across all our applications.
