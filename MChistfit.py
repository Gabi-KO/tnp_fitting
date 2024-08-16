import os
import argparse
import numpy as np
from scipy.integrate import quad
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import re
from collections.abc import Iterable
from scipy.stats import chisquare
#from iminuit import Minuit
#from iminuit.cost import LeastSquares

parser = argparse.ArgumentParser(description='fitting code')
parser.add_argument('--filename', help='name of .C file')
#parser.add_argument('--histname', help='name of histogram')
parser.add_argument('--run_number', help='name for png')

args = parser.parse_args()
print(args)

# Create directory if it does not exist
def makeDir(dir_name):
    os.makedirs(dir_name, exist_ok=True)

#check if iterable
def check_iterable(obj):
    if isinstance(obj, Iterable):
        is_iterable = True
    else:
        is_iterable = False
    
    return is_iterable

#signal function - double gaussian
def double_gauss(x, *params):

    mean = params[0]
    sigma1 = params[1]
    sigma2 = params[2]
    alpha = params[3]
    #phi = params[3]
    
    #A1 = params[3]
    #A2 = params[4]

    #cos = np.cos(phi)**2
    #sin = np.sin(phi)**2

    #gauss =  A1*np.exp((-(x-mean)**2)/(2*(sigma1**2))) + A2*np.exp((-(x-mean)**2)/(2*(sigma2**2)))
    gauss = (1/np.sqrt(2*np.pi))*( (alpha/sigma1)*np.exp((-(x-mean)**2)/(2*(sigma1**2))) + ((1-alpha)/sigma2)*np.exp((-(x-mean)**2)/(2*(sigma2**2))) )
    #gauss = (1/np.sqrt(2*np.pi))*( (cos/sigma1)*np.exp((-(x-mean)**2)/(2*(sigma1**2))) + ((sin)/sigma2)*np.exp((-(x-mean)**2)/(2*(sigma2**2))) )

    return gauss

#exponent for error function
def err_exp(t):
    return np.exp(-t**2)

#background function - error function
def bkg_func(x, *params):

    peak = params[0]
    alpha = params[1]
    beta = params[2]
    gamma = params[3]

    is_iterable = check_iterable(x)

    x0 = (alpha - x) * beta

    erfc_results = np.zeros_like(x0)
    u_results = np.zeros_like(x0)

    if is_iterable:

        for i, x0_val in enumerate(x0):
        
            # Integrate for each x0 value
            integral, _ = quad(err_exp, 0, x0_val)

            erfc_results[i] = 1 - (2 / np.sqrt(np.pi)) * integral
            u = (x[i] - peak) * gamma

            if u < -70:
                u_results[i] = 10**20
            elif u > 70:
                u_results[i] = 0
            else:
                u_results[i] = np.exp(-u)
    
        return erfc_results*u_results

    else:

        integral, _ = quad(err_exp, 0, x0)

        erfc = 1 - (2 / np.sqrt(np.pi)) * integral
        u0 = (x - peak) * gamma

        if u0 < -70:
            u = 10**20
        elif u0 > 70:
            u = 0
        else:
            u = np.exp(-u0)
        
        return erfc*u

#normal gaussian for testing
def gaussian(x, *params):

    mean = params[0]
    sigma = params[1]
    A = params[2]

    gauss = A * np.exp((-(x-mean)**2)/(2*(sigma**2)))

    return gauss

#RooCBEGaussShape
def CBEGauss(x, *params):

    mean = params[0]
    sigma1 = params[1]
    sigma2 = params[2]
    alpha = params[3]
    n = params[4]
    tailLeft = params[5]

    for i in range(len(x)):
        
        t = (x[i]-mean)/sigma1
        t0 = (x[i]-mean)/sigma2
        
        rval_results = np.zeros_like(x)

        if tailLeft >= 0:
            if t > 0:
                rval_results[i] = np.exp(- t0 / 2)
            elif t > - np.abs(alpha):
                rval_results[i] = np.exp(- t / 2)
            else:
                a = np.exp(-(np.abs(alpha)**2)/2)
                b = np.exp(n*(t+np.abs(alpha)))
            
                rval_results[i] = a*b
        else:
            if t0 > 0:
                rval_results[i] = np.exp(- t / 2)
            elif t0 < np.abs(alpha):
                rval_results[i] = np.exp(- t0 / 2)
            else:
                a = ((np.abs(n)/np.abs(alpha))**(np.abs(n))) * np.exp(-(np.abs(alpha)**2)/2)
                b = (np.abs(n)/np.abs(alpha)) - np.abs(alpha)

                rval_results[i] = a / (b + t0)**np.abs(n)

    
    return rval_results

