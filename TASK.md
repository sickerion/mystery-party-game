# TASK.md - Progress Tracker

## Current Task: Add French Language Support for Backend Generation

### Goal
Implement language-aware content generation so that when the browser language is set to French, all generated content (characters, plot, clues, metadata) is produced in French.

### Progress

#### ✅ Completed Tasks

1. **Analyzed frontend i18n system** (2025-10-04)
   - Reviewed `frontend/src/i18n/config.ts`
   - Confirmed language detection from browser/localStorage
   - Language stored in `i18n.language` (en/fr)

2. **Added language parameter to backend models** (2025-10-04)
   - Updated `src/models/schema.py` - Added `language` field to `GameRequest`
   - Updated `src/database/models.py` - Added `language` column to `Game` table
   - Created and applied Alembic migration `9faee399f856` for database schema
   - Updated `src/models/state.py` - Added `language` to `MysteryGenerationState`

3. **Updated services and API** (2025-10-04)
   - Modified `src/services/game_service.py` - Added `language` parameter to `create_game()`
   - Updated `src/api/routers/games.py` - Added language handling in create game endpoint
   - Modified `src/api/routers/generation.py` - Passed language to all state initializations

4. **Adapted LLM prompts for French** (2025-10-04)
   - Updated `src/graph/nodes/characters.py` - Added French prompts
   - Updated `src/graph/nodes/plot.py` - Added French prompts
   - Updated `src/graph/nodes/clues.py` - Added French prompts
   - Updated `src/graph/nodes/metadata.py` - Added French prompts
   - All nodes now check `state.get('language', 'en')` and use appropriate prompts

5. **Modified frontend to send language** (2025-10-04)
   - Updated `frontend/src/services/api.ts` - Import i18n and add language to createGame
   - Updated `frontend/src/types/index.ts` - Added `language` field to `GameRequest` and `Game` interfaces

6. **Tested implementation** (2025-10-04)
   - Ran pytest tests - All 11 selected tests passed
   - Database models working correctly
   - API endpoints accepting language parameter

### Implementation Details

**Backend Changes:**
- Database: Added `language` column to `games` table with default "en"
- Models: `GameRequest` and `Game` models include language field
- State: `MysteryGenerationState` includes language for workflow
- Nodes: All generation nodes (characters, plot, clues, metadata) support bilingual prompts
- Services: Game creation service accepts and stores language preference

**Frontend Changes:**
- API client automatically detects current language from i18n
- Language sent with game creation request
- Type definitions updated to match backend

**Language Detection Flow:**
1. User's browser language detected by i18n (or uses stored preference)
2. Frontend creates game with `language: i18n.language`
3. Backend stores language in database
4. Generation nodes read language from state
5. LLM receives language-specific prompts
6. Generated content is in the requested language

### Next Steps
- Monitor real-world usage and gather feedback
- Consider adding more languages in the future
- Ensure all UI feedback messages are also translated
