data = load("output1.txt");
m_mean = mean(data);
zstar  = (1-0.95)/2 % 95 percent conf. interval
printf('95per Conf interval: (%.4f,%.4f)\n',avg - zstar * stddev/sqrt(10),avg + zstar * stddev/sqrt(10))
