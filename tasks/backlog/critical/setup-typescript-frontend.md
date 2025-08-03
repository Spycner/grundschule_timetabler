# Setup TypeScript Frontend

## Priority
High

## Created
2025-08-03

## Description
Initialize the TypeScript frontend application with React + Vite and Mantine UI, configure development tools optimized for scheduling applications, and establish the component structure.

## Acceptance Criteria
- [ ] Initialize Vite + React project with TypeScript
- [ ] Configure Mantine UI with core components
- [ ] Setup ESLint and Prettier
- [ ] Create basic routing structure with React Router
- [ ] Setup TanStack Query for REST API communication
- [ ] Configure WebSocket connection for chat functionality
- [ ] Create basic layout components using Mantine
- [ ] Configure development proxy for API
- [ ] Setup Vitest testing framework
- [ ] Create responsive base layout with Mantine Grid

## Technical Details
### Dependencies to Include
- React 18+
- TypeScript (strict mode)
- Mantine UI (@mantine/core, @mantine/hooks, @mantine/form)
- TanStack Query for REST API calls
- React Router for navigation
- Zustand for state management
- React Hook Form + Zod for form validation
- WebSocket (native browser API) for chat
- TanStack Table (fallback for advanced data grids)

### Directory Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── common/
│   │   ├── layout/
│   │   ├── scheduling/     # Timetable, drag-drop components
│   │   └── chat/          # WebSocket chat components
│   ├── pages/
│   ├── services/
│   │   ├── api.ts         # TanStack Query setup
│   │   └── websocket.ts   # WebSocket chat service
│   ├── hooks/
│   │   ├── useWebSocket.ts # Chat WebSocket hook
│   │   └── useScheduling.ts # Scheduling logic hooks
│   ├── types/
│   │   ├── api.ts         # Backend API types
│   │   └── chat.ts        # Chat message schemas
│   ├── utils/
│   ├── stores/            # Zustand stores
│   └── main.tsx
├── public/
├── tests/
├── tsconfig.json
├── vite.config.ts
└── package.json
```

## Notes
- Ensure strict TypeScript configuration
- Leverage Mantine's responsive system for mobile support
- Use Mantine's accessibility features (ARIA, keyboard navigation)
- Setup for German localization (Mantine supports i18n)
- Mantine provides built-in drag-and-drop for scheduling interfaces
- TanStack Table available as fallback for advanced data grid needs
- WebSocket connection should handle reconnection and error states

## Dependencies
- Depends on backend API structure (REST endpoints + WebSocket chat)
- Requires Node.js 18+ and npm/pnpm
- Backend WebSocket endpoint at `/ws/chat` for AI assistant
- Mantine UI requires PostCSS configuration
