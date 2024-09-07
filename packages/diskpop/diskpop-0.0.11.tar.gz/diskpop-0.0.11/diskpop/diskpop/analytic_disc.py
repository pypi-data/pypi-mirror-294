import numpy as np
from scipy.special import gamma


from .DiscEvolution.src.ViscousEvolution import LBP_Solution

class LBP_Solution_Mdot(LBP_Solution):
    """
    This class handles the Lynden-Bell&Pringle (1974) solution.
    """
    def __init__(self, M, rc, nuc, gamma=1):
        LBP_Solution.__init__(self, M, rc, nuc, gamma=1)
        self.C = self._Sigma0*3*np.pi*self._nuc
    
    
    def mdot(self, t):
        tt = t / self._tc + 1
        return self.C*tt**((-2.5 + self._gamma)/(2-self._gamma))
        
        
class MHD_Solution:
    """
    This class handles the Tabone et al. (2021) MHD disc wind solution, in the case where omega = 0.
    """

    def __init__(self, M0, rc0, rin, tacc0, psi, xi):
        self._M0 = M0
        self._rc0 = rc0
        self._rin = rin
        self._tacc0 = tacc0
        self._psi = psi
        self._xi = xi

        self._flag_dispersion = False
        
        self._Sigma0 = M0 / (2 * np.pi * rc0**2 * gamma(xi + 1)) 
    
    def __call__(self, R, t):
        tt = 1 + t/((1 + self._psi) * self._tacc0)
        rc_t = self._rc0 * tt
        X = R/rc_t
        exponent = 5/2 + self._xi + self._psi/2
        Sigma_c = self._Sigma0 * tt**(- exponent)
        
        return Sigma_c * X**(self._xi - 1) * np.exp(- X)
        
        
    def mdot(self, t):
        tt = 1 + t/((1 + self._psi) * self._tacc0)
        K = (self._psi + 1 + 2*self._xi)/(self._psi + 1)
        X1 = self._rc0/self._rin
        fM0 = X1**(self._xi) - 1
        mdot0 = K * self._M0 / (2 * self._tacc0 *(1 + fM0))
        exponent = - (self._psi + 4.*self._xi + 3)/2.
        
        return mdot0 * tt**exponent

    def return_flag_dispersion(self):
        return self._flag_dispersion

class MHD_Solution_fiducial:
    """
    This class handles the Tabone et al. (2021) MHD disc wind solution, in the case where omega = 0 AND alpha_SS = 0 (equivalent to psi = +\infty).
    """

    def __init__(self, M0, rc0, rin, tacc0, leverarm):
        self._M0 = M0
        self._rc0 = rc0
        self._rin = rin
        self._tacc0 = tacc0
        self._leverarm = leverarm
        self._xi = 1/(2*(leverarm-1))   # Limit of csi where psi -> + \infty

        self._flag_dispersion = False
        
        self._Sigma0 = M0 / (2 * np.pi * rc0**2 * gamma(self._xi + 1))
        
    def __call__(self, R, t):
        tt = - t/(2*self._tacc0)
        self.X = R/self._rc0
        Sigma_c = self._Sigma0 * np.exp(tt)

        return Sigma_c * self.X**(self._xi - 1) * np.exp(-self.X)
    
    def mdot(self, t):
        tt = - t/(2*self._tacc0)
        X1 = self._rc0/self._rin
        fM0 = X1**(self._xi) - 1
        K = 2*self._tacc0*(1+fM0)
        mdot0 = self._M0/K
        
        return mdot0 * np.exp(tt)
    
    def return_flag_dispersion(self):
        return self._flag_dispersion


