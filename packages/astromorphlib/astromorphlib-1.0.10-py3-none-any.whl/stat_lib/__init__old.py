import numpy as np
import matplotlib.pyplot as plt

import statmorph
from statmorph.utils.image_diagnostics import make_figure

from astropy.io import fits, ascii
from astropy.table import Table
from astroquery import simbad
from astroquery.ipac.ned import Ned
from astropy.wcs import wcs
from astropy.coordinates import SkyCoord
import astropy.units as u

from photutils.segmentation import make_source_mask
from astropy.stats import sigma_clipped_stats
from photutils.background import Background2D, MedianBackground
from photutils.segmentation import detect_sources
from photutils.segmentation import deblend_sources

from astropy.convolution import Gaussian2DKernel
from astropy.stats import gaussian_fwhm_to_sigma

from urllib.parse import quote
from urllib.request import urlretrieve
from astropy.visualization import (MinMaxInterval, SqrtStretch, AsinhStretch,
                                   ImageNormalize, make_lupton_rgb)

from colorama import Fore

import scipy.ndimage as ndi

import photutils

import wget
from urllib import request

H=70.0
c_speed = 3e5
import os
import time

import plot_functions as pfunc

dr_dic = {8:'dr8',9:'ls-dr9', 10:'ls-dr10-early-grz'}

colormap = 'terrain'

server_fr = 'http://simbad.u-strasbg.fr/'
serve_usa = 'http://simbad.harvard.edu/'


#simbad.Simbad.list_votable_fields()
#simbad.Simbad.get_votable_fields()

simbad.Simbad.reset_votable_fields()

simbad.Simbad.remove_votable_fields('coordinates')


#simbad.Simbad.remove_votable_fields('ra(d)','dec(d)','rv_radvel','z_value',
#                                     'morphtype','dim_majaxis', 'dim_minaxis',
#                                     'dim_angle', 'flux(B)','flux(V)','flux(R)',
#                                    'flux(J)','flux(H)','flux(K)','otype')


simbad.Simbad.add_votable_fields('ra(d)', 'dec(d)', 'rv_value', 'z_value',
                                 'morphtype','dim_majaxis', 'dim_minaxis',
                                 'dim_angle', 'flux(B)', 'flux(V)', 'flux(R)',
                                 'flux(J)', 'flux(H)', 'flux(K)', 'otype')


def ima_fl2mag (namein, median_sky_v, area,t, zp):

    ima = np.copy(namein)
    ima[ima<=0]=np.nan
    return -2.5*np.log10((ima-median_sky_v)/(t*area))+zp

def cal_err_mag (I, I_err):
    return 2.5*(I_err/I)*(1./np.log(10.))

import matplotlib as mpl
mpl.rcParams['axes.labelsize']= 22
mpl.rcParams['legend.fontsize']= 15
mpl.rcParams['xtick.major.size']= 16
mpl.rcParams['xtick.minor.size']= 8
mpl.rcParams['ytick.major.size']= 16
mpl.rcParams['ytick.minor.size']= 8
mpl.rcParams['xtick.labelsize']= 16
mpl.rcParams['ytick.labelsize']= 16

def phot_mod (gal, tab_gal, conn, size_image_phy=50, snr_g = 2.0, areagal=2,
              user_order=None, user_list=None, user_claf =None, user_istage=None,
              sky_box=[100, 100],
              deblend='off', band='R', nsigma=2, npixels=5, dilate_size=11,
              segmap = None, petro_extent_cas=1.5,
              outputfile='properties.dat', eta=0.2, show_plot='yes',
              run_auto='no'):

    idg =np.where(tab_gal['gal']==gal)[0][0]
    D = tab_gal['vel'][idg]/H
    arc_kpc = np.tan(np.deg2rad(1./3600.))*D*1e3
    print (Fore.BLUE +"\nBasic information:")
    print (Fore.BLUE +"-------------------")
    print(Fore.BLUE +'arc_kpc {:.4f}'.format(arc_kpc))
    size_image=((size_image_phy/arc_kpc)/0.55)*2
    radius_cat = (size_image*0.5*0.55)/3600.
    print (Fore.BLUE + 'image size in pix: {:.1f}'.format(size_image))
    area_min=(((np.square(areagal)*np.pi)/arc_kpc**2)/0.55**2)
    print (Fore.BLUE +'Minimum detection area {:.1f} kcp^2 = {:.0f} pix'.format(areagal,
           area_min))

    out = conn.checkcoords(tab_gal['ra'][idg], tab_gal['dec'][idg])
    if np.char.startswith(out['field'], 'MC'):
        print (Fore.RED + "\n==================================================")
        print (Fore.RED +"\n\nThis galaxy is in the Magellanic Clouds Tiles, therefore")
        print (Fore.RED +"there is not a photometric catalog avaible for it, ")
        print (Fore.RED +"the photometric analysis is not possible")
        return

    if np.isnan(size_image):
        print (Fore.RED + "\n==================================================")
        print (Fore.RED +"\n\nThis galaxy has not radial from SIMBAD")
        print (Fore.RED +"the photometric analysis is not possible!")
        return

    print(Fore.RED +'\n\nLoading/Downloading the images and tables')
    print('---------------------------------------------')

    path = 'fits_images/{}_{}kpc.fz'.format(gal, size_image_phy)
    patht = 'fits_images/{}_{}_{}kpc.fz'.format(gal, band, size_image_phy)
    if os.path.exists(path) or os.path.exists(patht) and band=='R':
        print (f'\nThe image {path} already exist')
    if not os.path.exists(path) and  not os.path.exists(patht) and band=='R':
        print (f"\nDowloading {path} ...")
        conn.get_cut(tab_gal['ra'][idg], tab_gal['dec'][idg], int(size_image),
                     band, filepath=patht[0:-3])

    if  os.path.exists(patht):
        print (f'\nThe image {patht} already exist')

    if  not os.path.exists(patht) and  band!='R':
        print (f"\nDowloading {patht} ...")
        conn.get_cut(tab_gal['ra'][idg], tab_gal['dec'][idg], int(size_image),
                     band,
                   filepath=patht[0:-3])

    Field = out['field']
    #DR_array_all.append(out['dr'])
    print('#############################')
    print(Fore.BLUE +'\n\n Field: {}'.format(Field))
    print('#############################')

    path = f'tables/{gal}_fwhm.tab'
    patht = 'tables/{}_fwhm.tab'.format(gal[:-1])
    pathtt = 'tables/{}_fwhm.tab'.format(Field)
    if os.path.exists(path) or os.path.exists(patht) or os.path.exists(pathtt):
        #try:
        #     tab_fwhm = Table.read(path, format='ascii')
        #except:
        #    tab_fwhm = Table.read(patht, format='ascii')
        if os.path.exists(path):
            tab_fwhm = Table.read(path, format='ascii')
            print (f'\nThe table {path} already exist')
        if os.path.exists(patht):
            tab_fwhm = Table.read(patht, format='ascii')
            print (f'\nThe table {patht} already exist')
        if os.path.exists(pathtt):
            tab_fwhm = Table.read(pathtt, format='ascii')
            print (f'\nThe table {pathtt} already exist')
    else:
        query_txt1 = ("SELECT det.ID, det.RA, det.DEC, det.A, det.B, " +
                      "det.Theta, det.KRON_rADIUS, det.r_auto, det.CLASS_STAR," +
                      " det.FIELD, det.nDet_auto, det.FWHM,  det.FWHM_n," +
                      " claf.CLASS, claf.model_flag, claf.PROB_GAL," +
                      " claf.PROB_QSO, claf.PROB_STAR" +
                      "  FROM idr3.all_idr3 as det join " +
                      "idr3.vac_star_galaxy_quasar as claf on " +
                      "claf.ID = det.ID WHERE det.FIELD = '" +  str(Field) +   #tab0['Field'][0] +
                      "' and claf.PROB_STAR > 0.8 " +
                      "and det.r_auto >13 and det.r_auto<17 ")
        print ("\nDoing the following query ...\n", query_txt1)
        tab_fwhm=conn.query(query_txt1)

        #tab_fwhm.write(f'tables/{gal}_fwhm.tab', format='ascii')
        tab_fwhm.write(f'tables/{Field}_fwhm.tab', format='ascii')

    print(Fore.BLACK + '\n\nZP and mean PSF of the Field')
    print('--------------------------------')

    direcbase = os.path.dirname(os.path.realpath(__file__))
    ZP = Table.read(direcbase + '/zero_points.fits')
    id_zp = np.where(ZP['field']==tab_fwhm['Field'][0])[0][0]
    zp = ZP[band][id_zp]
    print ('\nid_zp_table:', id_zp, 'ZP={:.1f}'.format(zp),
           'Field:', out['field'])


    psf_g= np.round(np.nanmedian(tab_fwhm['FWHM']),1)
    print ('\nNumber of star 13<R_auto<17 : {}'.format(len(tab_fwhm['FWHM'])))
    print ('Median fwhm in the field : {:.1f}'.format(psf_g))

    sc_imag = 0.55
    gain=1
    median_sky_g = 0.0
    area=np.square(sc_imag)
    t=1

    path_a = tab_gal['gal'][idg]+'_{}_{}kpc.fz'.format(band, size_image_phy)
    if band=='R':
        try:
            imagn = fits.open('fits_images/' +
                    tab_gal['gal'][idg]+'_{}kpc.fz'.format(size_image_phy))
            print (Fore.RED+ '\nThe analysis is performed on {}'.format(
                   tab_gal['gal'][idg]+'_{}kpc.fz'.format(size_image_phy)))
        except:
            imagn = fits.open('fits_images/' + path_a)
            print (Fore.RED+ '\nThe analysis is performed on {}'.format(path_a))
    else:
        imagn = fits.open('fits_images/' + path_a)
        print (Fore.RED+ '\nThe analysis is performed on {}'.format(path_a))
    imag = imagn[1].data

    ###################
    # sky subtraction #
    ###################

    print(Fore.BLUE + '\n\nCalculating the image background')
    print('------------------------------------------')
    print ('Masking the sources over the image...')
    mask_g = make_source_mask(imag,  nsigma=nsigma, npixels=npixels,
                              dilate_size=dilate_size)
    fig=plt.figure(figsize=(6.5,6.5))
    plt.imshow(mask_g, origin='lower')
    plt.savefig('images/fig_'+gal+'_{}kpc_sky_mask.png'.format(size_image_phy),
                    bbox_inches='tight')
    if show_plot=='yes' and run_auto=='no':
        plt.show()
    else:
        plt.close()
    print("Saveving " + 'images/fig_' + gal +
          '_{}_{}kpc_sky_mask.png'.format(band, size_image_phy))

    mean_sky, median_sky, std_sky = sigma_clipped_stats(imag, sigma=11.0,
                                                              mask=mask_g)
    print(Fore.BLUE + '\n\nMedian Sky subtraction for the whole cutout')
    print('--------------------------------------------')
    print('mean_sky_:seg = {:.2f}'.format(mean_sky))
    print('median_sky_g = {:.2f}'.format(median_sky))
    print('std_sky_g = {:.2f}'.format(std_sky))


    print(('\n\nEstimating the 2D sky _background by using a sky box' +
            ' of {}x{} pixel').format(sky_box[0],sky_box[1]))
    print('-------------------------------------------------------------------')

    bkg_estimator = MedianBackground()
    bkg = Background2D(imag, sky_box, filter_size=(3, 3),
                       bkg_estimator=bkg_estimator, coverage_mask=mask_g,
                       fill_value=median_sky)

    imag = imag - bkg.background

    fig=plt.figure(figsize=(6.5,6.5))
    plt.imshow(bkg.background, origin='lower')
    plt.savefig('images/fig_'+gal+'_{}kpc_sky.png'.format(size_image_phy),
                    bbox_inches='tight')
    if show_plot=='yes' and run_auto=='no':
        plt.show()
    else:
        plt.close()
    print ("Saving " + 'images/fig_' + gal +
           '_{}_{}kpc_sky.png'.format(band, size_image_phy))

    pathgal = tab_gal['gal'][idg]+'_{}_{}kpc'.format(band, size_image_phy)
    fits.writeto('fits_images/' + pathgal + '_sky.fits', bkg.background, overwrite=True)
    fits.writeto('fits_images/' + pathgal + '_sky_sub.fits', imag, overwrite=True)
    print ("Saving " + 'fits_images/' + pathgal + '_sky.fits...')
    print ("Saving " + 'fits_images/' + pathgal + '_sky_sub.fits...\n')

    imagm = ima_fl2mag (imag, median_sky_g, area,t,zp)

    ########
    ## PSF #
    ########

    fac_sig=np.sqrt(np.log(2)*2)*2
    size = 20  # on each side from the center
    sigma_psf = psf_g/(fac_sig)
    y, x = np.mgrid[-size:size+1, -size:size+1]
    psfg = np.exp(-(x**2 + y**2)/(2.0*sigma_psf**2))
    psfg /= np.sum(psfg)
    #plt.imshow(psfg, origin='lower', cmap='gray')
    #fits.writeto('psfg.fits', psfg, overwrite=True)

    #####################
    ## Segmentation map #
    #####################

    if segmap is None:
        npixels_g = int(area_min) # minimum number of connected pixels
        threshold = photutils.detect_threshold(imag, nsigma=snr_g)
        segm = photutils.detect_sources(imag, threshold, npixels_g)

        if deblend=='on':
            print ("\nPerforming debleding:")
            print ("-----------------------")

            print ("Segmentation map without debleding")
            plt.figure(figsize=(6.5,6.5))
            plt.imshow(segm, origin='lower')
            if show_plot=='yes' and run_auto=='no':
                plt.show()
            else:
                plt.close()
            #sigma = psf_g * gaussian_fwhm_to_sigma
            #kernel = Gaussian2DKernel(sigma, x_size=3, y_size=3)
            #kernel.normalize()
            segm = deblend_sources(imag, segm, npixels=npixels_g,
                                    #kernel=kernel,
                                    nlevels=32, contrast=0.001)

        #######################################
        # Plotting the final segmentation map #
        #######################################

        print ("\nFinal Segmentation map:")
        print ("-------------------------")

        fig=plt.figure(figsize=(8,8))
        segmc = np.copy(segm.data).astype(float)
        segmc[segmc==0.0]=np.nan
        size_image_kpc = int(size_image)*0.5*0.55*arc_kpc

        imseg = plt.imshow(segmc, cmap='Paired', interpolation='nearest',
                           origin='lower')
                           #extent=np.array([-1,1,-1,1])*size_image_kpc)

        for i in np.arange(np.nanmax(segmc)):
           pos=np.where(segmc==(i+1))
           plt.text(pos[1][0], pos[0][0], str(int(i)), fontsize=30)

        cb = plt.colorbar(imseg)
        cb.ax.minorticks_on()
        plt.minorticks_on()
        saven = 'images/fig_'+tab_gal['gal'][idg]+'_{}_{}kpc_segm.png'.format(band,
                 size_image_phy)
        plt.savefig(saven, bbox_inches='tight')

        if show_plot=='yes' and run_auto=='no':
            plt.show()
        else:
            plt.close()
        print("Saving " + saven)
        segmap=np.copy(segm.data)
        pathseg = tab_gal['gal'][idg]+'_{}_{}kpc_segm.fits'.format(band,
                  size_image_phy)
        fits.writeto('fits_images/' + pathseg,  segm.data, overwrite=True)
        print('Saving '+'fits_images/' + pathseg)
    else:
        segmap = fits.open(segmap)[0].data


    ###################
    # Masking sources #
    ###################

    segmap_mask = np.full(segmap.shape, False)
    if user_order is None:
        pass
    else:
        nareas = np.arange(0,int(np.nanmax(segmap)))
        mask_areas = np.setdiff1d(nareas, user_order)
        for i in mask_areas:
            segmap_mask[segmap==i+1]=True
            segmap[segmap==i+1] = 0
        fits.writeto('fits_images/' + pathgal + '_mask.fits',
                     segmap_mask.astype(int), overwrite=True)


    print(Fore.RED + '\n\nRunning Statmorph')
    print('---------------------')

    start = time.time()
    source_morphs = statmorph.source_morphology(imag,
                            segmap, mask=segmap_mask, gain=gain, psf=psfg,
                            eta=eta,
                            petro_extent_cas=petro_extent_cas)
    print('Time: %g s.' % (time.time() - start))

    listl=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']

    print('\n\nResults')
    print('-----------\n')

    w =  wcs.WCS(imagn[1].header)
    if gal[0:2]=='AM' and gal[-1].isalpha():
        gal = gal[:-1]

    if user_order is None:
        sorta=np.argsort(segm.areas)
        if user_claf is None:
            user_claf = np.zeros((len(sorta)))
        if user_istage is None:
            user_istage = np.zeros((len(sorta)))
        for i, gali in enumerate(sorta[::-1]):

           morph = source_morphs[gali]
           plot_stat(morph, gal+listl[i], imag, imagm, median_sky_g, area,t, zp,
                         psfg,psf_g, sc_imag, arc_kpc, size_image_phy,
                         morpht = user_claf[i], istage = user_istage[i],
                         outputfile=outputfile, show_plot=show_plot,
                         petro_extent_cas=petro_extent_cas)

           data = ascii.read(outputfile)

           ind=np.where(data['GAL']==gal+listl[i])[0][0]
           indgal =np.where(tab_gal['gal']==gal)[0][0]

           coord_gal = w.all_pix2world(data['Ser_xc'][ind],
                                     data['Ser_yc'][ind], 0)
           data['ra'][ind] = coord_gal[0]
           data['dec'][ind] = coord_gal[1]
           #data['ra'][ind] = tab_gal['ra'][indgal]
           #data['dec'][ind] = tab_gal['dec'][indgal]
           data['radvel'][ind] = tab_gal['vel'][indgal]
           try:
               data['z'][ind] = tab_gal['z'][indgal]
           except:
               data['z'][ind] = tab_gal['vel'][indgal]/c_speed
           try:
               data['Jclass'][ind] = tab_gal['Jclass'][indgal]
           except:
               print ("")
           ascii.write(data, outputfile, overwrite=True)
    else:
       if user_claf is None:
           user_claf = np.zeros((len(user_order)))
       if user_istage is None:
           user_istage = np.zeros((len(user_order)))
       sorta=np.argsort(user_order)
       for i, gali in enumerate(sorta):
           morph = source_morphs[gali]
           plot_stat(morph, gal + user_list[i], imag, imagm, median_sky_g, area,
                     t, zp, psfg,psf_g, sc_imag, arc_kpc, size_image_phy,
                     morpht = user_claf[i], istage = user_istage[i],
                     outputfile=outputfile, show_plot=show_plot,
                     petro_extent_cas = petro_extent_cas)

           data = ascii.read(outputfile)

           ind=np.where(data['GAL']==gal + user_list[i])[0][0]
           indgal =np.where(tab_gal['gal']==gal)[0][0]
           coord_gal = w.all_pix2world(data['Ser_xc'][ind],
                                       data['Ser_yc'][ind], 0)
           data['ra'][ind] = coord_gal[0]
           data['dec'][ind] = coord_gal[1]
           #data['ra'][ind] = tab_gal['ra'][indgal]
           #data['dec'][ind] = tab_gal['dec'][indgal]
           data['radvel'][ind] = tab_gal['vel'][indgal]
           try:
               data['z'][ind] = tab_gal['z'][indgal]
           except:
               data['z'][ind] = tab_gal['vel'][indgal]/c_speed
           try:
               data['Jclass'][ind] = tab_gal['Jclass'][indgal]
           except:
               print ("")
           ascii.write(data, outputfile, overwrite=True)

    plt.show()
    nuser_list = []
    for i in user_list:
        nuser_list.append(gal + i)
    print("""SL.plot_simbad('{}', tab_gal, conn, size_image_phy=100,
                          table=output,  user_order={},
                          user_text={}, xtpos=60, ytpos=10,
                          deltay=10, savefig='yes', itsconsider='yes',
                          Nmembers={})""".format(gal, user_order, nuser_list,
                          len(user_order)))

