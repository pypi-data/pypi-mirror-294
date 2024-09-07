import pandas as pd
import numpy as np

# This function prints out the relevant information about the simulated population.

def print_info(population):

    """
    Prints the simulation's most significant parameters: 
    whether a population or a single disc has been simulated, if dust has been used, the (central)
    values of alpha, initial disc radius, initial disc mass, their spreads, the maximum and
    minimum disc masses, the number of snapshots used and their value (in code units - must be
    divided by 6 $\pi$ to convert to Myr).
    """
    
    print("\033[1mSimulations Parameters \033[0m")
    
    if population.parameters['nysos'] == 1:
        print("Simulating a single disc")
    else:
        print("Simulating a population of ", population.parameters['nysos'], " objects")
        
    ###############

    if population.parameters['dust'] == True:
        print("Using dust")
    else:
        print("Not using dust")
        
    if population.parameters['analytic'] == True:
        print("The evolution is analytic")
    else:
        print("The evolution is numeric")

    if population.parameters['options.REPRODUCIBILITY'] == True:
        print("Reproducibility is set to True with seed ", population.parameters['seed'])
        
    if population.parameters['options.MHD'] == True:
        print("MHD is turned on: omega = ", population.parameters['omega'], "lever arm: ", population.parameters['leverarm'])
    else:
        print("MHD is turned off")
        
    if population.parameters['imf'] == 'kroupa':
        print("Used the Kroupa (2002) Initial Mass Function")
        print('The minimum stellar mass is', population.parameters['mmin'], 'solar masses, and the maximum stellar mass is', population.parameters['mmax'], 'solar masses')
    elif population.parameters['imf'] == 'single':
        print("All stars in the population have the same mass of", population.parameters['mstar'], "solar masses")
    elif population.parameters['imf'] == 'custom':
        print("Used a custom set of stellar masses provided from the mstar.txt file")

    ######## Depending on the correlations

    if population.parameters['options.CORRELATION'] == True:
        print("Using correlations between the disc and the stellar properties:")

        print("\033[1m Disc mass: \033[0m")
        print("Normalisation at one solar mass:", population.parameters['mdisc_norm'], 'solar masses')
        print("Slope of the correlation:", population.parameters['mdisc_slope'])
        print("Spread of the correlation:", population.parameters['mdisc_spread'], 'dex')
        print("Distribution:", population.parameters['mdisc_method'])
        
        print("\033[1m Accretion rate: \033[0m")
        print("Normalisation at one solar mass: 10^(", population.parameters['log_mdot_norm'], ') solar masses per year')
        print("Slope of the correlation:", population.parameters['mdot_slope'])

        print("\033[1m Disc radius: \033[0m")
        print("The normalisation and slope are determined following the relations in Somigliana+2022")
        print("Spread of the correlation: ", population.parameters['rdisc_spread'], 'dex')
        print("Distribution: ", population.parameters['rdisc_method'])

        print("\033[1m Magnetisation beta: \033[0m")
        print("Normalisation at one solar mass:", population.parameters['beta_mag_norm'])
        print("Slope of the correlation:", population.parameters['beta_mag_slope'])
        print("Spread of the correlation:", population.parameters['beta_mag_spread'], 'dex')
        print("Distribution:", population.parameters['beta_mag_method'])

        if population.parameters['options.INTERNAL_PHOTOEV'] == True:
            if population.parameters['mdot_photoev_norm'] != 0:
                print("\033[1m Internal photoevaporation mass-loss rate: \033[0m")
                print("Normalisation at one solar mass:", population.parameters['mdot_photoev_norm'], 'solar masses')
                print("Slope of the correlation:", population.parameters['mdot_photoev_slope'])
                print("Spread of the correlation:", population.parameters['mdot_photoev_spread'], 'dex')
                print("Distribution:", population.parameters['mdot_photoev_method'])
            else:
                print("\033[1m Stellar X luminosity: \033[0m")
                print("Normalisation at one solar mass:", population.parameters['L_x_norm'], 'solar masses')
                print("Slope of the correlation:", population.parameters['L_x_slope'])
                print("Spread of the correlation:", population.parameters['L_x_spread'], 'dex')
                print("Distribution:", population.parameters['L_x_method'])
        else:
            print("Internal photoevaporation is turned off")



    else:
        print("Not using correlations between the disc and the stellar properties.")
        print("Mean disc mass: ", population.parameters['mdisc_mean'], 'solar masses')
        print("Disc mass spread: ", population.parameters['mdisc_spread'], 'dex')
        print("Mean disc radius: ", population.parameters['rdisc_mean'], 'au')
        print("Disc radius spread: ", population.parameters['rdisc_spread'], 'dex')
        print("Alpha Shakura&Sunyaev: ", population.parameters['alpha'])

        if population.parameters['options.MONTECARLO'] == True:
            print("Disc mass distribution:", population.parameters['mdisc_method'])
            print("Disc radius distribution:", population.parameters['rdisc_method'])
        


