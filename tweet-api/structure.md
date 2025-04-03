# Structure du Composant Tweet API

Ce composant est une API REST basée sur FastAPI qui expose les tweets traités stockés dans Elasticsearch.

```mermaid
flowchart TD
    %% Structure principale
    Root["tweet-api/"] --> Cache[cache.py]
    Root --> Config[config.py]
    Root --> Dockerfile[Dockerfile]
    Root --> Main[main.py]
    Root --> README[README.md]
    Root --> Requirements[requirements.txt]
    Root --> GitIgnore[.gitignore]
    Root --> EnvFiles[".env"]
    
    %% Relations entre fichiers
    Main -->|importe| Config
    Main -->|utiliser| Cache
    
    %% Connexions externes
    ES[("Elasticsearch\nIndex: tweets")] --> Main
    Main --> Clients["Clients API\n (Frontend, etc)"]

    
    %% Styles pour meilleure visualisation
    classDef root fill:#f9f0ff,stroke:#9d6aba,stroke-width:2px
    classDef code fill:#e6f0ff,stroke:#4a7ebb,stroke-width:1px
    classDef endpoint fill:#e6ffed,stroke:#2ea44f,stroke-width:1px
    classDef config fill:#fff8e6,stroke:#d9a012,stroke-width:1px
    classDef file fill:#f0f0f0,stroke:#666666,stroke-width:1px
    classDef datasource fill:#ffeecc,stroke:#e69500,stroke-width:2px
    
    class Root root
    class Main,Cache code
    class Endpoints,Root_,GetTweets,GetTrends,GetRegions,GetSentiment,GetMapData,GetTweetById endpoint
    class Config,Requirements,EnvFiles config
    class Dockerfile,README,GitIgnore file
    class ES,Clients datasource
```

## Description des fichiers principaux

### Configuration et Utilitaires
- **config.py**: Configuration de l'API (connexion à Elasticsearch, paramètres API)
- **cache.py**: Implémentation facultative de mise en cache pour améliorer les performances
- **requirements.txt**: Dépendances Python du service

### Code principal
- **main.py**: Point d'entrée de l'API FastAPI, définit tous les endpoints et la logique

## Endpoints de l'API

L'API expose plusieurs endpoints pour accéder aux données des tweets:

- **`/`**: Healthcheck et informations sur l'API
- **`/tweets`**: Liste de tweets avec filtrage et pagination
  - Paramètres: q (recherche), hashtag, sentiment, region, limit, offset
- **`/tweets/{id}`**: Récupère un tweet spécifique par ID
- **`/trends`**: Obtient les hashtags tendance
  - Paramètres: limit, q (filtre), sentiment
- **`/regions`**: Distribution géographique des tweets
- **`/sentiment`**: Résumé de l'analyse de sentiment
- **`/map-data`**: Données géographiques pour visualisation sur carte
  - Paramètres: sentiment, hashtag, limit

## Modèles de données

L'API utilise Pydantic pour valider et documenter les modèles de données:
- **Tweet**: Structure complète d'un tweet traité
- **TweetResponse**: Liste paginée de tweets
- **TrendingHashtag** et **TrendsResponse**: Hashtags tendance
- **RegionCount** et **RegionsResponse**: Distribution par région
- **SentimentSummary**: Distribution des sentiments