def plot_stat(morph, gal, imag, imagm, median_sky_g, area, t, zp, psfg, psf_g,
              sc_ima, arc_kpc, size_image_phy, morpht = 0, istage = 0,
              show_plot='yes', outputfile='properties.dat',
              petro_extent_cas=1.5):

    if os.path.exists(outputfile):
        data = ascii.read(outputfile)
    else:
        direcbase = os.path.dirname(os.path.realpath(__file__))
        datat = ascii.read(direcbase + '/properties.dat')
        print (Fore.RED + '\n*It was create the properties.dat to print the out parameters')

        unitst = [str, np.float64, np.float64, np.float64, np.float64, np.float64,
                 np.float64, np.float64, np.float64, np.float64, np.float64,
                 np.float64, np.float64, np.float64, np.float64, np.float64,
                 np.float64, np.float64, np.float64, np.float64, np.float64,
                 np.float64, np.float64, np.float64, np.float64, np.float64,
                 np.float64, np.float64, np.float64, np.float64, np.float64,
                 np.float64, np.float64, np.float64, np.float64, np.float64,
                 np.float64, np.float64, np.float64, np.float64, np.float64,
                 np.float64, np.float64, np.float64, np.float64, np.float64,
                 np.float64, np.float64, np.float64, np.float64, np.float64,
                 np.float64]
        data= Table( names=datat.colnames, dtype=unitst)
        data.add_row()
        data['GAL'] = data['GAL'].astype('U'+str(len(gal)))
        data['GAL'][0] = gal

    if any(data['GAL'] == gal):
        print (Fore.BLACK +'\nRow was updated')
        print (data['GAL'][data['GAL']==gal])
        ind=np.where(data['GAL']==gal)[0][0]

    else:
        print (Fore.BLACK +'\nRow was created for {}'.format(gal))
        data.add_row()
        ind = -1
        len_ar = np.array([len(s) for s in data['GAL']])
        if len(gal) > np.max(len_ar):
            print ('Change the string format of GAL column')
            #data['GAL'].asdtype = 'str'+str(len(gal))
            new_c = data['GAL'].astype('U'+str(len(gal)))
            data.replace_column('GAL', new_c)
        data['GAL'][ind] = gal

    print ('\nsky_mean_statmorph ={:.3f}'.format(morph.sky_mean))
    print ('sky_sigma_statmorph ={:.3f}'.format(morph.sky_sigma))
    print ('flag =', morph.flag)
    print ('flag_sersic =', morph.flag_sersic)
    print ('')

    data['r20'][ind] = morph.r20
    data['r80'][ind] = morph.r80
    data['Gini'][ind] = morph.gini
    data['M20'][ind] = morph.m20
    data['F(G_M20)'][ind] = morph.gini_m20_bulge
    data['S(G_M20)'][ind] = morph.gini_m20_merger
    data['S_N'][ind] = morph.sn_per_pixel
    data['C'][ind] = morph.concentration
    data['A'][ind] = morph.asymmetry
    data['S'][ind] = morph.smoothness

    data['r50'][ind] = morph.r50

    data['flux_c'][ind] = morph.flux_circ
    data['flux_e'][ind] = morph.flux_ellip
    data['rpetro_c'][ind] = morph.rpetro_circ
    data['rpetro_e'][ind] = morph.rpetro_ellip
    data['rhalf_c'][ind] =  morph.rhalf_circ
    data['rhalf_e'][ind] = morph.rhalf_ellip

    print (Fore.RED +'\n Petrosian Radius {:.1f}'.format(morph.rpetro_circ))

    data['M'][ind] = morph.multimode
    data['I'][ind] = morph.intensity
    data['D'][ind] = morph.deviation
    data['Ao'][ind] = morph.outer_asymmetry
    data['As'][ind] = morph.shape_asymmetry

    data['Ser_A'][ind] = morph.sersic_amplitude
    data['Ser_R'][ind] = morph.sersic_rhalf
    data['Ser_n'][ind] = morph.sersic_n
    data['Ser_xc'][ind] = morph.sersic_xc
    data['Ser_yc'][ind] = morph.sersic_yc
    data['Ser_ellip'][ind] = morph.sersic_ellip
    data['Ser_theta'][ind] = morph.sersic_theta
    data['flag_morph'][ind] = morph.flag
    data['flag_sersic'][ind] = morph.flag_sersic
    data['psf_R'][ind] = psf_g
    data['sizep'][ind] = size_image_phy

    data['sizep'][ind] = size_image_phy

    data['morph_type'][ind] = morpht

    try:
        data['istage'][ind] = istage
    except:
        pass
    data['petro_extent_cas'][ind] = petro_extent_cas

    ascii.write(data, outputfile, overwrite=True)

    ny, nx = imag.shape
    y, x = np.mgrid[0:ny, 0:nx]
    fitted_model = statmorph.ConvolvedSersic2D(
        amplitude=morph.sersic_amplitude,
        r_eff=morph.sersic_rhalf,
        n=morph.sersic_n,
        x_0=morph.sersic_xc,
        y_0=morph.sersic_yc,
        ellip=morph.sersic_ellip,
        theta=morph.sersic_theta)
    fitted_model.set_psf(psfg)
    image_modelg = fitted_model(x, y)

    fig = plt.figure(figsize=(15,5))

    from mpl_toolkits.axes_grid1 import ImageGrid
    grid = ImageGrid(fig, 111,                   # similar to subplot(111)
                          nrows_ncols = (1, 3),  # creates 2x2 grid of axes
                          axes_pad= 0.35,    #0.6,  # pad between axes in inch.
                          cbar_location="right",
                          cbar_mode= "single",    #"each",
                          cbar_size="5%",
                          cbar_pad=0.05,
                     )


    ax=grid[0]

    imag_c = np.copy(imagm)
    imag_c = imag_c[~np.isnan(imag_c)]

    imag_min = np.percentile(imag_c,1)
    imag_max = np.percentile(imag_c,90)


    pfunc.bar([imagm.shape[1]/2, imag.shape[0]/2], sc_ima, 5/arc_kpc, '5 kpc',
               parr='1', larrow=5, nx=1.0, ny=0.5,
               postxt=1.3, cbar='k-', ctex='k', linew=2, AX=ax, bartexs=20)

    pfunc.figure(imagm, cent=[0,0], delta=[0,0], limt=[imag_min,imag_max,0],
             cmap=colormap, scale=sc_ima, cbaropt=0, outima='none',
             nameaxis=['$\Delta\delta$ (arcsec)','$\Delta \\alpha$ (arcsec)'],
             AX=ax)

    ax1=grid[1]
    image_modelmg = ima_fl2mag(image_modelg, median_sky_g, area,t,zp)

    plt.setp(ax1.get_yticklabels(), visible=False)

    pfunc.bar([image_modelmg.shape[1]/2, image_modelmg.shape[0]/2], sc_ima,
               5/arc_kpc, '5 kpc', parr='1', larrow=5, nx=1.0, ny=0.5,
               postxt=1.3, cbar='k-', ctex='k', linew=2, AX=ax1, bartexs=20)

    pfunc.figure(image_modelmg, cent=[0,0], delta=[0,0],
                 limt=[imag_min,imag_max,0], cmap=colormap, scale=sc_ima,
                 outima='none',
              nameaxis=['$\Delta\delta$ (arcsec)','$\Delta \\alpha$ (arcsec)'],
              AX=ax1)



    ax2=grid[2]
    residualg = imag - image_modelg

    residualgm = ima_fl2mag(residualg, median_sky_g, area,t,zp)

    plt.setp(ax2.get_yticklabels(), visible=False)

    pfunc.bar([residualgm.shape[1]/2, residualgm.shape[0]/2], sc_ima, 5/arc_kpc,
               '5 kpc', parr='1', larrow=5, nx=1.0, ny=0.5,
               postxt=1.3, cbar='k-', ctex='k', linew=2, AX=ax2, bartexs=20)

    im= pfunc.figure(residualgm, cent=[0,0], delta=[0,0],
                     limt=[imag_min,imag_max,0],
                     cmap=colormap, scale=sc_ima, cbaropt=0,  outima='none',
             nameaxis=['$\Delta\delta$ (arcsec)','$\Delta \\alpha$ (arcsec)'],
             AX=ax2)

    cb=plt.colorbar(im, format='%.1f', label='$mag\,arcsec^{-2}$',
                    cax=grid.cbar_axes[0])
    cb.ax.invert_yaxis()

    plt.savefig('images/fig_'+gal+'_{}kpc_model.png'.format(size_image_phy),
                bbox_inches='tight')
    if show_plot != 'yes':
       plt.close()

    fig = make_figure(morph)
    plt.savefig('images/fig_' + gal + '_{}kpc_stat.png'.format(size_image_phy),
                bbox_inches='tight')
    if show_plot != 'yes':
        plt.close()


