# Implement WebSocket Chat Endpoint

## Priority
Medium

## Created
2025-08-03

## Description
Create a FastAPI WebSocket endpoint for real-time bidirectional communication with the AI assistant, enabling scheduling suggestions, conflict resolution, and interactive timetable optimization.

## Acceptance Criteria
- [ ] Create FastAPI WebSocket endpoint at `/ws/chat`
- [ ] Implement connection management (connect, disconnect, error handling)
- [ ] Add message routing for different chat commands
- [ ] Integrate with existing scheduling models and validation
- [ ] Implement heartbeat/ping-pong for connection monitoring
- [ ] Add message validation with Pydantic schemas
- [ ] Create scheduling context integration
- [ ] Implement AI model integration for responses
- [ ] Add error handling and graceful degradation
- [ ] Create comprehensive logging for debugging

## Technical Details

### WebSocket Endpoint Structure
```python
@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    # Connection management and message handling
```

### Message Schema (Pydantic)
```python
from enum import Enum
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class MessageType(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    COMMAND = "command"

class ChatMessage(BaseModel):
    id: str
    type: MessageType
    content: str
    timestamp: datetime
    metadata: Optional[dict] = None

class ScheduleContext(BaseModel):
    current_view: str  # "weekly", "teacher", "class", "room"
    selected_entities: List[str]  # IDs of selected teachers/classes/rooms
    visible_conflicts: List[str]  # Conflict IDs currently visible
    filters_applied: dict  # Current filter state

class ChatCommand(BaseModel):
    command: str  # "/schedule", "/conflicts", "/suggest", "/help"
    parameters: Optional[dict] = None
    context: Optional[ScheduleContext] = None
```

### Connection Management
- **WebSocket Manager**: Singleton class to handle multiple connections
- **Connection Registry**: Track active connections and user sessions
- **Graceful Shutdown**: Proper cleanup on server restart
- **Rate Limiting**: Prevent message spam and abuse
- **Authentication**: Prepare for future user auth integration

### Message Routing
- **Command Router**: Handle special commands like `/conflicts`, `/suggest`
- **AI Integration**: Route appropriate messages to AI model
- **Schedule Operations**: Handle direct scheduling requests
- **System Messages**: Send notifications and status updates

### Scheduling Integration
- **Context Awareness**: Access current schedule state from database
- **Conflict Detection**: Real-time conflict checking and reporting
- **Suggestion Generation**: AI-powered scheduling suggestions
- **Validation**: Ensure proposed changes meet constraints
- **Database Operations**: Apply approved suggestions to schedule

### AI Model Integration
- **Model Interface**: Abstract AI provider for flexibility
- **Prompt Engineering**: Craft effective prompts for scheduling domain
- **Response Streaming**: Stream AI responses for real-time feel
- **Error Handling**: Graceful fallback when AI unavailable
- **Context Injection**: Include relevant schedule data in prompts

### Error Handling
- **Connection Errors**: Handle network issues and reconnection
- **Validation Errors**: Proper error messages for invalid data
- **Database Errors**: Graceful handling of database failures
- **AI Errors**: Fallback responses when AI fails
- **Rate Limiting**: Clear messages when limits exceeded

### Performance Considerations
- **Message Queuing**: Handle high-frequency messages efficiently
- **Database Pooling**: Optimize database connections
- **Caching**: Cache frequently accessed schedule data
- **Memory Management**: Clean up inactive connections
- **Monitoring**: Track connection count and message throughput

## Implementation Details

### Core WebSocket Handler
```python
class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_metadata: Dict[WebSocket, dict] = {}
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        # Initialize connection metadata
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        # Cleanup connection metadata
    
    async def send_message(self, websocket: WebSocket, message: ChatMessage):
        await websocket.send_text(message.model_dump_json())
    
    async def broadcast(self, message: ChatMessage):
        for connection in self.active_connections:
            await self.send_message(connection, message)
```

