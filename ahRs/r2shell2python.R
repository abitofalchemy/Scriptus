#' ---
#' title:  "Call Shell From R, where Shell Calls Python"
#' author: "Sal Aguinaga"
#' date:   "28 Dec 2015"
#' ---
#' 

## invoke a system command 
scr_ret_val <- try (system("/Users/saguinag/ToolSet/sandbox/tst.sh", ignore.stderr = FALSE))

scr_ret_val <- try (system("python /Users/saguinag/ToolSet/sandbox/test.py", ignore.stderr = FALSE))
print (scr_ret_val)

print (src_ret_val)
