function aberrationParallelPlateModel, nplate,e,phi

beta = phi*!pi/180.d
pup = 3.2e-3
f = 200e-3
N = f/pup

alpha1 = atan(pup/2/f)
alpha2 = atan(-pup/2/f)

up1 = beta+alpha1
up2 = beta+alpha2

OPDast1 = (nplate*nplate-1)*e*up1*up1/(2*nplate*nplate*nplate*N)
OPDast2 = (nplate*nplate-1)*e*up2*up2/(2*nplate*nplate*nplate*N)

OPDcoma1 = (nplate*nplate-1)*e*up1/(8*nplate*nplate*nplate*N*N)
OPDcoma2 = (nplate*nplate-1)*e*up2/(8*nplate*nplate*nplate*N*N)

return, [[OPDast1-OPDast2],[OPDcoma1-OPDcoma2]]

end

