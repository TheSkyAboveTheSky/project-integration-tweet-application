graph LR
    %% Composants Principaux
    subgraph "Sources de Données"
        jsondb[(Serveur JSON)]
    end

    subgraph "File de Messages"
        kafka[Kafka]
        zookeeper[ZooKeeper]
    end

    subgraph "Pipeline de Traitement"
        collector[Collecteur de Tweets]
        processor[Processeur de Tweets]
    end

    subgraph "Stockage de Données"
        elastic[(Elasticsearch)]
    end

    subgraph "Services Utilisateurs"
        kibana[Kibana]
        api[API de Tweets]
        frontend[Interface Utilisateur]
    end

    subgraph "Utilisateurs Finaux"
        browser[Navigateurs Web]
    end

    %% Connexions avec descriptions plus conviviales
    jsondb -->|"Fournit des tweets d'exemple<br>pour le développement"| collector
    collector -->|"Capture et envoie<br>les tweets bruts"| kafka
    zookeeper -.->|"Coordonne et gère<br>le cluster Kafka"| kafka
    kafka -->|"Transmet les tweets pour<br>traitement en temps réel"| processor
    processor -->|"Analyse le sentiment,<br>extrait les informations clés"| processor
    processor -->|"Stocke les tweets<br>enrichis"| elastic
    processor -->|"Publie les tweets traités<br>pour les abonnés"| kafka
    elastic -->|"Alimente les recherches<br>et les requêtes d'analyse"| api
    elastic -->|"Fournit les données pour<br>les tableaux de bord"| kibana
    api -->|"Livre les données structurées<br>via REST"| frontend
    frontend -->|"Affiche des visualisations<br>interactives"| browser

    %% Styles pour une meilleure hiérarchie visuelle
    classDef source fill:#f9f0ff,stroke:#9d6aba,stroke-width:2px;
    classDef processing fill:#e6f0ff,stroke:#4a7ebb,stroke-width:2px;
    classDef storage fill:#e6ffed,stroke:#2ea44f,stroke-width:2px;
    classDef visualization fill:#fff0f0,stroke:#cf5555,stroke-width:2px;
    classDef broker fill:#fff8e6,stroke:#d9a012,stroke-width:2px;
    classDef client fill:#f0f0f0,stroke:#666666,stroke-width:1px;

    class jsondb source;
    class collector,processor processing;
    class elastic storage;
    class api,frontend,kibana visualization;
    class kafka,zookeeper broker;
    class browser client;