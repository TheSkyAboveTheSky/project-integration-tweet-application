# Structure du Composant Tweet Collector

Ce composant est responsable de la collecte des tweets depuis une source de données (JSON Server) et leur envoi vers Kafka.

```mermaid
flowchart TD
    %% Structure principale
    Root["tweet-collector/"] --> Config[config.ini]
    Root --> Data[data/]
    Root --> Dockerfile[Dockerfile]
    Root --> MockData[mock_data/]
    Root --> README[README.md]
    Root --> Requirements[requirements.txt]
    Root --> Src[src/]
    
    %% Répertoire src
    Src --> Main[main.py]
    Src --> Collector[collector.py]
    Src --> KafkaProducer[kafka_producer.py]
    Src --> AddTweets[add_tweets.py]
    
    %% Répertoire mock_data
    MockData --> DB[db.json]
    
    %% Data directory
    Data --> GitKeep[.gitkeep]
    
    %% Relations entre fichiers
    Main -->|importe| Collector
    Collector -->|importe| KafkaProducer
    
    %% Styles pour meilleure visualisation
    classDef root fill:#f9f0ff,stroke:#9d6aba,stroke-width:2px
    classDef code fill:#e6f0ff,stroke:#4a7ebb,stroke-width:1px
    classDef data fill:#e6ffed,stroke:#2ea44f,stroke-width:1px
    classDef config fill:#fff8e6,stroke:#d9a012,stroke-width:1px
    classDef file fill:#f0f0f0,stroke:#666666,stroke-width:1px
    
    class Root root
    class Src code
    class Main,Collector,KafkaProducer,AddTweets code
    class MockData,Data data
    class DB,GitKeep data
    class Config,Requirements config
    class Dockerfile,README file
```

## Description des fichiers principaux

### Configuration
- **config.ini**: Configuration du collecteur (URLs, identifiants, paramètres)
- **requirements.txt**: Dépendances Python du service

### Code source (src/)
- **main.py**: Point d'entrée du service, initialise et lance le collecteur
- **collector.py**: Classe principale qui récupère et filtre les tweets
- **kafka_producer.py**: Gère la connexion à Kafka et l'envoi des messages
- **add_tweets.py**: Utilitaire pour ajouter des tweets factices à la base de données

### Données
- **mock_data/db.json**: Données JSON simulées pour le développement
- **data/**: Répertoire pour stocker des données temporaires/locales

## Flux d'exécution
1. **main.py** initialise une instance de `TweetCollector`
2. Le collecteur se connecte à la source de données (JSON Server)
3. Le collecteur récupère les tweets et les filtre (nouveaux uniquement)
4. Les tweets sont envoyés vers Kafka via le `TweetKafkaProducer`
5. Le processus se répète à intervalles réguliers
