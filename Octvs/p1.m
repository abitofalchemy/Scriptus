data = [ 3.00000;
 3.00000;
 3.00000;
 2.00000;
 3.00000;
 3.00000;
 2.00000;
 3.00000;
 3.00000;
 3.00000];

data_secs = data.*1e-6;
means = data_secs./1e6;
meanofmeans = mean(means);
s_dev = std (means);
z_alpha_by2 = 1.960;
marg_err = z_alpha_by2*(s_dev/sqrt(1e6));

printf('\n----------------------------\n');
printf('Mean: %g for each call.\n',means);
printf('Standard deviation: %g\n',s_dev);
printf('z_{alpha/2} : %.4f\n', z_alpha_by2);
printf('The margin of error:%g\n', marg_err);
printf('For 95 percent confidence level, the CI is: (%g,%g)\n', meanofmeans-marg_err, meanofmeans+marg_err)

B = 1e-15;
n = (z_alpha_by2 * s_dev/B)^2
