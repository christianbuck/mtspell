#include "ug_faroo.h"
#include "ug_stringdist.h"
#include <iostream>
#include <boost/foreach.hpp>
#include <boost/program_options.hpp>

using namespace ugdiss;
using namespace std;
using namespace mtspell;
using namespace stringdist;

TokenIndex V;

void 
load_dictionary(string fname)
{
  V.setDynamic(true);
  ifstream in(fname.c_str());
  string w; int cnt;
  while (in>>cnt>>w) 
    if (isWord(UnicodeString(w.c_str()))) V[w];
  V.iniReverseIndex();
}

int main(int argc, char* argv[])
{
  load_dictionary(argv[1]);
  V.iniReverseIndex();
  Faroo F; F.init(V);
  string w; int cnt;
  while (cin>>cnt>>w)
    {
      if (!isWord(UnicodeString(w.c_str()))) continue;
      vector<id_type> cands; 
      F.lookup(w,cands);
      if (cands.size() == 0 || cands[0] == V[w])
	continue;
      cout << w << " :: " << V[cands[0]] << endl; 
      StringDiff diff;
      diff.set_a(string(V[cands[0]]));
      diff.set_b(w);
      diff.showDiff(cout);
      // BOOST_FOREACH(id_type k, cands)
      // 	{ 
      // 	  cout << w << " " << V[k] << endl;
      // 	}
      cout << endl;
    }
}
