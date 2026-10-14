import csky as cy
import numpy as np

bins_sin_dec_100 = np.array([-1.000,-0.942,-0.886,-0.832,-0.779,-0.734,-0.690,-0.648,-0.609,-0.577,-0.542,
                                 -0.510,-0.480,-0.450,-0.424,-0.398,-0.374,-0.351,-0.330,-0.309,-0.289,-0.270,
                                 -0.252,-0.234,-0.217,-0.200,-0.184,-0.168,-0.153,-0.138,-0.124,-0.110,-0.096,
                                 -0.083,-0.070,-0.057,-0.045,-0.033,-0.021,-0.009,0.002,0.013,0.024,0.035,0.046,
                                 0.057,0.068,0.079,0.090,0.101,0.111,0.122,0.134,0.145,0.157,0.169,0.181,0.193,
                                 0.206,0.219,0.232,0.246,0.259,0.274,0.288,0.303,0.318,0.333,0.348,0.364,0.379,
                                 0.395,0.411,0.428,0.444,0.461,0.479,0.496,0.514,0.532,0.550,0.569,0.588,0.608,
                                 0.628,0.648,0.669,0.690,0.711,0.733,0.755,0.777,0.800,0.823,0.846,0.871,0.895,
                                 0.920,0.945,0.972,1.000])

split = -0.14

south_bins = np.concatenate([
    bins_sin_dec_100[bins_sin_dec_100 < split],
    [split]
])

north_bins = np.concatenate([
    [split],
    bins_sin_dec_100[bins_sin_dec_100 > split]
])

fine_bins_log_energy = np.array([2.00,2.60,2.70,2.75,2.80,2.85,2.90,2.95,3.00,3.05,3.10,3.15,
                           3.20,3.30,3.45,3.70,3.95,4.15,4.30,4.50,4.70,4.95,5.15,5.65, 10.])

fine_bins_sindec = np.array([-1.000,-0.886,-0.779,-0.690,-0.609,-0.542,-0.480,-0.424,
                        -0.374,-0.330,-0.289,-0.252,-0.217,-0.184,-0.153,-0.124,
                        -0.096,-0.070,-0.045,-0.021,0.002,0.024,0.046,0.068,0.090,
                        0.111,0.134,0.157,0.181,0.206,0.232,0.259,0.288,0.318,0.348,
                        0.379,0.411,0.444,0.479,0.514,0.550,0.588,0.628,0.669,0.711,
                        0.755,0.800,0.846,0.895,0.945,1.000])

coarse_bins_log_energy = np.array([2.00,2.70,2.80,2.90,3.00,3.10,
                           3.20,3.45,3.95,4.30,4.70,5.15, 10.])

coarse_bins_sindec = np.array([-1.000,-0.779,-0.609,-0.480,
                        -0.374,-0.289,-0.217,-0.153,
                        -0.096,-0.045,0.002,0.046,0.090,
                        0.111,0.157,0.206,0.259,0.318,
                        0.379,0.444,0.514,0.588,0.669,
                        0.755,0.846,0.945,])


ps_tracks_bins_sindec = np.concatenate(
                [
                    np.linspace(-1, -0.93, 4 + 1),
                    np.linspace(-0.93, -0.3, 10 + 1),
                    np.linspace(-0.3, 0.05, 9 + 1),
                    np.linspace(0.05, 1, 18 + 1),
                ]
            )
ps_tracks_bins_log_energy = np.arange(1, 9.5 + 0.01, 0.125)