# This function converts the time in seconds from years (code unit)

def year2second(time):
    
    """
    Converts time from code units (years) to cgs units (seconds).

    time: value of time in years to be converted.
    """
    
    y2s = 3.154e+7                  # Was already defined above
    return time/y2s               # Returns the time in seconds

# This function converts the time in years (code unit) from seconds

def second2year(time):
    
    """
    Converts time from seconds (cgs units) to years (code units).

    time: value of time in seconds to be converted.
    """
    
    y2s = 3.154e+7
    return time*y2s

# This function converts the length in cm from au (code unit)

def au2cm(length):

    """
    Converts a length from code units (au) to cgs units (cm).

    length: length in au to be converted.
    """

    au2cm = 1.49598073e+13
    return length*au2cm

# This function converts the length in au (code unit) from cm

def cm2au(length):

    """
    Converts a length from cm (cgs units) to au (code units).

    length: length in cm to be converted.
    """

    au2cm = 1.49598073e+13     
    return length/au2cm

# This function converts the mass from grams to solar masses (code unit)

def g2Msun(mass):

    """
    Converts a mass from cgs units (grams) to code units (Msun).

    mass: mass in grams to be converted.
    """

    g2Ms = 5.0E-34             # Conversion factor from grams to solar masses
    return mass*g2Ms


# Filtering data - creates a new dictionary which only contains wanted_keys

def fildic2df(fulldata, wanted_keys):

    """
    Filters a dictionary, returning a new one with only the chosen variables.

    fulldata: full dictionary to be filtered.
    wanted_keys: list of variables to be mainteined in the new dictionary (ex. wanted_keys =
    ['t_Myear', 'sigma_g']).
    """

    dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])
    fildata = {}
    timedf = []
    
    for data in fulldata:
        
        fildata[data] = dictfilt(fulldata[data], wanted_keys)
        
    timedf = pd.DataFrame.from_dict(fildata,orient = 'index')
    
    return timedf

# This function converts the radius in AU (originally in cm) and the disc mass in solar masses.
# It tires to convert the dust mass (working if dust is present, skipping if not) and surely converts the gas mass.

def convert(data):

    """
    Converts the radius from cm to au and the disc mass (both in gas and dust, if applicable)
    from grams to Msun. 

    data: dictionary containing data, loaded with one of the loading functions.
    """
    
    data['R_au'] = cm2au(data['r_grid'])
    
    try:
        data['Mdisc_d_Msun'] = g2Msun(data['Mdisc_d'])
        
    except KeyError:
        pass
    
    data['Mdisc_g_Msun'] = g2Msun(data['Mdisc_g'])
    
    return data

#####################
# LOADING DATA: various functions to meet various requirements
#####################

# This function loads evolvedpop arrays with user-friendly names and correctly dimensionalises them in cgs units.
# Made for a SINGLE DISC (yso_index) and for a SINGLE TIMESTEP (time_index).

