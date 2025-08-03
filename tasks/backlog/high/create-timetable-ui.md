# Create Timetable UI

## Priority
Medium

## Created
2025-08-03

## Description
Design and implement the main timetable user interface using Mantine's DataTable and drag-and-drop components, with visual feedback and efficient navigation optimized for school scheduling.

## Acceptance Criteria
- [ ] Create weekly grid view component
- [ ] Implement drag-and-drop for lessons
- [ ] Add visual conflict indicators
- [ ] Create teacher/class/room filters
- [ ] Implement zoom levels
- [ ] Add print-friendly view
- [ ] Create mobile-responsive design
- [ ] Add keyboard navigation
- [ ] Implement undo/redo
- [ ] Add real-time validation

## Technical Details
### UI Components
- Mantine DataTable with virtualization (time slots x days)
- Draggable lesson cards using Mantine's drag-and-drop
- Sidebar with unassigned lessons (Mantine Navbar)
- Filter controls (Mantine Select, MultiSelect)
- Legend for color coding (Mantine ColorSwatch)
- Conflict notifications (Mantine Notifications)
- Quick actions menu (Mantine ActionIcon, Menu)
- TanStack Table fallback for advanced customization

### Interaction Features
- Drag lesson from sidebar to grid (Mantine drag-and-drop)
- Drag between grid cells with visual feedback
- Right-click context menu (Mantine ContextMenu)
- Hover for details (Mantine Tooltip, HoverCard)
- Click to edit (Mantine Modal with forms)
- Multi-select for bulk operations (Mantine DataTable selection)
- Keyboard navigation (built into Mantine components)

### Visual Design
- Color coding by subject (Mantine theme colors)
- Conflict highlighting (Mantine error styling)
- Teacher workload indicators (Mantine Progress, RingProgress)
- Room utilization heat map (Mantine ColorSwatch gradients)
- Current time indicator (custom overlay)
- Print optimization (Mantine responsive breakpoints)
- Dark/light theme support (Mantine ColorScheme)

## Notes
- Use Mantine's built-in drag-and-drop (replaces react-beautiful-dnd)
- Mantine provides WCAG-compliant accessibility features
- Mantine ColorScheme supports colorblind-friendly themes
- Mantine DataTable includes virtual scrolling for large datasets
- TanStack Table available for advanced customization needs
- Consider Mantine Spotlight for quick search/navigation
- Leverage Mantine's responsive grid system for mobile

## Dependencies
- Frontend framework setup complete (React + Mantine)
- REST API endpoints available (teachers, classes, subjects, schedules)
- Data models defined and TypeScript types generated
- Mantine drag-and-drop (@mantine/dnd) configured
- TanStack Table installed as fallback option
