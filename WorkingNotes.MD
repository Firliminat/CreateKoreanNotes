# Script d'import de notes de vocabulaire Coréen dans Anki

## Créer les notes

### Sens des mots

- Naver Dictionnary : Pas API ❌
- 한국어 기초 사전 : Open API ✅

Le dictionnaire : https://krdict.korean.go.kr/kor/mainAction

Documentation de l'api :

- https://krdict.korean.go.kr/openApi/openApiInfo
- https://pub.dev/documentation/korean_dictionary/latest/

Un exemple de requête : https://krdict.korean.go.kr/api/search?key=DUMMY_APY_KEY&part=word&q=%EC%95%A1%EC%85%98&translated=y&trans_lang=3&advanced=y&method=exact

API Key : Emails

### Exemple de prononciation audio

Disponible sur le dictionnaire ✅
=> Pas toujours dispo ❌

TODO : Accessible via l'API ✅

=> Backup : https://ttsmp3.com/text-to-speech/Korean/ ❓

## Ajouter à Anki

- Notes : Par CSV. cf : ExampleData ✅
- Media : Coller dans ~/.local/share/Anki2/Alex/collection.media/ ✅

### Autes fonctionnalitées

- Tags : Indiquer si le mot en coréen existes déjà ✅
- Tags : Indiquer si plusieurs cartes ont le même sens ✅
- Supprimer les doublons en français ✅ 
- Expressions ❓
- Mots dérivés (... + 하다) ❓
- Prononciation en Hangul : Dispo dans le dictionnaire ❓
- Catégorie grammaticale : Dispo dans le dictionnaire ❓
- Sous-deck :
   - Full automaique ❌
   - Possible d'ajouter des tags selon les catégories du dictionnaire ❓
- Conjuguaisons ❓

### Anomalies

- Mots sans son ? Utiliser le back up ❓
- Plusieurs fois la même erreur ? => Améliorer la gestion des erreurs  ✅