#background exponential
def bkg_exp(x, *params):
    a = params[0]
    b = params[1]
    c = params[2]

    return a*np.exp(-b*x) + c

# Fit gaussian with background
def fit_gaussian_with_background(file_name):

    #Setup

    variable = file_name.strip('.C')
    plot_dir = f'Preselection_Loose/Final_Plots_v2/{variable}/fit_{args.run_number}/'
    makeDir(plot_dir)
    figname = f"MC_{variable}_fit_{args.run_number}.png"

    #Double (2) or Single Gaussian (1)
    gauss_type = 1
    
    #Background Function (1) or Exponential (0)
    bkg_type = 1

    #Manual Override
    override = 1

    bin_contents = []
    bin_edges = []
    bin_errors = []
    bin_centers_sig = []
    bin_centers_bkg = []

    bin_content_pattern = re.compile(r'->SetBinContent\((\d+),([\d.]+)\);')
    bin_error_pattern = re.compile(r'->SetBinError\((\d+),([\d.]+)\);')
    hist_params = re.compile(r'TH1D\(".*",\s*(\d+),(\d+),(\d+)\)')
    pass_params = re.compile(r'_Pass__\d+ = new TH1D')
    fail_params = re.compile(r'_Fail__\d+ = new TH1D')
    entry_params = re.compile(r'SetEntries\((\d+)\)')

    ###############

    # Define the bins

    with open(file_name, "r") as f:
        
        df = f.readlines()

        for line in df:
            
            content_match = bin_content_pattern.search(line)
            error_match = bin_error_pattern.search(line)
            param_match = hist_params.search(line)
            pass_match = pass_params.search(line)
            fail_match = fail_params.search(line)
            entry_match = entry_params.search(line)

            if content_match:
                bin_contents.append(float(content_match.group(2)))
            
            if error_match:
                bin_errors.append(float(error_match.group(2)))

            if param_match:
                num_bins = float(param_match.group(1))
                x_min = float(param_match.group(2))
                x_max = float(param_match.group(3))
            
            if pass_match:
                passfail = 'P'
            
            if fail_match:
                passfail = 'F'

            if entry_match:
                entry_num = float(entry_match.group(1))

    
    if num_bins == len(bin_contents):
        print("# of Bins:", num_bins)
        print("# of Entries:", entry_num)
    else:
        print("# of Bins do not match")
        print(num_bins, len(bin_contents))

    bin_edges = np.linspace(x_min, x_max, num_bins + 1)

    bin_contents = np.array(bin_contents)
    bin_edges = np.array(bin_edges)
    bin_errors = np.array(bin_errors) 

    print("Bins Received")
    
    print("Setting Parameters ...")

    #bounds for fitting
    #changes what bins are used in fit
    sig_min = 80
    sig_max = 100
    
    bkg_min = 50
    bkg_max = 75

    bkg_min2 = 110
    bkg_max2 = 130
    
    mask_sig = (bin_edges[:-1] >= sig_min) & (bin_edges[:-1] <= sig_max)
    #mask_bkg = (bin_edges[:-1] >= bkg_min) & (bin_edges[:-1] <= bkg_max)
    mask_bkg = ((bin_edges[:-1] >= bkg_min) & (bin_edges[:-1] <= bkg_max)) | ((bin_edges[:-1] >= bkg_min2) & (bin_edges[:-1] <= bkg_max2))

    bin_contents_sig = bin_contents[mask_sig]
    bin_centers_sig = (bin_edges[:-1][mask_sig] + bin_edges[1:][mask_sig]) / 2
    bin_contents_bkg = bin_contents[mask_bkg]
    bin_centers_bkg = (bin_edges[:-1][mask_bkg] + bin_edges[1:][mask_bkg]) / 2

    bin_errors_sig = bin_errors[mask_sig]
    bin_errors_bkg = bin_errors[mask_bkg]
    
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    bin_centers_sig = np.array(bin_centers_sig)
    bin_centers_bkg = np.array(bin_centers_bkg)
    bin_centers = np.array(bin_centers)
    
    bin_errors_sig = np.array(bin_errors_sig)
    bin_errors_bkg = np.array(bin_errors_bkg)

    ###############

    #Finding Parameters
    
    #sigma = 0
    sigma = 1

    #for i in range(len(bin_centers)):
        #sigma += bin_centers[i]*bin_contents[i] / entry_num

    #print('Sigma Guess:', sigma)

    #Background
    alpha = 55
    beta = 0.05
    gamma = 0.01

    bkg_max_val = bin_contents_bkg.max() #maximum bin height
    mean_bkg_loc = np.where(bin_contents_bkg == bkg_max_val) #index
    mean_bkg = bin_centers_bkg[mean_bkg_loc]

    mean_bkg = mean_bkg[0]
    peak = bkg_max_val

    print('Background Mean:', mean_bkg)
    print('Background Peak:', peak)

    #background function
    if bkg_type == 1:
        p0_bkg = [peak, alpha, beta, gamma]  
        popt_bkg, pcov_bkg = curve_fit(bkg_func, bin_centers_bkg, bin_contents_bkg, p0=p0_bkg, maxfev=100000000)
    
    #exponential function
    if bkg_type == 0:
        popt_bkg, pcov_bkg = curve_fit(bkg_exp, bin_centers_bkg, bin_contents_bkg, p0=(1, 1e-6, 1), maxfev=100000000)
    
    #p0_bkg = [mean_bkg, sigma, bkg_max_val] #gaussian
    #popt_bkg, pcov_bkg = curve_fit(gaussian, bin_centers_bkg, bin_contents_bkg, p0=p0_bkg, maxfev=10000)

    #print(len(popt_bkg))

    print("Background Parameters Set")

    #Signal
    sig_max_val = bin_contents_sig.max() #maximum bin height
    mean_loc = np.where(bin_contents_sig == sig_max_val) #index
    mean = bin_centers_sig[mean_loc]

    if bkg_type == 1:
        bkg_at_mean = bkg_func(mean, *popt_bkg)
    if bkg_type == 0:
        bkg_at_mean = bkg_exp(mean, *popt_bkg)
    if bkg_at_mean > sig_max_val:
        bkg_at_mean = 0

    #bkg_at_mean = gaussian(mean, *popt_bkg)

    mean = mean[0]

    print('Signal Mean:', mean)
    #print(bkg_at_mean)

    amp = sig_max_val - bkg_at_mean
    #amp = amp[0]
    #print(amp)
    
    #double gaussian w/ phi
    phi = np.pi / 4

    #CBEGaussShape
    alpha_sig = 2
    n = 2
    tailLeft = 2

    #double gaussian
    if gauss_type == 2:
        p0_sig = [mean, sigma, sigma, amp] 
        #p0_sig = [mean, sigma, sigma, phi] # w/ phi
        bounds_sig = ([sig_min, -5, -5, 0], [sig_max, 5, 5, sig_max_val])
        popt_sig, pcov_sig = curve_fit(double_gauss, bin_centers_sig, bin_contents_sig, p0=p0_sig, bounds=bounds_sig, maxfev=10000)
        if override == 1:
            popt_sig[3] = ( amp*np.sqrt(2*np.pi) - 1/popt_sig[2] ) / ( (1/popt_sig[1]) - (1/popt_sig[2]) )


    #single gaussian
    if gauss_type == 1:
        p0_sig = [mean, sigma, amp]
        bounds_sig = ([sig_min, -5, 0], [sig_max, 5, sig_max_val])
        popt_sig, pcov_sig = curve_fit(gaussian, bin_centers_sig, bin_contents_sig, p0=p0_sig, bounds=bounds_sig, maxfev=10000)
        if override == 1:
            popt_sig[2] = amp
    
    #p0_sig = [mean, sigma, sigma, alpha_sig, n, tailLeft] #CBEGaussShape
    #popt_sig, pcov_sig = curve_fit(CBEGauss, bin_centers_sig, bin_contents_sig, p0=p0_sig, maxfev=10000) #CBEGaussShape

    print("Signal Parameters Set")

    #print('Signal Fit Parameters:', popt_sig)
    #print('Background Fit Parameters:', popt_bkg)

    ###############

    #Plotting
    print("Making Plots ...")

    #Graphing Interval
    interval = np.linspace(x_min, x_max, 10000)

    fig = plt.figure(figsize=(10, 10))
    plt.rcParams.update({'font.size': 22})

    plt.errorbar(bin_centers, bin_contents, yerr=bin_errors, fmt='none', linestyle='None', color='black', capsize=2) #Error Bars
    
    #plt.scatter(bin_centers_sig, bin_contents_sig, color='red')
    #plt.scatter(bin_centers_bkg, bin_contents_bkg, color='green')
    #plt.scatter(bin_centers, bin_contents, color='black')
    
    plt.hist(bin_edges[:-1], bins=bin_edges, weights=bin_contents, histtype = 'step', color='tab:blue') #Make Histogram
    
    #Plot Signal
    if gauss_type == 2:
        plt.plot(interval, double_gauss(interval, *popt_sig), label='Signal', color='red')
    if gauss_type == 1:
        plt.plot(interval, gaussian(interval, *popt_sig), label='Signal', color='red')
    
    #plt.plot(interval, CBEGauss(interval, *popt_sig), label='Signal', color='red') #CBEGaussShape
    
    #Plot Background
    if bkg_type == 1:
        plt.plot(interval, bkg_func(interval, *popt_bkg), label='Background', color='green') 
    if bkg_type == 0:
        plt.plot(interval, bkg_exp(interval, *popt_bkg), label='Background', color='green')
    
    #plt.plot(interval, gaussian(interval, *popt_bkg), label='Background', color='green') 

    #Plot Combined
    
    if gauss_type == 2 and bkg_type == 1:
        combined_fit = double_gauss(interval, *popt_sig) + bkg_func(interval, *popt_bkg) 
        combined_fit_2 = double_gauss(bin_centers, *popt_sig) + bkg_func(bin_centers, *popt_bkg)
    if gauss_type == 1 and bkg_type == 1:
        combined_fit = gaussian(interval, *popt_sig) + bkg_func(interval, *popt_bkg)
        combined_fit_2 = gaussian(bin_centers, *popt_sig) + bkg_func(bin_centers, *popt_bkg)
    if gauss_type == 2 and bkg_type == 0:
        combined_fit = double_gauss(interval, *popt_sig) + bkg_exp(interval, *popt_bkg) 
        combined_fit_2 = double_gauss(bin_centers, *popt_sig) + bkg_exp(bin_centers, *popt_bkg)
    if gauss_type == 1 and bkg_type == 0:
        combined_fit = gaussian(interval, *popt_sig) + bkg_exp(interval, *popt_bkg)
        combined_fit_2 = gaussian(bin_centers, *popt_sig) + bkg_exp(bin_centers, *popt_bkg)

    #combined_fit = gaussian(interval, *popt_sig) + gaussian(interval, *popt_bkg) #gaussian & gaussian
    #combined_fit = double_gauss(interval, *popt_sig) + gaussian(interval, *popt_bkg) #double gaussian & gaussian
    #combined_fit = CBEGauss(interval, *popt_sig) + bkg_func(interval, *popt_bkg) #CBEGaussShape & background function
    
    plt.plot(interval, combined_fit, label='Combined Fit', color='blue') 

    print("Checking Stats ...")

    if gauss_type == 2:
        intg_sig, _ = quad(double_gauss, x_min, x_max, args = tuple(popt_sig))
        intg_sig_2, _ = quad(double_gauss, sig_min, sig_max, args = tuple(popt_sig))
    if gauss_type == 1:
        intg_sig, _ = quad(gaussian, x_min, x_max, args = tuple(popt_sig))
        intg_sig_2, _ = quad(gaussian, sig_min, sig_max, args = tuple(popt_sig))

    if bkg_type == 1:
        intg_bkg, _ = quad(bkg_func, x_min, x_max, args = tuple(popt_bkg))
        intg_bkg_2, _ = quad(bkg_func, sig_min, sig_max, args = tuple(popt_bkg))
    if bkg_type == 0:
        intg_bkg, _ = quad(bkg_exp, x_min, x_max, args = tuple(popt_bkg))
        intg_bkg_2, _ = quad(bkg_exp, sig_min, sig_max, args = tuple(popt_bkg))
    
    #intg_bkg, _ = quad(gaussian, x_min, x_max, args = tuple(popt_bkg))
    
    combo = intg_sig + intg_bkg
    combo_2 = intg_sig_2 + intg_bkg_2

    print('Signal:', intg_sig)
    print('Signal Sum:', sum(bin_contents_sig))
    print('Background:', intg_bkg)
    #print('Background Sum:', sum(bin_contents_bkg))
    #print(combo)

    ratio = entry_num/combo
    print('Ratio of Actual Entries to Integral:', ratio)

    N_sig = intg_sig * ratio
    N_bkg = intg_bkg * ratio

    print('N_sig:', N_sig)
    print('N_bkg:', N_bkg)

    sig_err = np.sqrt(N_sig)
    bkg_err = np.sqrt(N_bkg)

    if bkg_type == 1:
        err_bkg = [pcov_bkg[0][0], pcov_bkg[1][1], pcov_bkg[2][2], pcov_bkg[3][3]] #Background Function
    if bkg_type == 0:
        err_bkg = [pcov_bkg[0][0], pcov_bkg[1][1], pcov_bkg[2][2]] #Background Function
    
    #err_bkg = [pcov_bkg[0][0], pcov_bkg[1][1], pcov_bkg[2][2]] #Gaussian

    if gauss_type == 2:
        err_sig = [pcov_sig[0][0], pcov_sig[1][1], pcov_sig[2][2], pcov_sig[3][3]]
    if gauss_type == 1:
        err_sig = [pcov_sig[0][0], pcov_sig[1][1], pcov_sig[2][2]]

    err_bkg = np.sqrt(err_bkg)
    err_sig = np.sqrt(err_sig)

    chi2 = chisquare(bin_contents, combined_fit_2)
    
    display1 = f'N_sig{passfail} = {int(N_sig)} $\pm$ {int(sig_err)}'
    display2 = f'N_bkg{passfail} = {int(N_bkg)} $\pm$ {int(bkg_err)}'
    display3 = f'$\chi^2$ / $n_\mathrm{{dof}}$ = {int(chi2[0])} / {len(bin_contents) - 1}'
    
    plt.plot([], [], " ", label=display1)
    plt.plot([], [], " ", label=display2)
    plt.plot([], [], " ", label=display3)
    #plt.annotate(f'N_sig{passfail} = {int(N_sig)} $\pm$ {int(sig_err)}', xy=(x_max - 30, 3*sig_max_val/4), xytext=(10,10), textcoords='offset points')
    #plt.annotate(f'N_bkg{passfail} = {int(N_bkg)} $\pm$ {int(bkg_err)}', xy=(x_max - 30, 5*sig_max_val/8), xytext=(10,10), textcoords='offset points')

    plt.xlim(x_min - 5, x_max + 5)
    #plt.ylim(0, sig_max_val + 500)
    plt.xlabel('$m_{ee}$')
    plt.ylabel('# of Events')
    plt.title(variable)
    plt.legend(loc='upper left', fontsize=15)
    plt.savefig(os.path.join(plot_dir, figname))

    print('=======> Plot saved as <=======')
    print(f"/{plot_dir}{figname}")


    print('Making Data File ...')

    with open(f'{plot_dir}/results.txt', 'w') as w:

        print('Background Parameters', file=w)
        print('---------------------', file=w)
        print(f'({bkg_min}, {bkg_max}) U ({bkg_min2}, {bkg_max2})', file=w)
        
        if bkg_type == 1:
            #Background Function
            print(f'Peak: {popt_bkg[0]} +/- {err_bkg[0]}', file=w)
            print(f'Alpha: {popt_bkg[1]} +/- {err_bkg[1]}', file=w)
            print(f'Beta: {popt_bkg[2]} +/- {err_bkg[2]}', file=w)
            print(f'Gamma: {popt_bkg[3]} +/- {err_bkg[3]}', file=w)
            #print('Covariance:', file=w)
            #print(pcov_bkg, file=w)
        if bkg_type == 0:
            #Exponential
            print(f'a: {popt_bkg[0]} +/- {err_bkg[0]}', file=w)
            print(f'b: {popt_bkg[1]} +/- {err_bkg[1]}', file=w)
            print(f'c: {popt_bkg[2]} +/- {err_bkg[2]}', file=w)
            #print('Covariance:', file=w)
            #print(pcov_bkg, file=w)

        '''
        #Gaussian
        print(f'Mean: {popt_bkg[0]} +/- {err_bkg[0]}', file=w)
        print(f'Sigma: {popt_bkg[1]} +/- {err_bkg[1]}', file=w)
        print(f'Amplitude: {popt_bkg[2]} +/- {err_bkg[2]}', file=w)
        print('Covariance:', file=w)
        print(pcov_bkg, file=w)
        '''
        
        print(file=w)
        
        print('Signal Parameters', file=w)
        print('---------------------', file=w)
        print(f'({sig_min}, {sig_max})', file=w)
        
        if gauss_type == 2:
            #Double Gaussian
            print(f'Mean: {popt_sig[0]} +/- {err_sig[0]}', file=w)
            print(f'Sigma 1: {popt_sig[1]} +/- {err_sig[1]}', file=w)
            print(f'Sigma 2: {popt_sig[2]} +/- {err_sig[2]}', file=w)
            print(f'Alpha: {popt_sig[3]} +/- {err_sig[3]}', file=w)
            #print('Covariance:', file=w)
            #print(pcov_sig, file=w)

        if gauss_type == 1:
            #Single Gaussian
            print(f'Mean: {popt_sig[0]} +/- {err_sig[0]}', file=w)
            print(f'Sigma: {popt_sig[1]} +/- {err_sig[1]}', file=w)
            print(f'Amplitude: {popt_sig[2]} +/- {err_sig[2]}', file=w)
            #print('Covariance:', file=w)
            #print(pcov_sig, file=w)
        
        print(file=w)
        
        print('Integrals & Sums', file=w)
        print('---------------------', file=w)
        print('Signal:', intg_sig, file=w)
        print('Background:', intg_bkg, file=w)
        print('Full Integral:', combo, file=w)
        print(file=w)
        print('Sum of Signal Bins:', sum(bin_contents_sig), file=w)
        print('Integral of Combined Fit on Signal Bins:', combo_2, file=w)
        print(file=w)

        print('Ratio of Actual Entries to Integral:', ratio, file=w)
        print(file=w)

        print(f'N_sig: {N_sig} +/- {sig_err}', file=w)
        print(f'N_bkg: {N_bkg} +/- {bkg_err}', file=w)
        print(f'Total: {N_sig + N_bkg}', file=w)

    print('=======> Data saved as <=======')
    print(f'{plot_dir}/results.txt')


if __name__ == "__main__":

    filename = args.filename
    #hist = args.histname #bin00_el_sc_eta_m0p80To0p80_el_pt_20p00To30p00_Fail
    
    fit_gaussian_with_background(filename)