def ex_phot_mod (gal, tab_gal, conn, size_image_phy=50, snr_g = 2.0, areagal=2,
                 region='circle', server=None, limtvel=500, xtpos=10, ytpos=20,
                 deltay=10, miny = 20, sky_box=[100, 100], deblend='off', psf=1,
                 usesimbad='no', band='R', field_size_phy=100, nsigma=2,
                 npixels=5, dilate_size=11, eta=0.2, show_plot='yes', run_auto='no',
                 outputfile='properties.dat', petro_extent_cas=1.5, segmap=None):

    idg =np.where(tab_gal['gal']==gal)[0][0]
    D = tab_gal['vel'][idg]/H
    arc_kpc = np.tan(np.deg2rad(1./3600.))*D*1e3

    print (Fore.RED +"\nArp & Maodore Catalog:")
    print ("------------------------")
    direcbase = os.path.dirname(os.path.realpath(__file__))
    AM = Table.read(direcbase + '/Table_Arp_Madore_pairs_updated.txt',
                    format='ascii')
    print(AM['cat','cross_ID'][np.where(AM['gal']==gal)[0]])
    print(AM['desc','codes'][np.where(AM['gal']==gal)[0]])

    print (Fore.BLUE +"\nBasic information:")
    print (Fore.BLUE +"-------------------")

    print(Fore.BLUE +'Distance {:.1f} Mpc'.format(D))
    print(Fore.BLUE +'arc_kpc {:.4f}'.format(arc_kpc))
    size_image=((size_image_phy/arc_kpc)/0.55)*2

    radius_cat = (size_image*0.5*0.55)/3600.
    print (Fore.BLUE +'image size in pix: {:.1f}'.format(size_image))
    area_min=(((np.square(areagal)*np.pi)/arc_kpc**2)/0.55**2)
    print (Fore.BLUE +'Minimum detection area {:.1f} kcp^2 = {:.0f} pix'.format(areagal,
           area_min))

    out = conn.checkcoords(tab_gal['ra'][idg], tab_gal['dec'][idg])
    if np.char.startswith(out['field'], 'MC'):
        print (Fore.RED + "\n==================================================")
        print (Fore.RED +"\n\nThis galaxy is in the Magellanic Clouds Tiles, therefore")
        print (Fore.RED +"there is not a photometric catalog avaible for it, ")
        print (Fore.RED +"the photometric analysis is not possible!")
        return

    if np.isnan(size_image):
        print (Fore.RED + "\n==================================================")
        print (Fore.RED +"\n\nThis galaxy has not radial from SIMBAD")
        print (Fore.RED +"the photometric analysis is not possible!")
        return

    if field_size_phy==100:
        path = 'images_100k/' + tab_gal['gal'][idg] + '_100_kpc_radius.png'
        patht = 'images_100k/' + tab_gal['gal'][idg][:-1] + '_100_kpc_radius.png'
        if (os.path.exists(path)) or (os.path.exists(patht)):
            print (Fore.RED + "\n==================================================")
            print (Fore.RED +"\n\nThis galaxy has 100 kpc image avaible")
        else:
            print (Fore.RED + "\n==================================================")
            print (Fore.RED +"\n\nThis galaxy has not 100 kpc image avaible")
            print (Fore.RED +"the photometric analysis is not possible!")
            return

    if not os.path.exists('fits_images'):
        os.system('mkdir fits_images')
        print (Fore.RED+ '\nThe folder fits_images was created')

    if not os.path.exists('images'):
        os.system('mkdir images')
        print (Fore.RED+ '\nThe folder images was created')

    print ('')
    radsimbad = field_size_phy
    if  size_image_phy < radsimbad:
        radsimbad = 100
    else:
        radsimbad = size_image_phy

    print(Fore.BLACK +'')

    ##################################
    # Indentifying objects with simbad
    if run_auto=='no':
        outsimbad = cat_simbad (gal, tab_gal, size_image_phy=radsimbad, region=region,
                            limtvel=limtvel, server=server)

    print(Fore.BLACK +'\n\nLoading/Downloading the images')
    print('---------------------------------------------')

    # Dowloading fits image
    path = 'fits_images/{}_{}kpc.fz'.format(gal, size_image_phy)
    patht = 'fits_images/{}_{}_{}kpc.fz'.format(gal, band, size_image_phy)
    if os.path.exists(path) or os.path.exists(patht) and band=='R':
        print (f'\nThe image {path} already exist')
    if not os.path.exists(path) and  not os.path.exists(patht) and band=='R':
        print (f"\nDowloading {path} ...")
        conn.get_cut(tab_gal['ra'][idg], tab_gal['dec'][idg], int(size_image),
                     band, filepath=path[0:-3])

    if  os.path.exists(patht):
        print (f'\nThe image {patht} already exist')

    if  not os.path.exists(patht) and  band!='R':
        print (f"\nDowloading {patht} ...")
        conn.get_cut(tab_gal['ra'][idg], tab_gal['dec'][idg], int(size_image),
                     band,
                   filepath=patht[0:-3])

    # Dowloading PNG image
    path = 'images/fig_{}_{}kpc.png'.format(gal, size_image_phy)
    if not os.path.exists(path):
        print ('\nDownloading the png file:',tab_gal['ra'][idg],
               tab_gal['dec'][idg], int(size_image))
        if  int(size_image) < 1000:
            print ("\n############################")
            print ("Downloading RGB 12 band image")
            print ("############################")
            imac = conn.twelve_band_img(tab_gal['ra'][idg], tab_gal['dec'][idg],
                                    int(size_image))
            imac.save(path, "PNG")
        elif int(size_image) < 2000:
            print ("\n#############################################")
            print ("Downoading RGB 3 band image (image>1000 pix!)")
            print ("#############################################")
            imac = conn.get_img(tab_gal['ra'][idg], tab_gal['dec'][idg],
                                int(size_image),
                                R='I', G='R', B='G', stretch=3, Q=8)
            imac.save(path, "PNG")
        else:
            print ("\n#############################################")
            print ("Downoading RGB 3 band image (image>2000 pix!)")
            print ("#############################################")

            patht = 'fits_images/{}_{}kpc'.format(gal, size_image_phy)
            if not os.path.exists(patht + '_G.fz'):
                conn.get_cut(tab_gal['ra'][idg], tab_gal['dec'][idg],
                             int(size_image), 'G',filepath=patht+'_G')
            if not os.path.exists(patht + '_I.fz'):
                conn.get_cut(tab_gal['ra'][idg], tab_gal['dec'][idg],
                             int(size_image), 'I', filepath=patht+'_I')

            imagn = fits.open('fits_images/{}_{}kpc_G.fz'.format(gal,
                               size_image_phy))
            imag_G = imagn[1].data
            imagn = fits.open('fits_images/{}_{}kpc_G.fz'.format(gal,
                               size_image_phy))
            imag_I = imagn[1].data
            imagn = fits.open('fits_images/{}_{}kpc.fz'.format(gal,
                               size_image_phy))
            imag = imagn[1].data

            make_lupton_rgb(imag_I, imag, imag_G, stretch=0.5, Q=8,
                            filename=path)

    else:
        print (f'\nThe image {path} already exist')


    if run_auto=='no':
        plot_simbad(gal, tab_gal, conn, size_image_phy=radsimbad, table=outsimbad,
                add_object=False, xtpos=xtpos, ytpos=ytpos, deltay=deltay,
                miny = miny, print_arp='no', print_scale='no',
                usesimbad=usesimbad, band=band)

    readn = 'images/fig_{}_{}kpc.png'.format(gal, size_image_phy)
    ima50 = plt.imread(readn)
    if band == 'R':
        try:
            imagn = fits.open('fits_images/{}_{}kpc.fz'.format(gal, size_image_phy))
        except:
            imagn = fits.open('fits_images/{}_{}_{}kpc.fz'.format(gal, band, size_image_phy))
    if band != 'R':
            imagn = fits.open('fits_images/{}_{}_{}kpc.fz'.format(gal, band, size_image_phy))
    imag = imagn[1].data

    ####################
    # Sky_substraction #
    ####################

    print ('Masking the sources over the image...')
    print(Fore.BLUE + '\n\nCalculating the image background')
    print('------------------------------------------')
    print ('Masking the sources over the image...')
    mask_g = make_source_mask(imag,  nsigma=nsigma, npixels=npixels,
                              dilate_size=dilate_size)
    fig=plt.figure(figsize=(6.5,6.5))
    plt.imshow(mask_g, origin='lower')
    if show_plot=='yes':
        plt.show()
    else:
        plt.close()

    mean_sky, median_sky, std_sky = sigma_clipped_stats(imag, sigma=11.0,
                                                              mask=mask_g)
    print(Fore.BLUE + '\n\nMedian Sky subtraction for the whole cutout')
    print('------------------------------------------')
    print('mean_sky_:seg = {:.2f}'.format(mean_sky))
    print('median_sky_g = {:.2f}'.format(median_sky))
    print('std_sky_g = {:.2f}'.format(std_sky))



    print(('\n\nEstimating the 2D sky _background by using a sky box' +
            ' of {}x{} pixel').format(sky_box[0],sky_box[1]))
    print('------------------------------------------')

    if sky_box[0] >= imag.shape[1]*0.5:
        print (Fore.RED +"\n\nThe sky box is bigger for the image size!")
        print (Fore.RED +"Please introduce a smaller box than {} pix!".format(
               imag.shape[1]*0.5))
        return

    bkg_estimator = MedianBackground()
    bkg = Background2D(imag, sky_box, filter_size=(3, 3),
                       bkg_estimator=bkg_estimator, coverage_mask=mask_g,
                       fill_value=median_sky)

    imag-= bkg.background

    print ("Background map")
    fig=plt.figure(figsize=(6.5,6.5))
    plt.imshow(bkg.background, origin='lower')
    if show_plot=='yes':
        plt.show()
    else:
        plt.close()

    # Segmentation map
    sigma = psf * gaussian_fwhm_to_sigma
    kernel = Gaussian2DKernel(sigma, x_size=3, y_size=3)
    kernel.normalize()
    #segm = detect_sources(imag, threshold, npixels=5, kernel=kernel)

    npixels_g = int(area_min) # minimum number of connected pixels
    threshold = photutils.detect_threshold(imag, nsigma=snr_g)
    segm = photutils.detect_sources(imag, threshold, npixels_g)

    if deblend=='on':
        print ("\nPerforming debleding:")
        print ("-----------------------")

        print ("Segmentation map without debleding")
        fig=plt.figure(figsize=(6.5, 6.5))
        plt.imshow(segm, origin='lower')
        if show_plot=='yes':
            plt.show()
        else:
            plt.close()
        segm = deblend_sources(imag, segm, npixels=npixels_g,
                               #kernel=kernel,
                                nlevels=32, contrast=0.001)

    gal_main = np.argmax(segm.areas)
    print("\nArea in pixel of the detection objects: ")
    print(segm.areas)
    print("ID of the detection objects: ")
    print(np.arange(len(segm.areas)))

    pathseg = tab_gal['gal'][idg]+'_{}_{}kpc_segm.fits'.format(band,
              size_image_phy)
    fits.writeto('fits_images/' + pathseg, segm.data, overwrite=True)
    print('\nSaving ' + 'fits_images/' + pathseg)

    if segmap==None:
        segmap = 'fits_images/' + pathseg
    #kerner_size = 20
    #segmap_float = ndi.uniform_filter(np.float64(segm.data), size=kerner_size)
    #segm = segmap_float > 0.5



    #############################
    # Plotting Segmentation map #
    #############################

    fig=plt.figure(figsize=(8,8))
    segmc = np.copy(segm.data).astype(float)
    segmc[segmc==0.0]=np.nan
    size_image_kpc = int(size_image)*0.5*0.55*arc_kpc

    imseg = plt.imshow(segmc, cmap='Paired', interpolation='nearest',
                       origin='lower')
                       #extent=np.array([-1,1,-1,1])*size_image_kpc)

    for i in np.arange(np.nanmax(segmc)):
       pos=np.where(segmc==(i+1))
       plt.text(pos[1][0], pos[0][0], str(int(i)), fontsize=30)

    cb = plt.colorbar(imseg)
    cb.ax.minorticks_on()
    plt.minorticks_on()
    saven = 'images/fig_'+tab_gal['gal'][idg]+'_{}_{}kpc_segm.png'.format(band,
             size_image_phy)
    plt.savefig(saven, bbox_inches='tight')
    if show_plot=='yes':
        plt.show()
    else:
        plt.close()
    print("Saving " + saven)

    if show_plot=='yes':
        if usesimbad=='no':
            path = 'images_100k/' + tab_gal['gal'][idg] + '_100_kpc_radius.png'
        else:
            path = 'images/{}_simbad_{}kpc.png'.format(gal, radsimbad)
        if not os.path.exists(path):
            print ('\nThe image of 100 kpc is not available')
            fig=plt.figure(figsize=(17,8))
            plt.subplot(121)
            plt.imshow(segm, origin='lower', cmap='gray',
                       extent=np.array([-1,1,-1,1])*size_image_kpc)
            plt.xlabel('x (kpc)')
            plt.ylabel('y (kpc)')
            plt.minorticks_on()
            plt.subplot(122)
            plt.imshow(ima50, extent=np.array([-1,1,-1,1])*size_image_kpc)
            plt.grid()
            plt.xlabel('x (kpc)')
            plt.minorticks_on()
            plt.show()


        else:
            ima100=plt.imread(path)
            fig=plt.figure(figsize=(21,8))
            plt.subplot(131)
            plt.imshow(segm, origin='lower', cmap='gray',
                       extent=np.array([-1,1,-1,1])*size_image_kpc)
            plt.xlabel('x (kpc)')
            plt.ylabel('y (kpc)')
            plt.minorticks_on()
            plt.subplot(132)
            plt.imshow(ima50,extent=np.array([-1,1,-1,1])*size_image_kpc)
            plt.grid()
            plt.xlabel('x (kpc)')
            plt.minorticks_on()
            plt.subplot(133)
            if usesimbad=='no':
                size_image=((100/arc_kpc)/0.55)*2
                size_image_kpc = int(size_image)*0.5*0.55*arc_kpc
            else:
                size_image= 300
                pix_scima = ((radsimbad*2)/arc_kpc)/size_image
                size_image_kpc = int(size_image)*0.5*pix_scima*arc_kpc
            plt.imshow(ima100, extent=np.array([-1,1,-1,1])*size_image_kpc)
            plt.grid()
            plt.xlabel('x (kpc)')
            plt.minorticks_on()
            plt.show()

    if run_auto!='yes':
        part0 = f"\n\nSL.phot_mod('{gal}', tab_gal, conn, size_image_phy={size_image_phy}, "
        part1 = f""" snr_g = {snr_g}, areagal={areagal},sky_box = {sky_box},\n deblend ="{deblend}", """
        part2 = f"""user_order=[1,2], user_list=["A","B"], band='{band}', segmap='{segmap}', """
        part3 = f"""petro_extent_cas='{petro_extent_cas}', eta='{eta}')"""
        print(part0 + part1 + part2 + part3)

        return outsimbad
    else:
        if segmap!=None:
            segmc = fits.open(segmap)[0].data
        maxarea = int(segmc[int(segmc.shape[0]*.5), int(segmc.shape[1]*.5)])-1

        part0 = f"\n\nSL.phot_mod('{gal}', tab_gal, conn, size_image_phy={size_image_phy}, "
        part1 = f""" snr_g = {snr_g}, areagal={areagal},sky_box = {sky_box},\n deblend ="{deblend}", """
        part2 = f"""user_order=[{maxarea}], user_list=[{band}], band='{band}', segmap='{segmap}', """
        part3 = f"""petro_extent_cas='{petro_extent_cas}', eta='{eta}', run_auto='yes')"""
        print(part0 + part1 + part2 + part3)

        phot_mod (gal, tab_gal, conn, size_image_phy=size_image_phy,
                  snr_g = snr_g, areagal=areagal,
                  user_order=[maxarea], user_list=[band], sky_box=sky_box,
                  deblend=deblend, band=band, nsigma=nsigma, npixels=npixels,
                  dilate_size=dilate_size, outputfile=outputfile, eta=eta,
                  show_plot=show_plot, petro_extent_cas=petro_extent_cas,
                  segmap=segmap, run_auto='yes')



