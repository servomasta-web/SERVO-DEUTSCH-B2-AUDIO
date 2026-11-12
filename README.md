# SERVO DEUTSCH B2 — Audio

Dépôt public réservé aux packs audio de l'application **SERVO DEUTSCH B2**.

Le code source de l'application reste dans le dépôt privé `SERVO-DEUTSCH-B2`.

## Format des packs

Les packs sont publiés comme pièces jointes de la GitHub Release `audio-v1`.

- Archives : `exam-001.zip` à `exam-033.zip`
- Chaque archive contient huit pistes MP3 :
  - `teil1_01.mp3` à `teil1_05.mp3`
  - `teil2_01.mp3`
  - `teil3_01.mp3`
  - `teil4_01.mp3`

## Utilisation dans l'application

L'application télécharge le pack correspondant à l'examen sélectionné et extrait les pistes dans son cache local. Les parties 2 et 4 sont diffusées deux fois ; les parties 1 et 3 une seule fois.

**Nature des voix :** les packs utilisent des voix allemandes neuronales de synthèse vocale.

## Maintenance

Les scripts `build_exam_NNN_aligned.py` servent de sources textuelles pour les pistes. Toute modification d'un script audio doit être suivie d'une vérification de cohérence avec les questions du dépôt de l'application avant toute nouvelle publication.

Aucune piste audio n'est modifiée par les contrôles de cohérence des questions.
