# Audit d'alignement Hören — SERVO DEUTSCH B2

Date : 12 novembre 2026

## Référence retenue

- Application : dépôt privé `servomasta-web/SERVO-DEUTSCH-B2`
- Branche source : `ameliorations-interface-v2`
- Version source : 7.2.0, versionCode 34
- Périmètre : examens Hören 001 à 030 uniquement
- Voix choisies : voix allemandes neuronales Edge TTS (Katja, Conrad, Amala, Killian)

## Résultat de la comparaison des anciennes sources audio

Seize anciens scripts contenaient des textes qui ne correspondaient pas au sujet ou au contenu audio de la classe Java correspondante :

| Examen | Sujet de l'application | Sujet/contenu de l'ancien script |
|---:|---|---|
| 009 | Intelligence artificielle au travail | Santé et prévention |
| 010 | Réduction du plastique | Médias numériques et concentration |
| 012 | Réseaux sociaux et protection des données | Services numériques de bibliothèque |
| 017 | Modèles de travail flexibles pour les parents | Formation tout au long de la vie |
| 018 | Stages pendant les études | Intelligence artificielle au travail |
| 019 | Formation tout au long de la vie | Animaux domestiques en location |
| 020 | Bruit dans les quartiers résidentiels | Tourisme dans les villes historiques |
| 021 | Pauses saines au travail | Relations entre générations |
| 022 | Services administratifs numériques | Éducation financière |
| 023 | Intégration des professionnels étrangers | Accessibilité des bâtiments |
| 024 | Logement abordable | Communication scientifique |
| 025 | Recyclage et économie circulaire | Éclairage des bâtiments publics |
| 026 | Service volontaire à l'étranger | Atelier de réparation |
| 027 | Mode durable | Petit-déjeuner de quartier |
| 028 | Repas scolaires et santé | Arbres et espaces verts urbains |
| 029 | Bibliothèques à l'ère numérique | Gaspillage alimentaire |

Autre anomalie de métadonnée : le script 008 portait encore le titre « Prüfung 006 — Ehrenamtliches Engagement », alors que son premier texte concerne le logement et correspond au thème de l'examen 008. Le générateur commun normalise également ce cas.

Les examens 001 à 007, 011, 013 à 016 et 030 présentaient une correspondance thématique dans les sources examinées. Le générateur commun les reconstruit néanmoins à partir de la source applicative afin d'assurer une méthode uniforme.

## Correction préparée

Les trente scripts `build_exam_NNN_aligned.py` sont désormais des points d'entrée vers un générateur commun : `rebuild_all_30_from_app.py`.

Ce générateur :
1. lit directement les textes dans `GoetheExamNNAudio.java` du dépôt de l'application ;
2. reprend les cinq documents courts, l'interview, la discussion et le Vortrag ;
3. conserve les textes de la source applicative, sans réécriture ;
4. vérifie la répartition des questions : 10 + 6 + 6 + 8 ;
5. génère huit MP3 avec les voix neuronales allemandes ;
6. mesure les durées, vérifie la taille et l'intégrité de chaque MP3 ;
7. crée un ZIP contenant exactement les huit noms de pistes attendus ;
8. écrit un manifeste par examen et un rapport global.

Ainsi, les textes audio sont extraits de la même classe Java que les questions, les choix de réponse et les explications. Cela supprime le risque de maintenir deux versions indépendantes des dialogues.

## Limites restantes avant livraison

- Les nouveaux fichiers MP3 et ZIP n'ont pas été générés dans cet environnement : la génération Edge TTS nécessite l'exécution du script avec accès réseau et FFmpeg.
- La release historique `audio-v1` contient encore les anciens fichiers ; elle ne doit pas être présentée comme la livraison corrigée.
- La release `audio-v2` doit être créée après génération et contrôle des 30 ZIP, avec uniquement les examens 001 à 030.
- La branche applicative de consolidation doit pointer vers `audio-v2`, mais ne doit pas être distribuée avant la publication de cette release.
- Les voix sont synthétiques neuronales, non humaines et non officielles Goethe.

## Critères d'acceptation

- 30 examens.
- 240 pistes MP3.
- Huit pistes par examen, avec les noms attendus par l'application.
- 30 ZIP valides et lisibles.
- Correspondance des textes audio avec les textes source de l'application.
- Répartition des questions 10 / 6 / 6 / 8.
- Écoutes autorisées 1 / 2 / 1 / 2.
- Release audio-v2 limitée à 30 archives.
