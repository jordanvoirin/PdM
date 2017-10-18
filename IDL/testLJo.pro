im1=readfits('C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\20171016113221_Ximea_-319.fits')
im2=readfits('C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\20171016105512_Ximea_0.fits')
im3=readfits('C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\PD\20171016111100_Ximea_319.fits')

lambda=0.6375d
pxs=5.3e-6/80e-3*!RADEG*3600.d
psfs = [[[im1]],[[im2]],[[im3]]]
res1=diversity(psfs,[-3.19,0,3.19],lambda,80d-3,pxs,1e-3,'modal',d1=3.2e-3,d2=0.d,jmax=231,/show)
res2=diversity([[[im1]],[[im2]]],[-3.19,0],lambda,80d-3,pxs,1e-3,'modal',d1=3.2e-3,d2=0.d,jmax=231,/show)
res3=diversity([[[im2]],[[im3]]],[0,3.19],lambda,80d-3,pxs,1e-3,'modal',d1=3.2e-3,d2=0.d,jmax=231,/show)

;zon1=diversity([[[im1]],[[im2]],[[im3]]],[-3.19,0,3.19],lambda,80d-3,pxs,1e-3,'zonal',d1=3.2e-3,d2=0.d,/show)
;zon2=diversity([[[im1]],[[im2]]],[-3.19,0],lambda,80d-3,pxs,1e-3,'zonal',d1=3.2e-3,d2=0.d,/show)
;zon3=diversity([[[im2]],[[im3]]],[0,3.19],lambda,80d-3,pxs,1e-3,'zonal',d1=3.2e-3,d2=0.d,/show)
end