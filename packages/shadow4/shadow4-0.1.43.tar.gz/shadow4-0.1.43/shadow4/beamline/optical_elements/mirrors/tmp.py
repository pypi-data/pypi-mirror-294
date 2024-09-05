from shadow4.beamline.s4_beamline import S4Beamline

beamline = S4Beamline()

# electron beam
from shadow4.sources.s4_electron_beam import S4ElectronBeam
electron_beam = S4ElectronBeam(energy_in_GeV=6,energy_spread=0.001,current=0.2)
electron_beam.set_sigmas_all(sigma_x=3.01836e-05, sigma_y=3.63641e-06, sigma_xp=4.36821e-06, sigma_yp=1.37498e-06)

# magnetic structure
from shadow4.sources.undulator.s4_undulator_gaussian import S4UndulatorGaussian
source = S4UndulatorGaussian(
    period_length     = 0.0164,     # syned Undulator parameter (length in m)
    number_of_periods = 121.951, # syned Undulator parameter
    photon_energy     = 10000.0, # Photon energy (in eV)
    delta_e           = 0.0, # Photon energy width (in eV)
    ng_e              = 100, # Photon energy scan number of points
    flag_emittance    = 1, # when sampling rays: Use emittance (0=No, 1=Yes)
    flag_energy_spread = 0, # when sampling rays: Use e- energy spread (0=No, 1=Yes)
    harmonic_number    = 1, # harmonic number
    flag_autoset_flux_central_cone  = 0, # value to set the flux peak
    flux_central_cone  = 10000000000.0, # value to set the flux peak
    )


# light source
from shadow4.sources.undulator.s4_undulator_gaussian_light_source import S4UndulatorGaussianLightSource
light_source = S4UndulatorGaussianLightSource(name='GaussianUndulator', electron_beam=electron_beam, magnetic_structure=source,nrays=15000,seed=5676561)
beam = light_source.get_beam()

beamline.set_light_source(light_source)


# Error getting python code for S4Beamline S4BeamlineElement # 1  :
#       <shadow4.beamline.optical_elements.refractors.s4_conic_interface.S4ConicInterfaceElement object at 0x7fdecb421390>


# test plot
if True:
   from srxraylib.plot.gol import plot_scatter
   plot_scatter(beam.get_photon_energy_eV(nolost=1), beam.get_column(23, nolost=1), title='(Intensity,Photon Energy)', plot_histograms=0)
   plot_scatter(1e6 * beam.get_column(1, nolost=1), 1e6 * beam.get_column(3, nolost=1), title='(X,Z) in microns')