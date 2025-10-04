#!/bin/bash

# Script to test the incremental API manually

echo "=== Testing Incremental API ==="
echo ""

# 1. Create game
echo "1. Creating game..."
RESPONSE=$(curl -s -X POST http://localhost:8000/games \
  -H "Content-Type: application/json" \
  -d '{
    "theme": "film noir",
    "num_players": 4,
    "difficulty": "easy"
  }')

echo "Response: $RESPONSE"
GAME_ID=$(echo $RESPONSE | python -c "import sys, json; print(json.load(sys.stdin).get('id', 'ERROR'))" 2>/dev/null)

if [ "$GAME_ID" = "ERROR" ] || [ -z "$GAME_ID" ]; then
  echo "ERROR: Failed to create game"
  exit 1
fi

echo "Game ID: $GAME_ID"
echo ""

# 2. Generate characters
echo "2. Generating characters..."
curl -X POST http://localhost:8000/games/$GAME_ID/characters \
  -H "Content-Type: application/json" \
  -v

echo ""
echo "=== Test Complete ==="
