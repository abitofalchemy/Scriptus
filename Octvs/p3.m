data = load('output3.txt');
avg_run_time = mean(data/1E6);

printf('Average running time for %d runs is: %.2f (us).\n',length(data(:,1)), mean(data)); 
printf('Average running time for each call as each run was looped %d is:%.4f (us).\n',
	   1E6,avg_run_time); 
printf('Standard Deviation: %.4f\n', std(data/1E6));


