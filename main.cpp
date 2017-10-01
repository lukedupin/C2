#include <vector>
#include <string>
#include <stdio.h>
#include <memory>

#include "j_token.h"
#include "parser.tab.h"

#include "auto_class.h"

using namespace std;

void yyset_in( FILE* handle );
int yylex();
extern int lineNo;

int main( int argc, char** argv )
{
    vector<string> files;

    //Load up the processors
    ProcessorBase* _base;
    AutoClass _autoClass;

    //Load the user's initial files
    for ( auto i = 1; i < argc; i++ )
        files.push_back( argv[i] );

    //Run through all my process files
    for ( auto i = 0; i < files.size(); i++ )
    {
      FILE* handle = nullptr;
      if ( (handle = fopen(files[i].c_str(), "r")) == nullptr )
        return 0;

      yyset_in( handle );

        //Handle the lex output of the user's file
      int val;
      while ( val = yylex() )
          switch ( val )
          {
            case AUTO_CLASS:
              _base = &_autoClass;
              break;

            default:
              base = nullptr;
              break;
          }

      //Get the output for this parser handler

      //Check that this parser has reached its expected completion

      //Have we been in a possibly nested output?  Re run with the now updated logic until we are done nesting


      //Close down this file
      fclose( handle );
    }

  return 0;
}
