
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import make_lupton_rgb
from astropy.table import Table
import astropy.wcs as wcs

import skimage.morphology as morph
import skimage.exposure as skie
from astropy.visualization import ZScaleInterval


#dir1 = '../../images/ACS/adrizzle/rot0/0.03/'
#dir2 = '../../images/ACS/B/adrizzle/0.03/'
dir1 = '/Users/isjang/data/Galaxies/NGC3370/images/ACS/adrizzle/0.04_square_rot0/'
dir2 = '/Users/isjang/data/Galaxies/NGC3370/images/ACS/B/adrizzle/0.04_square_rot0/'
imgg   = fits.getdata(dir2+'435_drc.fits',ext=1)
imgr   = fits.getdata(dir1+'555_drc.fits',ext=1)
imgi   = fits.getdata(dir1+'814_drc.fits',ext=1)

imgg   = imgg*1000. + 100
imgr   = imgr*1000. + 100
imgi   = imgi*1000. + 100

#imgg[np.isnan(imgg)] = 100
#imgr[np.isnan(imgr)] = 100
#imgi[np.isnan(imgi)] = 100


#print(imgi)
fits.writeto('temp.fits', imgi, overwrite=True)



con = 4

img = imgg
interval = ZScaleInterval()
val = interval.get_limits(img)
zmin = val[0]
zmax = val[1]*1.4*con
imgg = skie.exposure.rescale_intensity(img, in_range=(99.5-1.5, zmax))


img = imgr
interval = ZScaleInterval()
val = interval.get_limits(img)
zmin = val[0]
zmax = val[1]*1.8*con
imgr = skie.exposure.rescale_intensity(img, in_range=(99.5-1.5, zmax))


img = imgi
interval = ZScaleInterval()
val = interval.get_limits(img)
zmin = val[0]
zmax = val[1]*2.6*con
imgi = skie.exposure.rescale_intensity(img, in_range=(99.5-1.5, zmax))


imgg[np.isnan(imgg)] = 2
imgr[np.isnan(imgr)] = 2
imgi[np.isnan(imgi)] = 2

#img_all = make_lupton_rgb(imgi, imgr, imgg, stretch=0, Q=5)
#img_all = make_lupton_rgb(imgi, imgr, imgg, stretch=0.03, Q=7)
img_all = make_lupton_rgb(imgi, imgr, imgg, stretch=0.03, Q=7)






# Color image
fig = plt.figure(figsize=(10./2.54, (10.)/2.54))
ax = fig.add_axes([0.01, 0.01, 0.98, 0.98])

ax.imshow(img_all, origin='lower')
ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

#ax.patch.set_alpha(0.0) # transparent axes
#ax.set_xlim(0, 1, auto=False)
#ax.set_ylim(0, 1, auto=False)
ax.spines['top'   ].set_color('white')
ax.spines['bottom'].set_color('white')
ax.spines['left'  ].set_color('white')
ax.spines['right' ].set_color('white')


#ax.text(0.03,  0.91, 'NGC 3370', fontsize=18, transform=ax.transAxes, color='k')
#ax.text(0.82,  0.15, 'F814W', fontsize=12, ransform=ax.transAxes, color='r')
#ax.text(0.82,  0.10, 'F555W', fontsize=12, transform=ax.transAxes, color='green')
#ax.text(0.82,  0.05, 'F435W', fontsize=12, transform=ax.transAxes, color='b')




# Circle
rota = np.arange(361.) + 90
dum  = (rota > 360)
rota[dum] = rota[dum] - 360
cx   = 3523
cy   = 2392
rad  = 2 # arcmin
rad  = rad*60./0.05
xx   = 0.556*rad*np.cos(rota*np.pi/180)
yy   = 1.000*rad*np.sin(rota*np.pi/180)
rota = 146.5
xrot = cx + xx*np.cos(rota*np.pi/180.) - yy*np.sin(rota*np.pi/180.)
yrot = cy + xx*np.sin(rota*np.pi/180.) + yy*np.cos(rota*np.pi/180.)
#ax.plot(xrot, yrot, c='w', linewidth=1, linestyle = '--', alpha=0.5)


rota = np.arange(361.) + 90
dum  = (rota > 360)
rota[dum] = rota[dum] - 360
rad  = 0.5 # arcmin
rad  = rad*60./0.05
xx   = 0.556*rad*np.cos(rota*np.pi/180)
yy   = 1.000*rad*np.sin(rota*np.pi/180)
rota = 146.5
xrot = cx + xx*np.cos(rota*np.pi/180.) - yy*np.sin(rota*np.pi/180.)
yrot = cy + xx*np.sin(rota*np.pi/180.) + yy*np.cos(rota*np.pi/180.)
#ax.plot(xrot, yrot, c='w', linewidth=0.5, linestyle = '--')



#print(xx[dum])





'''
# Circle
rota = np.arange(361.) + 90
dum  = (rota > 360)
rota[dum] = rota[dum] - 360
cx   = 4844.3
cy   = 4121.2 
rad  = 10 # arcmin
rad  = rad*60./0.186
xx   = cx + rad*np.cos(rota*np.pi/180)
yy   = cy + rad*np.sin(rota*np.pi/180)
dum  = (yy < 6455)
#ax.plot(xx[dum], yy[dum], c='w', linewidth=0.5)
'''

