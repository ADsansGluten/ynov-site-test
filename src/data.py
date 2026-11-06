# -*- coding: utf-8 -*-
"""Contenu du concept de refonte (source : pages publiques de ynov.com, relevées le 6 nov. 2026).
Les textes sont reformulés ; les chiffres et noms de programmes sont ceux du site public."""

# ---------------------------------------------------------------- CAMPUS
CAMPUS = [
    # code, slug, nom, ville, lon, lat, texte
    ("AIX", "aix-en-provence", "Aix-en-Provence", "Aix-en-Provence", 5.45, 43.53),
    ("BDX", "bordeaux", "Bordeaux", "Bordeaux (Le Bouscat)", -0.58, 44.84),
    ("LIL", "lille", "Lille", "Lille (Croix)", 3.06, 50.63),
    ("LYO", "lyon", "Lyon", "Lyon", 4.84, 45.76),
    ("MTP", "montpellier", "Montpellier", "Montpellier", 3.88, 43.61),
    ("NAN", "nantes", "Nantes", "Nantes", -1.55, 47.22),
    ("SOP", "sophia", "Nice - Sophia", "Sophia Antipolis (Valbonne)", 7.05, 43.62),
    ("VDE", "val-deurope", "Paris Est Val d'Europe", "Val d'Europe (Seine-et-Marne)", 2.78, 48.86),
    ("PAR", "paris", "Paris Ouest Nanterre", "Nanterre", 2.2, 48.89),
    ("REN", "rennes", "Rennes", "Rennes", -1.68, 48.11),
    ("ROU", "rouen", "Rouen", "Rouen", 1.1, 49.44),
    ("STR", "strasbourg", "Strasbourg", "Strasbourg", 7.75, 48.58),
    ("TLS", "toulouse", "Toulouse", "Toulouse", 1.44, 43.6),
]
CAMPUS_BY_CODE = {c[0]: c for c in CAMPUS}
ALL13 = [c[0] for c in CAMPUS]

# Journées portes ouvertes relevées (2026)
JPO = [
    ("NAN", "2026-11-07", "9h – 13h"), ("AIX", "2026-11-14", "10h – 12h"), ("STR", "2026-11-14", "10h – 13h"),
    ("TLS", "2026-11-14", "9h – 15h"), ("LIL", "2026-11-21", "10h – 13h"), ("LYO", "2026-11-21", "10h – 15h"),
    ("MTP", "2026-11-21", "10h – 17h"), ("REN", "2026-11-21", "9h – 16h"), ("AIX", "2026-11-28", "10h – 12h"),
    ("BDX", "2026-11-28", "10h – 16h"), ("NAN", "2026-11-28", "9h – 16h"), ("PAR", "2026-11-28", "10h – 15h"),
    ("ROU", "2026-11-28", "10h – 13h"), ("SOP", "2026-11-28", "10h – 14h"), ("VDE", "2026-11-28", "10h – 16h"),
    ("SOP", "2026-12-09", "14h – 16h"),
]

# ---------------------------------------------------------------- PÔLES & FAMILLES
POLES = [
    dict(slug="technologies-et-ingenierie", nom="Technologies & Ingénierie", verbes="Coder · Sécuriser · Automatiser",
         color="#4F46FF", soft="#ECEBFF",
         intro="Du code au cloud, de la data à l'IA : tu apprends à concevoir, sécuriser et déployer les systèmes qui font tourner le monde, avec la souveraineté, la performance et l'éthique dès la conception.",
         corps="Ce pôle réunit quatre spécialités complémentaires — développement, cybersécurité, infrastructure & cloud, data & intelligence artificielle — autour d'une culture commune : l'informatique. L'IA transforme le rapport au code, à la donnée et à la décision technique : les métiers ne disparaissent pas, ils se réinventent.",
         metiers=["Développeur full stack", "Architecte IT", "Ingénieur DevOps", "Analyste SOC", "Pentester", "Architecte cloud", "Data engineer", "Ingénieur machine learning"],
         familles=["intelligence-artificielle-data", "informatique", "cybersecurite"]),
    dict(slug="medias-et-creation-de-contenus", nom="Médias & Création de contenus", verbes="Imaginer · Créer · Médiatiser",
         color="#FF5C39", soft="#FFEDE8",
         intro="De la stratégie marketing à la création de contenus — animation 3D, podcast, streaming — tu apprends à développer des marques et à engager des audiences.",
         corps="Comprendre les publics, développer une marque, imaginer une campagne ou donner vie à un univers : tu construis ton parcours selon tes envies, avec des projets qui réunissent plusieurs formations et une immersion dans la Creator Economy.",
         metiers=["Directeur artistique", "UX/UI designer", "Game programmer", "Motion designer", "Monteur truquiste", "Social media manager", "Responsable marketing digital", "Product builder no-code"],
         familles=["3d-animation-jeu-video", "creation-digital-design", "marketing-communication-digital", "audiovisuel"]),
    dict(slug="architectures-et-ingenierie-numerique-des-batiments", nom="Architectures & Ingénierie numérique des bâtiments", verbes="Concevoir · Construire · Transformer",
         color="#0E9F6E", soft="#E4F7EE",
         intro="Du plan à la maquette 3D BIM, de l'éco-rénovation au jumeau numérique : tu conçois, modélises et pilotes les bâtiments et les villes durables.",
         corps="Deux métiers distincts, une culture et un environnement professionnel communs, au service d'une meilleure qualité de vie : éco-conception, performance énergétique, durabilité, de la conception à l'exploitation.",
         metiers=["Architecte d'intérieur", "Maître d'œuvre", "BIM manager", "Expert en jumeaux numériques", "Manager en ingénierie numérique du BTP", "AMO BIM"],
         familles=["architecture-d-interieur", "batiment-numerique"]),
]
POLE_BY_SLUG = {p["slug"]: p for p in POLES}

