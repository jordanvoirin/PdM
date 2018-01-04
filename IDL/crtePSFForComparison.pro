;create PSF for comparison with python code
;
psf = zernike2psf([0],[4],400,1.5035377358490566037735849056604,0)
writefits,'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\devPD\psf4__1.fits',psf.psf
writefits,'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\devPD\psf4__1.fits',psf.phase,/APPEND
writefits,'C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\devPD\psf4__1.fits',psf.pup,/APPEND

end