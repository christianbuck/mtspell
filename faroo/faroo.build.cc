#include "ug_faroo.h"
#include "ug_stringdist.h"
#include <iostream>
#include <boost/foreach.hpp>
#include <boost/program_options.hpp>

using namespace ugdiss;
using namespace std;
using namespace mtspell;
using namespace stringdist;


int 
main(int argc, char* argv[])
{
  if (argc < 3) 
    {
      cerr << "usage: " << argv[0] << " <dictionary text file> <basename for output files>" << endl;
      cerr << "Output files are <basename>.{mph|cnt|vcb|map}" << endl;
    }
  Faroo F; 
  F.load_from_text(argv[1]);
  F.save(argv[2]);
  exit(0);
}