FAMILLES = [
    dict(slug="intelligence-artificielle-data", nom="Intelligence Artificielle & Data", pole="technologies-et-ingenierie",
         accroche="Des données brutes aux modèles d'IA.",
         texte="Tu apprends à collecter, fiabiliser et analyser les données, puis à concevoir et déployer des modèles d'IA. Après les fondamentaux de l'informatique en tronc commun, tu te spécialises : ingénierie des données, machine learning, IA générative — en pédagogie par projets, du Bachelor au Mastère."),
    dict(slug="informatique", nom="Informatique", pole="technologies-et-ingenierie",
         accroche="Tous les univers de l'IT, un socle technique solide.",
         texte="Développement web et mobile, game programming, robotique, systèmes embarqués, réseaux : du BTS au Mastère, tu construis les compétences pour concevoir, développer et faire évoluer des systèmes d'information."),
    dict(slug="cybersecurite", nom="Cybersécurité", pole="technologies-et-ingenierie",
         accroche="Protège les réseaux, maîtrise les systèmes.",
         texte="Lire un log, configurer un pare-feu, identifier des failles et les corriger : dès la première année, tu apprends en faisant. De l'administration sécurisée au pentest et à la gouvernance, du BTS au Mastère."),
    dict(slug="3d-animation-jeu-video", nom="3D, Animation & Jeu Vidéo", pole="medias-et-creation-de-contenus",
         accroche="Crée des univers immersifs.",
         texte="Modélisation, animation, moteurs temps réel, travail avec l'IA : tu transformes ta passion pour le jeu, l'animation et la 3D en carrière, avec les outils des professionnels."),
    dict(slug="creation-digital-design", nom="Création & Digital Design", pole="medias-et-creation-de-contenus",
         accroche="Design graphique, UX/UI, direction artistique.",
         texte="Design graphique, brand content, motion design, UX : tu explores l'univers visuel d'aujourd'hui avec les outils des pros et les IA génératives, sur de vrais projets."),
    dict(slug="marketing-communication-digital", nom="Marketing, Communication & Digital", pole="medias-et-creation-de-contenus",
         accroche="Pense, construis et fais rayonner les marques.",
         texte="Campagnes omnicanales, médias, réseaux sociaux, transformation digitale, no-code : du BTS au Mastère, des formations pour piloter la communication et le marketing à l'ère de l'IA."),
    dict(slug="audiovisuel", nom="Audiovisuel", pole="medias-et-creation-de-contenus",
         accroche="Image, son, montage, live.",
         texte="Tournage, lumière, son, plateau live, montage, étalonnage, podcast, formats verticaux : tu entres dans le vif du sujet dès la première année."),
    dict(slug="architecture-d-interieur", nom="Architecture d'Intérieur", pole="architectures-et-ingenierie-numerique-des-batiments",
         accroche="Imaginer, concevoir, rénover, coordonner.",
         texte="Tu conçois des projets d'architecture d'intérieur aux côtés de professionnels, du dessin à la maîtrise d'œuvre et à l'éco-rénovation."),
    dict(slug="batiment-numerique", nom="Bâtiment Numérique", pole="architectures-et-ingenierie-numerique-des-batiments",
         accroche="De la maquette BIM au jumeau numérique.",
         texte="Tu imagines et modélises les bâtiments, les villes et les territoires avec les outils du numérique : BIM, smart building, jumeaux numériques, économie de la construction."),
]
FAM_BY_SLUG = {f["slug"]: f for f in FAMILLES}

# ---------------------------------------------------------------- PROGRAMMES
# (famille, slug, type, titre, durée, entrée, campus, en_ligne, accroche, compétences)
C_ALL = ALL13
P = []

def add(fam, slug, typ, titre, duree, entree, campus, online, accroche, skills, titre_rncp=None, short=None):
    P.append(dict(fam=fam, slug=slug, typ=typ, titre=titre, duree=duree, entree=entree, campus=campus,
                  online=online, accroche=accroche, skills=skills, rncp=titre_rncp, short=short or titre))

# ---- IA & DATA
add("intelligence-artificielle-data", "bachelor-developpement-ia-data-engineering", "Bachelor", "Développement IA & data engineering",
    "3 ans", "Bac et Bac+2", C_ALL, False,
    "Apprends à faire parler les données et à construire l'IA, projet après projet. Un bachelor en trois ans, accessible après le bac, où tu manipules de la donnée dès la première année.",
    ["Programmer en Python, SQL et NoSQL", "Concevoir et administrer des bases de données relationnelles et NoSQL", "Construire des pipelines ETL et fiabiliser les flux de données",
     "Entraîner et évaluer des modèles de machine learning", "Créer des tableaux de bord et des visualisations", "Déployer avec Docker et les pratiques DevOps"],
    "Titre RNCP niveau 6", "Développement IA & data")
add("intelligence-artificielle-data", "mastere-expert-en-intelligence-artificielle", "Mastère", "Expert en intelligence artificielle",
    "2 ans", "Bac+3", C_ALL[:0] + ["AIX","BDX","LYO","PAR","TLS","SOP","MTP","LIL","REN","VDE","STR"], True,
    "Tout le monde utilise des modèles ; peu savent comment ils fonctionnent, les adapter à un besoin réel et les mettre en production. En deux ans, en alternance, tu passes du machine learning aux LLM, aux agents et à la vision par ordinateur.",
    ["Pipelines de données qui alimentent les modèles", "Machine learning et deep learning", "LLM : fine-tuning, RAG, agents intelligents, multimodalité",
     "Vision par ordinateur appliquée", "Explicabilité, RGPD et EU AI Act", "Déploiement et supervision en production", "Anglais technique"],
    "Titre RNCP niveau 7", "Expert en IA")
