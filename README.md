# MorpheesPlug

MorpheesPlug is a toolkit to prototype shape-changing interfaces, which are physical interfaces they can change their shapes and/or accept deformation as an input as an interaction method with users [1,2,3]. MorpheesPlug is built based on shape-changing interface taxonomies [4,5]. The design process and example applications of MorpheesPlug can be found in our publication at ACM [6].

[1] Marcelo Coelho and Jamie Zigelbaum. 2011. Shape-changing interfaces. Personal Ubiquitous Comput. 15, 2 (February 2011), 161–173. DOI:https://doi.org/10.1007/s00779-010-0311-y

[2] Majken K. Rasmussen, Esben W. Pedersen, Marianne G. Petersen, and Kasper Hornbæk. 2012. Shape-changing interfaces: a review of the design space and open research questions. In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (CHI '12). Association for Computing Machinery, New York, NY, USA, 735–744. DOI:https://doi.org/10.1145/2207676.2207781

[3] Jason Alexander, Anne Roudaut, Jürgen Steimle, Kasper Hornbæk, Miguel Bruns Alonso, Sean Follmer, and Timothy Merritt. 2018. Grand Challenges in Shape-Changing Interface Research. In Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems (CHI '18). Association for Computing Machinery, New York, NY, USA, Paper 299, 1–14. DOI:https://doi.org/10.1145/3173574.3173873

[4] Anne Roudaut, Abhijit Karnik, Markus Löchtefeld, and Sriram Subramanian. 2013. Morphees: toward high "shape resolution" in self-actuated flexible mobile devices. In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (CHI '13). Association for Computing Machinery, New York, NY, USA, 593–602. DOI:https://doi.org/10.1145/2470654.2470738

[5] Hyunyoung Kim, Celine Coutrix, and Anne Roudaut. 2018. Morphees+: Studying Everyday Reconfigurable Objects for the Design and Taxonomy of Reconfigurable UIs. In Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems (CHI '18). Association for Computing Machinery, New York, NY, USA, Paper 619, 1–14. DOI:https://doi.org/10.1145/3173574.3174193

[6] Hyunyoung Kim, Aluna Everitt, Carlos Tejada, Mengyu Zhong, and Daniel Ashbrook. 2021. MorpheesPlug: A Toolkit for Prototyping Shape-Changing Interfaces. In Proceedings of the 2021 CHI Conference on Human Factors in Computing Systems (CHI '21). Association for Computing Machinery, New York, NY, USA, Article 101, 1–13. https://doi.org/10.1145/3411764.3445786


## Authors
<ul>
<li>Hyunyoung Kim</li>
<li>Aluna Everitt</li>
<li>Carlos E. Tejada</li>
<li>Mengyu Zhong</li>
<li>Daniel Ashbrook</li>
</ul>

## Folders
<ul>
  <li>Module_Eagle: control module board Eagle files.</li>
  <li>Module_Enclosure: Enclosure stl files for control module.</li>
  <li>MorpheesPlug: Autodesk Fusion 360 add-in to design widgets.</li>
</ul>

## How to install the MorpheesPlug add-in on Autodesk Fusion 360
1. Download and place the [MorpheesPlug subfolder](./MorpheesPlug) under ~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/ (Mac).
2. Launch Fusion 360.
3. Go to Tools panel then click ADD-INS icon.
4. Click MorpheesPlug Script under My Scripts.
5. Click Run.
6. Choose a widget and change the parameters as needed.
Note: If you want to show the script icon on your Fusion 360, put the folder under ~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/ (Mac). The icon will show up under Tools/Add-ins arrow. You can click the icon to launch the script.

## License
[MIT](https://choosealicense.com/licenses/mit/)