def cat_simbad (GAL, tab_gal, size_image_phy=100, region='box', limtvel=500,
                server=None):

    idg =np.where(tab_gal['gal']==GAL)[0][0]
    velgal = tab_gal['vel'][idg]

    D = velgal/H

    kpc_arc = np.tan(np.deg2rad(1./3600))*D*1e3

    arcdist = size_image_phy/kpc_arc
    #arcdist=np.rad2deg(np.arctan((100*1e-3)/D))*3600

    if region == 'circle':
        fpart = 'region(circle, ICRS, {:+f} {:+f}, {:.0f}s)'.format(
                                                   tab_gal['ra'][idg],
                                                   tab_gal['dec'][idg], arcdist)
    if region == 'box':
        fpart = 'region(box, ICRS, {:+f} {:+f}, {:.0f}s {:.0f}s)'.format(
                                                   tab_gal['ra'][idg],
                                                   tab_gal['dec'][idg],
                                                   arcdist*2, arcdist*2)
    if limtvel==-1:
        spart=''
    else:
        spart =' & radvel  < {} & radvel > {}'.format(velgal+limtvel,
                                                     velgal-limtvel)
    allcrit = fpart + spart + ' & otype = Galaxy'

    print ("Simbad query ")
    print ("============\n")
    print (allcrit)

    if server is not None:
        simbad.Simbad.SIMBAD_URL = server + 'simbad/sim-script'
        print("Changing Simbad server to ", simbad.Simbad.SIMBAD_URL)
    result = simbad.Simbad.query_criteria(allcrit)

    print ("\nOutput")
    print ("======\n")
    print (result)

    return result

def simbad_download(GAL, tab_gal, size_image_phy=100,  width = 300,
                     height = 300):

    idg =np.where(tab_gal['gal']==GAL)[0][0]
    velgal = tab_gal['vel'][idg]

    D = velgal/H
    kpc_arc = np.tan(np.deg2rad(1./3600))*D*1e3

    arcdist = (size_image_phy*2)/kpc_arc
    fov = arcdist/3600.

    ra  = tab_gal['ra'][idg]
    dec = tab_gal['dec'][idg]

    basic_url = 'http://alasky.u-strasbg.fr/hips-image-services/hips2fits?'
    object_url1 = 'hips={}&width={}&height={}&fov={}'.format(quote('DSS2/color'),
                                                           width, height, fov)
    object_url2 = '&projection=TAN&coordsys=icrs&ra={}&dec={}'.format(ra, dec)

    #print (basic_url + object_url1 + object_url2 + '&format=png')

    # Downloading color  image from Simbad
    urlretrieve(basic_url + object_url1 + object_url2 + '&format=png',
                'images/{}_simbad_{}kpc.png'.format(GAL, size_image_phy))

    ima_simbad = plt.imread('images/{}_simbad_{}kpc.png'.format(GAL,
                            size_image_phy))


    # Dowloading r band image from DSS2
    object_url1 = 'hips={}&width={}&height={}&fov={}'.format(quote('DSS2/red'),
                                                           width, height, fov)
    hdu = fits.open(basic_url + object_url1 + object_url2)
    hdu.writeto('fits_images/{}_simbad_{}kpc.fits'.format(GAL, size_image_phy))