add("intelligence-artificielle-data", "mastere-data-engineer", "Mastère", "Data engineer",
    "2 ans", "Bac+3", ["AIX","BDX","LYO","NAN","PAR","TLS","MTP","LIL","REN","VDE","STR"], True,
    "Derrière chaque IA, il y a des pipelines. Tu deviens l'ingénieur qui construit les infrastructures qui collectent, fiabilisent et livrent la donnée aux équipes métier et aux modèles.",
    ["Pipelines de données robustes et orchestration", "Data warehouses et architectures lakehouse", "Volumes massifs avec Spark, temps réel avec Kafka",
     "Industrialisation : DevOps, CI/CD, Infrastructure as Code", "Supervision, sécurité et conformité RGPD", "Gouvernance : qualité, accès, coûts"],
    "Titre RNCP niveau 7", "Data engineer")
add("intelligence-artificielle-data", "mastere-expert-en-jumeaux-numeriques", "Mastère", "Expert en jumeaux numériques",
    "2 ans", "Bac+3", ["BDX","TLS"], False,
    "Une usine, un bâtiment, un réseau d'énergie : tu construis leur copie vivante, branchée sur les capteurs et les systèmes en place, pour simuler, surveiller et optimiser.",
    ["Cadrer un projet de jumeau numérique et démontrer sa rentabilité", "Lire l'architecture d'un site : automates, SCADA, MES, GMAO", "Maquette numérique en CAO et BIM",
     "Modéliser le comportement d'un système", "Collecter des données capteurs en temps réel (MQTT, OPC UA, Kafka)"],
    "Titre RNCP niveau 7", "Jumeaux numériques")

# ---- INFORMATIQUE
add("informatique", "bachelor-informatique", "Bachelor", "Informatique", "3 ans", "Bac, Bac+1 ou Bac+2", C_ALL, False,
    "Explore tous les univers de l'IT : développement web et mobile, game programming, robotique, systèmes embarqués. Tu touches à tout avant de choisir ta voie.",
    ["Concevoir des applications en intégrant la sécurité", "Développer des applications web, mobiles et logicielles", "Piloter un projet en approche DevOps",
     "Réaliser des interfaces d'échange de données", "Programmer des systèmes embarqués et robotiques (spécialité B3)"], "Titre RNCP niveau 6")
add("informatique", "bts-sio-sisr", "BTS", "BTS SIO – option SISR (infrastructure, systèmes et réseaux)", "2 ans", "Bac",
    ["AIX","BDX","LYO","NAN","PAR","TLS","MTP","LIL","REN","VDE","ROU","STR"], False,
    "Deviens le technicien expert de la sécurité et de la maintenance des réseaux informatiques d'une organisation : installer, administrer et sécuriser.", [], None, "BTS SIO SISR")
add("informatique", "bts-sio-slam", "BTS", "BTS SIO – option SLAM (solutions logicielles et applications métiers)", "2 ans", "Bac",
    ["AIX","BDX","LYO","NAN","PAR","TLS","MTP","LIL","REN","VDE","ROU","STR"], False,
    "Deviens le technicien expert capable de développer, déployer, sécuriser et maintenir des solutions informatiques pour une organisation.", [], None, "BTS SIO SLAM")
add("informatique", "mastere-expert-developpement-full-stack", "Mastère", "Expert développement full stack", "2 ans", "Bac+3 ou Bac+4", C_ALL, True,
    "Maîtrise toute la chaîne, de l'interface à l'infrastructure : applications web performantes, robustes et évolutives, du front-end au back-end.",
    ["Interfaces modernes avec React, rendu serveur avec Next.js", "API professionnelles : REST en Clean Architecture, microservices, GraphQL", "SQL avancé, optimisation de requêtes, NoSQL avec MongoDB",
     "Qualité : Test-Driven Development, tests unitaires et d'intégration", "Cadrage de projet de développement"], "Titre RNCP niveau 7", "Full stack")
add("informatique", "mastere-expert-developpement-mobile-iot", "Mastère", "Expert développement mobile & IoT", "2 ans", "Bac+3 ou Bac+4",
    ["AIX","BDX","LYO","NAN","PAR","TLS","SOP","REN","VDE"], True,
    "Des applications mobiles aux objets connectés industriels : tu conçois ce qui relie le physique au numérique.",
    ["Mobile cross-platform (React Native, Flutter) et natif Android (Kotlin, Jetpack Compose)", "Architectures IoT : capteurs, MQTT, plateformes industrielles, edge computing",
     "IA embarquée : inférence sur device, optimisation de modèles, détection d'anomalies"], "Titre RNCP niveau 7", "Mobile & IoT")
add("informatique", "mastere-game-programmer", "Mastère", "Game programmer", "2 ans", "Bac+3 ou Bac+4", [], True,
    "Conçois, développe et publie ton propre jeu, en format studio, sur les deux ans.",
    ["Game design document, core loop, architecture technique", "C# sous Unity : gameplay, physique, shaders, VFX", "C++, design patterns, Unreal Engine 5",
     "Multijoueur : architecture réseau, serveur autoritaire, netcode", "Optimisation : profiling CPU, GPU, mémoire"], "Titre RNCP niveau 7", "Game programmer")
add("informatique", "mastere-expert-en-systemes-embarques", "Mastère", "Expert en systèmes embarqués", "2 ans", "Bac+3 ou Bac+4", ["BDX","PAR","TLS"], False,
    "Du code au circuit : le logiciel embarqué fait fonctionner le monde physique — automobile, santé, aéronautique, énergie.",
    ["Ingénierie des exigences et architecture système", "C embarqué sur STM32, firmware multi-tâches avec FreeRTOS", "Conception matérielle : schémas, PCB, FPGA", "OS embarqués avancés (Linux embarqué)"],
    "Titre RNCP niveau 7", "Systèmes embarqués")
add("informatique", "mastere-expert-en-mecatronique", "Mastère", "Expert en mécatronique", "2 ans", "Bac+3 ou Bac+4", ["BDX","TLS"], False,
    "La robotique est l'innovation de demain : tu conçois les robots et les machines de l'industrie 4.0, là où mécanique, électronique et logiciel se rencontrent.",
    ["Traduire un besoin industriel en solution mécatronique", "Automates industriels (IEC 61131-3, OpenPLC, Siemens TIA Portal)", "Chaîne d'actionnement : moteurs, asservissement PID, électronique de puissance",
     "Conception mécanique : CAO 3D, prototypage par impression 3D"], "Titre RNCP niveau 7", "Mécatronique")
