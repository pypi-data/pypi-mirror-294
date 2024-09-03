r"""This module provides classes that emulate physical approximations of fluid dynamics
systems by exposing methods to calculate specific terms in the corresponding
mathematical equations. Users instantiate the appropriate class by providing relevant
parameters and pass the instance to other objects, such as solvers. Under the hood,
G-ADOPT queries variables and methods from the approximation.

"""

import abc
from numbers import Number
from typing import Optional

from firedrake import Function, Identity, div, grad, inner, sym, ufl

from .utility import ensure_constant, vertical_component

__all__ = [
    "BoussinesqApproximation",
    "ExtendedBoussinesqApproximation",
    "TruncatedAnelasticLiquidApproximation",
    "AnelasticLiquidApproximation"
]


class BaseApproximation(abc.ABC):
    """Base class to provide expressions for the coupled Stokes and Energy system.

    The basic assumption is that we are solving (to be extended when needed)

        div(dev_stress) + grad p + buoyancy(T, p) * khat = 0
        div(rho_continuity * u) = 0
        rhocp DT/Dt + linearized_energy_sink(u) * T
          = div(kappa * grad(Tbar + T)) + energy_source(u)

    where the following terms are provided by Approximation methods:

    - linearized_energy_sink(u) = 0 (BA), Di * rhobar * alphabar * g * w (EBA),
      or Di * rhobar * alphabar * w (TALA/ALA)
    - kappa() is diffusivity or conductivity depending on rhocp()
    - Tbar is 0 or reference temperature profile (ALA)
    - dev_stress depends on the compressible property (False or True):
        - if compressible then dev_stress = mu * [sym(grad(u) - 2/3 div(u)]
        - if not compressible then dev_stress = mu * sym(grad(u)) and
          rho_continuity is assumed to be 1

    """

    @property
    @abc.abstractmethod
    def compressible(self) -> bool:
        """Defines compressibility.

        Returns:
          A boolean signalling if the governing equations are in compressible form.

        """
        pass

    @abc.abstractmethod
    def buoyancy(self, p: Function, T: Function) -> ufl.core.expr.Expr:
        """Defines the buoyancy force.

        Returns:
          A UFL expression for the buoyancy term (momentum source in gravity direction).

        """
        pass

    @abc.abstractmethod
    def rho_continuity(self) -> ufl.core.expr.Expr:
        """Defines density.

        Returns:
          A UFL expression for density in the mass continuity equation.

        """
        pass

    @abc.abstractmethod
    def rhocp(self) -> ufl.core.expr.Expr:
        """Defines the volumetric heat capacity.

        Returns:
          A UFL expression for the volumetric heat capacity in the energy equation.

        """
        pass

    @abc.abstractmethod
    def kappa(self) -> ufl.core.expr.Expr:
        """Defines thermal diffusivity.

        Returns:
          A UFL expression for thermal diffusivity.

        """
        pass

    @property
    @abc.abstractmethod
    def Tbar(self) -> Function:
        """Defines the reference temperature profile.

        Returns:
          A Firedrake function for the reference temperature profile.

        """
        pass

    @abc.abstractmethod
    def linearized_energy_sink(self, u) -> ufl.core.expr.Expr:
        """Defines temperature-related sink terms.

        Returns:
          A UFL expression for temperature-related sink terms in the energy equation.

        """
        pass

    @abc.abstractmethod
    def energy_source(self, u) -> ufl.core.expr.Expr:
        """Defines additional terms.

        Returns:
          A UFL expression for additional independent terms in the energy equation.

        """
        pass


class BoussinesqApproximation(BaseApproximation):
    """Expressions for the Boussinesq approximation.

    Density variations are considered small and only affect the buoyancy term. Reference
    parameters are typically constant. Viscous dissipation is neglected (Di << 1).

    Arguments:
      Ra:        Rayleigh number
      rho:       reference density
      alpha:     coefficient of thermal expansion
      T0:        reference temperature
      g:         gravitational acceleration
      RaB:       compositional Rayleigh number; product of the Rayleigh and buoyancy numbers
      delta_rho: compositional density difference from the reference density
      kappa:     thermal diffusivity
      H:         internal heating rate

    Note:
      The thermal diffusivity, gravitational acceleration, reference
      density, and coefficient of thermal expansion are normally kept
      at 1 when non-dimensionalised.

    """
    compressible = False
    Tbar = 0

    def __init__(
        self,
        Ra: Function | Number,
        *,
        rho: Function | Number = 1,
        alpha: Function | Number = 1,
        T0: Function | Number = 0,
        g: Function | Number = 1,
        RaB: Function | Number = 0,
        delta_rho: Function | Number = 1,
        kappa: Function | Number = 1,
        H: Function | Number = 0,
    ):
        self.Ra = ensure_constant(Ra)
        self.rho = ensure_constant(rho)
        self.alpha = ensure_constant(alpha)
        self.T0 = T0
        self.g = ensure_constant(g)
        self.kappa_ref = ensure_constant(kappa)
        self.RaB = RaB
        self.delta_rho = ensure_constant(delta_rho)
        self.H = ensure_constant(H)

    def buoyancy(self, p, T):
        return (
            self.Ra * self.rho * self.alpha * (T - self.T0) * self.g
            - self.RaB * self.delta_rho * self.g
        )

    def rho_continuity(self):
        return 1

    def rhocp(self):
        return 1

    def kappa(self):
        return self.kappa_ref

    def linearized_energy_sink(self, u):
        return 0

    def energy_source(self, u):
        return self.rho * self.H


