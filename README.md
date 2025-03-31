# Solar Thermal Propulsion
This project aims to establish the feasibility of solar thermal propulsion for interplanetary and cislunar transport. 

The main performance goals are:
* Moderately high specific impulse with storable propellants (1000s with NH<sub>3</sub>)
* Comparable weight to hypergolic rocket engines of the same thrust
* Extremely high specific impulse with LH<sub>2</sub> in the range of 2000s.

The exhaust velocity will be computed using chemical kinetics to provide the most realistic values. The method is adapted from the work by F.J Krieger titled "Chemical Kinetics and Rocket Nozzle design" (1951). This is a quasi-kinetic method, using isentropic values for P, v, T, and rho, to compute the species mole fraction using reaction rates.

Currently, the numerical solver is highly unstable and tends to produce non-physical results with certain inputs. A new solver based on the quasi-1d euler equations is currently being implemented. 