def simbad_thumbnail(GAL, tab_gal, size_image_phy=100,  width = 300,
                     height = 300,  xtpos=10, ytpos=20, deltay=10, miny=20,
                     minx=20, labeltxt = 'off', limtvel=500, ned_plot='no'):


    idg =np.where(tab_gal['gal']==GAL)[0][0]
    velgal = tab_gal['vel'][idg]

    D = velgal/H
    kpc_arc = np.tan(np.deg2rad(1./3600))*D*1e3

    arcdist = (size_image_phy*2)/kpc_arc
    fov = arcdist/3600.

    ra  = tab_gal['ra'][idg]
    dec = tab_gal['dec'][idg]

    path = 'fits_images/{}_simbad_{}kpc.fits'.format(GAL, size_image_phy)
    if not os.path.exists(path):
        print (f"\nDowloading {path} ...")
        simbad_download(GAL, tab_gal, size_image_phy=size_image_phy,
                        width = width, height = height)
    else:
        print (Fore.RED + f"\nThis {path} file is already downloaded...")

    hdu = fits.open('fits_images/{}_simbad_{}kpc.fits'.format(GAL,
                    size_image_phy))
    ima_simbad = plt.imread('images/{}_simbad_{}kpc.png'.format(GAL,
                            size_image_phy))

    # Downloading  Simbad Table
    print (Fore.BLACK + "\n------------------------\n")
    table=cat_simbad(GAL, tab_gal, size_image_phy, region='circle',
                     limtvel=limtvel, server=None)
    table = table[table['RV_VALUE']>0]

    galcoord = SkyCoord(ra*u.deg, dec*u.deg)
    skyc=SkyCoord(table['RA_d'], table['DEC_d'])
    sep = galcoord.separation(skyc)

    sep_kpc = sep.arcsec*kpc_arc

    print('')
    print (Fore.BLUE + "\nProjected Distances")
    print ("------------------------")
    for i in np.arange(len(skyc)):

        txt = "Proyected distance "
        print (txt+"{} and ({}) {} ({} km/s) is = {:.1f}\\,kpc ({:.1f}$\\arcsec$)".format(
        GAL, i, table['MAIN_ID'][i], table['RV_VALUE'][i], sep_kpc[i],
        sep.arcsec[i]))



    if ned_plot == 'yes':
        plt.figure(figsize=(20,10))
        plt.subplot(121)
    else:
        plt.figure(figsize=(10,10))
        plt.subplot(111)
    plt.imshow(ima_simbad, extent=np.array([-1,1,-1,1])*size_image_phy)

    w = wcs.WCS(hdu[0].header)
    Xgc, Ygc = w.all_world2pix(table['RA_d'], table['DEC_d'], 0)

    scima =  (size_image_phy*2/width)

    Xgc = (Xgc - width*0.5)*scima
    Ygc = (Ygc - width*0.5)*scima

    ima = hdu[0].data

    cond = ( (Xgc>ima.shape[1]*scima*-0.5) & (Ygc>ima.shape[0]*scima*-0.5) &
              (Xgc<0.5*scima*ima.shape[1]) & (Ygc<0.5*scima*ima.shape[0]))

    plt.scatter(Xgc[cond], Ygc[cond], s=100, facecolors='none',
            edgecolors='g')

    ordem= np.argsort(Ygc)
    cond = cond[ordem]

    if labeltxt == 'on':
        for i, indg in enumerate(ordem[cond]):
            textl = str(table['OTYPE'][indg]) + ' Vrad={:.0f} ({})'.format(
                    table['RV_VALUE'][indg], indg)

            xpos = Xgc[ordem][cond][i] + xtpos
            ypos = Ygc[ordem][cond][i] + ytpos

            if i==0:
                plt.text(xpos, ypos, textl, fontsize=12, color='w')

            else:
                yposb = Ygc[ordem][cond][i-1]
                xposb = Xgc[ordem][cond][i-1]
                if abs(ypos - yposb)<miny and abs(xpos - xposb) < minx:
                    ypos+=deltay
                if i>1:
                    yposbb = Ygc[ordem][cond][i-2]
                    xposbb = Xgc[ordem][cond][i-2]
                    if abs(ypos - yposbb)<miny*2 and abs(xpos - xposbb) < minx*2:
                        ypos+=deltay

                plt.text(xpos, ypos, textl, fontsize=12, color='w')

    if ned_plot == 'yes':
        # Dowloading NED TABLE
        table_ned = Ned.query_region(galcoord, radius=0.5*arcdist*u.arcsec)
        table_ned = table_ned[table_ned['Velocity']>0]

        ned_ra  = table_ned['RA']
        ned_dec = table_ned['DEC']

        Xgc_ned, Ygc_ned = w.all_world2pix(ned_ra, ned_dec, 0)

        Xgc_ned = (Xgc_ned - width*0.5)*scima
        Ygc_ned = (Ygc_ned - width*0.5)*scima

        cond_ned = ( (Xgc_ned>ima.shape[1]*scima*-0.5) &
                     (Ygc_ned>ima.shape[0]*scima*-0.5) &
                     (Xgc_ned<0.5*scima*ima.shape[1]) &
                     (Ygc_ned<0.5*scima*ima.shape[0]))

        plt.xlabel('x (kpc)')
        plt.ylabel('y (kpc)')
        plt.minorticks_on()
        plt.subplot(122)
        plt.imshow(ima_simbad, extent=np.array([-1,1,-1,1])*size_image_phy)
        plt.scatter(Xgc_ned[cond_ned], Ygc_ned[cond_ned],
                    s=100, marker='x', color='r')
        print('')
        print (Fore.RED +"\nNED Table (No rectriction in Vrad)")
        print ("====================================\n")
        print(table_ned['Object Name', 'RA', 'DEC', 'Type', 'Velocity',
                        'Redshift'])
        table_ned['RA'].unit='deg'
        table_ned['DEC'].unit='deg'
        skyc=SkyCoord(table_ned['RA'], table_ned['DEC'])

        sep = galcoord.separation(skyc)

        sep_kpc = sep.arcsec*kpc_arc

        print('')
        print (Fore.BLUE + "\nProjected Distances")
        print ("------------------------")
        for i in np.arange(len(skyc)):
            txt = "Proyected distance "
            print (txt+"{} and ({}) {} ({} km/s) is = {:.1f}\\,kpc ({:.1f}$\\arcsec$)".format(
            GAL, i, table_ned['Object Name'][i], table_ned['Velocity'][i],
            sep_kpc[i], sep.arcsec[i]))

    if labeltxt == 'on' and ned_plot == 'yes':
        ordem= np.argsort(Ygc_ned)
        cond_ned = cond_ned[ordem]
        for i, indg in enumerate(ordem[cond_ned]):
            textl = (str(table_ned['Type'][indg]) + ' Vrad={:.0f} ({})'.format(
                    table_ned['Velocity'][indg], indg))

            xpos = Xgc_ned[ordem][cond_ned][i] + xtpos
            ypos = Ygc_ned[ordem][cond_ned][i] + ytpos

            if i==0:
                plt.text(xpos, ypos, textl, fontsize=12, color='r')
            else:
                yposb = Ygc_ned[ordem][cond_ned][i-1]
                xposb = Xgc_ned[ordem][cond_ned][i-1]
                if abs(ypos - yposb)<miny and abs(xpos - xposb) < minx :
                    ypos+=deltay
                if i>1:
                    yposbb = Ygc_ned[ordem][cond_ned][i-2]
                    xposbb = Xgc_ned[ordem][cond_ned][i-2]
                    if abs(ypos - yposbb)<miny*2 and abs(xpos - xposbb) < minx*2:
                        ypos+=deltay

                plt.text(xpos, ypos, textl, fontsize=12, color='r')

    plt.xlabel('x (kpc)')
    plt.ylabel('y (kpc)')
    plt.minorticks_on()
    plt.savefig('images/{}_simbad_{}kpc_markers.png'.format(GAL, size_image_phy),
                bbox_inches='tight')