class ExtendedBoussinesqApproximation(BoussinesqApproximation):
    """Expressions for the extended Boussinesq approximation.

    Extends the Boussinesq approximation by including viscous dissipation and work
    against gravity (both scaled with Di).

    Arguments:
      Ra: Rayleigh number
      Di: Dissipation number
      mu: dynamic viscosity
      H:  volumetric heat production

    Other Arguments:
      rho (Number):           reference density
      alpha (Number):         coefficient of thermal expansion
      T0 (Function | Number): reference temperature
      g (Number):             gravitational acceleration
      RaB (Number):           compositional Rayleigh number; product
                              of the Rayleigh and buoyancy numbers
      delta_rho (Number):     compositional density difference from
                              the reference density
      kappa (Number):         thermal diffusivity

    Note:
      The thermal diffusivity, gravitational acceleration, reference
      density, and coefficient of thermal expansion are normally kept
      at 1 when non-dimensionalised.

    """
    compressible = False

    def __init__(self, Ra: Number, Di: Number, *, mu: Number = 1, H: Optional[Number] = None, **kwargs):
        super().__init__(Ra, **kwargs)
        self.Di = Di
        self.mu = mu
        self.H = H

    def viscous_dissipation(self, u):
        stress = 2 * self.mu * sym(grad(u))
        if self.compressible:  # (used in AnelasticLiquidApproximations below)
            stress -= 2/3 * self.mu * div(u) * Identity(u.ufl_shape[0])
        phi = inner(stress, grad(u))
        return phi * self.Di / self.Ra

    def linearized_energy_sink(self, u):
        w = vertical_component(u)
        return self.Di * self.alpha * self.rho * self.g * w

    def work_against_gravity(self, u, T):
        return self.linearized_energy_sink(u) * T

    def energy_source(self, u):
        source = self.viscous_dissipation(u)
        if self.H:
            source += self.H * self.rho
        return source


class TruncatedAnelasticLiquidApproximation(ExtendedBoussinesqApproximation):
    """Truncated Anelastic Liquid Approximation

    Compressible approximation. Excludes linear dependence of density on pressure.

    Arguments:
      Ra:     Rayleigh number
      Di:     Dissipation number
      Tbar:   reference temperature. In the diffusion term we use Tbar + T (i.e. T is the pertubartion)
      cp:     reference specific heat at constant pressure

    Other Arguments:
      rho (Number):           reference density
      alpha (Number):         reference thermal expansion coefficient
      T0 (Function | Number): reference temperature
      g (Number):             gravitational acceleration
      RaB (Number):           compositional Rayleigh number; product
                              of the Rayleigh and buoyancy numbers
      delta_rho (Number):     compositional density difference from
                              the reference density
      kappa (Number):         diffusivity
      mu (Number):            viscosity used in viscous dissipation
      H (Number):             volumetric heat production

    Note:
      Other keyword arguments may be depth-dependent, but default to 1 if not supplied.

    """
    compressible = True

    def __init__(self,
                 Ra: Number,
                 Di: Number,
                 *,
                 Tbar: Function | Number = 0,
                 cp: Function | Number = 1,
                 **kwargs):
        super().__init__(Ra, Di, **kwargs)
        self.Tbar = Tbar
        self.cp = cp

    def rho_continuity(self):
        return self.rho

    def rhocp(self):
        return self.rho * self.cp


class AnelasticLiquidApproximation(TruncatedAnelasticLiquidApproximation):
    """Anelastic Liquid Approximation

    Compressible approximation. Includes linear dependence of density on pressure.

    Arguments:
      Ra:     Rayleigh number
      Di:     Dissipation number
      chi:    reference isothermal compressibility
      gamma0: Gruneisen number (in pressure-dependent buoyancy term)
      cp0:    specific heat at constant *pressure*, reference for entire Mantle (in pressure-dependent buoyancy term)
      cv0:    specific heat at constant *volume*, reference for entire Mantle (in pressure-dependent buoyancy term)

    Other Arguments:
      rho (Number):           reference density
      alpha (Number):         reference thermal expansion coefficient
      T0 (Function | Number): reference temperature
      g (Number):             gravitational acceleration
      RaB (Number):           compositional Rayleigh number; product
                              of the Rayleigh and buoyancy numbers
      delta_rho (Number):     compositional density difference from
                              the reference density
      kappa (Number):         diffusivity
      mu (Number):            viscosity used in viscous dissipation
      H (Number):             volumetric heat production
      Tbar (Number):          reference temperature. In the diffusion
                              term we use Tbar + T (i.e. T is the pertubartion)
      cp (Number):            reference specific heat at constant pressure

    """

    def __init__(self,
                 Ra: Number,
                 Di: Number,
                 *,
                 chi: Function | Number = 1,
                 gamma0: Function | Number = 1,
                 cp0: Function | Number = 1,
                 cv0: Function | Number = 1,
                 **kwargs):
        super().__init__(Ra, Di, **kwargs)
        # Dynamic pressure contribution towards buoyancy
        self.chi = chi
        self.gamma0, self.cp0, self.cv0 = gamma0, cp0, cv0

    def dbuoyancydp(self, p, T: ufl.core.expr.Expr):
        return -self.Di * self.cp0 / self.cv0 / self.gamma0 * self.g * self.rho * self.chi

    def buoyancy(self, p, T):
        pressure_part = self.dbuoyancydp(p, T) * p
        temperature_part = super().buoyancy(p, T)
        return pressure_part + temperature_part