class GFUDataSpecs(object):
    class GFUDataSpec(cy.selections.TrackSpec):

        
        #_bins_logenergy = fine_bins_log_energy
        #_bins_sindec = bins_sin_dec_100
        
        _bins_sindec = bins_sin_dec_100
        _bins_logenergy = ps_tracks_bins_log_energy
        
    class GFUDataSpecNorth(cy.selections.TrackSpec):
        _bins_sindec = north_bins
        _bins_logenergy = ps_tracks_bins_log_energy
    class GFUDataSpecSouth(cy.selections.TrackSpec):
        _bins_sindec = south_bins
        _bins_logenergy = ps_tracks_bins_log_energy
        
    class GFU_2011_2022(GFUDataSpec):
        #GFU BDT Smoothing Cut Applied (V01-P09)
        _path_sig = "gfu_online/{version}/IC86_2023_MC.npy"
        _path_data = [
            "gfu_online/{version}/IC86_2011_data.npy",
            "gfu_online/{version}/IC86_2012_data.npy",
            "gfu_online/{version}/IC86_2013_data.npy",
            "gfu_online/{version}/IC86_2014_data.npy",
            "gfu_online/{version}/IC86_2015_data.npy",
            "gfu_online/{version}/IC86_2016_data.npy",
            "gfu_online/{version}/IC86_2017_data.npy",
            
            "gfu_online/{version}/IC86_2018_data.npy",
            "gfu_online/{version}/IC86_2019_data.npy",
            "gfu_online/{version}/IC86_2020_data.npy",
            "gfu_online/{version}/IC86_2021_data.npy",
            "gfu_online/{version}/IC86_2022_data.npy",
        ]
        _path_grls = [
            "gfu_online/{version}/GRL/IC86_2011_data.npy",
            "gfu_online/{version}/GRL/IC86_2012_data.npy",
            "gfu_online/{version}/GRL/IC86_2013_data.npy",
            "gfu_online/{version}/GRL/IC86_2014_data.npy",
            "gfu_online/{version}/GRL/IC86_2015_data.npy",
            "gfu_online/{version}/GRL/IC86_2016_data.npy",
            "gfu_online/{version}/GRL/IC86_2017_data.npy",
            
            "gfu_online/{version}/GRL/IC86_2018_data.npy",
            "gfu_online/{version}/GRL/IC86_2019_data.npy",
            "gfu_online/{version}/GRL/IC86_2020_data.npy",
            "gfu_online/{version}/GRL/IC86_2021_data.npy",
            "gfu_online/{version}/GRL/IC86_2022_data.npy",
        ]
    class GFU_2019_2023(GFUDataSpec):
        #GFU BDT Smoothing Cut Applied (V01-P09)
        _path_sig = "gfu_online/{version}/IC86_2023_MC.npy"
        _path_data = [
            "gfu_online/{version}/IC86_2019_data.npy",
            "gfu_online/{version}/IC86_2020_data.npy",
            "gfu_online/{version}/IC86_2021_data.npy",
            "gfu_online/{version}/IC86_2022_data.npy",
        ]
        _path_grls = [
            "gfu_online/{version}/GRL/IC86_2019_data.npy",
            "gfu_online/{version}/GRL/IC86_2020_data.npy",
            "gfu_online/{version}/GRL/IC86_2021_data.npy",
            "gfu_online/{version}/GRL/IC86_2022_data.npy",
        ]
    class GFU_2019_2023_north(GFUDataSpecNorth):
        #GFU BDT Smoothing Cut Applied (V01-P09)
        _path_sig = "north/IC86_2023_MC.npy"
        _path_data = [
            "north/IC86_2019_data.npy",
            "north/IC86_2020_data.npy",
            "north/IC86_2021_data.npy",
            "north/IC86_2022_data.npy",
        ]
        _path_grls = [
            "north/GRL/IC86_2019_data.npy",
            "north/GRL/IC86_2020_data.npy",
            "north/GRL/IC86_2021_data.npy",
            "north/GRL/IC86_2022_data.npy",
        ]
    class GFU_2019_2023_south(GFUDataSpecSouth):
            #GFU BDT Smoothing Cut Applied (V01-P09)
            _path_sig = "south/IC86_2023_MC.npy"
            _path_data = [
                "south/IC86_2019_data.npy",
                "south/IC86_2020_data.npy",
                "south/IC86_2021_data.npy",
                "south/IC86_2022_data.npy",
            ]
            _path_grls = [
                "south/GRL/IC86_2019_data.npy",
                "south/GRL/IC86_2020_data.npy",
                "south/GRL/IC86_2021_data.npy",
                "south/GRL/IC86_2022_data.npy",
            ]
        
    class GFU_2011sig_19_22acv(GFUDataSpec):
        #GFU BDT Smoothing Cut Applied (V01-P09)
        _path_sig = "gfu_online/{version}/IC86_2011_MC.npy"
        _path_data = [
            "gfu_online/{version}/IC86_2019_data.npy",
            "gfu_online/{version}/IC86_2020_data.npy",
            "gfu_online/{version}/IC86_2021_data.npy",
            "gfu_online/{version}/IC86_2022_data.npy",
        ]
        _path_grls = [
            "gfu_online/{version}/GRL/IC86_2019_data.npy",
            "gfu_online/{version}/GRL/IC86_2020_data.npy",
            "gfu_online/{version}/GRL/IC86_2021_data.npy",
            "gfu_online/{version}/GRL/IC86_2022_data.npy",
        ]
    
   
    #gfu_11yr = [GFU_2011_2022] #not use bcs of bump problem
    gfu_19_to_23 = [GFU_2019_2023]
    north_gfu_19_to_23 = [GFU_2019_2023_north]
    south_gfu_19_to_23 = [GFU_2019_2023_south]
    gfu_11sig_19_22acv = [GFU_2011sig_19_22acv]