# Structure du Composant Tweet Frontend

Ce composant est l'interface utilisateur de l'application, développée avec Flask et des librairies JavaScript pour la visualisation.

```mermaid
flowchart TD
    %% Structure principale
    Root["tweet-frontend/"] --> App[app.py]
    Root --> CheckAPI[check_api.py]
    Root --> Config[config.ini]
    Root --> Dockerfile[Dockerfile]
    Root --> README[README.md]
    Root --> Requirements[requirements.txt]
    Root --> Static[static/]
    Root --> Templates[templates/]
    Root --> GitIgnore[.gitignore]
    
    %% Répertoire Static
    Static --> CSS[css/]
    CSS --> StyleCSS[style.css]
    
    %% Répertoire Templates
    Templates --> BaseHTML[base.html]
    Templates --> DashboardHTML[dashboard.html]
    Templates --> TweetsHTML[tweets.html]
    Templates --> MapHTML[map.html]
    
    %% Relations entre fichiers
    App -->|charge| Templates
    Templates -->|étend| BaseHTML
    App -->|sert| Static
    BaseHTML -->|importe| StyleCSS
    App -->|appelle| API["Tweet API\ (externe)"]
    CheckAPI -->|teste| API
    
    %% Vues de l'application
    App --> Views{Vues}
    Views --> Dashboard["/Dashboard"]
    Views --> TweetsView["/tweets"]
    Views --> MapView["/map"]
    
    Dashboard -->|utilise| DashboardHTML
    TweetsView -->|utilise| TweetsHTML
    MapView -->|utilise| MapHTML
    
    %% Styles pour meilleure visualisation
    classDef root fill:#f9f0ff,stroke:#9d6aba,stroke-width:2px
    classDef code fill:#e6f0ff,stroke:#4a7ebb,stroke-width:1px
    classDef static fill:#e6ffed,stroke:#2ea44f,stroke-width:1px
    classDef template fill:#fff0f0,stroke:#cf5555,stroke-width:1px
    classDef config fill:#fff8e6,stroke:#d9a012,stroke-width:1px
    classDef file fill:#f0f0f0,stroke:#666666,stroke-width:1px
    classDef view fill:#ffeecc,stroke:#e69500,stroke-width:1px
    
    class Root root
    class App,CheckAPI code
    class Static,CSS,StyleCSS static
    class Templates,BaseHTML,DashboardHTML,TweetsHTML,MapHTML template
    class Config,Requirements config
    class Dockerfile,README,GitIgnore file
    class Views,Dashboard,TweetsView,MapView,APIProxies view
```

## Description des fichiers principaux

### Application
- **app.py**: Point d'entrée de l'application Flask, définit les routes et la logique
- **check_api.py**: Outil de diagnostic pour vérifier la connexion à l'API
- **config.ini**: Configuration du frontend (URL de l'API, paramètres Flask)
- **requirements.txt**: Dépendances Python du service

### Interface utilisateur
- **static/**: Fichiers statiques servis directement
  - **css/style.css**: Styles personnalisés pour l'application

- **templates/**: Templates Jinja2 pour les vues HTML
  - **base.html**: Template de base avec structure commune (header, footer, navbar)
  - **dashboard.html**: Vue principale avec tableaux de bord et graphiques
  - **tweets.html**: Interface de navigation des tweets avec filtres
  - **map.html**: Visualisation géographique des tweets sur une carte

## Vues principales

1. **Dashboard** ('/')
   - Graphiques de tendances des hashtags
   - Distribution des sentiments
   - Répartition géographique
   - Tableaux de données résumées

2. **Tweets** ('/tweets')
   - Liste paginée des tweets
   - Filtrage par texte, hashtag, sentiment
   - Affichage détaillé des tweets et métadonnées

3. **Map** ('/map')
   - Carte interactive avec les emplacements des tweets
   - Filtrage par sentiment et hashtag
   - Visualisation par couleur selon le sentiment

4. **Proxies API** ('/api/*')
   - Endpoints qui relaient les requêtes à l'API principale
   - Évite les problèmes de CORS depuis le navigateur

## Technologies frontend

- **Bootstrap 5**: Framework CSS pour l'interface responsive
- **Chart.js**: Visualisations graphiques des données
- **Leaflet.js**: Cartes interactives pour la géolocalisation
