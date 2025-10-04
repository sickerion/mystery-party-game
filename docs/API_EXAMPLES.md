# API Usage Examples

## Overview

The Mystery Party Game Generator API provides two modes:
1. **Legacy Mode**: Complete generation in one request
2. **Incremental Mode**: Step-by-step generation with database persistence

## Base URL

```
http://localhost:8000
```

---

## Legacy Mode - Single Request Generation

### Generate Complete Mystery

Generate a complete mystery party game in one API call.

**Endpoint:** `POST /generate`

**Request:**
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "theme": "film noir detective story",
    "num_players": 6,
    "difficulty": "medium",
    "special_requests": "Include a femme fatale character"
  }'
```

**Response (200 OK):**
```json
{
  "title": "Murder at the Moonlight Lounge",
  "theme": "film noir detective story",
  "difficulty": "medium",
  "num_players": 6,
  "estimated_duration": 120,
  "plot": {
    "setting": "A smoky jazz lounge in 1940s Los Angeles",
    "victim": "Johnny Fontaine",
    "crime": "Murder by poisoning",
    "culprit": "Rita Diamond",
    "murder_method": "Cyanide in whiskey",
    "timeline": [
      "9:00 PM - Club opens, guests arrive",
      "10:30 PM - Victim found dead in office",
      "11:00 PM - Police arrive, investigation begins"
    ],
    "resolution": "The detective reveals Rita's motive..."
  },
  "characters": [
    {
      "name": "Rita Diamond",
      "role": "Femme Fatale",
      "background": "Former actress...",
      "personality": "Seductive and manipulative",
      "secret": "Embezzled money from victim",
      "motive": "Revenge and financial gain",
      "relationship_to_victim": "Former business partner"
    }
    // ... more characters
  ],
  "clues": [
    {
      "clue_id": "CLUE_001",
      "description": "Empty vial of cyanide",
      "location": "Behind the bar",
      "revealed_by": "Bartender",
      "significance": "Murder weapon container",
      "misleading": false
    }
    // ... more clues
  ],
  "game_instructions": "Host instructions here...",
  "introduction": "Opening scene text..."
}
```

---

## Incremental Mode - Step-by-Step Generation

### Complete Workflow Example

This example shows the full incremental workflow from game creation to final validation.

#### Step 1: Create Game

**Endpoint:** `POST /games`

```bash
curl -X POST http://localhost:8000/games \
  -H "Content-Type: application/json" \
  -d '{
    "theme": "victorian mansion murder",
    "num_players": 8,
    "difficulty": "hard",
    "special_requests": "Include secret passages"
  }'
```

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "theme": "victorian mansion murder",
  "num_players": 8,
  "difficulty": "hard",
  "special_requests": "Include secret passages",
  "status": "initialized",
  "created_at": "2025-10-04T14:30:00.000Z",
  "updated_at": "2025-10-04T14:30:00.000Z"
}
```

**Save the game ID for subsequent requests:**
```bash
GAME_ID="550e8400-e29b-41d4-a716-446655440000"
```

---

#### Step 2: Generate Characters

**Endpoint:** `POST /games/{game_id}/characters`

```bash
curl -X POST http://localhost:8000/games/$GAME_ID/characters
```

**Response (200 OK):**
```json
[
  {
    "name": "Lord Ashford",
    "role": "Mansion Owner",
    "background": "Wealthy aristocrat with dark secrets",
    "personality": "Arrogant and controlling",
    "secret": "Gambling debts",
    "motive": null,
    "relationship_to_victim": "Brother"
  },
  {
    "name": "Lady Margaret",
    "role": "Victim's Wife",
    "background": "Recently married into wealth",
    "personality": "Calculating and ambitious",
    "secret": "Affair with the butler",
    "motive": "Inheritance",
    "relationship_to_victim": "Wife"
  }
  // ... 6 more characters
]
```

**Game status now:** `characters_generated`

---

#### Step 3: Generate Plot

**Endpoint:** `POST /games/{game_id}/plot`

```bash
curl -X POST http://localhost:8000/games/$GAME_ID/plot
```

**Response (200 OK):**
```json
{
  "setting": "Ashford Manor, Victorian England, October 1895",
  "victim": "Lord Edward Ashford",
  "crime": "Murder in the study",
  "culprit": "Lady Margaret",
  "murder_method": "Poisoned brandy",
  "timeline": [
    "8:00 PM - Dinner party begins",
    "9:30 PM - Lord Ashford retires to study",
    "10:00 PM - Scream heard from study",
    "10:15 PM - Body discovered"
  ],
  "resolution": "Evidence of poison found in Lady Margaret's room"
}
```

