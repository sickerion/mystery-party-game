# Mystery Party Game Generator - Backend Development Tasks

## Status Legend
- [ ] Not started
- [x] Completed
- [~] In progress

## Tasks

### Phase 1: Setup & Architecture
- [x] 1. Initialiser le projet Python avec les dépendances (LangGraph, LangChain, etc.)
- [x] 2. Créer la structure de base du projet backend
- [x] 3. Ajouter la gestion de configuration (API keys, modèles LLM)

### Phase 2: Data Models
- [x] 4. Implémenter les modèles de données (Character, Clue, Mystery, Scenario)

### Phase 3: LangGraph Workflow
- [x] 5. Créer le graph LangGraph pour la génération de mystères
- [x] 6. Implémenter les nodes du graph (génération personnages, intrigue, indices)
- [x] 7. Ajouter la logique de validation et cohérence du scénario

### Phase 4: API
- [x] 8. Créer l'API REST/FastAPI pour exposer les fonctionnalités

### Phase 5: Testing & Documentation
- [x] 9. Créer des tests pour les composants critiques
- [x] 10. Documenter l'architecture et l'utilisation dans CLAUDE.md

---

## Phase 6: API Incrémentale avec Persistance en Base de Données

### Objectif
Diviser la génération de mystère en appels API séparés, un pour chaque étape du workflow, avec stockage intermédiaire en base de données.

### 6.1 Base de Données - Modèles SQLAlchemy
- [x] 11. Créer le modèle `Game` pour stocker l'état global d'une partie en cours
  - Colonnes: id (UUID), theme, num_players, difficulty, special_requests, status, created_at, updated_at
  - Status: 'initialized', 'characters_generated', 'plot_generated', 'clues_generated', 'metadata_generated', 'validated', 'completed', 'failed'
- [x] 12. Créer le modèle `GeneratedCharacter` pour stocker les personnages générés
  - Colonnes: id, game_id (FK), name, role, background, personality, secret, motive, relationship_to_victim
- [x] 13. Créer le modèle `GeneratedPlot` pour stocker l'intrigue
  - Colonnes: id, game_id (FK), setting, victim, crime, culprit, murder_method, timeline (JSON), resolution
- [x] 14. Créer le modèle `GeneratedClue` pour stocker les indices
  - Colonnes: id, game_id (FK), clue_id, description, location, revealed_by, significance, misleading
- [x] 15. Créer le modèle `GeneratedMetadata` pour stocker les métadonnées
  - Colonnes: id, game_id (FK), title, estimated_duration, game_instructions, introduction
- [x] 16. Créer le modèle `ValidationResult` pour stocker les résultats de validation
  - Colonnes: id, game_id (FK), iteration, validation_passed, validation_errors (JSON), created_at

### 6.2 Base de Données - Migrations Alembic
- [x] 17. Créer la migration Alembic pour la table `games`
- [x] 18. Créer la migration Alembic pour la table `generated_characters`
- [x] 19. Créer la migration Alembic pour la table `generated_plots`
- [x] 20. Créer la migration Alembic pour la table `generated_clues`
- [x] 21. Créer la migration Alembic pour la table `generated_metadata`
- [x] 22. Créer la migration Alembic pour la table `validation_results`
- [x] 23. Exécuter les migrations pour créer les tables

### 6.3 Services - Couche d'Accès aux Données
- [x] 24. Créer `src/services/game_service.py` avec les méthodes CRUD pour Game
  - create_game(), get_game(), update_game_status(), list_games(), delete_game()
- [x] 25. Créer `src/services/character_service.py` avec les méthodes pour GeneratedCharacter
  - save_characters(), get_characters_by_game(), delete_characters_by_game()
- [x] 26. Créer `src/services/plot_service.py` avec les méthodes pour GeneratedPlot
  - save_plot(), get_plot_by_game(), delete_plot_by_game()
- [x] 27. Créer `src/services/clue_service.py` avec les méthodes pour GeneratedClue
  - save_clues(), get_clues_by_game(), delete_clues_by_game()
- [x] 28. Créer `src/services/metadata_service.py` avec les méthodes pour GeneratedMetadata
  - save_metadata(), get_metadata_by_game(), delete_metadata_by_game()
- [x] 29. Créer `src/services/validation_service.py` avec les méthodes pour ValidationResult
  - save_validation(), get_validations_by_game(), get_latest_validation(), delete_validations_by_game()

### 6.4 API - Endpoints Incrémentaux
- [x] 30. POST `/games` - Créer une nouvelle partie avec paramètres initiaux
  - Input: GameRequest (theme, num_players, difficulty, special_requests)
  - Output: Game (id, status='initialized')
- [x] 31. POST `/games/{game_id}/characters` - Générer les personnages
  - Appelle generate_characters_node()
  - Sauvegarde dans GeneratedCharacter
  - Met à jour status à 'characters_generated'
  - Output: List[Character]
- [x] 32. POST `/games/{game_id}/plot` - Générer l'intrigue
  - Charge les personnages depuis la DB
  - Appelle generate_plot_node()
  - Sauvegarde dans GeneratedPlot
  - Met à jour status à 'plot_generated'
  - Output: Plot
- [x] 33. POST `/games/{game_id}/clues` - Générer les indices
  - Charge personnages et intrigue depuis la DB
  - Appelle generate_clues_node()
  - Sauvegarde dans GeneratedClue
  - Met à jour status à 'clues_generated'
  - Output: List[Clue]
- [x] 34. POST `/games/{game_id}/metadata` - Générer les métadonnées
  - Charge tous les éléments depuis la DB
  - Appelle generate_metadata_node()
  - Sauvegarde dans GeneratedMetadata
  - Met à jour status à 'metadata_generated'
  - Output: Metadata (title, duration, instructions, introduction)
- [x] 35. POST `/games/{game_id}/validate` - Valider le scénario
  - Charge tous les éléments depuis la DB
  - Appelle validate_scenario_node()
  - Sauvegarde dans ValidationResult
  - Met à jour status à 'validated' ou 'failed'
  - Output: ValidationResult
- [x] 36. GET `/games/{game_id}` - Récupérer l'état complet d'une partie
  - Charge Game + tous les éléments associés
  - Output: MysteryScenario complet
- [x] 37. GET `/games` - Lister toutes les parties
  - Query params: status, limit, offset
  - Output: List[Game] (métadonnées uniquement, sans détails)
- [x] 38. DELETE `/games/{game_id}` - Supprimer une partie
  - Supprime en cascade tous les éléments associés

### 6.5 Adaptations des Nodes
- [ ] 39. Modifier les nodes pour accepter des données en entrée depuis la DB
  - Actuellement les nodes utilisent MysteryGenerationState du graph
  - Adapter pour recevoir des objets Pydantic depuis la DB
- [ ] 40. Créer des fonctions wrapper pour chaque node
  - `generate_characters_from_db(game_id)` charge Game, appelle node, sauvegarde résultat
  - Idem pour plot, clues, metadata, validation

### 6.6 Tests
- [ ] 41. Tests unitaires pour les services de base de données
- [ ] 42. Tests d'intégration pour les nouveaux endpoints API
- [ ] 43. Tests end-to-end du workflow complet incrémental

### 6.7 Documentation
- [ ] 44. Mettre à jour CLAUDE.md avec la nouvelle architecture API incrémentale
- [ ] 45. Documenter le schéma de base de données
- [ ] 46. Créer des exemples d'utilisation de l'API incrémentale

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
