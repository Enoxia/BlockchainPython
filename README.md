# Projet Blockchain

Ce projet à pour but de simuler un système de vote (élection) en utilisant la technologie blockchain.


# Explication du sujet

L'idée était de mettre en place une élection "présidentielle" fictive avec un système de vote reposant sur une blockchain. Il nous fallait d'abord choisir un consensus, nous avons choisi le [Proof Of Authority](https://en.wikipedia.org/wiki/Proof_of_authority)


# Proof Of Authority

Le Proof-Of-Authority (PoA) est une méthode de consensus basé sur la réputation des noeuds, qui donne à un nombre restreint et définit d’acteurs d’une blockchain le pouvoir de valider des transactions ou interactions avec le réseau et de mettre à jour son registre plus ou moins distribué.

Ce consensus apporte des avantages pour notre projet que les autres consensus n'ont pas ; 

- Aucune haute performance hardware n'est requise pour compléter les blocs
- Un groupe de machines dites "validatrices" ou "légitimes" doivent valider chaque nouveau bloc de transactions (algorithme basé sur la confiance). Dans notre cas, le(s) groupe(s) de machines validatrices seraient les bureaux de votes
- Le consensus nécessite un nombre définit de noeuds, dans notre exemple


# Description du projet : 

Pour cela, il nous a fallu : 

- Une base de données contenant la liste des électeurs et des candidats
- Simuler 1 wallet / personne (nominatif)
- Simuler 1 token par votant / électeur
- Avoir une interface utilisateur le plus "User Friendly" possible
- Pouvoir avoir un accès à la blockchain et à ses blocs
- Vérifier l'anonymat de chaque bloc ; on ne doit pas savoir qui a voté pour qui
- Eventuellement faire tourner notre application dans un réseau décentralisé (P2P)

L'ensemble des avancées / problématiques du projet sont disponibles sur le Notion suivant : https://www.notion.so/Fil-Rouge-Blockchain-f5c6b70ee86940dd846711a1a397edcb