def plot_simbad(gal, tab_gal, conn, size_image_phy, table, user_order=None,
                user_text=None, xtpos=10, ytpos=20, deltay=10, miny=20, minx=20,
                savefig=None, add_object=True, itsconsider='no', itsgroup='off',
                Nmembers=0, print_arp='yes', print_scale='yes',
                usesimbad = 'no', band='R', outputfile='properties.dat'):

    idg =np.where(tab_gal['gal']==gal)[0][0]

    D = tab_gal['vel'][idg]/H
    arc_kpc = np.tan(np.deg2rad(1./3600.))*D*1e3
    if usesimbad == 'no':
        pix_scima = 0.55
    else:
        pix_scima =   ((size_image_phy*2)/arc_kpc)/300
        print ("Simbad scale pix/arcsec :", pix_scima)

    size_image=((size_image_phy/arc_kpc)/pix_scima)*2

    if print_scale=='yes':
        print(Fore.RED + "arc_kpc = {}".format(arc_kpc))

    if print_arp=='yes':
        print (Fore.BLUE + "\nArp & Maodore Catalog:")
        print ("------------------------")
        direcbase = os.path.dirname(os.path.realpath(__file__))
        AM = Table.read(direcbase + '/Table_Arp_Madore_pairs_updated.txt',
                        format='ascii')
        print(AM['cat','cross_ID'][np.where(AM['gal']==gal)[0]])
        print(AM['desc','codes'][np.where(AM['gal']==gal)[0]])

    if add_object:
        print(" ")
        data = ascii.read(outputfile)

        ind_inters = np.intersect1d(data['GAL'], user_text, return_indices=True)
        skyc=SkyCoord(data['ra'][ind_inters[1]]*u.deg,
                      data['dec'][ind_inters[1]]*u.deg)
        sep = skyc[0].separation(skyc[1::])
        #skyc=SkyCoord(table['RA_d'][user_order], table['DEC_d'][user_order])
        #sep = skyc[0].separation(skyc[1::])

        sep_kpc = sep.arcsec*arc_kpc

        for i in np.arange(len(skyc[1::])):
            txt = Fore.BLACK + "Proyected distance between "
            print (txt+"{} and {} is = {:.1f}\\,kpc ({:.1f}$\\arcsec$)".format(
            user_text[0], user_text[i+1], sep_kpc[i], sep.arcsec[i]))


        print("")
        for i, (comp_ind, comp) in enumerate(zip(user_order, user_text)):

            if len(data) == 0:
                data.add_row()


            if any(data['GAL'] == comp):
                print (Fore.RED +f"Row for {comp} was updated")
                #print (data['GAL'][data['GAL']==comp])
                ind=np.where(data['GAL']==comp)[0][0]

            else:
                print (Fore.RED +'Row was created for {}'.format(comp))
                data.add_row()
                ind = -1
                data['GAL'][ind] = comp

            #data['ra'][ind] = table['RA_d'][comp_ind]
            #data['dec'][ind] = table['DEC_d'][comp_ind]
            data['radvel'][ind] = table['RV_VALUE'][comp_ind]
            data['z'][ind] = table['Z_VALUE'][comp_ind]
            #data['morph_type'] = data['morph_type'].astype(str)
            #data['morph_type'][ind] = table['MORPH_TYPE'][comp_ind]
            if itsconsider=='yes':
                data['Its_considered?'][ind]=1
            if itsconsider=='no':
                data['Its_considered?'][ind]=0
            if len(user_order) >2:
                data['Its_group?'][ind]=1
            if itsgroup == 'yes':
                data['Its_group?'][ind]=1
            if itsgroup == 'no':
                data['Its_group?'][ind]=0
            if len(user_order) >1:
                if Nmembers == 0:
                    data['Nmembers'][ind]=len(user_order)
                else:
                    data['Nmembers'][ind]=Nmembers
            else:
                if Nmembers == 0:
                    data['Nmembers'][ind]=len(user_order)
                else:
                    data['Nmembers'][ind]=Nmembers
            if i>0:
                data['D_to_main'][ind] = sep_kpc[i-1]


        ascii.write(data, outputfile, overwrite=True)

    if usesimbad == 'no':

        # loading png image
        path="images/fig_{}_{}kpc.png".format(gal, size_image_phy)
        if size_image_phy ==100:
            path = 'images_100k/' + gal + '_100_kpc_radius.png'

        imapng = plt.imread(path)

        # loading fits image
        path = 'fits_images/{}_{}kpc.fz'.format(gal, size_image_phy)
        patht = 'fits_images/{}_{}_{}kpc.fz'.format(gal, band, size_image_phy)
        if os.path.exists(path) or os.path.exists(patht) and band=='R':
            print (Fore.BLACK +f'\nThe image {path} already exist')
            try:
                ima = fits.open(path)[1]
            except:
                ima = fits.open(patht)[1]
        if not os.path.exists(path) and  not os.path.exists(patht) and band=='R':
            print (Fore.BLACK +f"\nDowloading {path} ...")
            conn.get_cut(tab_gal['ra'][idg], tab_gal['dec'][idg], int(size_image),
                         band,
                       filepath=patht[0:-3])

        if  os.path.exists(patht):
            ima = fits.open(patht)[1]
            print (f'\nThe image {patht} already exist')

    else:
        path = 'fits_images/{}_simbad_{}kpc.fits'.format(gal, size_image_phy)
        if not os.path.exists(path):
            print (f"\nDowloading {path} ...")
            simbad_download(gal, tab_gal, size_image_phy=size_image_phy,
                            width = 300, height = 300)
        else:
            print (Fore.RED + f"\nThis {path} file is already downloaded...")

        ima = fits.open('fits_images/{}_simbad_{}kpc.fits'.format(gal,
                        size_image_phy))[0]
        imapng = plt.imread('images/{}_simbad_{}kpc.png'.format(gal,
                                size_image_phy))
        size_image = 300

    size_image=ima.shape[1]
    extent=np.array([1,-1,-1,1])*size_image*0.5*pix_scima

    plt.figure(figsize=(10,10))

    plt.imshow(imapng, extent=extent)
    pfunc.bar([0.5*size_image, 0.5*size_image], pix_scima,
              10/arc_kpc, '10 kpc', bartexs='12', parr='1', larrow=8.0, nx=1.0,
              ny=1.0, postxt=1.2, cbar='w-', ctex='w', linew=1, AX=None)


    w = wcs.WCS(ima.header)

    if table is None:
        return

    Xgc, Ygc = w.all_world2pix(table['RA_d'], table['DEC_d'], 0)

    Xgc = (Xgc*pix_scima - size_image*0.5*pix_scima)*-1
    Ygc = Ygc*pix_scima - size_image*0.5*pix_scima

    cond = ( (Xgc>ima.shape[1]*-0.5*pix_scima) & (Ygc>ima.shape[0]*-0.5*pix_scima) &
             (Xgc<0.5*pix_scima*ima.shape[1]) & (Ygc<0.5*pix_scima*ima.shape[0]))

    ordem= np.argsort(Ygc)


    if user_order is None:

        plt.scatter(Xgc[cond], Ygc[cond], s=100, facecolors='none',
                    edgecolors='g')

        for i, indg in enumerate(ordem[cond]):
            textl = table['OTYPE'][indg] + ' Vrad={:.0f} ({}) B={:.1f}'.format(
                    table['RV_VALUE'][indg], indg, table['FLUX_B'][indg])

            xpos = Xgc[ordem][cond][i] + xtpos
            ypos = Ygc[ordem][cond][i] + ytpos

            if i==0:
                plt.text(xpos, ypos, textl, fontsize=12, color='w')

            else:
                yposb = Ygc[ordem][cond][i-1]
                xposb = Xgc[ordem][cond][i-1]
                if abs(ypos - yposb)<miny and abs(xpos - xposb) < minx:
                    ypos+=deltay
                if i>1:
                    yposbb = Ygc[ordem][cond][i-2]
                    xposbb = Xgc[ordem][cond][i-2]
                    if abs(ypos - yposbb)<miny*2 and abs(xpos - xposbb) < minx*2:
                        ypos+=deltay

                plt.text(xpos, ypos, textl, fontsize=12, color='w')

        plt.minorticks_on()
        plt.ylabel('$\Delta\delta$ (arcsec)')
        plt.xlabel('$\Delta \\alpha$ (arcsec)')
        plt.show()

    else:
        ind_inters = np.intersect1d(data['GAL'], user_text, return_indices=True)
        Xgc, Ygc = w.all_world2pix(data['ra'][ind_inters[1]]*u.deg,
                                    data['dec'][ind_inters[1]]*u.deg, 0)

        Xgc = (Xgc*pix_scima - size_image*0.5*pix_scima)*-1
        Ygc = Ygc*pix_scima - size_image*0.5*pix_scima

        cond = ( (Xgc>ima.shape[1]*-0.5*pix_scima) & (Ygc>ima.shape[0]*-0.5*pix_scima) &
                 (Xgc<0.5*pix_scima*ima.shape[1]) & (Ygc<0.5*pix_scima*ima.shape[0]))

        #plt.scatter(Xgc[user_order], Ygc[user_order], s=100, facecolors='none',
        #            edgecolors='g')
        plt.scatter(Xgc, Ygc, s=100, facecolors='none',
                    edgecolors='g')

        for i, indg in enumerate(user_order):
            textl = user_text[i]

            #xpos = Xgc[indg] + xtpos
            #ypos = Ygc[indg] + ytpos
            xpos = Xgc[i] + xtpos
            ypos = Ygc[i] + ytpos

            if i==0:
                plt.text(xpos, ypos, textl, fontsize=12, color='w')
            else:
                #yposb = Ygc[user_order][i-1]
                yposb = Ygc[i-1]
                xposb = Xgc[i-1]

                if abs(ypos - yposb)<miny  and abs(xpos - xposb) < minx :
                    ypos+=deltay
                    print("sum deltay")
                if i>1:
                    #yposbb = Ygc[user_order][i-2]
                    yposbb = Ygc[i-2]
                    xposbb = Xgc[i-2]
                    if abs(ypos - yposbb)<miny*2 and abs(xpos - xposbb) < minx*2:
                        print("sum deltay2")
                        ypos+=deltay*2

                plt.text(xpos, ypos, textl, fontsize=12, color='w')

        plt.minorticks_on()
        plt.ylabel('$\Delta\delta$ (arcsec)')
        plt.xlabel('$\Delta \\alpha$ (arcsec)')
        if savefig is not None:
            print ("\nSaving figure in images/{}.png".format(gal))
            plt.savefig('images/{}.png'.format(gal), bbox_inches='tight')

        if usesimbad == 'yes':
            path = 'fits_images/{}_simbad_{}kpc.fits'.format(gal, size_image_phy)
        else:
            path = 'fits_images/{}_{}kpc.fz'.format(gal, size_image_phy)

        #################################################################
        # pritting info to add manually the coordinates

        ima_centX, ima_centY = w.all_world2pix(tab_gal['ra'][idg]*u.deg,
                                   tab_gal['dec'][idg]*u.deg, 0)

        print (Fore.GREEN + "\nIn case  to add manually the coordinates:")
        print ("--------------------------------------------------------")
        print ("\nfrom astropy.wcs import wcs")
        print ("ima = fits.open('{}')[1]".format(path))
        print ("w =  wcs.WCS(ima.header)")
        print ("coord_a = SkyCoord('{} {}', unit=u.deg)".format(
               data['ra'][ind_inters[1][0]], data['dec'][ind_inters[1][0]]))
        print ("coord_b = w.all_pix2world({} + delta_ra/{}*-1,".format(ima_centX,
                                                                    pix_scima))
        print ("                          {} + delta_dec/{}, 0)".format(ima_centY,
                                                                     pix_scima))
        print ("print (\"{:.7f} {:.7f}\".format(coord_b[0], coord_b[1]))")

        print ("\n")
        print ("tab_pro=Table.read('properties.dat', format='ascii')")
        print ("ind_g = np.where(tab_pro['GAL']=='{}B')[0][0]".format(gal))
        print ("print ('index of galaxy = ', ind_g)")
        print ("tab_pro['ra'][ind_g] = coord_b[0]")
        print ("tab_pro['dec'][ind_g] = coord_b[1]")
        print ("\n")
        print ("coord_b = SkyCoord(coord_b[0], coord_b[1], unit=u.deg)")
        print ("sep = coord_a.separation(coord_b)")
        print ("arc_kpc = {}".format(arc_kpc))
        print ("sep_kpc = sep.arcsec*arc_kpc")
        print ("print ('Separation between a Secondary and Primary" +
               " $\\sim$ {:.1f}\\,kpc ({:.1f}$\\\\arcsec$)'.format(sep_kpc, sep.arcsec))")
        print ("tab_pro['D_to_main'][ind_g] = sep_kpc")
        print ("tab_pro.write('properties.dat', format='ascii', overwrite=True)")

        #################################################################
        # pritting info to compute manually the distance between galaxies
        print (Fore.BLACK + "\nIn case  to compute manually the distance between galaxies:")
        print ("--------------------------------------------------------")
        print ("\nfrom astropy.wcs import wcs")
        for galid, i in enumerate(ind_inters[1][:]) :
            print ("coord_{} = SkyCoord('{} {}', unit=u.deg)".format(
                   galid, data['ra'][i], data['dec'][i]))

        print ("\nsep = coord_0.separation(coord_1)")
        print ("arc_kpc = {}".format(arc_kpc))
        print ("sep_kpc = sep.arcsec*arc_kpc")
        print ("print ('Separation between a Secondary and Primary" +
               " $\\sim$ {:.1f}\\,kpc ({:.1f}$\\\\arcsec$)'.format(sep_kpc, sep.arcsec))")

