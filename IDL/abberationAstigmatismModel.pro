function abberationAstigmatismModel, nplate,e,phi

beta = phi*!pi/180.d
pup = 3.2e-3
f = 200e-3
N = f/pup

alpha1 = atan(pup/2/f)
alpha2 = atan(-pup/2/f)

up1 = beta+alpha1
up2 = beta+alpha2

OPD1 = (nplate*nplate-1)*e*up1*up1/(2*nplate*nplate*nplate*N)
OPD2 = (nplate*nplate-1)*e*up2*up2/(2*nplate*nplate*nplate*N)

return, OPD1-OPD2

end