**Game status now:** `plot_generated`

---

#### Step 4: Generate Clues

**Endpoint:** `POST /games/{game_id}/clues`

```bash
curl -X POST http://localhost:8000/games/$GAME_ID/clues
```

**Response (200 OK):**
```json
[
  {
    "clue_id": "CLUE_001",
    "description": "Empty poison bottle",
    "location": "Lady Margaret's vanity",
    "revealed_by": "Chambermaid",
    "significance": "Links Lady Margaret to the murder",
    "misleading": false
  },
  {
    "clue_id": "CLUE_002",
    "description": "Torn love letter",
    "location": "Fireplace in study",
    "revealed_by": "Butler",
    "significance": "Suggests affair and motive",
    "misleading": false
  },
  {
    "clue_id": "RED_001",
    "description": "Muddy footprints",
    "location": "Garden path",
    "revealed_by": "Gardener",
    "significance": "Suggests intruder - actually false lead",
    "misleading": true
  }
  // ... more clues
]
```

**Game status now:** `clues_generated`

---

#### Step 5: Generate Metadata

**Endpoint:** `POST /games/{game_id}/metadata`

```bash
curl -X POST http://localhost:8000/games/$GAME_ID/metadata
```

**Response (200 OK):**
```json
{
  "title": "Murder at Ashford Manor",
  "estimated_duration": 150,
  "game_instructions": "Welcome, Game Host! This murder mystery is designed for 8 players...\n\nSetup:\n1. Distribute character cards\n2. Place clue cards in designated locations\n3. Read the introduction aloud\n\nGameplay:\n- Players have 2 hours to solve the mystery\n- Encourage roleplay and staying in character\n- Reveal clues progressively...",
  "introduction": "The year is 1895. You have been invited to an elegant dinner party at Ashford Manor, the ancestral home of Lord Edward Ashford. The evening begins pleasantly enough with fine dining and polite conversation, but as the grandfather clock strikes ten, a piercing scream echoes through the hallways...\n\nLord Ashford has been found dead in his study, a glass of poisoned brandy still clutched in his hand. The doors to the manor are locked, the storm raging outside. The killer must be among you..."
}
```

**Game status now:** `metadata_generated`

---

#### Step 6: Validate Scenario

**Endpoint:** `POST /games/{game_id}/validate`

```bash
curl -X POST http://localhost:8000/games/$GAME_ID/validate
```

**Response (200 OK) - Success:**
```json
{
  "validation_passed": true,
  "validation_errors": [],
  "iteration": 1
}
```

**Response (200 OK) - Failure:**
```json
{
  "validation_passed": false,
  "validation_errors": [
    "Victim 'Lord Edward Ashford' not found in character list",
    "Insufficient clues: only 3 clues for 8 players"
  ],
  "iteration": 1
}
```

**Game status now:** `validated` (if passed) or `failed` (if not passed)

---

#### Step 7: Retrieve Complete Scenario

**Endpoint:** `GET /games/{game_id}`

```bash
curl http://localhost:8000/games/$GAME_ID
```

**Response (200 OK):**
```json
{
  "title": "Murder at Ashford Manor",
  "theme": "victorian mansion murder",
  "difficulty": "hard",
  "num_players": 8,
  "estimated_duration": 150,
  "plot": { /* plot object */ },
  "characters": [ /* array of characters */ ],
  "clues": [ /* array of clues */ ],
  "game_instructions": "...",
  "introduction": "..."
}
```

**Error (400 Bad Request) - Components Missing:**
```json
{
  "detail": "Characters not yet generated. Call POST /games/{game_id}/characters first."
}
```

---

### List Games

**Endpoint:** `GET /games`

**Query Parameters:**
- `status` (optional): Filter by game status
- `limit` (optional): Max results (default: 100, max: 500)
- `offset` (optional): Skip results (default: 0)

**Examples:**

```bash
# List all games
curl http://localhost:8000/games

# List validated games only
curl "http://localhost:8000/games?status=validated"

# Pagination (page 2, 10 per page)
curl "http://localhost:8000/games?limit=10&offset=10"

# Combination
curl "http://localhost:8000/games?status=validated&limit=20&offset=0"
```