### Command Handlers
```python
class ChatCommandHandler:
    def __init__(self, db_session, ai_service):
        self.db = db_session
        self.ai = ai_service
    
    async def handle_command(self, command: ChatCommand, websocket: WebSocket):
        if command.command == "/conflicts":
            return await self.handle_conflicts_command(command)
        elif command.command == "/suggest":
            return await self.handle_suggest_command(command)
        elif command.command == "/schedule":
            return await self.handle_schedule_command(command)
        # ... more commands
    
    async def handle_conflicts_command(self, command: ChatCommand):
        # Query current conflicts from database
        # Format for AI-friendly response
        pass
```

### AI Service Integration
```python
class AIService:
    def __init__(self):
        # Initialize AI model (OpenAI, Anthropic, etc.)
        pass
    
    async def generate_response(self, 
                              message: str, 
                              context: ScheduleContext) -> str:
        # Craft prompt with scheduling context
        # Generate streaming response
        # Return formatted response
        pass
    
    async def suggest_schedule_improvements(self, 
                                          current_schedule: dict) -> List[dict]:
        # Analyze current schedule
        # Generate improvement suggestions
        # Return structured suggestions
        pass
```

### Database Integration
```python
async def get_schedule_context(db: AsyncSession, 
                             context_request: ScheduleContext) -> dict:
    # Query relevant schedule data based on context
    # Include teachers, classes, subjects, conflicts
    # Format for AI consumption
    pass

async def apply_schedule_suggestion(db: AsyncSession, 
                                  suggestion: dict) -> bool:
    # Validate suggestion against constraints
    # Apply changes to database
    # Return success/failure status
    pass
```

## Message Flow Examples

### Conflict Query
```
User: "What conflicts do we have on Monday morning?"
→ System parses as command: /conflicts day=monday time=morning
→ Query database for Monday morning conflicts
→ Format conflicts for AI context
→ AI generates human-readable response with suggestions
→ Send response with conflict IDs for frontend highlighting
```

### Scheduling Suggestion
```
User: "Can you help optimize Mrs. Smith's schedule?"
→ Extract teacher "Mrs. Smith" from message
→ Query current schedule for Mrs. Smith
→ Send schedule data to AI for analysis
→ AI generates optimization suggestions
→ Return suggestions with actionable buttons in frontend
```

## Implementation Steps
1. Create WebSocket endpoint with basic connection handling
2. Implement message validation with Pydantic schemas
3. Build WebSocket manager for connection lifecycle
4. Add command routing and parsing
5. Integrate with existing database models
6. Implement basic AI service interface
7. Add scheduling context queries
8. Create conflict detection and suggestion logic
9. Add comprehensive error handling
10. Implement logging and monitoring

## Testing Strategy
- **Unit Tests**: Test command parsing and routing logic
- **Integration Tests**: Test database integration and AI service
- **WebSocket Tests**: Test connection lifecycle and message flow
- **Load Tests**: Test multiple concurrent connections
- **Error Tests**: Test various failure scenarios
- **AI Integration Tests**: Mock AI responses for consistent testing

## Notes
- Design for multiple AI providers (OpenAI, Anthropic, local models)
- Ensure graceful degradation when AI service unavailable
- Plan for rate limiting and abuse prevention
- Consider message persistence for important conversations
- Design extensible command system for future features
- Include proper logging for debugging connection issues
- Consider WebSocket compression for large schedule data

## Dependencies
- FastAPI WebSocket support configured
- Database models and async session management
- AI service API keys and configuration
- Pydantic schemas for message validation
- Logging configuration for debugging
- Testing framework setup for WebSocket testing

## Security Considerations
- Input validation and sanitization
- Rate limiting per connection
- Authentication preparation (user sessions)
- CORS configuration for WebSocket connections
- Message size limits to prevent abuse
- Audit logging for scheduling changes
