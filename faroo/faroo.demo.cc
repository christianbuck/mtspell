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
  Faroo F; 
  // F.load_from_text(argv[1]);
  // F.save("en.faroo");
  // exit(0);
  F.open("en.faroo");
  cerr << "READY" << endl;
  string w; 
  while (cin>>w)
    {
      if (!isWord(UnicodeString(w.c_str()))) continue;
      vector<pair<id_type,float> > cands; 
      F.lookup(w,cands,true);
      if (cands.size() == 0) continue;
      cout << w << endl;
      // size_t mycnt = F.getCount(w);
      for(size_t i = 0; i < cands.size(); ++i)
	{
	  // if (i > 10 && F.getCount(cands[i].first) <= mycnt)
	  // continue;
	  cout << "   " 
	       << F.V[cands[i].first] << " " 
	       << cands[i].second << " " 
	       << F.getCount(cands[i].first) << endl;
	  // StringDiff(F.V[cands[i].first],w).showDiff(cout); cout << endl;
	}

      cout << endl;
    }			     
}