**Response (200 OK):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "theme": "victorian mansion murder",
    "num_players": 8,
    "difficulty": "hard",
    "status": "validated",
    "created_at": "2025-10-04T14:30:00.000Z"
  },
  {
    "id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
    "theme": "film noir",
    "num_players": 6,
    "difficulty": "medium",
    "status": "characters_generated",
    "created_at": "2025-10-04T13:15:00.000Z"
  }
]
```

---

### Delete Game

**Endpoint:** `DELETE /games/{game_id}`

```bash
curl -X DELETE http://localhost:8000/games/$GAME_ID
```

**Response (204 No Content):**
No response body. Game and all related data deleted.

**Response (404 Not Found):**
```json
{
  "detail": "Game not found"
}
```

---

## Error Handling

### Common Error Responses

#### 400 Bad Request - Missing Dependencies
```json
{
  "detail": "Plot must be generated first. Call POST /games/{game_id}/plot"
}
```

#### 404 Not Found
```json
{
  "detail": "Game not found"
}
```

#### 422 Unprocessable Entity - Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "num_players"],
      "msg": "ensure this value is greater than or equal to 3",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Failed to generate characters"
}
```

---

## Workflow Enforcement

The API enforces the correct generation sequence:

```
1. Create Game (POST /games)
   ↓
2. Generate Characters (POST /games/{id}/characters)
   ↓
3. Generate Plot (POST /games/{id}/plot) - requires characters
   ↓
4. Generate Clues (POST /games/{id}/clues) - requires plot
   ↓
5. Generate Metadata (POST /games/{id}/metadata) - requires clues
   ↓
6. Validate (POST /games/{id}/validate) - requires metadata
   ↓
7. Retrieve Complete (GET /games/{id})
```

**Attempting steps out of order will return 400 Bad Request with a descriptive error message.**

---

## Advanced Examples

### Bash Script - Complete Workflow

```bash
#!/bin/bash

# Create game
RESPONSE=$(curl -s -X POST http://localhost:8000/games \
  -H "Content-Type: application/json" \
  -d '{"theme": "space station mystery", "num_players": 5, "difficulty": "medium"}')

GAME_ID=$(echo $RESPONSE | jq -r '.id')
echo "Created game: $GAME_ID"

# Generate all components
echo "Generating characters..."
curl -s -X POST http://localhost:8000/games/$GAME_ID/characters > /dev/null

echo "Generating plot..."
curl -s -X POST http://localhost:8000/games/$GAME_ID/plot > /dev/null

echo "Generating clues..."
curl -s -X POST http://localhost:8000/games/$GAME_ID/clues > /dev/null

echo "Generating metadata..."
curl -s -X POST http://localhost:8000/games/$GAME_ID/metadata > /dev/null

echo "Validating..."
VALIDATION=$(curl -s -X POST http://localhost:8000/games/$GAME_ID/validate)
PASSED=$(echo $VALIDATION | jq -r '.validation_passed')

if [ "$PASSED" = "true" ]; then
  echo "✓ Validation passed!"
  echo "Retrieving complete scenario..."
  curl -s http://localhost:8000/games/$GAME_ID | jq '.'
else
  echo "✗ Validation failed"
  echo $VALIDATION | jq '.validation_errors'
fi
```

### Python Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Create game
response = requests.post(f"{BASE_URL}/games", json={
    "theme": "cyberpunk heist",
    "num_players": 6,
    "difficulty": "hard"
})
game_id = response.json()["id"]
print(f"Created game: {game_id}")

# Generate components
endpoints = ["characters", "plot", "clues", "metadata"]
for endpoint in endpoints:
    print(f"Generating {endpoint}...")
    response = requests.post(f"{BASE_URL}/games/{game_id}/{endpoint}")
    if response.status_code != 200:
        print(f"Error: {response.json()}")
        exit(1)

# Validate
print("Validating...")
response = requests.post(f"{BASE_URL}/games/{game_id}/validate")
validation = response.json()

if validation["validation_passed"]:
    print("✓ Validation passed!")

    # Get complete scenario
    response = requests.get(f"{BASE_URL}/games/{game_id}")
    scenario = response.json()
    print(f"Title: {scenario['title']}")
    print(f"Characters: {len(scenario['characters'])}")
    print(f"Clues: {len(scenario['clues'])}")
else:
    print("✗ Validation failed:")
    for error in validation["validation_errors"]:
        print(f"  - {error}")
```

---

## Health Check

**Endpoint:** `GET /health`

```bash
curl http://localhost:8000/health
```

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

---

## API Documentation

Interactive API documentation is available at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
