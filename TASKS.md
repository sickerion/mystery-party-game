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
- [x] 39. Modifier les nodes pour accepter des données en entrée depuis la DB
  - Les endpoints API chargent depuis la DB et construisent MysteryGenerationState
  - Les nodes reçoivent des objets Pydantic depuis la DB via les endpoints
- [x] 40. Créer des fonctions wrapper pour chaque node
  - Implémenté dans generation.py: charge Game, appelle node, sauvegarde résultat
  - Chaque endpoint (characters, plot, clues, metadata, validate) fait ce workflow

### 6.6 Tests
- [x] 41. Tests unitaires pour les services de base de données (20 tests dans test_services.py)
- [x] 42. Tests d'intégration pour les nouveaux endpoints API (14 tests dans test_api_incremental.py)
- [x] 43. Tests end-to-end du workflow complet incrémental avec mocks LLM

### 6.7 Documentation
- [x] 44. Mettre à jour CLAUDE.md avec la nouvelle architecture API incrémentale
- [x] 45. Documenter le schéma de base de données (docs/DATABASE_SCHEMA.md)
- [x] 46. Créer des exemples d'utilisation de l'API incrémentale (docs/API_EXAMPLES.md)

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

---

## Phase 7: Frontend Web Application

### Objectif
Créer une interface web moderne avec React, Vite et shadcn/ui pour générer et gérer les mystery party games.

### 7.1 Configuration Initiale
- [x] 47. Initialiser le projet React avec Vite et TypeScript
  - Créer le projet dans le répertoire `frontend/`
  - Configurer TypeScript, ESLint, Prettier
- [x] 48. Installer et configurer shadcn/ui
  - Installer les dépendances (tailwindcss, shadcn/ui)
  - Configurer la palette de couleurs personnalisée
