#include <string>
#include <sstream>
#include <iostream>
#include <vector>
#include <sys/types.h>
#include <signal.h>
#include <unistd.h>

int main (int argc, char *argv[] ){
	std::vector<std::string> vector;
  const char *programname = "/usr/local/bin/node";

  const char **nargv = new const char* [5];   // extra room for program name and sentinel
  nargv [0] = programname;         // by convention, argv[0] is program name
  nargv [1] = "/Users/sal.aguinaga/KynKon/Sandbox/EXPERIMENTAL-keylines/process-contraction-json.js";
  nargv [2] = "/Users/sal.aguinaga/cm_debug/5add7239c567723edc747c39.json";
  nargv [3] = "/tmp/data.json";
  nargv [4] = NULL;  // end of arguments sentinel is NULL

  pid_t pid = fork();
  if (pid == 0) /* child */ {
    //std::cout << execv(programname,(char **)nargv)  <<std::endl;
    if (execv(programname, (char **)nargv) == -1) {
      /* Handle error */
      std::cout << "!! an error in calling node\n";
    }
    _exit(1);  /* in case execve() fails */
  }
    
	return 0;
}
