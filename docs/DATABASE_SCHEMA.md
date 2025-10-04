# Database Schema Documentation

## Overview

The Mystery Party Game Generator uses SQLite/PostgreSQL with SQLAlchemy ORM for data persistence. The schema supports incremental mystery generation with full tracking of game state and generation history.

## Entity Relationship Diagram

```
┌─────────────────┐
│     games       │
│─────────────────│
│ id (PK)         │───┐
│ theme           │   │
│ num_players     │   │
│ difficulty      │   │
│ special_requests│   │
│ status          │   │
│ created_at      │   │
│ updated_at      │   │
└─────────────────┘   │
                      │
         ┌────────────┼────────────┬──────────────┬────────────────┐
         │            │            │              │                │
         ▼            ▼            ▼              ▼                ▼
┌──────────────────┐ ┌─────────┐ ┌──────────┐ ┌────────────────┐ ┌──────────────────┐
│generated_chars   │ │plots    │ │clues     │ │metadata        │ │validation_results│
│──────────────────│ │─────────│ │──────────│ │────────────────│ │──────────────────│
│id (PK)           │ │id (PK)  │ │id (PK)   │ │id (PK)         │ │id (PK)           │
│game_id (FK)      │ │game_id  │ │game_id   │ │game_id (FK,UQ) │ │game_id (FK)      │
│name              │ │ (FK,UQ) │ │ (FK)     │ │title           │ │iteration         │
│role              │ │setting  │ │clue_id   │ │est_duration    │ │validation_passed │
│background        │ │victim   │ │desc      │ │instructions    │ │validation_errors │
│personality       │ │crime    │ │location  │ │introduction    │ │created_at        │
│secret            │ │culprit  │ │revealed  │ └────────────────┘ └──────────────────┘
│motive            │ │method   │ │ _by      │
│relationship_to_v │ │timeline │ │signif    │
└──────────────────┘ │resolut  │ │mislead   │
                     └─────────┘ └──────────┘
```

## Tables

### games

**Purpose:** Main table storing game metadata and generation state.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | String (UUID) | PRIMARY KEY | Unique game identifier |
| theme | String | NOT NULL | Theme of the mystery (e.g., "film noir", "mansion") |
| num_players | Integer | NOT NULL | Number of players (3-12) |
| difficulty | String | NOT NULL | Difficulty level: "easy", "medium", "hard" |
| special_requests | Text | NULL | Optional special requirements |
| status | Enum | NOT NULL | Current generation status (see below) |
| created_at | DateTime | NOT NULL | Game creation timestamp |
| updated_at | DateTime | NOT NULL | Last update timestamp |

**Status Enum Values:**
- `initialized` - Game created, no components generated
- `characters_generated` - Characters generated
- `plot_generated` - Plot generated
- `clues_generated` - Clues generated
- `metadata_generated` - Metadata generated
- `validated` - Scenario validated successfully
- `completed` - Fully generated and validated
- `failed` - Validation failed

**Relationships:**
- One-to-Many with `generated_characters`
- One-to-One with `generated_plots`
- One-to-Many with `generated_clues`
- One-to-One with `generated_metadata`
- One-to-Many with `validation_results`

**Cascade:** DELETE CASCADE on all child tables

---

### generated_characters

**Purpose:** Stores character information for each game.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY AUTOINCREMENT | Character ID |
| game_id | String | FOREIGN KEY (games.id), NOT NULL | Reference to parent game |
| name | String | NOT NULL | Character's name |
| role | String | NOT NULL | Character's role/occupation |
| background | Text | NOT NULL | Character's background story |
| personality | Text | NOT NULL | Personality traits |
| secret | Text | NOT NULL | Hidden secret |
| motive | Text | NULL | Motive if involved in crime |
| relationship_to_victim | String | NULL | Relationship to the victim |

**Indexes:**
- Foreign key index on `game_id`

---

### generated_plots

**Purpose:** Stores the main plot/storyline for each game.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY AUTOINCREMENT | Plot ID |
| game_id | String | FOREIGN KEY (games.id), UNIQUE, NOT NULL | Reference to parent game |
| setting | Text | NOT NULL | Time and place of the mystery |
| victim | String | NOT NULL | Name of the victim |
| crime | Text | NOT NULL | Description of the crime |
| culprit | String | NOT NULL | Name of the culprit |
| murder_method | Text | NOT NULL | How the crime was committed |
| timeline | JSON | NOT NULL | Array of timeline events |
| resolution | Text | NOT NULL | How the mystery is solved |

**Constraints:**
- UNIQUE constraint on `game_id` (one plot per game)

**Indexes:**
- Unique index on `game_id`

---

### generated_clues

