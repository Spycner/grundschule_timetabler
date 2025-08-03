# Implement AI Assistant UI

## Priority
Medium

## Created
2025-08-03

## Description
Create a WebSocket-powered AI chat assistant interface for providing scheduling suggestions, conflict resolution, and interactive timetable optimization guidance.

## Acceptance Criteria
- [ ] Create WebSocket connection hook with React
- [ ] Implement chat interface with message history
- [ ] Add typing indicators and connection status
- [ ] Handle message streaming with optimistic UI updates
- [ ] Implement error handling and auto-reconnection
- [ ] Create scheduling context integration
- [ ] Add message validation with Zod schemas
- [ ] Implement chat commands for scheduling operations
- [ ] Create mobile-responsive chat layout
- [ ] Add accessibility features for chat interface

## Technical Details

### Core Components
- **ChatContainer**: Main chat interface container
- **MessageList**: Virtualized message history display
- **MessageInput**: Input with send button and typing detection
- **ConnectionStatus**: WebSocket connection indicator
- **TypingIndicator**: Shows when AI is responding
- **ScheduleContext**: Integration with current timetable view

### WebSocket Integration
- **useWebSocket Hook**: Manages connection, messages, and state
- **Message Schema**: Zod validation for type safety
- **Reconnection Logic**: Automatic retry with exponential backoff
- **Error Boundaries**: Graceful error handling for chat failures
- **Message Queue**: Handle offline messages and retry logic

### Chat Features
- **Message Types**: 
  - User text messages
  - AI responses with formatting
  - System notifications (conflicts, suggestions)
  - Schedule-specific commands (/schedule, /conflicts, /suggest)
- **Optimistic Updates**: Immediate UI feedback before server response
- **Message Persistence**: Store chat history in local storage
- **Context Awareness**: Include current schedule state in messages

### UI Components (Mantine)
- **Paper/Card**: Chat container with proper spacing
- **ScrollArea**: Message list with auto-scroll to bottom
- **Textarea**: Multi-line message input with auto-resize
- **Badge**: Connection status and typing indicators
- **ActionIcon**: Send button and chat controls
- **Notifications**: Error messages and system alerts
- **Spotlight**: Quick chat commands integration

### State Management
- **Chat Store (Zustand)**:
  - messages: Message[]
  - connectionStatus: 'connecting' | 'connected' | 'disconnected' | 'error'
  - isTyping: boolean
  - currentScheduleContext: ScheduleContext | null
- **Message Interface**:
  ```typescript
  interface ChatMessage {
    id: string
    type: 'user' | 'assistant' | 'system'
    content: string
    timestamp: Date
    metadata?: {
      scheduleId?: string
      conflictIds?: string[]
      suggestions?: ScheduleSuggestion[]
    }
  }
  ```

### WebSocket Protocol
- **Connection Endpoint**: `ws://localhost:8000/ws/chat`
- **Message Format**: JSON with Zod validation
- **Heartbeat**: Ping/pong for connection monitoring
- **Authentication**: Include user session if implemented
- **Rate Limiting**: Client-side throttling for message sending

### Scheduling Integration
- **Context Sharing**: Send current timetable state to AI
- **Conflict Highlighting**: Highlight schedule conflicts mentioned in chat
- **Suggestion Application**: Apply AI suggestions directly to schedule
- **Quick Actions**: Buttons for common scheduling operations
- **Schedule Links**: Clickable references to specific time slots

### Performance Considerations
- **Message Virtualization**: Handle large chat histories efficiently
- **Debounced Typing**: Reduce typing indicator network calls
- **Message Compression**: Gzip WebSocket messages for large payloads
- **Memory Management**: Clean up old messages and connections

### Accessibility Features
- **Screen Reader Support**: Proper ARIA labels and live regions
- **Keyboard Navigation**: Full keyboard accessibility
- **Focus Management**: Proper focus handling for new messages
- **High Contrast**: Support for high contrast themes
- **Text Scaling**: Responsive to browser text size settings

## Implementation Steps
1. Create useWebSocket hook with connection management
2. Build basic chat UI components with Mantine
3. Implement message validation with Zod schemas
4. Add typing indicators and connection status
5. Integrate with scheduling context and current timetable
6. Add error handling and reconnection logic
7. Implement chat commands for scheduling operations
8. Add accessibility features and mobile responsiveness
9. Create comprehensive error boundaries
10. Add performance optimizations and virtualization

## Notes
- Focus on real-time responsiveness for good UX
- Ensure graceful degradation when WebSocket unavailable
- Consider chat persistence across browser sessions
- Plan for eventual user authentication integration
- Design for extensibility (future AI models, features)
- Include proper loading states and error messages
- Consider internationalization for German educational terms

## Dependencies
- Frontend framework setup complete (React + Mantine)
- WebSocket backend endpoint implemented
- Zustand store configuration
- Zod validation schemas defined
- Schedule models and types available
- Mantine components and theming configured

## Testing Strategy
- Unit tests for WebSocket hook and message handling
- Integration tests for chat UI components
- E2E tests for complete chat workflows
- Performance tests for large message histories
- Accessibility tests with screen reader simulation
- Error scenario testing (connection drops, invalid messages)
