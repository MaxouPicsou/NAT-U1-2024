# Network Activity Traces 2024

Ce répertoire détail la méthode utilisée pour l'enregistrement et l'étiquetage des jeux de données. Il comporte l'ensemble des scripts qui ont servi à leur création.

## Architecture

L'architecture choisie est plutôt simple. Il s'agit du réseau d'une entreprise divisé en 3 sous-réseaux pour chacune des équipes:

| Network        | Address     | masq          |
|----------------|-------------|---------------|
| Management     | 192.168.1.0 | 255.255.255.0 |
| Administrative | 192.168.2.0 | 255.255.255.0 |
| Developer      | 192.168.3.0 | 255.255.255.0 |

![Architecture](images/architecture_company.png "Architecture")

On s'intéresse aux activités d'un des développeurs de la compagnie. Pour simuler celà, on virtualise une partie du réseau à l'aide de VMware. L'enregistrement des données réseau se fait au niveau du routeur de bordure. La machine physique, elle, se comporte comme le couplage du routeur de sortie et le firewall.  

![Architecture_Locale](images/architecture_local.png "Architecture Locale")

## Enregistrement

La phase d'enregistrement des données est composée de plusieurs parties:
- Enregistrement vidéo
- Récupération des entrées (souris et clavier)
- Capture réseau

Les deux premiers enregistrements permettent de plus facilement labeliser le jeu de données.

### Enregistrement vidéo
L'enregistrement vidéo est fait à l'aide de l'outils par défaut sous ubuntu 22.04. On tâche de bien faire apparaître le pointeur lors de la capture pour faciliter le suivi des différentes actions.

![Video Record](images/img.png "Video record")

Le format de sortie par défaut est le *.webm* qui est très lourd. Pour faciliter le traitement, la vidéo a été convertie en *.mp4*.
### Récupération des entrées (souris et clavier)
Pour récupérer les entrées on utilise la bibliothèque python [python-evdev](https://python-evdev.readthedocs.io/en/latest/). Elle permet de gérer les periphériques d'entrées en lecture et écriture sous Linux. Dans un premier temps, il est nécessaire de repérer sur quelles entrées se trouve nos périphériques. La commande suivante permet de les lister:

```bash
$ ls -l /dev/input/by-id/*

lrwxrwxrwx 1 root root  9 avril  9 08:11 /dev/input/by-id/usb-4e53_USB_OPTICAL_MOUSE-event-mouse -> ../event9
lrwxrwxrwx 1 root root 10 avril  9 08:11 /dev/input/by-id/usb-4e53_USB_OPTICAL_MOUSE-if01-event-kbd -> ../event14
lrwxrwxrwx 1 root root  9 avril  9 08:11 /dev/input/by-id/usb-4e53_USB_OPTICAL_MOUSE-mouse -> ../mouse3
lrwxrwxrwx 1 root root  9 avril  9 08:10 /dev/input/by-id/usb-NOVATEK_USB_Keyboard-event-if01 -> ../event8
lrwxrwxrwx 1 root root  9 avril  9 08:10 /dev/input/by-id/usb-NOVATEK_USB_Keyboard-event-kbd -> ../event5
```

Dans notre cas, nous avons les entrées suivantes:

| Device   | File              | 
|----------|-------------------|
| Keyboard | /dev/input/event5 | 
| Mouse    | /dev/input/event9 | 

Il est important d'adapter les paramètres du script **Recorder.py** en fonction.

### Capture réseau
La capture réseau est effectuée au niveau du routeur de bordure à l'aide d'une simple ligne de commande utilisant tshark:

```bash
$ tshark -i <interface> -w <nom_du_fichier>
```

Pour obtenir les flows, on peut utiliser le script **Converter.py** qui utilise la bibliothèque python [NFStream](https://www.nfstream.org/) à l'aide de la commande suivante:
```bash
$ python3 Converter.py <PCAP filename>
```
Vous obtiendrez le fichier du même nom au format *.csv*.
## Labelisation des données
La labelisation des données se fait en partie automatiquement à l'aide du script  **Processing.py**.
```bash
$ python3 Processing.py
```
Il va lire les données du fichier *event_file.txt* qui contient les données des entrées (clavier + souris) enregistrées précédemment. Le format des données est le suivant:

```
event at 1712649868.332587, code 272, type 01, val 01
```

Chaque ligne se forme du timestamp de l'évènement, suivi du code correspondant à l'entrée, son type et enfin sa valeur. Les codes et types, bien que souvent similaires, sont propre au périphérique. On peut les trouver à l'aide de la commande suivante:

```bash
$ sudo evemu-describe
```
Dans notre cas, nous avons décidés de ne prendre en compte qu'uniquement les codes ci-dessous, estimant que ce sont les actions les plus couramment utilisées et générant le plus d'opérations.

| Code | Device   | Event                                 | 
|------|----------|---------------------------------------|
| 272  | Mouse    | BTN_LEFT                              | 
| 273  | Mouse    | BTN_RIGHT                             | 
| 274  | Mouse    | BTN_MIDDLE *(wheel click)*           | 
| 28   | Keyboard | KEY_ENTER                             | 
| 96   | Keyboard | KEY_KPENTER *(numeric keypad enter key)* | 

Ces évènements peuvent prendre 2 valeurs, **01** lorsque la touche/click est enfoncé et **00** lorsqu'il est relaché.
Nous cherchons donc l'ensemble des timestamps où s'est produit un des évènements correspondant à l'une de ces actions au moment ou la touche/click est relaché. 
Ensuite, manuellement, nous étiquetons colonnes les Actions, Activités et Applications.