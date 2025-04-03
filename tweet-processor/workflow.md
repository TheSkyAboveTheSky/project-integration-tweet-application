# Flux de Fonctionnement du Tweet Processor

Ce document décrit le flux de données et le fonctionnement du composant Tweet Processor.

## Diagramme de Flux

```mermaid
flowchart TD
    subgraph "Entrée"
        kafka[("Kafka<br>Topic: raw-tweets")]
    end
    
    subgraph "Tweet Processor"
        direction TB
        main["main.py<br>Orchestrateur"]
        process["process_tweet()<br>Fonction principale"]
        
        subgraph "Processeurs spécialisés"
            hashtags["hashtag_processor.py<br>Extraction des hashtags"]
            location["location_processor.py<br>Normalisation géographique"]
            sentiment["sentiment_processor.py<br>Analyse de sentiment"]
        end
        
        main -->|"Consomme les<br>tweets bruts"| process
        process -->|"Applique"| hashtags
        process -->|"Applique"| location
        process -->|"Applique"| sentiment
    end
    
    subgraph "Sortie"
        es[("Elasticsearch<br>Index: tweets")]
        processed[("Kafka<br>Topic: processed-tweets")]
    end
    
    kafka --> main
    process -->|"Stocke"| es
    process -->|"Publie"| processed
    
    classDef input fill:#f9f0ff,stroke:#9d6aba,stroke-width:2px
    classDef process fill:#e6f0ff,stroke:#4a7ebb,stroke-width:2px
    classDef processor fill:#ccffcc,stroke:#66cc66,stroke-width:1px
    classDef output fill:#fff0f0,stroke:#cf5555,stroke-width:2px
    
    class kafka input
    class main,process process
    class hashtags,location,sentiment processor
    class es,processed output
```

## Description du Fonctionnement

1. **Consommation des Tweets** (`main.py`):
   - Crée un consommateur Kafka connecté au topic `raw-tweets`
   - Configure la connexion à Elasticsearch
   - Initialise le producteur Kafka pour le topic `processed-tweets`
   - Consomme les messages Kafka en continu

2. **Traitement des Tweets** (`process_tweet()`):
   - Reçoit les tweets bruts depuis Kafka
   - Applique en séquence les différents processeurs spécialisés
   - Ajoute des métadonnées de traitement (horodatage, etc.)

3. **Processeurs Spécialisés**:
   - **Extraction des Hashtags** (`hashtag_processor.py`):
     - Extrait les hashtags du texte du tweet
     - Standardise les hashtags (minuscules)
     - Compte les occurrences et calcule la fréquence

   - **Normalisation Géographique** (`location_processor.py`):
     - Valide et normalise les coordonnées géographiques
     - Détermine la région/continent basée sur les coordonnées
     - Formate les données géographiques pour Elasticsearch (geo_point)

   - **Analyse de Sentiment** (`sentiment_processor.py`):
     - Analyse le texte du tweet pour déterminer la polarité (positif/négatif)
     - Calcule la subjectivité du texte
     - Attribue une étiquette de sentiment (positif, négatif, neutre)

4. **Stockage et Publication**:
   - Indexe les tweets enrichis dans Elasticsearch
   - Publie les tweets traités dans le topic Kafka `processed-tweets`

Ce pipeline de traitement transforme les tweets bruts en données structurées et enrichies, prêtes à être analysées et visualisées. Le traitement est effectué en temps réel, permettant une analyse continue du flux de tweets.