def ex_phot_mod_decals (gal, tab_gal, size_image_phy=50, snr_g = 2.0,
                        areagal=2, band='r', sky_box=[100, 100], deblend='off',
                        psf=1, run_auto='no', show_plot='yes',
                        nsigma=2, npixels=5, dilate_size=11,
                        outputfile='properties.dat', dr=8, petro_extent_cas=1.5,
                        segmap=None, eta=0.2):

    idg =np.where(tab_gal['gal']==gal)[0][0]
    D = tab_gal['vel'][idg]/H
    arc_kpc = np.tan(np.deg2rad(1./3600.))*D*1e3
    sc_ima = 0.27
    print (Fore.BLUE +"\nBasic information:")
    print (Fore.BLUE +"-------------------")
    print(Fore.RED +'Jclass {} '.format(tab_gal['Jclass'][idg]))
    print(Fore.BLUE +'Distance {:.1f} Mpc'.format(D))
    print(Fore.BLUE +'arc_kpc {:.4f}'.format(arc_kpc))
    size_image=((size_image_phy/arc_kpc)/sc_ima)*2

    radius_cat = (size_image*0.5*0.55)/3600.
    print (Fore.BLUE +'image size in pix: {:.1f}'.format(size_image))
    area_min=(((np.square(areagal)*np.pi)/arc_kpc**2)/0.55**2)
    print (Fore.BLUE +'Minimum detection area {:.1f} kcp^2 = {:.0f} pix'.format(areagal,
           area_min))

    if not os.path.exists('fits_images'):
        os.system('mkdir fits_images')
        print (Fore.RED+ '\nThe folder fits_images was created')

    if not os.path.exists('images'):
        os.system('mkdir images')
        print (Fore.RED+ '\nThe folder images was created')

    print(Fore.BLACK +'\n\nLoading/Downloading the images and tables')
    print('---------------------------------------------')

    home = 'https://www.legacysurvey.org/viewer/fits-cutout?'
    path = 'fits_images/{}_{}_{}kpc.fits'.format(gal, band, size_image_phy)
    if not os.path.exists(path):
        print (f"\nDowloading {path} ...")
        part0 = 'ra={}&dec={}&layer={}&pixscale=0.27&bands={}&size={}'.format(
             tab_gal['ra'][idg], tab_gal['dec'][idg],  dr_dic[dr], band,
                     int(size_image))
        targ = home + part0
        print (targ)
        #wget.download(targ, out=path)
        request.urlretrieve(targ, path)

    else:
        print (f'\nThe image {path} already exist')

    home = 'https://www.legacysurvey.org/viewer/jpeg-cutout?'
    path = 'images/fig_{}_{}kpc.jpeg'.format(gal, size_image_phy)
    if not os.path.exists(path):
        print ('\nDownloading the jpeg file..')
        part0 = 'ra={}&dec={}&layer={}&pixscale=0.27&bands=grz&size={}'.format(
             tab_gal['ra'][idg], tab_gal['dec'][idg], dr_dic[dr],
                     int(size_image))
        targ = home + part0
        print (targ)
        #wget.download(targ, out=path)
        request.urlretrieve(targ, path)

    else:
        print (f'\nThe image {path} already exist')

    #########
    # stamp #
    #########

    readn = 'images/fig_{}_{}kpc.jpeg'.format(gal, size_image_phy)
    ima50 = plt.imread(readn)
    imagn = fits.open('fits_images/{}_{}_{}kpc.fits'.format(gal, band,
                      size_image_phy))
    imag = imagn[0].data

    size_image_kpc = int(size_image)*0.5*0.55*arc_kpc
    fig=plt.figure(figsize=(6.5,6.5))
    plt.imshow(ima50, extent=np.array([-1,1,-1,1])*size_image_kpc*0.5)
    plt.grid()
    plt.xlabel('x (kpc)')
    plt.ylabel('y (kpc)')
    plt.minorticks_on()

    if show_plot=='yes':
        plt.show()
    else:
        plt.close()

    ####################
    # Sky_substraction #
    ####################

    print ('Masking the sources over the image...')
    print(Fore.BLUE + '\n\nCalculating the image background')
    print('------------------------------------------')
    print ('Masking the sources over the image...')
    mask_g = make_source_mask(imag, nsigma=nsigma, npixels=npixels,
                              dilate_size=dilate_size)
    fig=plt.figure(figsize=(6.5,6.5))
    plt.imshow(mask_g, origin='lower')
    if show_plot=='yes':
        plt.show()
    else:
        plt.close()
    mean_sky, median_sky, std_sky = sigma_clipped_stats(imag, sigma=11.0,
                                                              mask=mask_g)
    print(Fore.BLUE + '\n\nMedian Sky subtraction for the whole cutout')
    print('------------------------------------------')
    print('mean_sky_:seg = {:.2f}'.format(mean_sky))
    print('median_sky_g = {:.2f}'.format(median_sky))
    print('std_sky_g = {:.2f}'.format(std_sky))

    print(('\n\nEstimating the 2D sky _background by using a sky box' +
            ' of {}x{} pixel').format(sky_box[0],sky_box[1]))
    print('------------------------------------------')


    bkg_estimator = MedianBackground()
    bkg = Background2D(imag, sky_box, filter_size=(3, 3),
                       bkg_estimator=bkg_estimator, coverage_mask=mask_g,
                       fill_value=median_sky)

    imag-= bkg.background

    print ("Background map")
    fig=plt.figure(figsize=(6.5,6.5))
    plt.imshow(bkg.background, origin='lower')
    if show_plot=='yes':
        plt.show()
    else:
        plt.close()

    ####################
    # Segmentation map #
    ####################

    #sigma = psf * gaussian_fwhm_to_sigma
    #kernel = Gaussian2DKernel(sigma, x_size=3, y_size=3)
    #kernel.normalize()
    #segm = detect_sources(imag, threshold, npixels=5, kernel=kernel)

    npixels_g = int(area_min) # minimum number of connected pixels
    threshold = photutils.detect_threshold(imag, nsigma=snr_g)
    segm = photutils.detect_sources(imag, threshold, npixels_g)

    if deblend=='on':
        print ("\nPerforming debleding:")
        print ("-----------------------")


        fig=plt.figure(figsize=(6.5, 6.5))
        plt.imshow(segm, origin='lower')
        segm = deblend_sources(imag, segm, npixels=npixels_g,
                               #kernel=kernel,
                                nlevels=32, contrast=0.001)
        if show_plot=='yes':
            print ("Segmentation map without debleding")
            plt.show()
            print ("Segmentation after debleding")
        else:
            plt.close()

    gal_main = np.argmax(segm.areas)
    print("\nArea in pixel of the detection objects: ")
    print(segm.areas)
    print("\nID of the detection objects: ")
    print(np.arange(len(segm.areas)))

    pathseg = tab_gal['gal'][idg]+'_{}_{}kpc_segm.fits'.format(band,
              size_image_phy)
    fits.writeto('fits_images/' + pathseg,  segm.data, overwrite=True)
    print('Saving '+'fits_images/' + pathseg)

    if segmap==None:
        segmap = 'fits_images/' + pathseg

    #kerner_size = 20
    #segmap_float = ndi.uniform_filter(np.float64(segm.data), size=kerner_size)
    #segm = segmap_float > 0.5

    segmc = np.copy(segm.data).astype(float)
    segmc[segmc==0.0]=np.nan

    #############################
    # Plotting Segmentation map #
    #############################

    fig=plt.figure(figsize=(8,8))
    imseg = plt.imshow(segmc, cmap='Paired', interpolation='nearest',
                       origin='lower')

    for i in np.arange(np.nanmax(segmc)):
       pos=np.where(segmc==(i+1))
       plt.text(pos[1][0], pos[0][0], str(int(i)), fontsize=30)

    cb = plt.colorbar(imseg)
    cb.ax.minorticks_on()
    plt.minorticks_on()

    saven = 'images/fig_'+tab_gal['gal'][idg]+'_{}_{}kpc_segm.png'.format(
             band, size_image_phy)
    plt.savefig(saven, bbox_inches='tight')

    if show_plot=='yes':
        plt.show()
    else:
        plt.close()
    print ("Saving " + saven)

    if run_auto == 'no':

        part0 = f"\n\nSL.phot_mod_decals('{gal}', tab, size_image_phy={size_image_phy}, "
        part1 = f""" snr_g = {snr_g}, areagal={areagal}, band="{band}", """
        part2 = f"""sky_box = {sky_box},\n deblend ="{deblend}", """
        part3 = """user_order=[1,2], user_list=["A","B"], outputfile={outputfile}, """
        part4 = f"""segmap='{segmap}', petro_extent_cas={petro_extent_cas}, eta={eta})"""
        print(part0 + part1 + part2 + part3 + part4)
    else:
        if segmap!=None:
            segmc = fits.open(segmap)[0].data

        maxarea = int(segmc[int(segmc.shape[0]*.5), int(segmc.shape[1]*.5)])-1

        part0 = f"\n\nSL.phot_mod_decals('{gal}', tab, size_image_phy={size_image_phy}, "
        part1 = f""" snr_g = {snr_g}, areagal={areagal}, band="{band}", """
        part2 = f"""sky_box = {sky_box},\n deblend ="{deblend}", """
        part3 = f"""user_order=[{maxarea}], user_list=["{band}"], outputfile={outputfile}, """
        part4 = f"""segmap='{segmap}', petro_extent_cas={petro_extent_cas}, eta={eta}, run_auto='yes')"""
        print(part0 + part1 + part2 + part3 + part4)

        phot_mod_decals(gal, tab_gal, size_image_phy=size_image_phy, snr_g = snr_g,
                           areagal=areagal, band=band, sky_box = sky_box,
                           deblend =deblend, user_order=[maxarea], user_list=[band],
                           show_plot=show_plot, outputfile=outputfile,
                           petro_extent_cas=petro_extent_cas, eta=eta,
                           segmap=segmap, run_auto='yes')


def phot_mod_decals (gal, tab_gal, size_image_phy=50, snr_g = 2.0, areagal=2,
                     band = 'r',
                     user_order=None, user_list=None, sky_box=[100, 100],
                     deblend='off', show_plot='yes',nsigma=2, npixels=5,
                     dilate_size=11, outputfile='properties.dat', eta=0.2,
                     petro_extent_cas=1.5, segmap=None, run_auto='no'):

    idg =np.where(tab_gal['gal']==gal)[0][0]
    D = tab_gal['vel'][idg]/H
    arc_kpc = np.tan(np.deg2rad(1./3600.))*D*1e3
    print (Fore.BLUE +"\nBasic information:")
    print (Fore.BLUE +"-------------------")
    print(Fore.RED +'Jclass {} '.format(tab_gal['Jclass'][idg]))
    print(Fore.BLUE +'arc_kpc {:.4f}'.format(arc_kpc))
    size_image=((size_image_phy/arc_kpc)/0.55)*2
    radius_cat = (size_image*0.5*0.55)/3600.
    print (Fore.BLUE + 'image size in pix: {:.1f}'.format(size_image))
    area_min=(((np.square(areagal)*np.pi)/arc_kpc**2)/0.55**2)
    textt = 'Minimum detection area {:.1f} kcp^2 = {:.0f} pix'.format(areagal,
           area_min)
    print (Fore.BLUE + textt)

    print(Fore.BLACK + '\n\nZP and mean PSF of the Field')
    print('--------------------------------')

    zp = 22.5
    psf_g= tab_gal['psfsize_'+band][idg]

    print ('\nZP:{:.1f}'.format(zp))
    print ('Median fwhm in the field : {:.1f}'.format(psf_g))

    sc_imag = 0.27
    gain=1
    median_sky_g = 0.0
    area=np.square(sc_imag)
    t=1

    #####################
    # Loading the image #
    #####################

    patht = 'fits_images/' + tab_gal['gal'][idg]+'_{}_{}kpc.fits'.format(
            band, size_image_phy)
    imagn = fits.open(patht)
    imag = imagn[0].data

    ###################
    # sky subtraction #
    ###################

    print(Fore.BLUE + '\n\nCalculating the image background')
    print('------------------------------------------')
    print ('Masking the sources over the image...')
    mask_g = make_source_mask(imag, nsigma=nsigma, npixels=npixels,
                              dilate_size=dilate_size)
    fig=plt.figure(figsize=(6.5,6.5))
    plt.imshow(mask_g, origin='lower')
    plt.savefig('images/fig_'+gal+'_{}_{}kpc_sky_mask.png'.format(band,
                 size_image_phy), bbox_inches='tight')
    if show_plot=='yes' and run_auto=='no':
        plt.show()
    else:
        plt.close()
    print ("Saving " + 'images/fig_'+gal+'_{}_{}kpc_sky_mask.png'.format(band,
                 size_image_phy))

    mean_sky, median_sky, std_sky = sigma_clipped_stats(imag, sigma=11.0,
                                                              mask=mask_g)
    print(Fore.BLUE + '\n\nMedian Sky subtraction for the whole cutout')
    print('--------------------------------------------')
    print('mean_sky_:seg = {:.2f}'.format(mean_sky))
    print('median_sky_g = {:.2f}'.format(median_sky))
    print('std_sky_g = {:.2f}'.format(std_sky))


    print(('\n\nEstimating the 2D sky _background by using a sky box' +
            ' of {}x{} pixel').format(sky_box[0],sky_box[1]))
    print('-------------------------------------------------------------------')

    bkg_estimator = MedianBackground()
    bkg = Background2D(imag, sky_box, filter_size=(3, 3),
                       bkg_estimator=bkg_estimator, coverage_mask=mask_g,
                       fill_value=median_sky)

    imag = imag - bkg.background

    fig=plt.figure(figsize=(6.5,6.5))
    plt.imshow(bkg.background, origin='lower')
    plt.savefig('images/fig_' + gal + '_{}_{}kpc_sky.png'.format(band,
                 size_image_phy), bbox_inches='tight')
    if show_plot=='yes' and run_auto=='no':
        plt.show()
    else:
        plt.close()
    print ("Saving " + 'images/fig_'+gal+'_{}_{}kpc_sky.png'.format(band,
                 size_image_phy))

    pathgal = tab_gal['gal'][idg]+'_{}_{}kpc'.format(band, size_image_phy)
    fits.writeto('fits_images/' + pathgal + '_sky.fits', bkg.background,
                 overwrite=True)
    fits.writeto('fits_images/' + pathgal + '_sky_sub.fits', imag,
                 overwrite=True)
    print ("Saving " + 'fits_images/' + pathgal + '_sky.fits...')
    print ("Saving " + 'fits_images/' + pathgal + '_sky_sub.fits...\n')


    imagm = ima_fl2mag (imag, median_sky_g, area,t,zp)

    ########
    ## PSF #
    ########

    fac_sig=np.sqrt(np.log(2)*2)*2
    size = 20  # on each side from the center
    sigma_psf = psf_g/(fac_sig)
    y, x = np.mgrid[-size:size+1, -size:size+1]
    psfg = np.exp(-(x**2 + y**2)/(2.0*sigma_psf**2))
    psfg /= np.sum(psfg)
    #plt.imshow(psfg, origin='lower', cmap='gray')
    #fits.writeto('psfg.fits', psfg, overwrite=True)

    if segmap is None:
        npixels_g = int(area_min) # minimum number of connected pixels
        threshold = photutils.detect_threshold(imag, nsigma=snr_g)
        segm = photutils.detect_sources(imag, threshold, npixels_g)

        if deblend=='on':
            print ("\nPerforming debleding:")
            print ("-----------------------")

            print ("Segmentation map without debleding")
            plt.figure(figsize=(6.5,6.5))
            plt.imshow(segm, origin='lower')
            if show_plot=='yes':
                plt.show()
            else:
                plt.close()
            #sigma = psf_g * gaussian_fwhm_to_sigma
            #kernel = Gaussian2DKernel(sigma, x_size=3, y_size=3)
            #kernel.normalize()
            segm = deblend_sources(imag, segm, npixels=npixels_g,
                                    #kernel=kernel,
                                    nlevels=32, contrast=0.001)

        print ("\nFinal Segmentation map:")
        print ("-------------------------")

        fig=plt.figure(figsize=(8,8))
        segmc = np.copy(segm.data).astype(float)
        segmc[segmc==0.0]=np.nan

        imseg = plt.imshow(segmc, cmap='Paired', interpolation='nearest',
                           origin='lower')
        for i in np.arange(np.nanmax(segmc)):
           pos=np.where(segmc==(i+1))
           plt.text(pos[1][0], pos[0][0], str(int(i)), fontsize=30)

        cb = plt.colorbar(imseg)
        cb.ax.minorticks_on()
        plt.minorticks_on()
        saven = 'images/fig_'+tab_gal['gal'][idg]+'_{}_{}kpc_segm.png'.format(
                 band, size_image_phy)
        plt.savefig(saven, bbox_inches='tight')
        if show_plot=='yes' and run_auto=='no':
            plt.show()
        else:
            plt.close()
        print ("Saving " + saven)
        segmap=np.copy(segm.data)
        pathseg = tab_gal['gal'][idg]+'_{}_{}kpc_segm.fits'.format(band,
                  size_image_phy)
        fits.writeto('fits_images/' + pathseg,  segm.data, overwrite=True)
        print('Saving '+'fits_images/' + pathseg)
    else:
        segmap = fits.open(segmap)[0].data

    print(Fore.RED + '\n\nRunning Statmorph')
    print('---------------------')

    ###################
    # Masking sources #
    ###################

    segmap_mask = np.full(segmap.shape, False)
    if user_order is None:
        pass
    else:
        nareas = np.arange(0,int(np.nanmax(segmap)))
        mask_areas = np.setdiff1d(nareas, user_order)
        for i in mask_areas:
            segmap_mask[segmap==i+1]=True
            segmap[segmap==i+1] = 0
        fits.writeto('fits_images/' + pathgal + '_mask.fits',
                     segmap_mask.astype(int), overwrite=True)

    #####################
    # Running Statmorph #
    #####################

    start = time.time()
    source_morphs = statmorph.source_morphology(imag,
                            segmap, mask =  segmap_mask,
                            gain=gain, psf=psfg, eta=eta,
                            petro_extent_cas=petro_extent_cas)
    print('Time: %g s.' % (time.time() - start))
    print (len(source_morphs))

    ####################
    # Plotting Results #
    ####################

    listl=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']

    print('\n\nResults')
    print('-----------\n')

    if user_order is None:
        sorta=np.argsort(segm.areas)
        for i, gali in enumerate(sorta[::-1]):

           morph = source_morphs[gali]
           plot_stat(morph, gal+listl[i], imag, imagm, median_sky_g, area,t, zp,
                         psfg,psf_g, sc_imag, arc_kpc, size_image_phy,
                         show_plot=show_plot, outputfile=outputfile,
                         petro_extent_cas=petro_extent_cas)

           data = ascii.read(outputfile)

           ind=np.where(data['GAL']==gal+listl[i])[0][0]
           indgal =np.where(tab_gal['gal']==gal)[0][0]

           data['ra'][ind] = tab_gal['ra'][indgal]
           data['dec'][ind] = tab_gal['dec'][indgal]
           data['radvel'][ind] = tab_gal['vel'][indgal]
           data['z'][ind] = tab_gal['z'][indgal]
           data['Jclass'][ind] = tab_gal['Jclass'][indgal]

           ascii.write(data, outputfile, overwrite=True)
    else:
       sorta=np.argsort(user_order)
       for i, gali in enumerate(sorta):
           morph = source_morphs[gali]
           plot_stat(morph, gal + user_list[i], imag, imagm, median_sky_g, area,
                     t, zp, psfg,psf_g, sc_imag, arc_kpc, size_image_phy,
                     show_plot=show_plot, outputfile=outputfile,
                     petro_extent_cas=petro_extent_cas)

           data = ascii.read(outputfile)

           ind=np.where(data['GAL']==gal + user_list[i])[0][0]
           indgal =np.where(tab_gal['gal']==gal)[0][0]

           data['ra'][ind] = tab_gal['ra'][indgal]
           data['dec'][ind] = tab_gal['dec'][indgal]
           data['radvel'][ind] = tab_gal['vel'][indgal]
           data['z'][ind] = tab_gal['z'][indgal]
           data['Jclass'][ind] = tab_gal['Jclass'][indgal]

           ascii.write(data, outputfile, overwrite=True)

    plt.show()

