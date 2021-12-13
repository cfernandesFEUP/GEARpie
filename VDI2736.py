class THERMAL:
    def __init__(self,xx,AB,AC,AD,AE,T1A,T2A,LS,fbn,fnx,E,v,al,x,m,z,alpha,alpha_tw,\
                 r,rl,ra,rb,rf,b,k,rho,cp,vr,Pin,COF,n,Tamb,HVL,HV,PAIR,GB,cofT):

        # IN VDI 2736 is RLG = 1/k3 on page 11, Part 2
        # open gearbox free entry of air:   RLG = 0
        # partially open housing:           RLG = 0.015 to 0.045
        # closed housing:                   RLG 0.06
        if self.GB=='O':
            self.RLG = 0.0
        elif self.GB=='C':
            self.RLG = 0.06   
        else:
            self.RLG = (0.015+0.045)/2  
        self.A2V = 0.03
        
        if self.PAIR=='PS':
            # PLASTIC/STEEL
            self.kF = 6300 
            self.kR = 895
        else:
            #PLASTIC/PLASTIC
            self.kF = 9000
            self.kR = 2148
           
        # MESHING POWER LOSS
        self.QFV = self.POWER*self.cof*self.HV

        # GEAR TOOTH TEMPERATURE (FLANK)
        self.TV_F = self.TO + self.QFV*(self.kF/(1000*self.b*self.z1*(self.vt*1000*self.m)**0.75) + self.RLG/self.A2V)
        
        # GEAR TOOTH TEMPERATURE (ROOT)
        self.TV_R = self.TO + self.QFV*(self.kR/(1000*self.b*self.z1*(self.vt*1000*self.m)**0.75) + self.RLG/self.A2V)

        self.FV1 = self.kR/(1000*self.b*self.z1*(self.vt*1000*self.m)**0.75)
        
        self.FV2 = self.RLG/self.A2V
        
        self.k1 = 10.159
        
        self.AV = self.k1*self.m*self.z1*self.b
        
        self.hcV = (1/20)*(self.lambda_air/self.m)*(self.vt*self.m/self.dif_air)**0.75
        
        self.QCV = (self.TV_R-self.TO)*(self.hcV*self.AV)
        
        self.ECV = self.QCV*self.t1
        
        self.QTV = self.QCV/(self.TV_R-self.TO)
        
