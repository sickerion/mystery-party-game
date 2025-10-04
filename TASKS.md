# Mystery Party Game Generator - Backend Development Tasks

## Status Legend
- [ ] Not started
- [x] Completed
- [~] In progress

## Tasks

### Phase 1: Setup & Architecture
- [ ] 1. Initialiser le projet Python avec les dépendances (LangGraph, LangChain, etc.)
- [ ] 2. Créer la structure de base du projet backend
- [ ] 3. Ajouter la gestion de configuration (API keys, modèles LLM)

### Phase 2: Data Models
- [ ] 4. Implémenter les modèles de données (Character, Clue, Mystery, Scenario)

### Phase 3: LangGraph Workflow
- [ ] 5. Créer le graph LangGraph pour la génération de mystères
- [ ] 6. Implémenter les nodes du graph (génération personnages, intrigue, indices)
- [ ] 7. Ajouter la logique de validation et cohérence du scénario

### Phase 4: API
- [ ] 8. Créer l'API REST/FastAPI pour exposer les fonctionnalités

### Phase 5: Testing & Documentation
- [ ] 9. Créer des tests pour les composants critiques
- [ ] 10. Documenter l'architecture et l'utilisation dans CLAUDE.md

## Architecture Overview

### LangGraph Nodes
1. **Input Node**: Réception des paramètres (thème, nombre de joueurs, complexité)
2. **Character Generation Node**: Génération des personnages avec profils et secrets
3. **Plot Generation Node**: Création de l'intrigue principale et du coupable
4. **Clues Generation Node**: Génération des indices distribués entre personnages
5. **Validation Node**: Vérification de la cohérence et solvabilité du mystère
6. **Output Formatting Node**: Structuration finale du scénario

### State Structure
```python
TypedDict:
- theme: str
- num_players: int
- difficulty: str
- characters: List[Character]
- plot: Plot
- clues: List[Clue]
- mystery_solution: Solution
- validation_status: bool
```

### Tech Stack
- LangGraph: Orchestration du workflow
- LangChain: Intégration LLM (OpenAI, Anthropic, etc.)
- FastAPI: API REST
- Pydantic: Validation des modèles
- Python 3.11+
