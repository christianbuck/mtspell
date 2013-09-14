#include "ug_faroo.h"
#include <boost/foreach.hpp>
#include <iostream>
#include <fstream>
#include "VectorIndexSorter.h"

namespace mtspell
{
  
  using namespace std;
  using namespace icu;
  using namespace ugdiss;
  using namespace stringdist;
  using namespace Moses;
  namespace bio=boost::iostreams;
  Faroo::Ranker::Ranker(uint32_t const* c) : count(c) {}

  bool
  Faroo::
  Ranker::
  operator()(pair<uint32_t,float> const& a,
	     pair<uint32_t,float> const& b) const
  { 
    return (a.second != b.second ? (a.second < b.second)
	    : (count[a.first] > count[b.first]));
  }

  bool 
  isWord(UnicodeString const& w)
  {
    if (w.length() == 0) return false;
    if (!u_isalpha(w[0])) return false;
    for (int i = 1; i < w.length(); ++i)
      if (!u_islower(w[i])) return false;
    return true;
  }

  size_t 
  unihasher::
  operator()(icu::UnicodeString const& s) const
  {
    return s.hashCode();
  }

  Faroo::
  Faroo()
    : count(NULL)
  {
    V.setDynamic(true);
    V["NULL"];
    V["UNK"];
    wcount.reserve(1000000);
    wcount.push_back(0);
    wcount.push_back(0);
    count = &(wcount[0]);
  }
 
  void
  Faroo::
  addWord(UnicodeString const w, id_type id, size_t d)
  {
    // if (w.length() >= 2)
    dict[w].push_back(id);
    if (!d) return;
    addWord(UnicodeString(w, 1), id, d-1);
    for (int i = 1; i + 1 < w.length(); ++i)
       addWord(UnicodeString(w,0,i) + UnicodeString(w,i+1), id, d-1);
    addWord(UnicodeString(w, 0, w.length() - 1), id, d-1);
  }

  void
  Faroo::
  lookup(UnicodeString const & w, vector<pair<id_type, float> > & dest, 
	 bitvector & check, size_t d) const
  {
    assert(count);
    dict_t::const_iterator i = dict.find(w);
    if (i != dict.end())
      {
	BOOST_FOREACH(id_type id, i->second) 
	  {
	    if (!check[id]) 
	      { 
		check.set(id); 
		dest.push_back(pair<id_type, float>(id,count[id])); 
	      }
	  }
      }
    int id = H[w];
    if (id >= 0)
      {
	for (uint32_t i = index[id]; i < index[id+1]; ++i)
	  {
	    id_type id = cands[i];
	    if (!check[id])
	      {
		check.set(id);
		dest.push_back(pair<id_type,float>(id,count[id]));
	      }
	  }
      }
    if (!d) return;
    lookup(UnicodeString(w, 1), dest, check, d-1);
    for (int i = 1; i + 1 < w.length(); ++i)
      lookup(UnicodeString(w,0,i) + UnicodeString(w,i+1), dest, check, d-1);
    lookup(UnicodeString(w, 0, w.length() - 1), dest, check, d-1);
  }

  void 
  Faroo::
  lookup(string const w, vector<pair<id_type,float> > & cands, bool const rank) const
  {
    bitvector check(V.tsize());
    cands.clear();
    cands.reserve(100);
    lookup(UnicodeString::fromUTF8(StringPiece(w.c_str())), cands, check, 2);
    for (size_t c = 0; c < cands.size(); ++c)
      {
	StringDiff diff(string(V[cands[c].first]),w);
	if (rank)
	  {
	    float& score = cands[c].second = 0;
	    for (size_t d = 0; d < diff.size(); ++d)
	      score += diff[d].dist;
	  }
      }
    sort(cands.begin(),cands.end(),Ranker(count));
  }

  // void 
  // Faroo::
  // dump(ostream& out, TokenIndex const& V) const
  // {
  //   for (dict_t::const_iterator m = dict.begin(); m != dict.end(); ++m)
  //     {
  // 	string fambaloo;
  // 	m->first.toUTF8String(fambaloo);
  // 	out << fambaloo;
  // 	BOOST_FOREACH(id_type const i, m->second) 
  // 	  out << " " << i << ":" << V[i];
  // 	out << endl;
  //     }
  // }