add("informatique", "mastere-expert-en-developpement-informatique-specialise-banque-assurance", "Mastère", "Expert en développement informatique spécialisé banque & assurance", "2 ans", "Bac+3", ["BDX"], False,
    "Un mastère construit avec La Banque Postale et CGI, en alternance chez eux, qui t'ouvre les deux mondes de l'informatique bancaire : grands systèmes Mainframe et développement moderne.",
    ["Grands systèmes : z/OS, COBOL, CICS, DB2", "Full stack : Java Spring, Angular, API REST en microservices", "Industrialisation : Git, CI/CD, conteneurs, Kubernetes, OpenShift",
     "Qualité : TDD, sécurité applicative OWASP, DevSecOps", "Comprendre le métier : IT appliqué à la finance"], "Titre RNCP niveau 7", "Banque & assurance")

# ---- CYBER
add("cybersecurite", "bachelor-cybersecurite", "Bachelor", "Cybersécurité", "3 ans", "Bac, Bac+1 ou Bac+2", C_ALL, False,
    "Protège les réseaux, maîtrise les systèmes : deux premières années pour un socle technique complet, puis la spécialisation.",
    ["Administrer et sécuriser réseaux, systèmes et environnements virtualisés", "Concevoir une solution en réponse à un besoin d'évolution de l'infrastructure",
     "Superviser l'infrastructure et traiter les incidents", "Participer à la gestion de la cybersécurité : politique, détection, traitement des incidents", "Conduire des audits techniques et des tests d'intrusion"],
    "Titre RNCP niveau 6")
add("cybersecurite", "bts-ciel", "BTS", "BTS CIEL – option A, informatique et réseaux", "2 ans", "Bac",
    ["AIX","BDX","LYO","PAR","MTP","LIL","VDE","ROU","STR"], False,
    "Cybersécurité, informatique et réseaux, électronique : tu formes à concevoir, sécuriser, exploiter et maintenir des réseaux informatiques.", [], None, "BTS CIEL")
add("cybersecurite", "mastere-expert-en-cybersecurite", "Mastère", "Expert en cybersécurité", "2 ans", "Bac+3 ou Bac+4", C_ALL, True,
    "De la gouvernance au Red Team : apprends à défendre une organisation en conditions réelles.",
    ["Auditer et cartographier un système d'information", "Analyse de risques EBIOS RM, conformité ISO 27001, NIS2, RGPD", "Architectures sécurisées : défense en profondeur, Zero Trust, PKI, IAM",
     "DevSecOps et pipelines CI/CD sécurisés", "Durcissement Windows et Linux, SOC et réponse à incident"], "Titre RNCP niveau 7")
add("cybersecurite", "mastere-expert-en-cloud-securite-infrastructure", "Mastère", "Expert en cloud, sécurité & infrastructure", "2 ans", "Bac+3 ou Bac+4", C_ALL, True,
    "Tout ce que le numérique produit tourne sur une infrastructure : conçois-la, sécurise-la, fais-la durer.",
    ["Auditer un SI et cadrer une stratégie d'évolution", "Infrastructures cloud : IaaS, réseaux virtualisés, Infrastructure as Code", "Automatiser : CI/CD, GitOps, environnements multiples",
     "Orchestrer à l'échelle avec Kubernetes", "Sécuriser : Zero Trust, micro-segmentation, ISO 27001, RGPD", "Continuité : monitoring et observabilité"], "Titre RNCP niveau 7", "Cloud, sécurité & infra")
add("cybersecurite", "mastere-expert-en-cybersecurite-pentester", "Mastère", "Expert en cybersécurité – Pentester", "2 ans", "Bac+3 ou Bac+4", [], True,
    "Construit sur Hack The Box, ce mastère est 100 % en ligne : tu apprends à attaquer les systèmes pour mieux les protéger.",
    ["Mener un test d'intrusion de bout en bout", "Attaquer et sécuriser des environnements Active Directory", "Rechercher et exploiter des vulnérabilités web et systèmes",
     "Détecter une attaque et conduire la réponse à incident", "Rédiger un rapport d'audit avec recommandations hiérarchisées", "Piloter la sécurité : SMSI, accès, PCA/PRA"], "Titre RNCP niveau 7", "Pentester")

# ---- 3D
add("3d-animation-jeu-video", "bachelor-designer-d-images-animees-3d-jeu-video", "Bachelor", "Designer d'images animées, 3D et jeu vidéo", "3 ans", "Bac et Bac+2",
    ["AIX","BDX","LYO","NAN","PAR","TLS","MTP","LIL","REN","VDE","ROU","STR"], False,
    "Tu apprends à modéliser, animer, coder et travailler avec l'IA pour produire des univers sur des moteurs temps réel, projet après projet.",
    ["Préparer, conceptualiser et prototyper un projet visuel animé ou immersif", "Créer et produire en 2D/3D, animer", "Concevoir des assets 2D & 3D : personnages, décors",
     "Maîtriser un moteur temps réel"], "Titre RNCP niveau 6", "Images animées, 3D & jeu vidéo")

# ---- CRÉATION
add("creation-digital-design", "bachelor-designer-graphique-et-d-interface", "Bachelor", "Design graphique et d'interface", "3 ans", "Bac, Bac+1 ou Bac+2", C_ALL, False,
    "Imagine, crée et donne du sens à ton univers visuel avec l'IA comme alliée : design graphique, brand content, motion design, UX.",
    ["Cadrer un projet digital", "Piloter avec agilité un projet digital", "Concevoir l'identité graphique et l'ergonomie d'une solution digitale"], "Titre RNCP niveau 6")
