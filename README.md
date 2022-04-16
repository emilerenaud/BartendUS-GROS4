# BartendUS 
## GRO-S4H2022 - Université de Sherbrooke

BartendUS est un projet académique de 4e session du programme de génie robotique de l'Université de Sherbrooke réalisé par 6 étudiants. C'est un projet réalisé dans le cadre du cours _GRO400:_ _Conception agile et ouverte en robotique_.

BartendUS est une plateforme surmontée d'un bras robotisé de type SCARA qui permet de créer des breuvages alcoolisés sur mesure. Le robot est assisté par un algorithme de vision ainsi qu'une interface utilisateur graphique. Également, des supports conçus sur mesure permettent le maintien des bouteilles en place tout en facilitant la distribution des liquides.

<img src="https://user-images.githubusercontent.com/73348957/163657518-e04d23d6-ec03-403d-bd4a-50c1b9cfee96.png" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png">


## Table des matières
* Présentation de l'équipe
* Vidéo promotionnelle du projet
* Requis matériel
* Installation
* Licence

## Présentation de l'équipe


*De gauche à droite: Simon Chayer, Émile Renaud, Antoine Landry, Hugues Dupuis et Thomas Landry*

IMPORTANT : Sur cette photo, il manque un membre de l'équipe : Frédéric Forest, qui ne pouvait pas être présent lors de la présentation.

## Vidéo promotionnelle du projet
Voici une vidéo réalisée par Antoine Landry mettant en vedette la solution développée tout au long de la session:
https://www.youtube.com/watch?v=95p3Jdjmmvk

## Requis matériel
- Un bras robotisé SCARA et sa plateforme. Les instructions d'assemblage sont disponibles dans [le répertoire « Mécanique »](https://github.com/mimil2014/BartendUS-GROS4/tree/main/M%C3%A9canique).
- Distributeur d'alcool et le support sur mesure. Les plans sont disponibles dans [le répertoire « Mécanique »](https://github.com/mimil2014/BartendUS-GROS4/tree/main/M%C3%A9canique).
- Éléments présentés dans le [BOM](https://github.com/mimil2014/BartendUS-GROS4/blob/main/BOM/liste_pieces.pdf).

## Installation 
### Installation des librairies sur le RaspberryPi:
Assurez-vous que votre Pi est à jour avec les commandes suivantes: 
```
sudo apt update  
sudo apt upgrade  
```
Installer le terminal Terminator (si vous désirez):   
```
sudo apt-get install terminator   
```
Installer Python sur le Pi:   
```
sudo apt install python3-dev   
sudo apt-get install python3-pip 
```
À partir du fichier requirements.txt, installer les librairies avec la commande: 
```
pip3 install -r requirements.txt  
```
Cette commande installera toutes les librairies nécessaires au projet sur votre Pi. Si vous avez de la difficulté à installer OpenCV, vous pouvez suivre les étapes du site suivant:   https://singleboardbytes.com/647/install-opencv-raspberry-pi-4.htm

*Prendre note que la version installée pour ce projet est la version courte détaillée sur le site.

De la façon suggérée sur ce site, les librairies sont installées dans un environnement virtuel. Il faut seulement s'assurer que les autres librairies utilisées     dans le projet sont également dans cet environnement virtuel. 

## Licence
BSD License

Voir [LICENSE](LICENSE)
