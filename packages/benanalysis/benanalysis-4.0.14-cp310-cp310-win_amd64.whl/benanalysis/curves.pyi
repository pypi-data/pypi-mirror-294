from __future__ import annotations
import benanalysis._benpy_core
__all__ = ['lognormal', 'longpass_filter', 'shortpass_filter']
def lognormal(peak_wl: float, fwhm: float, min_wl: float, max_wl: float, step_wl: float) -> benanalysis._benpy_core.Scan:
    """
      Generates a lognormal scan over a specified wavelength range.
    
      This function computes a lognormal distribution of values over a wavelength 
      range specified by the minimum (`min_wl`) and maximum (`max_wl`) wavelengths, 
      with a given step size (`step_wl`). The distribution is characterized by a 
      peak wavelength (`peak_wl`) and a full width at half maximum (`fwhm`).
    
      Parameters:
        peak_wl (double): The peak wavelength of the lognormal distribution. Must be greater than 0.
        fwhm (double): The full width at half maximum of the lognormal distribution. Must be greater than 0.
        min_wl (double): The minimum wavelength for the scan. Must be less than `max_wl`.
        max_wl (double): The maximum wavelength for the scan. Must be greater than `min_wl`.
        step_wl (double): The step size for the scan. Must be positive and less than or equal to (`max_wl - min_wl`).
    
      Returns:
        Scan: A Scan object containing the computed lognormal values mapped to their corresponding wavelengths.
    
      Throws:
        std::invalid_argument: If any of the following conditions are met:
        - `peak_wl <= 0`
        - `fwhm <= 0`
        - `min_wl >= max_wl`
        - `step_wl > (max_wl - min_wl)`
        - `step_wl <= 0`
    """
def longpass_filter(center_wl: float, bandwidth: float, min_wl: float, max_wl: float, step_wl: float) -> benanalysis._benpy_core.Scan:
    """
      Generate a long-pass filter scan based on specified parameters.
    
      The filter's bandwidth is defined as the wavelength range over which transmission
      rises from 5% to 95%. The transmission values in the scan range from 0 to 1.
    
      Parameters:
        center_wl (double): The center wavelength of the filter.
        bandwidth (double): The bandwidth of the filter (5% to 95% transmission range).
        min_wl (double): The minimum wavelength for the scan.
        max_wl (double): The maximum wavelength for the scan.
        step_wl (double): The step size for the wavelength increments.
    
      Returns:
        Scan: A Scan object representing the long-pass filter response.
    
      Throws:
        std::invalid_argument: If the wavelength parameters are invalid 
                               (e.g., min_wl >= max_wl, step_wl <= 0, or 
                               step_wl > (max_wl - min_wl)).
    """
def shortpass_filter(center_wl: float, bandwidth: float, min_wl: float, max_wl: float, step_wl: float) -> benanalysis._benpy_core.Scan:
    """
      Generate a short-pass filter scan based on specified parameters.
    
      The filter's bandwidth is defined as the wavelength range over which transmission
      falls from 95% to 5%. The transmission values in the scan range from 0 to 1.
    
      Parameters:
        center_wl (double): The center wavelength of the filter.
        bandwidth (double): The bandwidth of the filter (5% to 95% transmission range).
        min_wl (double): The minimum wavelength for the scan.
        max_wl (double): The maximum wavelength for the scan.
        step_wl (double): The step size for the wavelength increments.
    
      Returns:
        Scan: A Scan object representing the short-pass filter response.
    
      Throws:
        std::invalid_argument: If the wavelength parameters are invalid 
                               (e.g., min_wl >= max_wl, step_wl <= 0, or 
                               step_wl > (max_wl - min_wl)).
    """
