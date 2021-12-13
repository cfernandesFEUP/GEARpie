# Gear Calculation


<p align="center"> 
<img src="https://github.com/cfernandesFEUP/Gear-Calculation/blob/master/GearC/logo.png">
</p>

The software was validated for its typical usage by the author. No warranty is given and the user should always verify the results.

The software is capable to calculate cylindrical gears geometry according to MAAG book, predict Hertz contact pressure and corresponding stress field, gear and rolling bearings power losses [1-6]. Only NJ 406 MA and QJ 308 N2MA rolling bearing equations are implemented. Additional bearing data can be easily added on the 'bearings.py' file - just follow the same format. 

The DIN3990 safety factors for contact stress and bending stress are also calculated. 

Other features not included on the repository: gear geometry and structured FEM mesh (Gmsh Python API), CalculiX themo-mechanical integration, heat transfer coefficients calculation [7,8]. Please contact me.

How to use:

- the main file is 'GearCP.py':

    'GearCP.py' where you should select:
    
        - Gear geometry (C14, C40, H501, H701, H951 [1,3]) which is stored into the file "gears.py" and additional geometries can be added - just use the same format.
        
        - Gear material:
        
            mat = [STEEL STEEL]; meaning pinion and gear material respectively;
            
        - Operating Conditions:
        
            nmotor - list of motor speeds (meaning wheel z2 speed)
            load - list of FZG load stages, available with load arm of 0.35 m and 0.5 m
            (check LoadStage.py);
            
            a required torque can also be defined.
            
        - Oil Selection:
        
           'dry' - no lubricant, a Cofficient of Friction should be given - useful for plastic gears;
           'PAOR', 'MINR', etc - "oils.py"  according to papers [1-4]. Calculates the 
           Coefficient of Friction using Schlenk equation and the corresponding lubricant parameter XL [1,3]; 
           Additional lubricants can be added - just use the same format.
                 
 References:
 
 [1] Fernandes, C. M. C. G., Martins, R. C., & Seabra, J. H. O. (2014). 
 Torque loss of type C40 FZG gears lubricated with wind turbine gear oils. 
 Tribology International, 70(0), 83–93. https://doi.org/10.1016/j.triboint.2013.10.003
 
 [2] Fernandes, C. M. C. G., Marques, P. M. T., Martins, R. C., & Seabra, J. H. O. (2015). 
 Gearbox power loss. Part I: Losses in rolling bearings. 
 Tribology International, 88(0), 298–308. https://doi.org/10.1016/j.triboint.2014.11.017
 
 [3] Fernandes, C. M. C. G., Marques, P. M. T. T., Martins, R. C., & Seabra, J. H. O. (2015). 
 Gearbox power loss. Part II: Friction losses in gears. 
 Tribology International, 88, 309–316. https://doi.org/10.1016/j.triboint.2014.12.004
 
 [4] Fernandes, C. M. C. G., Marques, P. M. T., Martins, R. C., & Seabra, J. H. O. (2015). 
 Gearbox power loss. Part III: Application to a parallel axis and a planetary gearbox. 
 Tribology International, 88, 317–326. https://doi.org/10.1016/j.triboint.2015.03.029
 
 [5] Fernandes, C., Martins, R., Seabra, J. H. O., & Blazquez, L. (2016). 
 FZG Gearboxes Lubricated with Different Formulations of Polyalphaolefin Wind Turbine Gear Oils. 
 August, 56–60.
 
 [6] Fernandes, C. M. C. G. M., Hammami, M., Martins, R. C., & Seabra, J. H. O. H. (2016). 
 Power loss prediction: Application to a 2.5 MW wind turbine gearbox. 
 Proceedings of the Institution of Mechanical Engineers, Part J: Journal of Engineering Tribology, 
 230(8), 983–995. https://doi.org/10.1177/1350650115622362
 
 Dry conditions/polymer gears:
 
 [7] Fernandes, C. M. C. G., Rocha, D. M. P., Martins, R. C., Magalhães, L., & Seabra, J. H. O. (2018). 
 Finite element method model to predict bulk and flash temperatures on polymer gears. 
 Tribology International, 120, 255–268. https://doi.org/10.1016/j.triboint.2017.12.027
 
 [8] Fernandes, C. M. C. G., Rocha, D. M. P., Martins, R. C., Magalhães, L., & Seabra, J. H. O. (2019). 
 Hybrid Polymer Gear Concepts to Improve Thermal Behavior. 
 Journal of Tribology, 141(3), 032201. https://doi.org/10.1115/1.4041461
 
 -------------------------------------------------------------------------------
MIT License

Copyright (c) 2021 Carlos M.C.G. Fernandes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "README"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
