function permutation_1, arr, n
  
  dim = size(arr,/Dimensions)
  
  if dim[0] eq n then begin
    return, arr
  endif
  
  tmparr = arr[0,*]
  tmparr = [[tmparr],[switcher(tmparr)]]
  arr = [[arr],[arr]]
  arr = [arr,tmparr]
  
  arr = permutation_1(arr,n)
  
  return, arr
end