def load_data(population, yso_index, time_index, verbose = False):

    """
    Loads data for a given disc and timestep. Returns a dictionary filled with data. Includes
    the convert function, meaning that the radius is loaded in au and the masses in Msun.

    population: the population to which the disc belongs.
    yso_index: the progressive identification number of the disc.
    time_index: the progressive identification number of the timestep.
    verbose: if True, prints informations on the object (identification number of the disc,
    quantities loaded, units system).
    """

    au2cm_conv = 1.49598073e+13
    Msun2g_conv = 1.989*10**33
                
    arraysDict = {}                                    # (Empty) Dictionary of quantities
        
    snap = population.snapshots[time_index]

    # Identification number of the YSO

    arraysDict['n_yso'] = yso_index   
        
    # Time in Myr
        
    t_year = population.parameters['times_snapshot'][time_index]/(2.*np.pi)      # 2pi for code units dynamical time
    arraysDict['t_Myear'] = t_year                                            # Filling the dictionary with time

    # Quantities: Mdot (2pi for code units dynamical time)
    # Mdot's RAW unit is not consistent with the other units. The conversion is performed to make it Msun/yr.
        
    arraysDict['Mdot_star'] = snap.ysos[yso_index].star.mdot*au2cm_conv**2./Msun2g_conv*2.*np.pi  
    #arraysDict['yso_type'] = snap.ysos[yso_index].yso_parameters['yso_type']
    

    # Check whether you have a Class II or Class III object

    if snap.ysos[yso_index].yso_parameters['yso_type'] == 'ClassII':

        # Quantities: radius in cm
            
        arraysDict['r_grid'] = au2cm(snap.ysos[yso_index].disc.grid.Rc)    
                            
        # This try - except works only if dust quantities have been evaluated by discpop, i.e. if there was dust 
        # in the simulation. Otherwise, it does absolutely nothing. Would it be useful to print something? (Like - are 
        # you aware that there's no dust?)

        arraysDict['tacc0_Myr'] = snap.ysos[yso_index].disc_parameters['tacc0_Myr']
        arraysDict['Rd'] = snap.ysos[yso_index].disc_parameters['Rd']

        # Quantities: sigma gas [g cm^-2]
        arraysDict['sigma_g'] = snap.ysos[yso_index].disc.Sigma
            
        # Quantities: Mdisc gas - evaluated by integration of sigma_gas*2pi r dr - REMOVED A 2 (2*6.28)
        arraysDict['Mdisc_g'] = np.trapz(arraysDict['sigma_g']*2*np.pi*arraysDict['r_grid'], arraysDict['r_grid'])

        if snap.ysos[yso_index].disc_parameters['alpha_DW'] != 0:

            # Quantities: fM0 (MHD model)
            arraysDict['fM0'] = snap.ysos[yso_index].disc_parameters['fM0']
            try:
                arraysDict['alpha_DW'] = snap.ysos[yso_index].disc_parameters['alpha_DW']
                arraysDict['beta_mag'] = snap.ysos[yso_index].disc_parameters['beta_mag']
            except KeyError:
                pass

        if snap.ysos[yso_index].disc_parameters['dust'] == 'true':
                        
            # Quantities: sigma dust SMALL and LARGE grains [g cm^-2]
            arraysDict['sigma_d_small'] = snap.ysos[yso_index].disc.Sigma_D[0]
            arraysDict['sigma_d_large'] = snap.ysos[yso_index].disc.Sigma_D[1]
                
            # Quantities: sigma dust [g cm^-2], ALL grains
            arraysDict['sigma_d'] = arraysDict['sigma_d_small'] + arraysDict['sigma_d_large']
                
            # Quantities: grain size SMALL and LARGE grains cm (small:useless) - E' IL TWOPOP
            arraysDict['a_large'] = snap.ysos[yso_index].disc.grain_size[1]  # Raggio della polvere grande, componente 1
            arraysDict['a_small'] = snap.ysos[yso_index].disc.grain_size[0]  # Raggio della polvere piccola, componente 0
                
            # Quantities: Mdisc dust - evaluated by integration of sigma_dust*2pi r dr - REMOVED A 2 (2*6.28)
            arraysDict['Mdisc_d'] = np.trapz(arraysDict['sigma_d']*2.*np.pi*arraysDict['r_grid'],arraysDict['r_grid'])
            
            
        arraysDict = convert(arraysDict)
            
            
        # Info on the yso, time, and units printed 

        if verbose:
                
            print("data for the yso = %d at time = %f My"%(yso_index, t_year ))
            print("load raw quantities = \n\r %s  \n\r"%(list(arraysDict.keys())))
            print("units system: cgs")
                    
    return arraysDict
        