  // id_type 
  // Faroo::
  // Vocab::
  // operator[](string const& w)
  // {
  //   map_t::value_type item(w,id.size());
  //   map_t::iterator m = id.emplace(item).first;
  //   if (id.size() > word.size()) 
  //     {
  // 	word.push_back(w);
  // 	count.push_back(0);
  //     }
  //   return m->second;
  // }

  // string const&
  // Faroo::
  // Vocab::
  // operator[](uint32_t const wid) const
  // {
  //   return word.at(wid);
  // }

  // Faroo::
  // Vocab::
  // Vocab()
  // {
  //   id["NULL"] = 0;
  //   id["UNK"]  = 1;
  //   word.reserve(1000000);
  //   word.push_back("NULL");
  //   word.push_back("UNK");
  //   count.reserve(1000000);
  //   count.push_back(0);
  //   count.push_back(0);
  // }

  // uint32_t
  // Faroo::
  // Vocab::
  // size() const
  // {
  //   return id.size();
  // }
  
  // uint32_t
  // Faroo::
  // Vocab::
  // addCount(string const& w, uint32_t const c)
  // {
  //   uint32_t wid = (*this)[w];
  //   return (this->count[wid] += c);
  // }

  // uint32_t
  // Faroo::
  // Vocab::
  // addCount(id_type const wid, uint32_t const c)
  // {
  //   return (this->count.at(wid) += c);
  // }

  // uint32_t
  // Faroo::
  // Vocab::
  // getCount(id_type const wid) const
  // {
  //   if (wid >= this->count.size()) return 0;
  //   return this->count[wid];
  // }

  // uint32_t
  // Faroo::
  // Vocab::
  // getCount(string const& w) const
  // {
  //   map_t::const_iterator m = id.find(w);
  //   if (m == id.end()) return 0;
  //   return this->count[m->second];
  // }

  void 
  Faroo::
  load_from_text(string fname)
  {
    ifstream in(fname.c_str());
    string w; int cnt;
    int ctr=0;
    while (in>>w>>cnt)
      {
	if (++ctr %  1000 == 0) cerr << ".";
	if (  ctr % 50000 == 0) cerr << endl;
	if (true || (cnt > 25 && isWord(UnicodeString(w.c_str()))))
	  {
	    id_type id = V[w];
	    if (id_type(wcount.size()) <= id)
	      {
		while (id_type(wcount.size()) <= id) 
		  wcount.push_back(0);
		count = &(wcount[0]);
	      }
	    wcount[id] = cnt;
	  }
      }
    cerr << endl;
    cerr << "LOADED DICTIONARY. CREATING INDEX." << endl;
    for (uint32_t i = 0; i < this->V.tsize(); ++i)
      {
	this->addWord(UnicodeString::fromUTF8(StringPiece(this->V[i])),i,2);
	if (i && i %  1000 == 0) cerr << ".";
	if (i && i % 50000 == 0) cerr << endl;
      }
    cerr << "\nDONE." << endl;
  }

  void
  Faroo::
  MPH::
  build(Faroo::dict_t const& dict, string fname)
  {
    cerr << "BUILDING MINIMAL PERFECT HASH" << endl;
    assert(!hash);
    vector<string> key(dict.size());
    size_t i = 0;
    for (dict_t::const_iterator m = dict.begin(); m != dict.end(); ++m)
      m->first.toUTF8String(key[i++]);
    vector<char*> keystring(key.size());
    for (size_t i = 0; i < key.size(); ++i)
      keystring[i] = const_cast<char*>(key[i].c_str());

    hashfile = fopen(fname.c_str(),"w");
    cmph_io_adapter_t *source = cmph_io_vector_adapter(&(keystring[0]), key.size());
    cmph_config_t     *config = cmph_config_new(source);
    cmph_config_set_algo(config, CMPH_BDZ);
    cmph_config_set_mphf_fd(config, hashfile);
    hash = cmph_new(config);
    cmph_config_destroy(config);
    cerr << "SAVING" << endl;
    cmph_dump(hash, hashfile);
    cmph_destroy(hash);
    fclose(hashfile);
    cmph_io_vector_adapter_destroy(source);
    hash = NULL;
    open(fname);
    cerr << "DONE" << endl;
  }

  Faroo::
  MPH::
  MPH()
    : hash(NULL) 
  {}
  