add("creation-digital-design", "mastere-ux-ui-design", "Mastère", "UX/UI Design", "2 ans", "Bac+3",
    ["AIX","BDX","LYO","PAR","TLS","SOP","MTP","LIL","REN","VDE","ROU","STR"], True,
    "Crée des expériences qui font la différence : des interfaces intelligentes, accessibles et responsables.",
    ["Chaîne de production d'un product designer : brief, parcours, tests, itération", "Gestion de projet agile (Scrum)", "Outils : Figma, Adobe XD, WordPress", "Analyse de données et recueil de data"], "Titre RNCP niveau 7")
add("creation-digital-design", "mastere-direction-artistique", "Mastère", "Direction artistique", "2 ans", "Bac+3",
    ["AIX","BDX","LYO","PAR","TLS","SOP","MTP","LIL","REN","VDE","ROU","STR"], True,
    "Créativité, vision, IA : deviens un directeur artistique nouvelle génération, capable de mixer sens créatif, culture visuelle et intelligence artificielle.",
    ["Conduite d'un projet de la brief client au déploiement", "Stratégie de communication multicanale", "Production avec les outils créatifs et l'IA"], "Titre RNCP niveau 7")

# ---- MARKETING
add("marketing-communication-digital", "bachelor-marketing-communication-digital", "Bachelor", "Marketing, Communication & Digital", "3 ans", "Bac et Bac+2", C_ALL, False,
    "Conçois des campagnes omnicanales, pilote un média de A à Z et construis une audience qui devient un business, au sein d'un Studio Creator Economy réunissant plusieurs formations chaque mercredi.",
    ["Analyser la demande d'un commanditaire", "Cadrer un projet : spécifications, livrables, faisabilité", "Planifier : planning, budget prévisionnel, feuille de route"], "Titre RNCP niveau 6")
add("marketing-communication-digital", "bachelor-product-builder-no-code", "Bachelor", "Product builder no-code", "3 ans", "Bac et Bac+2", [], True,
    "Conçois, teste et lance : pilote un produit digital de A à Z, du cadrage au lancement, et fais grandir des applications sans écrire une ligne de code.",
    ["Analyser les besoins utilisateurs et concevoir une solution no-code", "Développer une solution digitale no-code", "Déployer et maintenir la performance"], "Titre RNCP niveau 6")
add("marketing-communication-digital", "bts-communication", "BTS", "BTS Communication", "2 ans", "Bac",
    ["AIX","BDX","LYO","PAR","TLS","SOP","MTP","LIL","REN","VDE","ROU","STR"], False,
    "Deviens l'expert de la stratégie et des actions de communication d'une organisation : concevoir, réaliser et piloter des actions internes et externes, print, digitales et événementielles.", [], None, "BTS Communication")
add("marketing-communication-digital", "bts-ndrc", "BTS", "BTS NDRC – Négociation et digitalisation de la relation client", "2 ans", "Bac",
    ["AIX","BDX","LYO","PAR","TLS","MTP","VDE","STR"], False,
    "Deviens le commercial expert de la prospection, de la négociation et de la relation client à l'ère du digital.", [], None, "BTS NDRC")
add("marketing-communication-digital", "bts-mco", "BTS", "BTS MCO – Management commercial opérationnel", "2 ans", "Bac", ["AIX","PAR","MTP","VDE"], False,
    "Prends en charge la relation client, développe les ventes et assure le management opérationnel d'une unité commerciale.", [], None, "BTS MCO")
add("marketing-communication-digital", "bts-gpme", "BTS", "BTS GPME – Gestion de la PME", "2 ans", "Bac", ["BDX","PAR","MTP","VDE"], False,
    "Deviens le collaborateur polyvalent et le bras droit du dirigeant d'une PME : clients, fournisseurs, suivi administratif du personnel, gestion.", [], None, "BTS GPME")
add("marketing-communication-digital", "mastere-expert-en-marketing-communication-transformation-digitale", "Mastère", "Expert en marketing, communication & transformation digitale", "2 ans", "Bac+3",
    ["AIX","BDX","LYO","PAR","TLS","SOP","MTP","LIL","REN","VDE","ROU"], True,
    "Passe de l'exécutant au stratège : conçois et pilote des systèmes de croissance et des écosystèmes marketing.",
    ["Stratégies marketing systémiques et data-driven", "Systèmes marketing autonomes : automatisation et langages d'IA", "Architecture marketing omnicanale alignée sur les objectifs business"], "Titre RNCP niveau 7", "Marketing & transformation")
add("marketing-communication-digital", "mastere-expert-en-social-media-communication-transformation-digitale", "Mastère", "Expert en social média, communication & transformation digitale", "2 ans", "Bac+3",
    ["AIX","BDX","LYO","NAN","PAR","TLS","REN","VDE","ROU"], True,
    "Storytelling, influence, IA : deviens l'architecte des réputations et crée des récits de marque qui marquent les esprits.",
    ["Faire rayonner une marque selon ses valeurs", "Créer une expérience de marque mémorable", "Positionnement stratégique et cohérence on et off line", "Produire des contenus : vidéos, podcasts, réseaux sociaux, livres blancs"], "Titre RNCP niveau 7", "Social media")
add("marketing-communication-digital", "mastere-management-de-la-transformation-digitale", "Mastère", "Management de la transformation digitale", "2 ans", "Bac+3", [], True,
    "Ce mastère 100 % en ligne forme des managers capables de diagnostiquer une organisation, de concevoir et construire une solution digitale avec l'IA et le no-code, puis d'en piloter le déploiement.",
    ["Auditer les processus métiers et technologiques", "Cadrer une solution : besoins, budget, ROI, faisabilité no-code", "Expérience utilisateur : recherche, wireframes, prototypage assisté par IA", "MVP no-code (Bubble, Softr, Airtable…)"], "Titre RNCP niveau 7", "Transformation digitale")

