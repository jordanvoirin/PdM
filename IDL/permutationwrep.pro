function permutationWrep, arr, permutations, data,  n, ix

optionsLength = n_elements(arr)

for i=0,optionsLength-1 do begin
  
  data[ix] = arr[i]
  
  if ix eq n-1 then begin
    permutations = [[permutations],[data]]
  endif else begin
    permutations = permutationWrep(arr,permutations,data,n,ix+1)
  endelse
   
endfor

return, permutations
end
