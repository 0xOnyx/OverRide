so the programe take two input and make some hash and compare with the value
is correct is spawn a new /bin/bash


the problem is thah check if the program have some already attach debug :
  if ( ptrace(PTRACE_TRACEME, 0, 1, 0) == -1 )


  so the solution is to make a break point juste before and jump to to the next instruction 

  but i prefer the aproch that juste code the function and look wat's is expect from the input


so i found for the string jerdos
i found the serial : 6232807

  and GET THE FLAG =>
  GbcPDRgsFK77LNnnuh7QyFYA2942Gp8yKj9KrWD8