# ---- AUDIOVISUEL
add("audiovisuel", "bachelor-audiovisuel", "Bachelor", "Création de contenus et audiovisuel", "3 ans", "Bac ou Bac+2", C_ALL, False,
    "Construis ta carrière dans l'audiovisuel dès la première année : image, son, montage, live, contenus pour les réseaux. Tout est concret, tu manipules, tu crées, tu participes à des tournages.",
    ["Écrire pour le web comme pour la fiction", "Préparer un projet de A à Z : dossier de production, plan de tournage", "Tourner, cadrer, gérer lumière et son",
     "Réaliser en direct : plateau live, régie streaming", "Monter, étalonner, mixer, sound design", "Formats d'aujourd'hui : vertical social, podcast"], "Titre RNCP niveau 6")
add("audiovisuel", "bts-metiers-de-l-audiovisuel-option-metiers-du-montage-et-de-la-postproduction", "BTS", "BTS Métiers de l'audiovisuel – montage et postproduction", "2 ans", "Bac",
    ["AIX","BDX","PAR","TLS","MTP","VDE","ROU","STR"], False,
    "Les images sont tournées : à toi de leur donner du rythme, du sens et de l'impact. Monter, truquer et finaliser des productions audiovisuelles professionnelles.", [], None, "BTS Montage & postproduction")

# ---- ARCHI INT
add("architecture-d-interieur", "bachelor-architecture-d-interieur", "Bachelor", "Architecture d'intérieur", "3 ans", "Bac ou Bac+2", C_ALL, False,
    "Construis ton expertise et prends progressivement en main des projets d'architecture d'intérieur aux côtés de professionnels du métier.",
    ["Dessiner l'existant et des concepts créatifs", "Modéliser en 3D un projet de bâtiment ou d'intérieur", "Concevoir et développer un projet d'architecture d'intérieur",
     "Connaître l'environnement professionnel : délais, budgets, normes, réglementation"], "Titre RNCP niveau 6")
add("architecture-d-interieur", "bts-era", "BTS", "BTS ERA – Étude et réalisation d'agencement", "2 ans", "Bac", ["STR"], False,
    "Deviens le technicien expert de la conception et de la réalisation d'agencements intérieurs sur mesure.", [], None, "BTS ERA")
add("architecture-d-interieur", "mastere-architecte-d-interieur-maitre-d-aeuvre", "Mastère", "Architecte d'intérieur – Maître d'œuvre", "2 ans", "Bac+3 ou Bac+4", C_ALL, False,
    "Maîtriser, coordonner, piloter : tu vas plus loin dans le savoir-faire technique et la conduite de projet d'architecture d'intérieur.",
    ["Étudier la faisabilité d'un projet", "Analyser le besoin du maître d'ouvrage et rédiger l'offre de mission", "Concevoir jusqu'à l'avant-projet sommaire puis définitif"], "Titre RNCP niveau 7", "Maître d'œuvre")
add("architecture-d-interieur", "mastere-architecte-d-interieur-expert-en-eco-renovation-et-energies-renouvelables", "Mastère", "Architecte d'intérieur – Expert en éco-rénovation et énergies renouvelables", "2 ans", "Bac+3 ou Bac+4",
    ["BDX","LYO","PAR","TLS","MTP","VDE","ROU"], False,
    "Imaginer, tester, réaliser : une expertise en éco-conception, rénovation écologique, performance énergétique et énergies renouvelables.",
    ["Étudier la faisabilité d'un projet d'intérieur", "Définir et développer des concepts créatifs", "Éco-conception et performance énergétique"], "Titre RNCP niveau 7", "Éco-rénovation")

# ---- BÂTIMENT NUMÉRIQUE
add("batiment-numerique", "bachelor-batiment-numerique", "Bachelor", "Bâtiment numérique", "1 an", "Bac+2", ["BDX","LYO","NAN","PAR","TLS","SOP","LIL","VDE"], False,
    "Deviens l'expert qui imagine et modélise les bâtiments, les villes et les territoires avec les outils du numérique : de la maquette BIM à la stratégie de projet.",
    ["Développer les pratiques BIM spécifiques à l'entreprise", "Analyser la maturité BIM et développer les processus internes", "Coordonner l'action de l'entreprise durant un projet BIM",
     "Modéliser et exploiter les maquettes numériques"], "Titre RNCP niveau 6")
add("batiment-numerique", "bts-mec", "BTS", "BTS MEC – Management économique de la construction", "2 ans", "Bac", ["BDX","LYO","NAN","PAR","TLS","LIL","REN","VDE","ROU"], False,
    "Deviens le technicien expert de l'étude, du chiffrage et du suivi économique des projets de construction.", [], None, "BTS MEC")
add("batiment-numerique", "mastere-manager-de-projet-bim-smart-building", "Mastère", "Manager de projet BIM & Smart Building", "2 ans", "Bac+3",
    ["AIX","BDX","LYO","NAN","PAR","TLS","LIL","REN","VDE","ROU"], True,
    "Piloter, connecter, optimiser : du scan 3D au Smart Building, tu construis une stratégie de digitalisation adaptée aux usages du bâtiment et coordonnes des projets BIM collaboratifs.",
    ["Élaborer la stratégie de digitalisation d'un bâtiment", "Analyser l'environnement, le périmètre et la faisabilité", "Conduire un projet de digitalisation"], "Titre RNCP niveau 7", "BIM & Smart Building")
add("batiment-numerique", "mastere-expert-en-jumeaux-numeriques-du-batiment-de-la-ville-et-des-territoires", "Mastère", "Expert en jumeaux numériques du bâtiment, de la ville et des territoires", "2 ans", "Bac+3",
    ["BDX","PAR","TLS"], True,
    "Analyser, anticiper, optimiser : du cadrage stratégique à l'exploitation, tu conçois, simules et pilotes des jumeaux numériques de bâtiments, de villes et de territoires.",
    ["Cadrer et sécuriser un projet de jumeau numérique", "Évaluer la maturité numérique de l'organisation", "Définir les indicateurs de performance", "Conformité réglementaire, éthique et cybersécurité"], "Titre RNCP niveau 7", "Jumeaux numériques bâtiment")

