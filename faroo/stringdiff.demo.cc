// Little demo program for StringDiff class that analyses the
// difference between two strings.
// Code by Ulrich Germann.
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
  if (argc != 3)
    {
      cerr << "usage: " << argv[0] << " <word1> <word2> " << endl;
      exit(1);
    }
  string a = argv[1];
  string b = argv[2];
  StringDiff diff(a,b);
  diff.showDiff(cout);
}
