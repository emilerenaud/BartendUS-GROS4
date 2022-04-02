# BartendUS 
## GRO-S4H2022 - Université de Sherbrooke

BartendUS est un projet académique de 4e session du programme de génie robotique de l'Université de Sherbrooke. C'est un projet réalisé dans le cadre du cours _GRO400:_ _Conception agile et ouverte en robotique_.

BartendUS est une plateforme surmontée d'un bras robotisé de type SCARA qui permet de créer des breuvages alcoolisés sur mesure. Le robot est assisté par un algorithme de vision ainsi qu'une interface utilisateur graphique. Également, des supports conçus sur mesure permettent le maintien des bouteilles en place tout en facilitant la distribution des liquides.

## Table des matières
* Présentation de l'équipe
* Requis matériel
* Installation
* Guide d'utilisation
* Licence

## Présentation de l'équipe
- (Photo d'équipe à la fin de la session avec le robot et noms des membres originaux)

## Requis matériel
- Un bras robotisé SCARA et sa plateforme. Les instructions d'assemblage sont disponibles dans [le répertoire « Mécanique »](https://github.com/mimil2014/BartendUS-GROS4/tree/main/M%C3%A9canique).
- Raspberry PI 4 et une écran tactile. Les liens d'achats sont disponibles dans la liste de matériel [BOM](www.google.com).
- Distributeur d'alcool et le support sur mesure. Les plans sont disponibles dans [le répertoire « Mécanique »](https://github.com/mimil2014/BartendUS-GROS4/tree/main/M%C3%A9canique).
- Une caméra compatible avec un Raspberry Pi

## Installation 
### Installation du setup environ, avec le bras sur la base.

### Procédure pour flasher l'Arduino

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

### Ouvrir le software avec script sur un ordi ou le Pi.

## Guide d'utilisation
- (Guide de comment utiliser notre robot)

## Licence
BSD License

Voir [LICENSE](LICENSE)