# ---------------------------------------------------------------- AUTRES CONTENUS
STATS = [("14", "campus", "dont Connect, 100 % en ligne"), ("9 000", "étudiants", "du BTS au Mastère"), ("5 000+", "entreprises partenaires", "un réseau qui recrute"),
         ("12", "diplômes RNCP", "niveaux 6 et 7, reconnus par l'État"), ("4 200+", "apprenants en alternance", "dès le Bachelor 2 ou 3")]

PEDAGOGIE = [
    ("Ymmersions", "3 semaines", "La période d'intégration : dès la rentrée, tu travailles en équipe sur un défi réel. Tu poses les bases, rencontres ta promo et comprends les enjeux de ton futur métier."),
    ("Ydays", "chaque semaine", "Une journée hebdomadaire (le mercredi, selon le campus) consacrée à des projets inter-formations : un développeur, une artiste 3D et un chef de projet marketing autour du même prototype."),
    ("Challenges 48h", "2 jours", "Des sessions intensives : chaque équipe reçoit un brief et 48 heures pour concevoir une réponse et la défendre, au rythme d'un vrai projet d'entreprise."),
    ("Ytrack", "à ton rythme", "La plateforme d'apprentissage exclusive d'Ynov : tu avances à ton rythme, valides des badges de compétences et collabores avec les autres étudiants."),
]

PILIERS = [
    ("Apprendre par la pratique", "Des formats variés qui alternent apports théoriques, mises en pratique, projets individuels et travaux collectifs. Essayer, analyser, ajuster et recommencer font partie du parcours."),
    ("Développer et valider des compétences", "Les formations sont construites autour de compétences concrètes, validées par des projets et par des titres RNCP de niveaux 6 et 7 reconnus par l'État."),
    ("Rencontrer des professionnels", "Des intervenants en activité transmettent ce qui se passe vraiment sur le terrain, et des entreprises partenaires entrent dans les projets de l'école."),
    ("Construire son projet professionnel", "Alternance, stages, job datings, réseau d'alumni : l'expérience professionnelle ne vient pas après le diplôme, elle commence bien avant."),
]

NEWS = [
    ("2026-11-06", "Paris Games Week 2026 : Ynov met à l'honneur les créations de ses étudiants", "Événement"),
    ("2026-11-06", "Ynov Rennes participe à l'European Cyber Week 2026", "Campus Rennes"),
    ("2026-11-05", "DuoDay 2026 : encourager les étudiants en situation de handicap à découvrir le monde professionnel", "Inclusion"),
    ("2026-11-04", "Stage découverte Ynov Lyon : 2 jours pour tester ta filière", "Campus Lyon"),
    ("2026-11-02", "Ynov Hand You : accompagner les étudiants en situation de handicap tout au long de leur parcours", "Inclusion"),
    ("2026-11-02", "Ynov et Trimble explorent les nouvelles perspectives de SketchUp et de l'intelligence artificielle", "Partenariat"),
    ("2026-10-28", "Premiers secours : l'équipe Ynov Strasbourg formée SST", "Campus Strasbourg"),
    ("2026-10-28", "La Fête du court métrage à Strasbourg avec Ynov", "Projet"),
    ("2026-10-09", "Prendre soin de sa santé mentale : Ynov s'engage", "Vie étudiante"),
    ("2026-10-06", "Les Ydays : apprendre autrement grâce à des projets concrets", "Pédagogie"),
    ("2026-10-06", "Jumeau numérique : quand les technologies transforment les métiers de l'industrie", "Dossier"),
    ("2026-10-05", "Ynov participe à la Paris Games Week 2026", "Événement"),
    ("2026-09-24", "Huit étudiants Ynov à l'International Game Concept Challenge 2026 au Japon", "International"),
    ("2026-09-11", "France Design Week 2026 : Ynov participe à la 7e édition", "Design"),
    ("2026-09-11", "Ynov lance sa première E-sport League sur League of Legends", "E-sport"),
    ("2026-09-09", "Les Ymmersions : une première immersion dans la pédagogie par projet", "Pédagogie"),
]

METIERS = [
    ("Cybersécurité", "Spécialiste en cybersécurité", 60000, "Bac+5"), ("Cybersécurité", "Administrateur de solution de sécurité", 38000, "Bac+3"),
    ("Cybersécurité", "Pentester", 36000, "Bac+5"), ("Cybersécurité", "Administrateur de solution de sécurité (accès Bac+5)", 36000, "Bac+5"),
    ("Architecture d'intérieur", "Scénographe (décorateur / architecte)", 36000, "Bac+5"), ("Architecture d'intérieur", "AMO BIM", 32000, "Bac+5"),
    ("Audiovisuel", "Monteur truquiste", 38400, "Bac+3"), ("Audiovisuel", "Cadreur / chef cadreur", 33600, "Bac+3"), ("Audiovisuel", "Cadreur-monteur", 33600, "Bac+3"),
    ("Audiovisuel", "Motion designer", 32000, "Bac+3"), ("Audiovisuel", "Étalonneur", 24000, "Bac+3"), ("Audiovisuel", "Coloriste", 24000, "Bac+3"),
]

PARTENAIRES = {
    "3D, Animation, Jeu vidéo": ["SNJV", "Unreal Engine", "Houdini", "SoWhen?", "Gendarmerie nationale", "Sapeurs-pompiers du Tarn"],
    "Architecture d'intérieur": ["Autodesk", "Unaid", "France Design Week", "Boesner", "Materiaux.archi"],
    "Bâtiment numérique": ["Graphisoft", "Dassault Systèmes", "Build & Connect", "Bimers", "Autodesk"],
    "Audiovisuel": ["Blackmagic Design"],
}