# This function loads evolvedpop arrays with user-friendly names and correctly dimensionalises them in cgs units.
# It works for a single disc (yso_index) and for all timesteps.

def load_data_alltimes(population, yso_index):

    """
    Loads data for a given disc at all timesteps. Returns a dictionary filled with data. 
    Includes the convert function, meaning that the radius is loaded in au and the masses 
    in Msun.

    population: the population to which the disc belongs.
    yso_index: the progressive identification number of the disc.
    """
    
    data = {}
    verbose = True
    
    for i in range(0, len(population.parameters['times_snapshot'])):

        if not population.snapshots[i].ysos[yso_index].yso_parameters['yso_type'] == 'ClassII':
            print("The disc of the chosen YSO is dispersed at timestep ", i)
            i = i + 1

        data[i] = load_data(population, yso_index, i, verbose)
        verbose = False
        
    return data

# This function loads evolvedpop arrays with user-friendly names and correctly dimensionalises them in cgs units.
# It works for all of the discs in the population for a given timestep.

def load_data_population(population, timestep):

    """
    Loads data for all of the discs in a population at a given timestep. Returns a dictionary 
    filled with data. Includes the convert function, meaning that the radius is loaded in au 
    and the masses in Msun.

    population: the population to which the discs belong.
    timesteps: the progressive identification number of the timestep.
    """
    
    data = {}
    
    for n_yso in range(0, population.parameters['nysos']):

        if not population.snapshots[timestep].ysos[n_ysos].yso_parameters['yso_type'] == 'ClassII':
            print("The disc of the YSO with identification number ", n_yso, " is dispersed at the chosen timestep.")
            n_yso = n_yso + 1

        data[n_yso] = load_data(population, n_yso, timestep, verbose = False)

    return data

# Load all data for all discs

def load_data_pop_alltimes(population):

    """
    Loads data for all of the discs in a population at all timesteps. Returns a dictionary 
    filled with data. Includes the convert function, meaning that the radius is loaded in au 
    and the masses in Msun.

    population: the population to which the discs belong.
    """

    popdata = {} # Definisco un dizionario in cui tenere tutti i dati di tutti i dischi a tutti i tempi

    for timestep in range(0, len(population.parameters['times_snapshot'])):

        ysoappo = {}   # Definisco un dizionario di appoggio

        for n_ysos in range(0, population.parameters['nysos']):        # Ciclo sul numero degli oggetti

            ysoappo[n_ysos] = load_data(population, n_ysos, timestep, verbose = False)   # Carico i dati per oggetto e tempo

            popdata[timestep] = ysoappo
        
        # Filtering data
    
    try:

        wanted_keys = ['n_yso', 't_Myear','R_au', 'sigma_g', 'Mdot_star','Mdisc_d_Msun','Mdisc_g_Msun', 'Mdisc_d_Msun', 'sigma_d_small', 'sigma_d_large', 'sigma_d', 'a_large', 'a_small', 'fM0', 'alpha_DW', 'beta_mag', 'tacc0_Myr', 'Rd']
        popdata_tot = []                      # Questa qui è una LISTA!

        for timestep in range(0, len(population.parameters['times_snapshot'])):

            popdata_tot.append(fildic2df(popdata[timestep], wanted_keys))


        return popdata_tot
    
    except AttributeError:
        
        wanted_keys = ['n_yso', 't_Myear','R_au', 'sigma_g', 'Mdot_star','Mdisc_d_Msun','Mdisc_g_Msun', 'fM0', 'alpha_DW', 'beta_mag', 'tacc0_Myr', 'Rd']
        popdata_tot = []                   

        for timestep in range(0, len(population.parameters['times_snapshot'])):

            popdata_tot.append(fildic2df(popdata[timestep], wanted_keys))


        return popdata_tot


