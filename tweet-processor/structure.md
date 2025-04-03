# Structure du Composant Tweet Processor

Ce composant est responsable du traitement et de l'enrichissement des tweets bruts provenant de Kafka, avant de les stocker dans Elasticsearch.

```mermaid
flowchart TD
    %% Structure principale
    Root["tweet-processor/"] --> Config[config.ini]
    Root --> Dockerfile[Dockerfile]
    Root --> README[README.md]
    Root --> Requirements[requirements.txt]
    Root --> RunLocal[run-local.sh]
    Root --> Src[src/]
    
    %% Répertoire src
    Src --> Init[__init__.py]
    Src --> Main[main.py]
    Src --> Processors[processors/]
    
    %% Répertoire processors
    Processors --> ProcInit[__init__.py]
    Processors --> HashtagProc[hashtag_processor.py]
    Processors --> LocationProc[location_processor.py]
    Processors --> SentimentProc[sentiment_processor.py]
    
    %% Relations entre fichiers
    Main -->|importe| HashtagProc
    Main -->|importe| LocationProc
    Main -->|importe| SentimentProc
    
    %% Flux de données
    KafkaInput[("Kafka\nraw-tweets")] --> Main
    Main --> ESOutput[("Elasticsearch\ntweets")]
    Main --> KafkaOutput[("Kafka\nprocessed-tweets")]
    
    %% Styles pour meilleure visualisation
    classDef root fill:#f9f0ff,stroke:#9d6aba,stroke-width:2px
    classDef code fill:#e6f0ff,stroke:#4a7ebb,stroke-width:1px
    classDef module fill:#e6ffed,stroke:#2ea44f,stroke-width:1px
    classDef config fill:#fff8e6,stroke:#d9a012,stroke-width:1px
    classDef file fill:#f0f0f0,stroke:#666666,stroke-width:1px
    classDef data fill:#ffeecc,stroke:#e69500,stroke-width:2px
    
    class Root root
    class Src code
    class Processors module
    class Main,Init,ProcInit code
    class HashtagProc,LocationProc,SentimentProc module
    class Config,Requirements config
    class RunLocal,Dockerfile,README file
    class KafkaInput,ESOutput,KafkaOutput data
```

## Description des fichiers principaux

### Configuration
- **config.ini**: Configuration du processeur (connexions Kafka/Elasticsearch, paramètres de traitement)
- **requirements.txt**: Dépendances Python du service
- **run-local.sh**: Script pour exécuter le processeur en environnement local

### Code source (src/)
- **main.py**: Point d'entrée du service, gère la connexion à Kafka et Elasticsearch, et orchestre le processus de traitement
- **processors/**: Modules spécialisés pour le traitement des tweets
  - **hashtag_processor.py**: Extraction et analyse des hashtags
  - **location_processor.py**: Normalisation des données géographiques
  - **sentiment_processor.py**: Analyse de sentiment des textes des tweets

## Traitement des tweets
Le processeur effectue plusieurs transformations sur chaque tweet:

1. **Extraction des hashtags** (hashtag_processor.py):
   - Extraction des hashtags à partir du texte
   - Comptage et calcul de fréquence

2. **Normalisation géographique** (location_processor.py):
   - Validation des coordonnées géographiques
   - Détermination de la région (continent)
   - Formatage pour Elasticsearch (geo_point)

3. **Analyse de sentiment** (sentiment_processor.py):
   - Calcul de la polarité (positive/négative)
   - Calcul de la subjectivité
   - Attribution d'une étiquette (positive/négative/neutre)

Après traitement, les tweets enrichis sont:
- Indexés dans Elasticsearch
- Publiés dans un topic Kafka de sortie