FAQ = [
    ("Les diplômes sont-ils reconnus ?", "Oui. Les diplômes sont des titres RNCP de niveaux 6 et 7 reconnus par l'État, dont Ynov est certificateur. Ils garantissent l'employabilité et un niveau de salaire cohérent avec le nombre d'années d'études."),
    ("Quels sont les différents types de contrats en alternance ?", "Deux contrats existent. Le contrat d'apprentissage concerne les 16 à 29 ans, dure de 6 mois à 3 ans (CDD ou CDI) et est rémunéré entre 27 % et 100 % du Smic selon l'âge et le niveau. Le contrat de professionnalisation concerne les 16 à 25 ans (et plus sous conditions), avec une durée minimale de 6 à 12 mois en CDD, et une rémunération entre 55 % et 100 % du Smic."),
    ("Quel est le rythme de l'alternance ?", "Il varie selon les formations : une semaine d'école pour deux semaines en entreprise, ou deux jours d'école pour trois jours en entreprise. Au total, près de 70 % du temps se passe en entreprise."),
    ("Quel est le rythme de formation sous statut étudiant ?", "Pour les formations Marketing, Communication & Digital et Création & Digital Design, les journées de cours sont condensées en demi-journées, ce qui laisse du temps pour un engagement associatif, un emploi à temps partiel ou un perfectionnement."),
    ("Comment financer mes études ?", "L'alternance est la voie principale : elle te donne un salaire et prend en charge les frais de formation (par l'entreprise ou son OPCO). Elle est disponible dès la 2e année de Bachelor pour certaines formations et pour l'ensemble des Mastères."),
    ("À quelle date candidater ?", "Les inscriptions ouvrent un an avant la rentrée visée, en septembre-octobre. Pour la rentrée 2027-2028, elles sont ouvertes depuis le 1er octobre 2026. Le dossier est validé sous réserve d'un effectif minimal : sinon, un transfert vers un autre campus peut être proposé."),
]

ADMISSION_STEPS = [
    ("Candidature en ligne", "Tu déposes ta candidature en moins d'une minute. Sur certains campus (Montpellier, Rouen, Rennes, Nice-Sophia, Toulouse), pas de mot de passe : tu envoies ton projet, l'équipe s'occupe du reste."),
    ("Étude du dossier", "Sous 48 heures, un conseiller te recontacte pour t'orienter, t'accompagner et coordonner, si besoin, les tests et l'entretien."),
    ("Entretien d'admission", "Une heure d'échange sur ta motivation et ton profil avec un chargé d'admission, sur le campus de ton choix, seul ou avec tes parents. Visite des salles et rencontre avec des étudiants incluses."),
    ("Décision finale", "Réponse sous 48 h après l'entretien. Tu as ensuite 10 jours pour valider ton inscription."),
]

HISTOIRE = [
    ("1938", "Point de départ de l'histoire d'Ynov, qui s'appuie sur plusieurs écoles historiques, dont ESTEI."),
    ("+ de 15 ans", "Ynov s'affirme comme école de l'enseignement supérieur privé dédiée aux métiers du numérique, avec une pédagogie par projets."),
    ("2022", "Ouverture du campus de Lille, puis extension de 3 000 m² à Croix inaugurée en 2024."),
    ("2024", "Ouverture de trois nouveaux campus : Strasbourg, Val d'Europe et Rouen. Livraison du campus de Montpellier (6 600 m²)."),
    ("2025", "Connect, le campus 100 % en ligne, se dote d'un campus virtuel immersif et gamifié."),
    ("2026", "Ynov se réorganise en trois pôles d'excellence et devient « l'école des transformations digitales »."),
]

PRESSE = [
    ("2026-10-13", "Ynov restructure son offre et s'impose comme l'école des transformations digitales"),
    ("2026-10-15", "Paris Games Week 2026 : Ynov fait son entrée sur le salon aux côtés de Webedia"),
    ("", "Ynov renforce son pôle Médias et Création de contenus avec Vincent Panozzo, figure majeure de l'audiovisuel"),
    ("2024-12-17", "Lille Ynov Campus : inauguration de la nouvelle extension de 3 000 m² à Croix"),
    ("2023-10-12", "Le groupe Ynov dévoile son nouveau site internet"),
]

SOPHIA_EQUIPE = [("Direction", "Pierre-Henri Dubois"), ("Direction", "Anaïs Menard"), ("Pédagogie", "Harmonie Vermandé"), ("Admission", "Alice Blouin")]
SOPHIA_YDAYS = ["Polewin et Agrivia", "Studio 360 et Dekin", "Infinite Doors", "Synapsis et Symoni", "7MINMAX et Pokito", "Marina Yacht Wear",
                "Delivry For Grandpa et Bubble Empire", "Cas 7 et Déclic", "Eco-Tag et Phaistos", "SignSpeak et Klouders", "Z6 et Rêves brisés"]

LEVEL_ORDER = {"BTS": 0, "Bachelor": 1, "Mastère": 2}

# ---------------------------------------------------------------- PROJETS ÉTUDIANTS
PROJETS = [
    dict(slug="mr-ybot", titre="Projet RED — « Mr Ybot »", court="Mr Ybot",
         accroche="Un jeu de rôle en terminal, écrit en Go, dans l'univers de la cybersécurité.",
         contexte="Projet final de l'Ymmersion · B1 · Ynov Sophia", equipe="Équipe de 3 · 3 semaines",
         tags=["Go", "CLI", "Cybersécurité", "Git"], fam="cybersecurite", prog="bachelor-cybersecurite"),
    dict(slug="recrutia", titre="RecrutIA — « Survie contre le Biais »", court="RecrutIA",
         accroche="Un mini-jeu de décisions en HTML/CSS : tu es data scientist et tu entraînes une IA de tri de CV.",
         contexte="Projet B1 Data · Ynov Sophia", equipe="Réalisé avec l'aide d'un mentor",
         tags=["HTML", "CSS", "JavaScript", "IA & éthique"], fam="intelligence-artificielle-data", prog="bachelor-developpement-ia-data-engineering"),
]
PROJ_BY_SLUG = {p["slug"]: p for p in PROJETS}
PROJ_BY_PROG = {p["prog"]: p["slug"] for p in PROJETS}