def mass_decals(gal, tab_gal, size_image_phy, outputfile='properties.dat',
                suf_num=-1, show_plot='yes', dr=8):

    import functions as func

    idg =np.where(tab_gal['gal']==gal[:suf_num])[0][0]
    D = tab_gal['vel'][idg]/H
    arc_kpc = np.tan(np.deg2rad(1./3600.))*D*1e3
    sc_ima=0.27
    size_image=((size_image_phy/arc_kpc)/sc_ima)*2

    print(Fore.BLACK +'\n\nLoading/Downloading Decals images')
    print('---------------------------------------------')

    home = 'https://www.legacysurvey.org/viewer/fits-cutout?'
    path = 'fits_images/{}_{}_{}kpc.fits'.format(gal[:suf_num], 'g',
            size_image_phy)
    if not os.path.exists(path):
        print (f"\nDowloading {path} ...")
        part0 = 'ra={}&dec={}&layer={}&pixscale=0.27&bands=g&size={}'.format(
             tab_gal['ra'][idg], tab_gal['dec'][idg], dr_dic[dr],
                     int(size_image))
        targ = home + part0
        print (targ)

        #https://www.legacysurvey.org/viewer/fits-cutout?ra=153.445175&dec=-0.9142411&layer=ls-dr10-early-grz&pixscale=0.27&bands=g&size=420
        #wget.download(targ, out=path)
        request.urlretrieve(targ, path)
    else:
       print (f'\nThe image {path} already exist')

    path = 'fits_images/{}_{}_{}kpc.fits'.format(gal[:suf_num], 'r',
           size_image_phy)
    if not os.path.exists(path):
        print (f"\nDowloading {path} ...")
        part0 = 'ra={}&dec={}&layer={}&pixscale=0.27&bands=r&size={}'.format(
             tab_gal['ra'][idg], tab_gal['dec'][idg], dr_dic[dr],
                     int(size_image))
        targ = home + part0
        print (targ)
        #wget.download(targ, out=path)
        request.urlretrieve(targ, path)
    else:
        print (f'\nThe image {path} already exist')

    imagn = fits.open('fits_images/{}_{}_{}kpc.fits'.format(gal[:suf_num], 'g',
                      size_image_phy))
    imag = imagn[0].data

    imaxy = pfunc.callf('fits_images/{}_{}_{}kpc.fits'.format(gal[:suf_num],'g',
                      size_image_phy))[0]


    imarn = fits.open('fits_images/{}_{}_{}kpc.fits'.format(gal[:suf_num], 'r',
                      size_image_phy))
    imar = imarn[0].data

    data = ascii.read(outputfile)

    ind=np.where(data['GAL']==gal)[0][0]

    centx_phot = data['Ser_xc'][ind]
    centy_phot = data['Ser_yc'][ind]
    eps0 = data['Ser_ellip'][ind]
    theta = np.rad2deg(data['Ser_theta'][ind])
    smaellip = data['Ser_R'][ind]
    z_gal = data['z'][ind]

    gal_pol_1Reff = pfunc.ellipse(x0=centx_phot-0.5, y0=centy_phot-0.5,
                     sma=smaellip, eps=eps0, pa=theta+90,
                     step=int(func.peri_ellip_exact(smaellip,
                              smaellip*(1-eps0))*2))

    smaellip = smaellip*2
    gal_pol_2Reff = pfunc.ellipse(x0=centx_phot-0.5, y0=centy_phot-0.5,
                     sma=smaellip, eps=eps0, pa=theta+90,
                     step=int(func.peri_ellip_exact(smaellip,
                              smaellip*(1-eps0))*2))

    mask_gal1=pfunc.maskpoly(gal_pol_1Reff, imaxy, imag*np.nan)
    mask_gal2=pfunc.maskpoly(gal_pol_2Reff, imaxy, imag*np.nan)

    fig=plt.figure(figsize=(6.5,6.5))
    vmin = np.nanpercentile(imag,50)
    vmax = np.nanpercentile(imag,99.5)

    plt.imshow(imag, interpolation='nearest',cmap='RdYlBu_r',origin='lower',
    vmin=vmin, vmax=vmax)
    plt.plot(gal_pol_2Reff[:,0],gal_pol_2Reff[:,1], 'k--')
    plt.grid()
    plt.xlabel('x (pix)')
    plt.ylabel('y (pix)')
    plt.minorticks_on()
    plt.savefig('images/fig_{}_g_{}kpc_2Re.png'.format(gal[:suf_num], 'g',
                      size_image_phy), bbox_inches='tight')
    if show_plot == 'yes':
        plt.show()
    else:
        plt.close()

    fluxg = np.nansum(imag + mask_gal2)
    fluxr = np.nansum(imar + mask_gal2)

    zp = 22.5

    mag_g =-2.5*np.log10(fluxg)+22.5
    mag_r =-2.5*np.log10(fluxr)+22.5

    MLg = 10**(-0.499 + 1.519*(mag_g-mag_r))
    Mg = -5.0*np.log10(D*1e6) + 5.0 + mag_g
    Mr = -5.0*np.log10(D*1e6) + 5.0 + mag_r
    Lg = 10**((1.0/2.5)*(5.11-Mg))
    mass_stellar = Lg*MLg


    try:
        z_C = tab_gal['Z'][idg]
        D_gal = (c_speed*z_C)/H
        delta_D = abs(D-D_gal)*1000

        ra=np.array(tab_gal['RA'])
        if ra[idg]!=0.0:
            coord_gal = SkyCoord(tab_gal['ra'][idg], tab_gal['dec'][idg],
                                 unit=u.deg)
            coord_C = SkyCoord(tab_gal['RA'][idg], tab_gal['DEC'][idg],
                               unit=u.deg)
            sep = coord_gal.separation(coord_C)

            sep_kpc = sep.arcsec*arc_kpc
            D_int = np.sqrt(np.square(sep_kpc)+ np.square(delta_D))
        else:
            sep_kpc = np.nan
            D_int = np.nan
    except:
        pass

    data = ascii.read(outputfile)
    ind=np.where(data['GAL']==gal)[0][0]

    print (Fore.BLUE +"\nGeneral information:")
    print (Fore.BLUE +"-------------------")

    try:
        data['mass'][ind] = np.log10(mass_stellar)
        print(Fore.RED +'\nMass (log) = {:.1f}'.format(np.log10(mass_stellar)))
    except:
        print(Fore.BLACK +'The column <<mass>> was added to the {}'.format(
              outputfile))
        data.add_column(np.zeros((len(data)))*np.nan, name='mass')
        data['mass'][ind] = np.log10(mass_stellar)
        print(Fore.RED +'\nMass (log) = {:.1f}'.format(np.log10(mass_stellar)))
    try:
        data['mag_r_2Re'][ind] = mag_r
        print(Fore.RED +'mag_r_2Re = {:.1f}'.format(mag_r))
    except:
        print(Fore.BLACK +'The column <<mag_r_2Re>> was added to the {}'.format(
              outputfile))
        data.add_column(np.zeros((len(data)))*np.nan, name='mag_r_2Re')
        data['mag_r_2Re'][ind] = mag_r
        print(Fore.RED +'mag_r_2Re = {:.1f}'.format(mag_r))
    try:
        data['mag_g_2Re'][ind] = mag_g
        print(Fore.RED +'mag_g_2Re = {:.1f}'.format(mag_g))
    except:
        print(Fore.BLACK +'The column <<mag_g_2Re>> was added to the {}'.format(
              outputfile))
        data.add_column(np.zeros((len(data)))*np.nan, name='mag_g_2Re')
        data['mag_g_2Re'][ind] = mag_g
        print(Fore.RED +'mag_g_2Re = {:.1f}'.format(mag_g))
    try:
        data['Mr_2Re'][ind] = Mr
        print(Fore.RED +'Mr_2Re = {:.1f}'.format(Mr))
    except:
        print(Fore.BLACK +'The column <<Mr_2Re>> was added to the {}'.format(
              outputfile))
        data.add_column(np.zeros((len(data)))*np.nan, name='Mr_2Re')
        data['Mr_2Re'][ind] = Mr
        print(Fore.RED +'Mr_2Re = {:.1f}'.format(Mr))
    try:
        data['Mg_2Re'][ind] = Mg
        print(Fore.RED +'Mg_2Re = {:.1f}'.format(Mg))
    except:
        print(Fore.BLACK +'The column <<Mg_2Re>> was added to the {}'.format(
              outputfile))
        data.add_column(np.zeros((len(data)))*np.nan, name='Mg_2Re')
        data['Mg_2Re'][ind] = Mg
        print(Fore.RED +'Mg_2Re = {:.1f}'.format(Mg))
    try:
        data['sig_C'][ind] = tab_gal['sigma_C'][idg]
        print(Fore.BLUE +'\nLx (log) = {:.1f}'.format(tab_gal['Lx'][idg]))
    except:
        pass
    try:
        data['D_proj'][ind] = sep_kpc
        print(Fore.BLUE +'sigma = {:.1f} km/s'.format(tab_gal['sigma_C'][idg]))
    except:
        pass
    try:
        data['D_intr'][ind] = D_int
        print(Fore.BLUE +'D_proj = {:.1f} kpc'.format(sep_kpc))
    except:
        pass
    try:
        data['Lx'][ind] = tab_gal['Lx'][idg]
        print(Fore.BLUE +'D_intr = {:.1f} kpc'.format(D_int))
    except:
        pass

    ascii.write(data, outputfile, overwrite=True)
