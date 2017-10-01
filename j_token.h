#ifndef __JTOKEN_H__
#define __JTOKEN_H__
/** \struct jToken
    \brief Defines the token types that the lexer will feed the parser.
*/

struct JToken
{
    int numericValue;
    int floatValue;
    const char * stringValue;
    
    int line;
};

#endif //#ifndef __STRUCT_H__