- [x] 49. Configurer la palette de couleurs dans Tailwind
  - Couleurs principales: navy (#1a1a2e), darkNavy (#16213e), teal (#0f3460)
  - Couleurs d'accentuation: gold (#d4af37), crimson (#8b0000), purple (#9b59b6)
  - Couleurs neutres: offWhite (#e8e8e8), lightGray (#a8a8a8), darkGray (#2d2d2d)
- [x] 50. Créer la structure de base du projet frontend
  - Dossiers: components/, pages/, services/, hooks/, types/, utils/

### 7.2 Services API
- [x] 51. Créer le service API client pour communiquer avec le backend
  - Fonctions pour tous les endpoints: POST /games, POST /games/{id}/characters, etc.
  - Gestion des erreurs et loading states
- [x] 52. Créer les types TypeScript pour les modèles de données
  - Game, Character, Plot, Clue, Metadata, ValidationResult
  - GameRequest, MysteryScenario

### 7.3 Composants de Base
- [x] 53. Créer le composant Layout avec navigation
- [x] 54. Créer le composant Header avec branding
- [x] 55. Créer le composant LoadingSpinner
- [x] 56. Créer le composant ErrorAlert
- [x] 57. Créer le composant GameCard pour afficher une partie dans la liste

### 7.4 Page Landing (Liste des Parties)
- [x] 58. Créer la page Landing (`pages/Landing.tsx`)
  - Afficher la liste des parties générées (GET /games)
  - Filtres par status
  - Bouton "Nouvelle Partie"
- [ ] 59. Implémenter la pagination pour la liste des parties
- [x] 60. Ajouter la fonctionnalité de suppression de partie (DELETE /games/{id})

### 7.5 Pipeline de Génération
- [x] 61. Créer le composant GenerationWizard avec stepper
  - Étape 1: Formulaire initial (thème, nombre de joueurs, difficulté)
  - Étape 2: Génération des personnages
  - Étape 3: Génération de l'intrigue
  - Étape 4: Génération des indices
  - Étape 5: Génération des métadonnées
  - Étape 6: Validation
- [x] 62. Créer le composant StepIndicator pour visualiser la progression
- [x] 63. Créer le formulaire de création de partie (GameForm)
  - Champs: theme, num_players, difficulty, special_requests
  - Validation des champs
- [x] 64. Implémenter la logique de génération séquentielle
  - Appels API successifs pour chaque étape
  - Affichage des résultats intermédiaires
  - Gestion des erreurs et retry

### 7.6 Composants d'Affichage des Résultats
- [x] 65. Créer le composant CharacterDisplay pour afficher un personnage
  - Afficher name, role, background, personality, secret, motive
- [x] 66. Créer le composant PlotDisplay pour afficher l'intrigue
  - Afficher setting, victim, crime, culprit, method, timeline, resolution
- [x] 67. Créer le composant ClueDisplay pour afficher un indice
  - Afficher description, location, revealed_by, significance
  - Badge pour les red herrings
- [x] 68. Créer le composant MetadataDisplay pour titre et instructions
- [x] 69. Créer le composant ValidationDisplay pour résultats de validation

### 7.7 Page de Détails d'une Partie
- [x] 70. Créer la page GameDetails (`pages/GameDetails.tsx`)
  - Route: /games/{id}
  - Charger et afficher toutes les informations (GET /games/{id})
  - Sections: Characters, Plot, Clues, Metadata, Validation
- [x] 71. Ajouter des onglets pour organiser les sections
- [ ] 72. Implémenter le bouton "Exporter PDF" (optionnel)

### 7.8 Formulaire d'Envoi de Courriels
- [x] 73. Créer le composant EmailAssignmentForm
  - Liste des personnages avec champ email
  - Validation des emails
  - Bouton "Envoyer les emails"
- [ ] 74. Créer l'endpoint backend POST /games/{id}/send-emails
  - Service d'envoi d'emails (SMTP ou service tiers)
  - Template d'email avec informations du personnage
- [x] 75. Intégrer le formulaire dans la page GameDetails

### 7.9 Routing et Navigation
- [x] 76. Configurer React Router
  - Route "/" → Landing
  - Route "/games/new" → GenerationWizard
  - Route "/games/{id}" → GameDetails
- [x] 77. Implémenter la navigation entre les pages

### 7.10 Tests et Finitions
- [x] 78. Ajouter des tests pour les composants principaux
  - Tests avec React Testing Library
- [x] 83. Créer un README pour le frontend

---

## Phase 8: Dark/Light Mode et Internationalisation (i18n)

### Objectif
Ajouter un système de thème (dark/light mode) et l'internationalisation pour supporter le français et l'anglais.

### 8.1 Dark/Light Mode
- [x] 84. Installer et configurer next-themes ou créer un context pour le theme
  - Créer ThemeProvider dans src/contexts/ThemeContext.tsx
  - Utiliser localStorage pour persister la préférence
- [x] 85. Créer le composant ThemeToggle
  - Bouton avec icône soleil/lune
  - Placer dans le Header
- [x] 86. Définir les couleurs pour le light mode dans Tailwind
  - Ajouter les variantes light des couleurs existantes
  - Utiliser les classes dark: de Tailwind
- [x] 87. Adapter tous les composants pour supporter les deux modes
  - Mettre à jour Button, Card, Input, Badge, etc.
  - Mettre à jour Layout et Header
  - Utiliser les classes dark: pour les couleurs de fond, texte, bordures
- [x] 88. Tester le theme toggle sur toutes les pages

### 8.2 Internationalisation (i18n)
- [x] 89. Installer react-i18next
  - npm install react-i18next i18next
- [ ] 90. Créer la structure des fichiers de traduction
  - src/locales/en/translation.json
  - src/locales/fr/translation.json
- [ ] 91. Configurer i18next
  - Créer src/i18n/config.ts avec configuration
  - Détecter la langue du navigateur par défaut
  - Persister la langue choisie dans localStorage
- [ ] 92. Créer le composant LanguageSwitcher
  - Dropdown avec drapeaux FR/EN (utiliser les assets existants)
  - Placer dans le Header à côté du ThemeToggle
- [ ] 93. Traduire tous les textes de l'interface
  - Traduire les pages: Landing, GameDetails, GenerationWizard
  - Traduire les composants: Header, GameCard, tous les steps
  - Traduire les messages d'erreur et de validation
  - Traduire les labels de formulaire et boutons
- [ ] 94. Adapter l'affichage des dates selon la locale
  - Utiliser Intl.DateTimeFormat pour formater les dates
- [ ] 95. Tester le changement de langue sur toutes les pages
- [ ] 96. Mettre à jour les tests pour supporter l'i18n
  - Wrapper les tests avec I18nextProvider

### 8.3 Layout et Header
- [ ] 97. Créer ou mettre à jour le composant Header
  - Ajouter ThemeToggle (soleil/lune)
  - Ajouter LanguageSwitcher (drapeaux FR/EN)
  - Aligner les contrôles à droite du header
- [ ] 98. Mettre à jour le Layout pour inclure le Header sur toutes les pages

### 8.4 Documentation
- [ ] 99. Mettre à jour CLAUDE.md avec les nouvelles fonctionnalités
- [ ] 100. Mettre à jour frontend/README.md
  - Documenter le système de thème
  - Documenter le système i18n
  - Expliquer comment ajouter de nouvelles traductions

### Palette de Couleurs (Tailwind Config)
```js
colors: {
  // Couleurs principales
  navy: '#1a1a2e',        // Fond principal
  darkNavy: '#16213e',    // Sections
  teal: '#0f3460',        // Accents

  // Couleurs d'accentuation
  gold: '#d4af37',        // CTA, éléments importants
  crimson: '#8b0000',     // Alertes, mystère
  purple: '#9b59b6',      // Liens, hover

  // Couleurs neutres
  offWhite: '#e8e8e8',    // Texte principal
  lightGray: '#a8a8a8',   // Texte secondaire
  darkGray: '#2d2d2d',    // Cartes, panels
}
```
