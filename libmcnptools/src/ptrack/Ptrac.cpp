#include <cassert>
#include <string>
#include <sstream>

#include "mcnptools/Ptrac.hpp"

#include "mcnptools/StringOps.hpp"

namespace mcnptools {

const std::vector<std::string> Ptrac::m_lines = {"nps","src1","src2","bnk1","bnk2","sur1","sur2","col1","col2","ter1","ter2"};

Ptrac::Ptrac(const std::string& filename, const unsigned int format):
  m_filename( filename ),
  m_format( static_cast<Ptrac::PtracFormat>(format) ) {

  if( format == Ptrac::HDF5_PTRAC ) {
    m_handle = {};
    auto file_h5 = f5::File(m_filename, 'r');
    m_hdf5_parser = std::make_unique<Ptrac::HDF5Parser>( MakeHDF5PtrackParser(file_h5, "ptrack") );
  }
  else
  {
    if( format == Ptrac::BIN_PTRAC ) {
      m_handle.open(filename.c_str(), std::ifstream::binary);
      if (m_handle.fail()) {
        std::stringstream ss;
        ss << "Failed to open binary PTRAC file " << filename;
        throw McnpToolsException( ss.str() );
      }
    }
    else { //ASCII format 
      m_handle.open(filename.c_str());
      if (m_handle.fail()) {
        std::stringstream ss;
        ss << "Failed to open ASCII PTRAC file " << filename;
        throw McnpToolsException( ss.str() );
      }
    }
    ReadHeader();
  }
}

void Ptrac::ReadHeader() {
  if( m_format == Ptrac::BIN_PTRAC ) {
    int size1, size2;

    // determine file size
    m_handle.seekg(0,std::ios::end);
    int64_t fsize = m_handle.tellg();
    m_handle.seekg(0,std::ios::beg);

    // read the version
    m_handle.read( (char*) &size1, sizeof(int) );

    if( size1 >= fsize || size1 != sizeof(int) ) {
      std::stringstream ss;
      ss << "Failed to read binary PTRAC";
      throw McnpToolsException( ss.str() );
    }

    m_handle.read( (char*) &m_version, size1);
    m_handle.read( (char*) &size2, sizeof(int) );

    if( size1 != size2 || m_version != -1 ) {
      std::stringstream ss;
      ss << "Failed to read binary PTRAC";
      throw McnpToolsException( ss.str() );
    }

    // read the code data 
    m_handle.read( (char*) &size1, sizeof(int) );
    
    char code[8], ver[5], loddat[8], idtm[19];
    m_handle.read( code, sizeof(code) );
    m_code = std::string(code,sizeof(code));
    m_handle.read( ver, sizeof(ver) );
    m_codever = std::string(ver,sizeof(ver));
    m_handle.read( loddat, sizeof(loddat) );
    m_loddat = std::string(loddat,sizeof(loddat));
    m_handle.read( idtm, sizeof(idtm) );
    m_idtm = std::string(idtm,sizeof(idtm));
    cjsoft::stringops::trim(m_idtm);

    m_handle.read( (char*) &size2, sizeof(int) );

    if( size1 != size2 ) {
      std::stringstream ss;
      ss << "Failed to read binary PTRAC";
      throw McnpToolsException( ss.str() );
    }

    // read the comment line
    m_handle.read( (char*) &size1, sizeof(int) );
    assert( size1 == 80 || size1 == 128 );

    m_comment.resize(size1);
    m_handle.read(&m_comment[0], size1*sizeof(char));
    
    m_handle.read( (char*) &size2, sizeof(int) );

    if( size1 != size2 ) {
      std::stringstream ss;
      ss << "Failed to read binary PTRAC";
      throw McnpToolsException( ss.str() );
    }

    // read the keyword entries
    bool done = false;
    std::vector<double> kwent;
    unsigned int nkw = 0;
    unsigned int kwlinecnt = 0;
    while (! done) {
      kwlinecnt++;
      m_handle.read( (char*) &size1, sizeof(int) );

      double buffer[10];
      m_handle.read( (char*) buffer, 10*sizeof(double) );
      if( kwlinecnt == 1 ) {
        nkw = (unsigned int) buffer[0];
        kwent.insert(kwent.end(), &buffer[1], &buffer[1] + 9);
      }
      else {
        kwent.insert(kwent.end(), buffer, buffer + 10);
      }

      unsigned int nkwcnt = 0;
      unsigned int i=0;
      while( i<kwent.size() ) {
        nkwcnt++;
        unsigned int num_ent = (unsigned int) kwent[i];
        i += num_ent+1;
      }

      m_handle.read( (char*) &size2, sizeof(int) );

      if( size1 != size2 ) {
        std::stringstream ss;
        ss << "Failed to read binary PTRAC";
        throw McnpToolsException( ss.str() );
      }

      if( nkwcnt >= nkw )
        done = true;
    }

    // read number data
    m_handle.read( (char*) &size1, sizeof(int) );

    int nnps, ipt, single_double, unused[7];
    int64_t nsrc1, nsrc2, nbnk1, nbnk2, nsur1, nsur2, ncol1, ncol2, nter1, nter2;
    m_handle.read( (char*) &nnps, sizeof(int) );
    m_handle.read( (char*) &nsrc1, sizeof(nsrc1) );
    m_handle.read( (char*) &nsrc2, sizeof(nsrc2) );
    m_handle.read( (char*) &nbnk1, sizeof(nbnk1) );
    m_handle.read( (char*) &nbnk2, sizeof(nbnk2) );
    m_handle.read( (char*) &nsur1, sizeof(nsur1) );
    m_handle.read( (char*) &nsur2, sizeof(nsur2) );
    m_handle.read( (char*) &ncol1, sizeof(ncol1) );
    m_handle.read( (char*) &ncol2, sizeof(ncol2) );
    m_handle.read( (char*) &nter1, sizeof(nter1) );
    m_handle.read( (char*) &nter2, sizeof(nter2) );
    m_handle.read( (char*) &ipt, sizeof(int) );
    m_handle.read( (char*) &single_double, sizeof(int) );
    m_handle.read( (char*) &unused, sizeof(unused) );

    m_nument.insert( std::pair<std::string, int64_t>( "nps", nnps ) );
    m_nument.insert( std::pair<std::string, int64_t>( "src1", nsrc1 ) );
    m_nument.insert( std::pair<std::string, int64_t>( "src2", nsrc2 ) );
    m_nument.insert( std::pair<std::string, int64_t>( "bnk1", nbnk1 ) );
    m_nument.insert( std::pair<std::string, int64_t>( "bnk2", nbnk2 ) );
    m_nument.insert( std::pair<std::string, int64_t>( "sur1", nsur1 ) );
    m_nument.insert( std::pair<std::string, int64_t>( "sur2", nsur2 ) );
    m_nument.insert( std::pair<std::string, int64_t>( "col1", ncol1 ) );
    m_nument.insert( std::pair<std::string, int64_t>( "col2", ncol2 ) );
    m_nument.insert( std::pair<std::string, int64_t>( "ter1", nter1 ) );
    m_nument.insert( std::pair<std::string, int64_t>( "ter2", nter2 ) );

    m_handle.read( (char*) &size2, sizeof(int) );
    
    if( size1 != size2 ) {
      std::stringstream ss;
      ss << "Failed to read binary PTRAC";
      throw McnpToolsException( ss.str() );
    }

    // MCNPTOOLSPRO: Detect filtered PTRAC files (binary format)
    // DISABLED: This heuristic detection is too aggressive and causes false positives
    // on regular binary PTRAC files (e.g., when nter1 is a small number like 0 or 1).
    // TODO: Implement more robust detection or require explicit format specification
    // For now, binary filter support is disabled to prevent breaking regular files.
    //
    // Filtered PTRAC files have an extra record of filter parameters before the data types
    // We detect this by checking specific header values that change with filters
    // For filtered files, we need to skip this extra record
    bool is_filtered_bin = false; // DISABLED: (nbnk2 > 0) || (nter1 < 100) || (unused[2] > 0);

    if(is_filtered_bin) {
      // Skip the extra filter parameters record
      // Read size1, then 10 doubles, then size2
      int filter_size1, filter_size2;
      m_handle.read( (char*) &filter_size1, sizeof(int) );
      double filter_param;
      for(int i=0; i<10; i++) {
        m_handle.read( (char*) &filter_param, sizeof(double) );
      }
      m_handle.read( (char*) &filter_size2, sizeof(int) );
    }

    // read data types
    m_handle.read( (char*) &size1, sizeof(int) );

    for(unsigned int i=0; i<m_lines.size(); i++) {
      for(unsigned int j=0; j<m_nument[ m_lines[i] ]; j++) {
        if( m_lines[i] == "nps" ) {
          int64_t tmp;
          m_handle.read( (char*) &tmp, sizeof(tmp) );
          m_datent[ m_lines[i] ].push_back( tmp );
        }
        else {
          int tmp;
          m_handle.read( (char*) &tmp, sizeof(tmp) );
          m_datent[ m_lines[i] ].push_back( tmp );
        }
      }
    }

    m_handle.read( (char*) &size2, sizeof(int) );

    if( size1 != size2 ) {
      std::stringstream ss;
      ss << "Failed to read binary PTRAC";
      throw McnpToolsException( ss.str() );
    }

  }
  else {
    // read the version
    m_handle >> m_version;

    // read the code data, if it is available (prdmp third entry effects this)
    std::string idtm1, idtm2;
    std::string optional_version_line;
    std::getline(m_handle, optional_version_line); // processes to the next line
    std::getline(m_handle, optional_version_line); 
    if (optional_version_line != " ") { 
      std::stringstream ss {optional_version_line};
      ss >> m_code >> m_codever >> m_loddat >> idtm1 >> idtm2;
      m_idtm = idtm1 + " " + idtm2;
    } // else, the above variables are default-constructed empty strings

    // read the comment line
    cjsoft::stringops::getline(m_handle, m_comment); // processes to the next line

    // MCNPTOOLEXPERT: Read line 4 and parse it to detect filters
    std::string line4_potential_kwent;
    cjsoft::stringops::getline(m_handle, line4_potential_kwent);
    std::vector<double> line4_values;
    std::stringstream ss_line4(line4_potential_kwent);
    double val;
    while(ss_line4 >> val && line4_values.size() < 10) {
      line4_values.push_back(val);
    }

    // read the keyword entries
    // MCNPTOOLEXPERT: Simplified approach for filter_all support
    // nkw < 3: read 1 line (line 5 only)
    // nkw >= 3: read 2 lines (line 5 AND line 6)
    std::vector<double> kwent;
    unsigned int nkw = 0;

    // Read line 5 (first kwent line)
    double tmp;
    m_handle >> tmp;
    nkw = (unsigned int) tmp;

    for(unsigned int i=1; i<10; i++) {
      m_handle >> tmp;
      kwent.push_back(tmp);
    }

    // If nkw >= 3, read line 6 (second kwent line) for filter_all
    if(nkw >= 3) {
      for(unsigned int i=0; i<10; i++) {
        m_handle >> tmp;
        kwent.push_back(tmp);
      }
    }

    // MCNPTOOLEXPERT: Detect filter types from LINE 4
    // Line 4 values contain the actual filter keywords
    // line4[4] = event filter count (3 for event=src,col,ter)
    // line4[7] = filter number (9 for filter=9,...)
    // kwent (line 5) values:
    //   kwent[3] > 0 and kwent[4] > 0 = type filter (e.g. kwent[3]=2, kwent[4]=9 for type=n)
    //   kwent[3] > 0 and kwent[4] < 0 = tally filter (e.g. kwent[3]=1, kwent[4]=-2 for tally=8)
    bool has_filter = false;
    bool has_tally = false;

    // Check line 4 for event/filter keywords
    bool has_event_filter = (line4_values.size() > 4 && line4_values[4] > 0.0);
    bool has_filter_keyword = (line4_values.size() > 7 && line4_values[7] > 0.0);

    // Check line 5 (kwent[0-8]) for type/tally filter
    // Also check line 6 (kwent[9-18]) for filter_all tally info
    // tally: kwent[2] > 0 and kwent[3] < 0 (e.g. 1.0, -2.0)
    // type: kwent[3] > 0 and kwent[4] > 0 (e.g. 2.0, 9.0)
    bool has_type_filter = false;
    bool has_tally_filter = false;
    if(kwent.size() >= 5) {
      // Tally detection: kwent[2] positive, kwent[3] negative
      has_tally_filter = (kwent[2] > 0.0 && kwent[3] < 0.0);

      // Type detection: kwent[3] positive, kwent[4] positive
      has_type_filter = (kwent[3] > 0.0 && kwent[4] > 0.0);
    }

    // MCNPTOOLEXPERT: Check line 6 (kwent[9-18]) for filter_all tally
    // filter_all has line 6 starting at kwent[9]
    // tally marker: kwent[9] < 0 (e.g. -1.0 for tally)
    if(kwent.size() >= 10 && kwent[9] < 0.0) {
      has_tally_filter = true;
    }

    has_filter = has_event_filter || has_filter_keyword || has_type_filter || has_tally_filter;
    has_tally = has_tally_filter;

    // MCNPTOOLEXPERT: MCNP 6.3 tally-only format has an extra line of 10 floats
    // This ONLY affects tally-only files (nkw < 3), NOT filter_all (nkw >= 3)
    bool is_mcnp63 = (m_code == "mcnp6");

    if(is_mcnp63 && has_tally_filter && nkw < 3) {
      // Skip the extra line of 10 floats in MCNP 6.3 tally-only files
      double skip_val;
      for(int i=0; i<10; i++) {
        m_handle >> skip_val;
      }
    }

    // Skip filter parameter line (10 floats) for filters that need it
    // MCNPTOOLEXPERT: filter_all (nkw >= 3) has NO extra line to skip
    // because line 6 (tally info) is already read into kwent
    if(has_filter && has_tally) {
      // tally-only (nkw < 3): no skip needed for MCNP 6.2 (already handled above for 6.3)
      // filter_all (nkw >= 3): no skip needed, line 6 already in kwent
    }
    else if(has_filter) {
      // event=, type=, filter= without tally: skip 1 line
      double filter_param;
      for(int i=0; i<10; i++) {
        m_handle >> filter_param;
      }
    }

    // read number data
    int nnps, ipt, single_double, unused[7];
    int64_t nsrc1, nsrc2, nbnk1, nbnk2, nsur1, nsur2, ncol1, ncol2, nter1, nter2;

    m_handle >> nnps >> nsrc1 >> nsrc2 >> nbnk1 >> nbnk2 >> nsur1 >> nsur2 >> ncol1 >> ncol2 >> nter1 >> nter2 >> ipt >> single_double;
    for(unsigned int i=0; i<7; i++) {
      m_handle >> unused[i];
    }

    m_nument.insert( std::pair<std::string, int64_t>( "nps", nnps ) );
    m_nument.insert( std::pair<std::string, int64_t>( "src1", nsrc1 ) );
    m_nument.insert( std::pair<std::string, int64_t>( "src2", nsrc2 ) );
    m_nument.insert( std::pair<std::string, int64_t>( "bnk1", nbnk1 ) );
    m_nument.insert( std::pair<std::string, int64_t>( "bnk2", nbnk2 ) );
    m_nument.insert( std::pair<std::string, int64_t>( "sur1", nsur1 ) );
    m_nument.insert( std::pair<std::string, int64_t>( "sur2", nsur2 ) );
    m_nument.insert( std::pair<std::string, int64_t>( "col1", ncol1 ) );
    m_nument.insert( std::pair<std::string, int64_t>( "col2", ncol2 ) );
    m_nument.insert( std::pair<std::string, int64_t>( "ter1", nter1 ) );
    m_nument.insert( std::pair<std::string, int64_t>( "ter2", nter2 ) );

    // read data types
    for(unsigned int i=0; i<m_lines.size(); i++) {
      for(unsigned int j=0; j<m_nument[ m_lines[i] ]; j++) {
        if( m_lines[i] == "nps" ) {
          int64_t tmp;
          m_handle >> tmp;
          m_datent[ m_lines[i] ].push_back( tmp );
        }
        else {
          int tmp;
          m_handle >> tmp;
          m_datent[ m_lines[i] ].push_back( tmp );
        }
      }
    }

    // MCNPTOOLEXPERT: Add tally data types if tally filter detected
    // For tally= or filter= with tally, NPS line has: NPS, EVENT_TYPE, TALLY(5), VALUE(6)
    if(has_tally) {
      // Check if TALLY (5) already in list
      bool already_has_tally = false;
      for(unsigned int i=0; i<m_datent["nps"].size(); i++) {
        if(m_datent["nps"][i] == 5) {
          already_has_tally = true;
          break;
        }
      }

      if(!already_has_tally) {
        // Find EVENT_TYPE (2) position
        int pos = -1;
        for(unsigned int i=0; i<m_datent["nps"].size(); i++) {
          if(m_datent["nps"][i] == 2) {
            pos = i;
            break;
          }
        }

        if(pos >= 0) {
          // Insert TALLY(5) and VALUE(6) after EVENT_TYPE
          m_datent["nps"].insert(m_datent["nps"].begin() + pos + 1, 5);
          m_datent["nps"].insert(m_datent["nps"].begin() + pos + 2, 6);
          m_nument["nps"] += 2;
        }
      }
    }
  }
}

PtracHistory Ptrac::ReadHistory() {
  int size1, size2;

  PtracHistory hist;

  // read the nps line
  double next_event_type;
  if( m_format == Ptrac::BIN_PTRAC ) ReadValue(size1);

  PtracNps nps;
  for(unsigned int i=0; i<m_nument["nps"]; i++) {
    // MCNPTOOLEXPERT: VALUE (6) is a double, all others are int64_t
    if( m_datent["nps"][i] == Ptrac::VALUE ) {
      double tmp_double;
      ReadValue(tmp_double);

      if( ! m_handle.good() )
        return hist;

      nps.m_value = tmp_double;
    }
    else {
      int64_t tmp;
      ReadValue(tmp);

      if( ! m_handle.good() )
        return hist;

      switch( m_datent["nps"][i] ) {
        case Ptrac::NPS:
          nps.m_nps = tmp;
          break;
        case Ptrac::FIRST_EVENT_TYPE:
          next_event_type = tmp;
          break;
        case Ptrac::NPSCELL:
          nps.m_cell = tmp;
          break;
        case Ptrac::NPSSURFACE:
          nps.m_surface = tmp;
          break;
        case Ptrac::TALLY:
          nps.m_tally = tmp;
          break;
      }
    }
  }

  if( m_format == Ptrac::BIN_PTRAC ) {
    ReadValue(size2);

    if( size1 != size2 ) {
      std::stringstream ss;
      ss << "Failed to read binary PTRAC";
      throw McnpToolsException( ss.str() );
    }
  }

  hist.m_nps = nps;

  // read the events
  while( (int) next_event_type != Ptrac::LST ) {
    int bnk_type = std::abs(static_cast<int>(next_event_type)) % 1000;
    next_event_type = std::abs(static_cast<int>(next_event_type)) - bnk_type;

    std::string typestr;
    switch( (int) next_event_type ) {
      case Ptrac::SRC:
        typestr = "src";
        break;
      case Ptrac::BNK:
        typestr = "bnk";
        break;
      case Ptrac::SUR:
        typestr = "sur";
        break;
      case Ptrac::COL:
        typestr = "col";
        break;
      case Ptrac::TER:
        typestr = "ter";
        break;
    }

    PtracEvent event;
    event.m_type = next_event_type;
    event.m_bnktype = bnk_type;
  
    std::vector<int> all_data_types;
    all_data_types.insert(all_data_types.end(), m_datent[typestr + "1"].begin(), m_datent[typestr + "1"].end());
    all_data_types.insert(all_data_types.end(), m_datent[typestr + "2"].begin(), m_datent[typestr + "2"].end());

    if( m_format == Ptrac::BIN_PTRAC) ReadValue(size1);

    for(unsigned int i=0; i<all_data_types.size(); i++) {
      double tmp;

      ReadValue(tmp);

      switch( all_data_types[i] ) {
        case Ptrac::NEXT_EVENT_TYPE:
          next_event_type = tmp;
          break;
        case Ptrac::NODE:
          event.m_data[Ptrac::NODE] = tmp;
          break;
        case Ptrac::NSR:
          event.m_data[Ptrac::NSR] = tmp;
          break;
        case Ptrac::ZAID:
          event.m_data[Ptrac::ZAID] = tmp;
          break;
        case Ptrac::RXN:
          event.m_data[Ptrac::RXN] = tmp;
          break;
        case Ptrac::SURFACE:
          event.m_data[Ptrac::SURFACE] = tmp;
          break;
        case Ptrac::ANGLE:
          event.m_data[Ptrac::ANGLE] = tmp;
          break;
        case Ptrac::TERMINATION_TYPE:
          event.m_data[Ptrac::TERMINATION_TYPE] = tmp;
          break;
        case Ptrac::BRANCH:
          event.m_data[Ptrac::BRANCH] = tmp;
          break;
        case Ptrac::PARTICLE:
          event.m_data[Ptrac::PARTICLE] = tmp;
          break;
        case Ptrac::CELL:
          event.m_data[Ptrac::CELL] = tmp;
          break;
        case Ptrac::MATERIAL:
          event.m_data[Ptrac::MATERIAL] = tmp;
          break;
        case Ptrac::COLLISION_NUMBER:
          event.m_data[Ptrac::COLLISION_NUMBER] = tmp;
          break;
        case Ptrac::X:
          event.m_data[Ptrac::X] = tmp;
          break;
        case Ptrac::Y:
          event.m_data[Ptrac::Y] = tmp;
          break;
        case Ptrac::Z:
          event.m_data[Ptrac::Z] = tmp;
          break;
        case Ptrac::U:
          event.m_data[Ptrac::U] = tmp;
          break;
        case Ptrac::V:
          event.m_data[Ptrac::V] = tmp;
          break;
        case Ptrac::W:
          event.m_data[Ptrac::W] = tmp;
          break;
        case Ptrac::ENERGY:
          event.m_data[Ptrac::ENERGY] = tmp;
          break;
        case Ptrac::WEIGHT:
          event.m_data[Ptrac::WEIGHT] = tmp;
          break;
        case Ptrac::TIME:
          event.m_data[Ptrac::TIME] = tmp;
          break;
      }
    }

    if( m_format == Ptrac::BIN_PTRAC ) {
      ReadValue(size2);

      if( size1 != size2 ) {
        std::stringstream ss;
        ss << "Failed to read binary PTRAC";
        throw McnpToolsException( ss.str() );
      }
    }

    hist.m_events.push_back(event);
  }

  // make sure to read until end of line if ASCII
  if( m_format == Ptrac::ASC_PTRAC ) {
    std::string chkstr;
    cjsoft::stringops::getline(m_handle, chkstr);
  }

  return hist;
}

std::vector<PtracHistory> Ptrac::ReadHistoriesLegacy(const unsigned int& num) {
  std::vector<PtracHistory> retval;

  for(unsigned int i=0; i<num; i++) {
    m_handle.peek();
    if( !m_handle.eof() ) {
      PtracHistory hist = ReadHistory();
      retval.push_back( hist );
    }
    else {
      break;
    }
  }

  return retval;
}


std::vector<PtracHistory> Ptrac::ReadHistories(const unsigned int& num) {
  return (m_format == Ptrac::HDF5_PTRAC) ? m_hdf5_parser->ReadHistories( num ) :
                                           ReadHistoriesLegacy( num );
}

} // end namespace mcnptools