  Faroo::
  MPH::
  ~MPH() 
  {
    if (hash) 
      {
	cmph_destroy(hash);
	fclose(hashfile);
      }
  }

  bool
  Faroo::
  MPH::
  save(string fname)
  {
    return true;
  }

  int
  Faroo::
  MPH::
  operator[](UnicodeString const& s) const
  {
    if (!hash) return -1; // hash not ready
    string key; s.toUTF8String(key);
    return cmph_search(hash, key.c_str(), cmph_uint32(key.size()));
  }
  void
  Faroo::
  MPH::
  open(string fname)
  {
    if (hash) 
      {
	cmph_destroy(hash);
	fclose(hashfile);
      }
    hashfile = fopen(fname.c_str(), "r");
    hash = cmph_load(hashfile); 
  }

  void
  Faroo::
  save(string bname)
  {
#if 0
    for (dict_t::const_iterator m = dict.begin(); m != dict.end(); ++m)
      {
	string w; m->first.toUTF8String(w);
	cout << w << endl;
      }
    return;
#endif
    // save the vocabulary
    H.build(dict,bname + ".mph");

#if 0
    for (dict_t::const_iterator m = dict.begin(); m != dict.end(); ++m)
      {
	string w; m->first.toUTF8String(w);
	cout << w << " " << H[m->first] << endl;
      }
#endif

    // H.save(bname + ".mph");
    // return;
    vector<uint32_t> idmap;
    this->save_vocab(bname + ".vcb",idmap);
    vector<vector<id_type> const*> cnd(dict.size());
    for (dict_t::const_iterator m = dict.begin(); m != dict.end(); ++m)
      {
	string w; m->first.toUTF8String(w);
	cnd.at(H[m->first]) = &(m->second);
      }
    ofstream mp((bname + ".map").c_str());
    ofstream idx((bname + ".idx").c_str());
    uint32_t ctr=0;
    for (size_t i = 0; i < cnd.size(); ++i)
      {
	idx.write(reinterpret_cast<char const*>(&ctr),sizeof(uint32_t));
	vector<id_type> const& c = *(cnd[i]);
	if (c.size())
	  {
	    BOOST_FOREACH(uint32_t const id, c)
	      mp.write(reinterpret_cast<char const*>(&(idmap[id])),
		       sizeof(id_type));
	    ctr += c.size();
	  }
      }
    idx.write(reinterpret_cast<char const*>(&ctr),sizeof(uint32_t));
    mp.close();
    idx.close();
    ofstream cnt((bname + ".cnt").c_str());
    assert(&(wcount[0]) == count);
    cnt.write(reinterpret_cast<char const*>(count),V.tsize() * sizeof(uint32_t));
    cnt.close();
    // dict.clear();
  }

  void
  Faroo::
  save_vocab(string fname,vector<uint32_t> & idmap) const
  {
    VectorIndexSorter<uint32_t,greater<uint32_t>,uint32_t> sorter(wcount);
    idmap.resize(wcount.size()); 
    for (size_t i = 0; i < idmap.size(); ++i) 
      idmap[i] = i;
    // sort(idmap.begin()+2, idmap.end(), sorter);
    vector<pair<string,id_type> > wlist(V.tsize());
    for (size_t i = 0; i < V.tsize(); ++i)
      {
	wlist[i].first  = V[i];
	wlist[i].second = idmap[i];
      }
    sort(wlist.begin(),wlist.end());
    write_tokenindex_to_disk(wlist,fname,string("UNK"));
  }
  
  size_t
  Faroo::
  getCount(string const& w) const
  {
    if (!count) return 0;
    id_type id = V[w];
    return count[id];
  }

  size_t
  Faroo::
  getCount(id_type const id) const
  {
    if (!count) return 0;
    return count[id];
  }

  void
  Faroo::
  open(string bname)
  {
    H.open(bname + ".mph");
    V.open(bname + ".vcb"); V.iniReverseIndex();
    cntfile.open(bname + ".cnt");
    count = reinterpret_cast<uint32_t const*>(cntfile.data());
    idxfile.open(bname + ".idx");
    index = reinterpret_cast<uint32_t const*>(idxfile.data());
    cndfile.open(bname + ".map");
    cands = reinterpret_cast<uint32_t const*>(cndfile.data());
    wcount.clear();
  }
  

  

}
