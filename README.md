# SERVO DEUTSCH B2 — Audio

Dépôt public des packs audio de **SERVO DEUTSCH B2**. La version de référence de l'application est la branche `ameliorations-interface-v2` du dépôt privé `SERVO-DEUTSCH-B2` (version 7.2.0).

## Périmètre

- **30 examens Hören uniquement** : `exam-001.zip` à `exam-030.zip`.
- Chaque archive contient exactement huit pistes MP3 :
  - `teil1_01.mp3` à `teil1_05.mp3`
  - `teil2_01.mp3`
  - `teil3_01.mp3`
  - `teil4_01.mp3`
- Les examens 031 à 033 sont exclus de la version actuelle.
- Les parties 1 et 3 sont écoutées une fois ; les parties 2 et 4 deux fois.

## Nature des voix

Les enregistrements utilisent des **voix allemandes neuronales de synthèse (Edge TTS)**. Ce sont des voix synthétiques naturelles, et non des enregistrements de locuteurs humains ni des audios officiels du Goethe-Institut. Les contenus sont des exercices originaux d'entraînement.

## Source de vérité et alignement

Les textes prononcés doivent toujours provenir des mêmes classes Java que les questions et les corrigés de l'application :

`app/src/main/java/com/servo/deutschb2/GoetheExamNNAudio.java`

Le générateur unique `rebuild_all_30_from_app.py` extrait directement les cinq textes du Teil 1, l'interview du Teil 2, la discussion du Teil 3 et le Vortrag du Teil 4. Il ne réécrit pas ces textes. Il valide aussi les nombres de questions (10, 6, 6 et 8), crée les huit MP3, mesure leurs durées avec `ffprobe`, vérifie l'archive ZIP et écrit un manifeste de contrôle pour chaque examen.

## Reconstruction complète dans Termux

Place les deux dépôts côte à côte, puis exécute depuis ce dépôt :

```bash
bash rebuild_all_30_termux.sh ../SERVO-DEUTSCH-B2-7.2.0
```

Le script installe les dépendances manquantes, lance la reconstruction des 30 examens et vérifie les archives. Si le dossier de l'application porte un autre nom, remplace le chemin indiqué.

Le générateur produit :
- `output/exam-001.zip` à `output/exam-030.zip`
- un manifeste `exam-NNN.manifest.json` pour chaque pack
- `output/audio-build-report.json`, récapitulatif des 30 examens et des 240 pistes.

Un script individuel reste disponible, par exemple :

```bash
SERVO_APP_ROOT=../SERVO-DEUTSCH-B2-7.2.0 python build_exam_009_aligned.py
```

## Publication

Les archives de la release historique `audio-v1` sont des fichiers hérités et ne constituent pas la livraison consolidée. Après reconstruction et vérification des 30 ZIP, publier une nouvelle release **`audio-v2`** contenant uniquement `exam-001.zip` à `exam-030.zip`.

La branche applicative consolidée doit pointer vers `audio-v2`. Ne pas fusionner cette branche ni distribuer l'APK avant que les 30 nouveaux packs soient générés et que la release `audio-v2` soit publiée.
