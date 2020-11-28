
**Qu'est-ce qu'un projet LABTEC**

Notre contribution consiste à développer un laboratoire distant par nos propre moyens
disponibles dans nos laboratoiresdu centre universitaire, permettant de commander des
instruments de mesure et de contrôler les circuits électriques à partir d’un navigateur
Internet, dans l’enceinte du campus et à distance. Grâce à ce système, les étudiants auront
la capacité de concevoir et de réaliser des expériences sans devoir être présents
physiquement dans le laboratoire réel. Ainsi qu'un système complet qui permet aux
enseignants et aux étudiantsde réaliser de nombreuses tâches. L'enseignant peut ajouter un
nouveau travail pratique et toutes les informations dont l'étudiant a besoin pour réaliser le
travail pratique.
Une fois que l'étudiant a terminé son travail, l'enseignant peut évaluer son travail à
travers le compte-rendu remis
Les étudiants peuvent interagir avec le circuit et des instruments de mesure via un
navigateur Web.
Presque tous les laboratoires distants actuels utilisent un logiciel propriétaire (un logiciel
semblable à Labview) et un matériel coûteux (un serveur) pour les mettre en œuvre.
Dans notre projet, nous avons développé une solution en utilisant les moyens les plus
simples possibles. Tels que Raspberry-Pi et les instruments de mesure universitaires. Le
circuit utilisé dans notre exemple a été conçu pour redressement et filtrage monophasé
avec un transformateur point milieu.
Une interface web est développée pour permettre à l'étudiant de configurer la partie
matérielle des travaux pratiques en changent par exemple de composants ou en
positionnant le point de mesure en différents endroits du circuit étudié. Les circuits
électriques sont dessinés à l'aide de l’outil SVG. l’ouverture et la fermeture des switch
s’effectue en implémentant du javascripttandisque du côté serveur web nous utilisons
l’'environnement Django.
**Architecture cible de projet LABTEC**
![Nouveau Apresentação do 11Microsoft PowerPoint](https://user-images.githubusercontent.com/39880129/100521084-c2a4ad80-31a1-11eb-8f35-db685817729e.jpg)

**_Serveur principal_** : Le serveur principal du laboratoire. Il contient la base de données et toutes les opérations nécessaires pour gérer le système
_**Serveur des instruments mesures**_ : Ce serveur partage l'image d'écran des instruments de mesure (pour notre système **)
 _**Instrument de mesure**_ :: Appareils de mesure avec ou sans serveur web intégré
_**Carte TP**_ :  Constitué une circuit électronique et la matrice de commutation et commander via le serveur principal

_****_Flux de données du système  (serveur principal)_****_
![Nouveau Apresentação do Microsoft PowerPoint](https://user-images.githubusercontent.com/39880129/100521215-802fa080-31a2-11eb-9d7b-1ace0ed3f44d.jpg)

**Méthodologie de  création les utilisateurs**

![Nouveau Apresentação do Microsoft PowerP1oint](https://user-images.githubusercontent.com/39880129/100521276-cedd3a80-31a2-11eb-858a-f6b7f803bc37.jpg)

**Autorisations par utilisateur**
![Nouveau Apresentaçã1o do Microsoft PowerPoint](https://user-images.githubusercontent.com/39880129/100521294-051aba00-31a3-11eb-8958-052f640f3aab.jpg)

**Développement de Serveur des instruments mesures**
on a  développé ce serveur avec  l'utilisation de framework  Flask 
[code ici 
](https://github.com/hemid32/flask_labo)
![Nouveau Apresentação do Micr12osoft PowerPoint](https://user-images.githubusercontent.com/39880129/100521404-be798f80-31a3-11eb-871f-22e567217c09.jpg)

**Caractéristiques du laboratoire LABTEC**

- [ ]  Multi-utilisateur

- [ ] plateforme facile  à manipuler par les utilisateurs

- [ ] Économique. Il n'a pas besoin d'appareils coûteux

- [ ] Open source. Et c'est évolutif

- [ ] permettre de développer et de réaliser des expériences sur des plate-forme et systèmes d'exploitation différents

- [ ]  Utiliser un seule langage de programmation pour gérer le serveur et contrôler le GPIO  (python) qui rend le système homogène et facile à maintenir

- [ ] L'utilisation des technologies web modernes (Ajax, Django, Flask ,  Bootstrap ... etc). Facile et gratuit

- [ ] Permettre d’utiliser un oscilloscope disponible (avec ou sans serveur web intégré)



**Quelques photos de l'application**
![9](https://user-images.githubusercontent.com/39880129/95535655-e426bb80-09e0-11eb-9783-c4489680e0f2.png)
![1](https://user-images.githubusercontent.com/39880129/95535668-edb02380-09e0-11eb-81d8-0d1709ae9d5b.png)
![2](https://user-images.githubusercontent.com/39880129/95535677-f143aa80-09e0-11eb-8979-c6a0be37e680.jpg)
![3](https://user-images.githubusercontent.com/39880129/95535684-f4d73180-09e0-11eb-88be-9cab5c361255.jpg)
![4](https://user-images.githubusercontent.com/39880129/95535692-f86ab880-09e0-11eb-9e26-4450928de2e8.jpg)
![5](https://user-images.githubusercontent.com/39880129/95535710-04ef1100-09e1-11eb-8a65-13700db472d0.png)
![6](https://user-images.githubusercontent.com/39880129/95535712-07516b00-09e1-11eb-8b9e-e3c1510a02ce.jpg)
![7](https://user-images.githubusercontent.com/39880129/95535722-0e787900-09e1-11eb-9652-7f988a5735ae.png)
![8](https://user-images.githubusercontent.com/39880129/95535725-120c0000-09e1-11eb-9e35-dfe0e70f9d21.png)


**Pour plus d'informations, téléchargez le document suivant**
[PFC.pdf](https://github.com/hemid32/django_labo/files/5352182/PFC.pdf)