class MHD_Solution_omega:
    """
    This class handles the Tabone et al. (2021) MHD disc winds solution in the case where omega is not zero.
    """

    def __init__(self, M0, rc0, rin, tacc0, omega, xi = False, leverarm = False, flag_dispersion = False):

        self._M0 = M0
        self._rc0 = rc0
        self._rin = rin
        self._tacc0 = tacc0
        if xi:
            self._xi = xi
        elif leverarm:
            self._xi = 1/(2*(leverarm - 1))
        else:
            raise ValueError("I need one between xi and leverarm")
        self._omega = omega
        self._flag_dispersion = flag_dispersion

        self._Sigma0 = M0 / (2 * np.pi * rc0**2 * gamma(xi + 1)) 

    
    def __call__(self, R, t):

        X = R/self._rc0
        t_omega, self._flag_dispersion = self.t_omega(t)
        exponent = 1/self._omega
        if self._flag_dispersion == True:
           Sigma_c = 0
        else:
            Sigma_c = self._Sigma0 * t_omega**exponent
        
        return Sigma_c * X**(self._xi - 1) * np.exp(- X)
        
        
    def mdot(self, t):
        t_omega, self._flag_dispersion = self.t_omega(t)
        if self._flag_dispersion == True:
            t_omega = 0
        X1 = self._rc0/self._rin
        fM0 = X1**(self._xi) - 1
        mdot0 = self._M0 / (2 * self._tacc0 *(1 + fM0))
        exponent = - 1 + 1/self._omega
        
        return mdot0 * t_omega**exponent

    def t_omega(self, t):
        t_omega = 1 - (self._omega*t)/(2 * self._tacc0)
        if t_omega < 0:
            self._flag_dispersion = True
        return t_omega, self._flag_dispersion


    def return_flag_dispersion(self):
        return self._flag_dispersion



class MockAnalyticDynamicsModel(object):
    
    def __init__(self, disc, disc_parameters, yso_type):
        self._disc = disc
        self._disc_parameters = disc_parameters
        eos = self._disc._eos
        grid = self._disc._grid
        self._Rc = self._disc_parameters['Rd']
        self._yso_type = yso_type

        self._flag_dispersion = False


        if disc_parameters['alpha_DW'] == 0:
            self._nuc = np.interp(self._Rc, grid.Rc, eos.nu)

        else:
            self._Hrc = eos._f_H(self._Rc)/self._Rc
            self._Csc = eos._f_cs(self._Rc)
            alphatilde = disc_parameters['alpha'] + disc_parameters['alpha_DW']
            leverarm = disc_parameters['leverarm']
            self._omega = disc_parameters['omega']
            self._tacc0 = self._Rc/(3*self._Hrc*self._Csc*alphatilde)
            self._xi = 1/(2*(leverarm - 1))

            self._fM0 = (self._Rc/self._disc_parameters['rin'])**(self._xi)


            if self._omega == 0 and disc_parameters['alpha'] != 0:
                self._psi = disc_parameters['alpha_DW']/disc_parameters['alpha']
                K1 = 4*self._psi/((leverarm-1)*(self._psi+1)**2)
                self._xi = (self._psi+1)/4 * (np.sqrt(1+K1)-1)
    

        self._def_evolution_method()
        self._t = 0



    def max_timestep(self):
        return np.Inf
        
    
    def __call__(self, dt):

        self._t += dt

        self._disc.Sigma[:] = self._solver(self._disc._grid.Rc, self._t)

        flag_dispersion = self._solver.return_flag_dispersion()

        return self._solver.mdot(self._t), 0, flag_dispersion
    

    def _def_evolution_method(self):
        """
        Define the analytical solution to use, based on the value of alpha disc wind and omega. 
        """
        if self._disc_parameters['alpha_DW'] == 0:
            self._solver = LBP_Solution_Mdot(self._disc_parameters['Md'], self._Rc, self._nuc, 1)
        else:
            if self._omega == 0 and self._disc_parameters['alpha'] != 0:
                self._solver = MHD_Solution(self._disc_parameters['Md'], self._Rc, self._disc_parameters['rin'], self._tacc0, self._psi, self._xi)
            elif self._omega == 0 and self._disc_parameters['alpha'] == 0:
                self._solver = MHD_Solution_fiducial(self._disc_parameters['Md'], self._Rc, self._disc_parameters['rin'], self._tacc0, self._disc_parameters['leverarm'])
            else:
                self._solver = MHD_Solution_omega(self._disc_parameters['Md'], self._Rc, self._disc_parameters['rin'], self._tacc0, self._omega, xi = self._xi, leverarm = self._disc_parameters['leverarm'], flag_dispersion = self._flag_dispersion)