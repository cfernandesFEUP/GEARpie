# GEARpie

## Requirements

GEARpie requires Python 3 with the following libraries:

- scipy, numpy and matplotlib -- install with "pip install scipy", "pip install numpy" and "pip install matplotlib"
- gmsh API -- install with "pip install gmsh"

## How to use

Run 'GEARpie.py' and complete the following prompt window:

<p align="center">
    <img src="SCREENSHOTS/INPUT.png"height="800"/>
</p>

## Capabilities

GEARpie is useful to calculate cylindrical gears:

- geometry according to MAAG book (imposing axis distance plus one profile shift or providing profile shifts x1 and x2)
- contact pressure and stress fields considering friction (select the position along the path of contact: A, B, C, D, E or any other)
- film thickness along the path of contact
- gear power losses (local and average)
- instantaneous and average heat generation according to [8]
- structured FEM mesh (1st or 2nd order elements)
- load carrying capacity according to DIN 3990 method B (steel gears)
- load carrying capacity and bulk temperature according to VDI 2736 Part 2 (plastic gears) [10]
- VDI 2736 tooth root stress is calculated according to method C as suggested in the standard (method B is possible)
- VDI 2736 local wear, deformation and peak loads verification. 

The rigid load sharing model implemented on the software is descibed in [1]. If a load sharing result is provided (for example a FEM result in a text file, k=f(meshing position)) the stiffness is considered for all the calculations.

The power loss models are described in [2-5,7]. The Ohlendorf (analytic) and Wimmer (numerical) gear loss factors are implemented.

The VDI 2736 temperature calculation uses Wimmer gear loss factor instead of Ohlendorf (to have more accuracy). The calculation according to VDI 2736 is done by default for open gearboxes (gearbox surface area is not needed). If the user needs the calculation for closed or semi-open gearboxes, just change the default value inside VDI 2736 class.

The implementation of VDI 2736 standard makes the verification both for tooth root stress and tooth flank stress. However, the tooth flank is tipically performed only for lubricated PA66 gears (so only for those cases is accurate and according to the standard). The material properties are available only for an operating temperature lower than 120 °C. Every safety factor (SF or SH) calculated above 120 °C is incorrect due to lack of material data - the material properties have the values calaculated for 120 °C. If the user has accurate material data, should include it on MATERIAL_LIBRARY class.

The mesh generation is useful to create, for example, the FEM thermal model described in [8-9]. The mesh is useful for any Finite Element Analysis (tested in Abaqus and CalculiX).

## Graphical Output Example
<p align="center">
    <img src="SCREENSHOTS/logo1.png"height="400"/>
    <img src="SCREENSHOTS/logo2.png"height="400" />
</p>

The 3D output is not implemented by default, but is possible adding 3D entries to PLOTTING class. Every quantity calculated in CONTACT class is discretized along path of contact and facewidth, so it is adequate to 3D output. Example: central film thickness with inlet shear heating correction for an helical gear:
<p align="center">
    <img src="SCREENSHOTS/logo3.png"height="400"/>
</p>

## Report Output Example

The report is automatically saved to "REPORT" folder in txt format.

<p align="center"> 
    <img src="SCREENSHOTS/OUT0.png"width="600"/>
    <img src="SCREENSHOTS/OUT1.png"width="600"/>
    <img src="SCREENSHOTS/OUT2.png"width="600"/>
    <img src="SCREENSHOTS/OUT3.png"width="600"/>
</p>

 ## References
 
 [1] Fernandes, C. M. C. G., Marques, P. M. T., Martins, R. C., & Seabra, J. H. O. (2015). 
 Influence of gear loss factor on the power loss prediction. Mechanical Sciences, 6(2), 
 81–88. https://doi.org/10.5194/ms-6-81-2015
 
 [2] Fernandes, C. M. C. G., Martins, R. C., & Seabra, J. H. O. (2014). 
 Torque loss of type C40 FZG gears lubricated with wind turbine gear oils. 
 Tribology International, 70(0), 83–93. https://doi.org/10.1016/j.triboint.2013.10.003
 
 [3] Fernandes, C. M. C. G., Marques, P. M. T., Martins, R. C., & Seabra, J. H. O. (2015). 
 Gearbox power loss. Part I: Losses in rolling bearings. 
 Tribology International, 88(0), 298–308. https://doi.org/10.1016/j.triboint.2014.11.017
 
 [4] Fernandes, C. M. C. G., Marques, P. M. T. T., Martins, R. C., & Seabra, J. H. O. (2015). 
 Gearbox power loss. Part II: Friction losses in gears. 
 Tribology International, 88, 309–316. https://doi.org/10.1016/j.triboint.2014.12.004
 
 [5] Fernandes, C. M. C. G., Marques, P. M. T., Martins, R. C., & Seabra, J. H. O. (2015). 
 Gearbox power loss. Part III: Application to a parallel axis and a planetary gearbox. 
 Tribology International, 88, 317–326. https://doi.org/10.1016/j.triboint.2015.03.029
 
 [6] Fernandes, C. M. C. G., Martins, R. C., & Seabra, J. H. O. (2016). Coefficient of 
 friction equation for gears based on a modified Hersey parameter. Tribology International, 
 101, 204–217. https://doi.org/10.1016/j.triboint.2016.03.028
 
 [7] Fernandes, C. M. C. G. M., Hammami, M., Martins, R. C., & Seabra, J. H. O. H. (2016). 
 Power loss prediction: Application to a 2.5 MW wind turbine gearbox. 
 Proceedings of the Institution of Mechanical Engineers, Part J: Journal of Engineering Tribology, 
 230(8), 983–995. https://doi.org/10.1177/1350650115622362
 
 [8] Fernandes, C. M. C. G., Rocha, D. M. P., Martins, R. C., Magalhães, L., & Seabra, J. H. O. (2018). 
 Finite element method model to predict bulk and flash temperatures on polymer gears. 
 Tribology International, 120, 255–268. https://doi.org/10.1016/j.triboint.2017.12.027
 
 [9] Fernandes, C. M. C. G., Rocha, D. M. P., Martins, R. C., Magalhães, L., & Seabra, J. H. O. (2019). 
 Hybrid Polymer Gear Concepts to Improve Thermal Behavior. 
 Journal of Tribology, 141(3), 032201. https://doi.org/10.1115/1.4041461
 
 [10] V. Roda-casanova, C.M.C.G. Fernandes, A comparison of analytical methods to predict the bulk temperature in polymer spur gears, Mechanism and Machine Theory. 173 (2022) 104849. https://doi.org/10.1016/j.mechmachtheory.2022.104849.


Copyright (c) 2023 Carlos M.C.G. Fernandes