def evolved_timesteps(population, data):

    array = np.zeros((len(data), len(data[0])))
    timesteps = []

    for i  in range(0, len(data)):
        for j in range(0, len(data[0])):
            if population.snapshots[i].ysos[j].yso_parameters['yso_type'] == 'ClassII':
                array[i][j] = True
            else:
                array[i][j] = False

    for i  in range(0, len(data)):
        if any(array[i]):
            timesteps.append(np.array(data[i]['t_Myear'])[0])

    return np.array(timesteps)


def load_arrays_time(population, data, time, mhd = False):
    
    mstar = []
    mdisc = []
    mdot = []
    #yso_type = []
    sigma_g = [[] for i in range(len(data[time]))]
    mask = [[] for i in range(len(data[time]))]
    tacc0_Myr = []
    fM0 = []
    beta = []
    alpha_DW = []
    Rd = []
    
    solarToCodeMass = 2e33/(1.5e13)**2 

    for i in range(0, len(data[time])):
        mask[i] = bool(np.where(population.snapshots[time].ysos[i].yso_parameters['yso_type'] == 'ClassII', True, False))
        mstar.append(np.array(population.snapshots[time].ysos[i].star.mass))
        mdot.append(np.array(population.snapshots[time].ysos[i].star.mdot*2.*np.pi/solarToCodeMass))
        sigma_g[i] = data[time]['sigma_g'][i]


    mdisc = data[time]['Mdisc_g_Msun']
    tacc0_Myr = data[0]['tacc0_Myr']
    Rd = data[0]['Rd']
    
    if mhd == True:
        fM0 = data[0]['fM0']
        alpha_DW = data[0]['alpha_DW']
        beta = data[0]['beta_mag']
        return np.array(mstar), np.array(mdisc), np.array(mdot), np.array(sigma_g, object), np.array(tacc0_Myr), np.array(Rd), mask, fM0, alpha_DW, beta
    else:
	    return np.array(mstar), np.array(mdisc), np.array(mdot), np.array(sigma_g, object), np.array(tacc0_Myr), np.array(Rd), mask
		

def load_arrays(population, data, timesteps, mhd = False):
    
    mstar = []
    mdisc = []
    mdot = []
    #yso_type = []
    sigma_g = []
    R = []
    mask = []
    tacc0_Myr = []
    Rd = []
    
    R = np.array(data[0]['R_au'][0])
    
    for time in range(0, len(timesteps)):
        mstar.append(load_arrays_time(population, data, time)[0])
        mdisc.append(load_arrays_time(population, data, time)[1])
        mdot.append(load_arrays_time(population, data, time)[2])
        sigma_g.append(load_arrays_time(population, data, time)[3])
        tacc0_Myr.append(load_arrays_time(population, data, time)[4])
        Rd.append(load_arrays_time(population, data, time)[5])
        mask.append(load_arrays_time(population, data, time)[6])
        
    if mhd == True:
        fM0 = []
        alpha_DW = []
        beta = []
        for time in range(0, len(timesteps)):
            fM0.append(load_arrays_time(population, data, time, mhd = True)[7])
            alpha_DW.append(load_arrays_time(population, data, time, mhd = True)[8])
            beta.append(load_arrays_time(population, data, time, mhd = True)[9])
        return mstar, mdisc, mdot, sigma_g, R, tacc0_Myr, Rd, mask, fM0, alpha_DW, beta
    else:
        return mstar, mdisc, mdot, sigma_g, R, tacc0_Myr, Rd, mask