'''
# Mosaic field
res = pd.read_csv('Edge.reg', header=None, skiprows=3, engine='python', sep='[(,]')
ra  = res[1]
dec = res[2]
#data, head = fits.getdata(dir+'g.fits', header=True, ext=0)
hdulist = fits.open(dir+'g.fits')
w1 = wcs.WCS(hdulist[0].header, hdulist)
hdulist.close()
xx, yy = w1.all_world2pix(ra, dec, 1)
xx = xx - 4100.
yy = yy - 8150
#ax.plot(xx, yy, c='w', linewidth=0.5, alpha=0.5) # mosaic field


# F5
res = pd.read_csv('F5.reg', header=None, skiprows=3, engine='python', sep='[(,]')
ra  = res[1] ; dec = res[2]
xx, yy = w1.all_world2pix(ra, dec, 1)
xx = xx - 4100.
yy = yy - 8150
ax.plot(xx, yy, c='w', linewidth=0.5, alpha=0.5) # mosaic field


# F7
res = pd.read_csv('F7.reg', header=None, skiprows=3, engine='python', sep='[(,]')
ra  = res[1] ; dec = res[2]
xx, yy = w1.all_world2pix(ra, dec, 1)
xx = xx - 4100.
yy = yy - 8150
ax.plot(xx, yy, c='w', linewidth=0.5, alpha=0.5) # mosaic field



# Field 2 in Tikhonov+14
ra  = [308.7639441, 308.7324365, 308.8447973, 308.8739740, 308.7639441]
dec = [60.1635623, 60.2175960, 60.2289959, 60.1729899, 60.1635623]
xx, yy = w1.all_world2pix(ra, dec, 1)
xx = xx - 4100.
yy = yy - 8150
ax.plot(xx, yy, c='w', linewidth=0.5, alpha=0.5)



# Field A in Anand+18
ra  = [308.92785, 308.98416, 308.90919, 308.85292, 308.92785]
dec = [60.121335, 60.085926, 60.060015, 60.096174, 60.121335]
xx, yy = w1.all_world2pix(ra, dec, 1)
xx = xx - 4100.
yy = yy - 8150
ax.plot(xx, yy, c='w', linewidth=0.5, alpha=0.5) 



# Field B in Anand+18
ra  = [308.79106, 308.86584, 308.92211, 308.84725, 308.79106]
dec = [60.043451, 60.068610, 60.033198, 60.007288, 60.043451]
xx, yy = w1.all_world2pix(ra, dec, 1)
xx = xx - 4100.
yy = yy - 8150
ax.plot(xx, yy, c='w', linewidth=0.5, alpha=0.5)


# NIR field
ra  = [308.8283984, 308.9062236, 308.9087965, 308.8328606, 308.8283984]
dec = [ 60.1505591,  60.1524297,  60.11806432, 60.11636139, 60.15055915]
xx, yy = w1.all_world2pix(ra, dec, 1)
xx = xx - 4100.
yy = yy - 8150
ax.plot(xx, yy, c='w', linewidth=0.5, alpha=0.5)

# NIR field
ra  = [308.8195428, 308.8898256, 308.9187235, 308.8500657, 308.8195428]
dec = [60.14232371, 60.15880723, 60.12785969, 60.11171022, 60.14232371]
xx, yy = w1.all_world2pix(ra, dec, 1)
xx = xx - 4100.
yy = yy - 8150
ax.plot(xx, yy, c='w', linewidth=0.5, alpha=0.5)



# plot arrow
#ax.plot([300, 3227+300], [500, 500], color = 'w')
ax.arrow( 400, 400,  3047, 0, color='gainsboro', head_width=60, linewidth=1)
ax.arrow(2000, 400, -1610, 0, color='gainsboro', head_width=60, linewidth=1)
ax.text(0.1,  0.08, "10', 20 kpc", fontsize=8, transform=ax.transAxes, color='white', alpha=0.9)
'''

'''
ax.text(0.03,  0.91, '$NGC\,6946$', fontsize=15, transform=ax.transAxes, color='white')
ax.text(0.27,  0.595, 'F1', fontsize=8, transform=ax.transAxes, color='white', alpha=0.9)
ax.text(0.72,  0.25, 'F2', fontsize=8, transform=ax.transAxes, color='white', alpha=0.9)
ax.text(0.31,  0.76, 'F3', fontsize=8, transform=ax.transAxes, color='white', alpha=0.9)
ax.text(0.24,  0.35, 'F4', fontsize=8, transform=ax.transAxes, color='white', alpha=0.9)
ax.text(0.295, 0.20, 'F5', fontsize=8, transform=ax.transAxes, color='white', alpha=0.9)





ax.text(0.75 , 0.11, 'CFHT/Megacam', fontsize=8, transform=ax.transAxes, color='white')
ax.text(0.89 , 0.06, '(      )', fontsize=8, transform=ax.transAxes, color='white')
ax.text(0.904, 0.06, 'g', fontsize=8, transform=ax.transAxes, color='dodgerblue')
ax.text(0.928 , 0.06, 'r', fontsize=8, transform=ax.transAxes, color='lime')
ax.text(0.947 , 0.06, 'i', fontsize=8, transform=ax.transAxes, color='r')
#ax.text(0.83 , 0.06, '(   ,   , and  )', fontsize=8, transform=ax.transAxes, color='white')
#ax.text(0.84 , 0.06, 'g', fontsize=8, transform=ax.transAxes, color='dodgerblue')
#ax.text(0.89 , 0.06, 'r', fontsize=8, transform=ax.transAxes, color='lime')
#ax.text(0.93 , 0.06, 'i', fontsize=8, transform=ax.transAxes, color='r')
'''




#fig.savefig(''+str(name)+'.pdf',dpi=1000, Transparent = True)
#plt.savefig(''+str(name)+'.png',dpi=1000, Transparent = True)
plt.savefig('fig1.png',dpi=1000)#, Transparent = True)
#plt.savefig(''+str(name)+'_small.jpg',dpi=200, Transparent = True)
