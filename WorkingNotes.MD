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

### Exemple de prononciation

Disponible sur le dictionnaire

TODO : Accessible via l'API?

=> Backup : https://ttsmp3.com/text-to-speech/Korean/

## Ajouter à Anki

- Notes : Par CSV. cf : ExampleData
- Media : Coller dans ~/.local/share/Anki2/Alex/collection.media/

### Autes fonctionnalitées

- Expressions ?
- Mots dérivés (... + 하다)
- Ne pas ajouter cartes existantes ?
- Contexte : Indiquer si plusieurs cartes ont le même sens 
- Prononciation en Hangul : Dispo dans le dictionnaire
- Catégorie grammaticale : Dispo dans le dictionnaire
- Sous-deck : Manuel ? :/

### Anomalies

- Mots sans son ?
- Plusieurs fois la même erreur ?