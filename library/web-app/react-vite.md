# Skill: React + Vite Web App

## Overview
Build a modern React web application using Vite as the build tool.

## Tech Stack
- Language: TypeScript
- Framework: React 18
- Build Tool: Vite
- Styling: Tailwind CSS (default) or CSS Modules
- State: Zustand (simple) or React Query + Context
- Routing: React Router v6

## Project Structure
```
project/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/          # Route-level components
│   ├── hooks/          # Custom hooks
│   ├── store/          # State management
│   ├── services/       # API calls
│   ├── types/          # TypeScript types
│   ├── utils/          # Helper functions
│   ├── App.tsx
│   └── main.tsx
├── public/
├── index.html
├── vite.config.ts
├── tsconfig.json
└── package.json
```

## Setup Steps
1. `npm create vite@latest project-name -- --template react-ts`
2. `cd project-name && npm install`
3. `npm install tailwindcss @tailwindcss/vite`
4. Configure Tailwind in `vite.config.ts`
5. Add Tailwind directives to `src/index.css`

## Conventions & Patterns
- Use functional components with hooks only
- One component per file, named same as file
- Use `cn()` utility for conditional classNames
- Prefer composition over inheritance
- Keep components small (< 150 lines)
- Co-locate styles, tests, and component files

## Common Commands
```bash
npm run dev      # Start dev server
npm run build    # Production build
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

## Best Practices
- Use React.memo() only when you measure a performance problem
- Prefer useState + useEffect for simple state
- Use Zustand for shared global state
- Always type props with TypeScript interfaces
- Use `import.meta.env.VITE_*` for environment variables

## Common Pitfalls
- Don't use default exports for components (use named exports)
- Don't put business logic in components - use hooks/services
- Don't forget to handle loading and error states
- Vite env vars must start with `VITE_` prefix

## References
- Docs: https://vitejs.dev/guide/
- React: https://react.dev/
