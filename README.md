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
