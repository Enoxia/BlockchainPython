# Projet Blockchain

Ce projet à pour but de simuler un système de vote fictif (élection) en utilisant la technologie blockchain. Le projet devra retrouver tous les avantages d'une blockchain (immuabilité, anonymat / pseudonymat, décentralisation)


# Délimitation du projet : choix du consensus

Parmi tous les différents consensus qui existent, notre choix s'est porté sur le [Proof Of Authority](https://en.wikipedia.org/wiki/Proof_of_authority)


## Proof Of Authority

Le Proof-Of-Authority (PoA) est une méthode de consensus basé sur la réputation des noeuds, qui donne à un nombre restreint et définit d’acteurs d’une blockchain le pouvoir de valider des transactions ou interactions avec le réseau et de mettre à jour son registre plus ou moins distribué.

Ce consensus apporte des avantages pour notre projet que les autres consensus n'ont pas ; 

- Aucune haute performance hardware n'est requise pour compléter les blocs ( ≠ Proof Of Work)
- Un groupe de machines dites "validatrices" ou "légitimes" doivent valider chaque nouveau bloc de transactions (algorithme basé sur la confiance). Dans notre cas, le(s) groupe(s) de machines validatrices seraient les bureaux de votes
- Le consensus nécessite un nombre définit et restreint de noeuds, ce qui s'adapte parfaitement à notre contexte puisqu'à chaque élection présidentielle, nous sommes en mesure de savoir exactement le nombre de votants (= le nombre de personnes majeures d'origine française inscrites sur les listes électorales) 
- Les transactions effectuées sont plus rapides, les blocs fermés plus rapidement car pas besoin de vérifications (confiance)


# Description du projet : 

Pour construire notre projet, nous nous sommes basés sur les réflexions suivantes :  

- Une base de données contenant la liste des électeurs et des candidats
- Simuler 1 wallet / personne (nominatif)
- Simuler 1 token par votant / électeur
- Avoir une interface utilisateur le plus "User Friendly" possible
- Pouvoir avoir un accès à la blockchain et à ses blocs
- Vérifier l'anonymat de chaque bloc ; on ne doit pas savoir qui a voté pour qui
- Eventuellement faire tourner notre application dans un réseau décentralisé (P2P)
- 


# Réalisation du projet :
## 08/02 : Structure de la Blockchain
Réflexion sur les différentes fonctions à utiliser:
* Création des fichiers JSON
* Ecriture dans les fichiers JSON
* Structure des transactions :
```json
 {
        "timestamp":"08-02-2023_16:19:12",
        "id":1,
        "Tokens":0,
        "Source":"INE1",
        "Desti":"INE2"
    }
```

## 01/03 : Formation BDD & Génération blockchain
* Réglage de la création automatique des JSON -> Besoin de [].
* Mise en place de la vérification des blocs (MAX 10 transactions)
* Mise en place du changement de fichier bloc (e-vote-0.sjon à e-vote-1.json)
* Installation d'une GUI minimale:
```bash
What is your choice : 1: Send token | 2: See wallet1
For Who you want to send the token ? : q
[+] Generate the transaction ....
Block Completed
[+]Transaction implemented !
What is your choice : 1: Send token | 2: See wallet
```

* Génération de la BDD des candidats:
```json
[
    {
        "ine": "02jn28nB2",
        "nom": "Dan",
        "mdp":"f71dbe52628a3f83a77ab494817525c6",
        "porte-feuille": "18162673JDUC29",
        "candidat": true,
        "aVoter": true
    },
    {
        "ine": "02jn33B3",
        "nom": "Arthur",
        "mdp": "f71dbe52628a3f83a77ab494817525c6",
        "porte-feuille": "18162673JD23019",
        "candidat": true,
        "aVoter": true
    }
]
```

## 15/03 : Ajout du hachage des blocks
* Mise en place de la fonction de hachage + structure de "lien" dans les blocs :
```json
{
        "timestamp": "15-03-2023_11:51:12",
        "Hash": "b9d478df49a2763e857436f600a423222b951eb812f7f1712fc8371b61c81d2a"
},
```

## 29/03 : Fusion Script/GUI
* Vérification de la présence des fichiers "genesis bloc" et "bloc 0" -> Evite de refaire l'initialisation
* Ajout des résultats, gestion des erreurs + modifications post-vote
* Inscription du candidat + Modification MDP première connexion

## 12/04 : Proof Of Authority ou renoncer à la décentralisation
* C'est la nature sélective des noeuds ainsi que leur nombre réduit / défini qui ne permet pas la décentralisation
* Dans le cadre de notre projet, nous avons décidé d'abandonner le développement du réseau P2P, et nous avons choisi de mettre à disposition notre application sur une machine virtuelle en ligne

## 19/04 : Déploiement automatisé via Terraform 
* Nous avons choisi Terraform pour déployer notre infrastructure
* L'idée est de centraliser sur une machine virtuelle le script, et que chaque participant puisse s'y connecter et voter 
* Terraform permet d'avoir une souplesse pour notre configuration, et nous permet à tout moment de pouvoir détruire la machine virtuelle créée


# Démonstration :

Après avoir téléchargé le dépôt, il faut initialiser Terraform avec la commande :  
```$ terraform init```

Une fois initialisé, nous pouvons valider la configuration et la syntaxe du code avec :   
```$ terraform plan```

Si aucune erreur n'est retournée, nous pouvons déployer notre machine virtuelle avec la commande :   
```$ terraform apply```

Une fois déployée, c'est cette machine virtuelle qui jouera le rôle "d'entitée de confiance"

L'ensemble des avancées / problématiques du projet sont disponibles (en lecture seule) sur le Notion suivant : https://www.notion.so/Fil-Rouge-Blockchain-f5c6b70ee86940dd846711a1a397edcb
