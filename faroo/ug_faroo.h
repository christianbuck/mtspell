// -*- c++ -*-
// implementation of the faroo algorithm for word-level spelling correction;
// see here: http://blog.faroo.com/2012/06/07/improved-edit-distance-based-spelling-correction/
// Code by Ulrich Germann.

#ifndef ug_faroo_h
#define ug_faroo_h

#include <boost/unordered_map.hpp>
#include <boost/dynamic_bitset.hpp>
#include <boost/iostreams/device/mapped_file.hpp>

#include <unicode/stringpiece.h>
#include <unicode/utypes.h>
#include <unicode/unistr.h>
#include <unicode/uchar.h>
#include <unicode/utf8.h>

#include "tpt_tokenindex.h"
#include "tpt_typedefs.h"
#include "ug_stringdist.h"
#include "cmph.h"

namespace mtspell
{
  using namespace std;
  using namespace icu;
  using namespace ugdiss;
  using namespace boost;
  namespace bio=boost::iostreams;
#ifndef bitvector
  typedef boost::dynamic_bitset<uint64_t> bitvector;
#endif

  bool isWord(UnicodeString const& w);

  // needed for use with boost::unordered_map
  struct unihasher
  {
    size_t operator()(icu::UnicodeString const& s) const;
  };

  class Faroo
  {
    typedef unordered_map<UnicodeString,vector<id_type>, unihasher> dict_t;
  
  public:
    void addWord(UnicodeString const w, id_type id, size_t d);
    void lookup(UnicodeString const & w, 
		vector<pair<id_type,float> > & dest, 
		bitvector & check, size_t d) const;
    class MPH
    {
      cmph_t * hash;
      FILE   * hashfile;
    public:
      MPH();
      ~MPH();
      void build(dict_t const& idmap, string fname);
      bool save(string fname);
      void open(string fname);
      int operator[](UnicodeString const& key) const;
    };

    class Ranker
    {
      uint32_t const* count;
    public:
      Ranker(uint32_t const* c);
      bool operator()(pair<uint32_t,float> const& a,
		      pair<uint32_t,float> const& b) const;
    };

  private:
    vector<uint32_t> wcount; // word counts
    dict_t             dict; // maps from faroo keys to candidate ids
    uint32_t const* index;
    uint32_t const* cands;
    uint32_t const* count;
    bio::mapped_file_source cntfile;
    bio::mapped_file_source idxfile;
    bio::mapped_file_source cndfile;
    MPH        H; /* minimal perfect hash that maps from faroo keys 
		   * to offsets in the array of candidate arrays */
    void save_vocab(string fname, vector<uint32_t> & idmap) const;
  public:
    typedef vector<pair<id_type,float> > candlist_t;
    TokenIndex V; // vocabulary
    
    Faroo();

    void load_from_text(string fname);
    void save(string bname);
    void open(string bname);

    size_t getCount(string const& w)  const;
    size_t getCount(id_type const id) const;

    void lookup(string const w, candlist_t & cands, bool const rank) const;
  };
}

#endif
