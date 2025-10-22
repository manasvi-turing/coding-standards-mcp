---
description: Comprehensive React & Next.js coding standards, patterns, best practices, and guidelines for maintainable, performant, and secure applications
status: active
---

# React & Next.js Coding Standards

## Table of Contents
1. [Component Structure](#component-structure)
2. [Best Practices](#best-practices)
3. [Next.js Specific](#nextjs-specific)
4. [State Management & API Calls](#state-management--api-calls)
5. [Custom Hooks](#custom-hooks)
6. [Testing](#testing)
7. [Maintenance](#maintenance)
8. [Performance](#performance)
9. [Security](#security)

---

## Component Structure
- **Functional Components**: Use functional components exclusively; avoid class components.
- **Prop Types / TypeScript**: Define prop types using TypeScript interfaces or `PropTypes`.
- **Hooks Rules**: Follow React [Rules of Hooks](https://reactjs.org/docs/hooks-rules.html).
- **Memoization**: Use `React.memo`, `useMemo`, and `useCallback` to optimize re-renders.
- **Server Components**: Leverage React Server Components (RSC) for server-side logic to reduce bundle size.
- **Single Responsibility Principle**: Components should have a single focus and responsibility.
- **Folder Structure**: Modular folder layout: `components/`, `features/`, `pages/`, `hooks/`, `utils/`, `api/`.

---

## Best Practices
- **Component Size**: Keep components small and focused.
- **State Management**: Use lightweight or context-based state management (Zustand, Jotai) for client/UI state.
- **Error Boundaries**: Wrap top-level components in error boundaries.
- **Code Documentation**: Self-documenting code; include JSDoc/TSDoc where complex logic exists.
- **Type Safety**: Use TypeScript for type-safe code.
- **Code Splitting & Lazy Loading**: Dynamically import components to reduce initial load.
- **Accessibility**: Follow WAI-ARIA standards; ensure components are accessible (a11y).

---

## Next.js Specific
- **App Router**: Use App Router for layouts and nested routes.
- **Data Fetching**: Prefer `getServerSideProps`, `getStaticProps`, or `fetch()` in server components.
- **Image Optimization**: Use `next/image`.
- **Font Optimization**: Use `next/font`.
- **Edge Functions**: Leverage Edge Functions for faster response times.
- **ISR (Incremental Static Regeneration)**: Update static content without full rebuilds.
- **Middleware**: Use for authentication, logging, and cross-cutting concerns.
- **SEO Best Practices**: Implement canonical URLs, structured data, and metadata.

---

## State Management & API Calls

### RTK Query (Server State)
- **Centralized API Layer**: Define endpoints in a single `apiSlice`.
- **Auto Caching & Invalidations**: Use `providesTags` and `invalidatesTags`.
- **Hooks**: Use generated hooks (`useGetUserQuery()`, `useUpdatePostMutation()`).
- **Type Safety**: Define request/response interfaces.
- **Error & Loading States**: Handle with `isLoading`, `isError`, `isSuccess`.

**Example**:

```ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  tagTypes: ['User', 'Post'],
  endpoints: (builder) => ({
    getUser: builder.query<User, number>({
      query: (id) => `users/${id}`,
      providesTags: ['User'],
    }),
    updatePost: builder.mutation<Post, Partial<Post>>({
      query: (data) => ({
        url: `posts/${data.id}`,
        method: 'PUT',
        body: data,
      }),
      invalidatesTags: ['Post'],
    }),
  }),
});

export const { useGetUserQuery, useUpdatePostMutation } = apiSlice;
````

### Zustand (Client/UI State)

* **Modular Stores**: Create separate stores for unrelated state.
* **Immer Support**: Simplify immutable updates.
* **Persistence**: Optional via `zustand/middleware`.
* **Minimal Boilerplate**: No actions/reducers needed.

**Example**:

```ts
import create from 'zustand';
import { persist } from 'zustand/middleware';

interface UIState {
  darkMode: boolean;
  toggleDarkMode: () => void;
}

export const useUIStore = create<UIState>()(
  persist(
    (set) => ({
      darkMode: false,
      toggleDarkMode: () => set((state) => ({ darkMode: !state.darkMode })),
    }),
    { name: 'ui-storage' }
  )
);
```

**Guidelines**:

* Use **RTK Query** for server-driven state.
* Use **Zustand** for client/UI state.
* Avoid mixing server and client state in a single store.
* Keep components free from API logic; use hooks.

---

## Custom Hooks

**Concept**: Custom hooks are reusable functions prefixed with `use` that encapsulate stateful or side-effect logic.
**Purpose**: Reduce code duplication, isolate logic, improve readability, and enhance maintainability.

**When to use**:

* Shared logic between components (`useFetchUser`, `useForm`, `useWindowSize`).
* Local state management with effects (`useLocalStorage`, `useTheme`).
* Encapsulation of subscriptions or event listeners.

**Example: `useLocalStorage`**

```ts
import { useState, useEffect } from 'react';

export function useLocalStorage<T>(key: string, defaultValue: T) {
  const [value, setValue] = useState<T>(() => {
    if (typeof window === 'undefined') return defaultValue;
    try {
      const stored = window.localStorage.getItem(key);
      return stored ? JSON.parse(stored) : defaultValue;
    } catch {
      return defaultValue;
    }
  });

  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch {}
  }, [key, value]);

  return [value, setValue] as const;
}
```

**Usage**:

```ts
const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('theme', 'light');
```

**Best Practices**:

1. Always prefix with `use`.
2. Only include stateful or side-effect logic; no JSX.
3. Keep hooks generic and reusable.
4. Split large hooks into smaller, focused hooks.
5. Use TypeScript for type safety.

---

## Maintenance

* **Code Reviews**: Enforce strict code reviews.
* **Dependency Management**: Regularly update dependencies and run `npm audit`.
* **CI/CD**: Implement automated pipelines for builds, linting, testing, and deployments.
* **Documentation**: Maintain a project `README` and coding standards.

---

## Performance

* **Lazy Loading**: Images and non-critical components.
* **Dynamic Imports / Code Splitting**: Reduce bundle size.
* **Caching Strategies**: SWR, RTK Query caching, stale-while-revalidate.
* **Profiling**: Use React DevTools and Lighthouse.

---

## Security

* **XSS Protection**: Sanitize inputs using libraries like DOMPurify.
* **Content Security Policy (CSP)**: Strong CSP headers.
* **Secure API Routes**: Authentication & authorization enforced.
* **Server Actions**: Handle sensitive logic server-side.
* **Secure Headers**: Strict-Transport-Security, X-Content-Type-Options.
* **Input Validation**: Both client-side and server-side.
* **Error Handling**: Prevent information leaks.

---

### References

* [React Official Docs](https://reactjs.org/docs/getting-started.html)
* [Next.js Official Docs](https://nextjs.org/docs)
* [Redux Toolkit Query](https://redux-toolkit.js.org/rtk-query/overview)
* [Zustand Documentation](https://zustand-demo.pmnd.rs/)
* [Web.dev Performance & Security](https://web.dev/)

---