**Purpose:** Stores clues to be discovered during the game.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY AUTOINCREMENT | Clue ID |
| game_id | String | FOREIGN KEY (games.id), NOT NULL | Reference to parent game |
| clue_id | String | NOT NULL | Unique identifier for the clue (e.g., "CLUE_001") |
| description | Text | NOT NULL | Description of the clue |
| location | String | NOT NULL | Where the clue is found |
| revealed_by | String | NULL | Character who reveals this clue |
| significance | Text | NOT NULL | Why this clue is important |
| misleading | Boolean | NOT NULL, DEFAULT FALSE | Whether this is a red herring |

**Indexes:**
- Foreign key index on `game_id`

---

### generated_metadata

**Purpose:** Stores game metadata like title, instructions, and introduction.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY AUTOINCREMENT | Metadata ID |
| game_id | String | FOREIGN KEY (games.id), UNIQUE, NOT NULL | Reference to parent game |
| title | String | NOT NULL | Title of the mystery scenario |
| estimated_duration | Integer | NOT NULL | Estimated play duration in minutes |
| game_instructions | Text | NOT NULL | Instructions for the game host |
| introduction | Text | NOT NULL | Opening scene/introduction text |

**Constraints:**
- UNIQUE constraint on `game_id` (one metadata record per game)

**Indexes:**
- Unique index on `game_id`

---

### validation_results

**Purpose:** Tracks validation attempts and results for quality assurance.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY AUTOINCREMENT | Validation ID |
| game_id | String | FOREIGN KEY (games.id), NOT NULL | Reference to parent game |
| iteration | Integer | NOT NULL | Validation iteration number |
| validation_passed | Boolean | NOT NULL | Whether validation passed |
| validation_errors | JSON | NULL | Array of error messages if failed |
| created_at | DateTime | NOT NULL | Timestamp of validation |

**Indexes:**
- Foreign key index on `game_id`
- Can have multiple validation records per game (iteration history)

---

## Database Migrations

### Migration Tool: Alembic

Location: `alembic/versions/`

### Current Migration

**File:** `8a8a4a35a747_create_all_database_tables_for_game_.py`

**Description:** Initial migration creating all 6 tables with proper constraints and relationships.

### Running Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Rollback all migrations
alembic downgrade base

# Create new migration (auto-generates from model changes)
alembic revision --autogenerate -m "Description"
```

---

## Query Patterns

### Common Queries

#### Get Complete Game Scenario
```python
game = db.query(Game).filter(Game.id == game_id).first()
characters = db.query(GeneratedCharacter).filter(GeneratedCharacter.game_id == game_id).all()
plot = db.query(GeneratedPlot).filter(GeneratedPlot.game_id == game_id).first()
clues = db.query(GeneratedClue).filter(GeneratedClue.game_id == game_id).all()
metadata = db.query(GeneratedMetadata).filter(GeneratedMetadata.game_id == game_id).first()
```

#### List Games by Status
```python
games = db.query(Game).filter(Game.status == GameStatus.VALIDATED).order_by(Game.created_at.desc()).all()
```

#### Get Latest Validation
```python
validation = db.query(ValidationResult).filter(ValidationResult.game_id == game_id).order_by(ValidationResult.iteration.desc()).first()
```

### Using Services Layer

All database operations should go through the service layer for better separation:

```python
from src.services import game_service, character_service, plot_service

# Create game
game = game_service.create_game(db, "film noir", 6, "medium")

# Save characters
characters = [...]  # List of Character Pydantic models
character_service.save_characters(db, game.id, characters)

# Get complete game
game = game_service.get_game(db, game_id)
characters = character_service.get_characters_by_game(db, game_id)
```

---

## Database Performance

### Indexing Strategy

- Primary keys on all tables (automatic indexes)
- Foreign key indexes for efficient joins
- Unique indexes on singleton relationships (plot, metadata)

### Cascade Deletes

Deleting a game automatically removes:
- All characters
- Plot
- All clues
- Metadata
- All validation results

This is handled at the database level via ON DELETE CASCADE.

### Connection Pooling

SQLAlchemy handles connection pooling automatically. Default settings work well for SQLite development and PostgreSQL production.

---

## Data Integrity

### Constraints

1. **Foreign Keys:** All child tables reference `games.id`
2. **NOT NULL:** Required fields cannot be null
3. **UNIQUE:** Plot and metadata have unique game_id (1:1 relationship)
4. **Enums:** Status field uses enum for type safety

### Validation

- Application-level validation via Pydantic models
- Database-level constraints via SQLAlchemy
- Cascade deletes prevent orphaned records

---

## Backup and Recovery

### SQLite (Development)

```bash
# Backup
cp mystery_party.db mystery_party_backup.db

# Restore
cp mystery_party_backup.db mystery_party.db
```

### PostgreSQL (Production)

```bash
# Backup
pg_dump mystery_party > backup.sql

# Restore
psql mystery_party < backup.sql
```
