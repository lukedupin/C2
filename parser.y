%{
	//C includes
	#include <stdio.h>
  #include <stack>

	//Custom includes
	#include "j_token.h"
  #include "parser.tab.h"

  int yylex();
  //int yydebug;

  int lineNo;

  void yyerror( const char *msg )
	{
		printf("ERROR Value: %s detected on line %d.\n", msg, lineNo );
	}

  int yywrap()
  {
      return 1;
  }

%}

%union {
	JToken * tokInfo;
}

//Token list
%token <tokInfo> AUTO_CLASS
%token <tokInfo> IF ELSE RETURN WHILE BREAK STARTCURLY INIT EVENT PRE_EVENT POST_EVENT
%token <tokInfo> IDENT NUMBER FLOAT INT VAR DOT VAR_EX
%token <tokInfo> MUL DIV MOD AND
%token <tokInfo> ADD SUBT OR
%token <tokInfo> GEQ NEQ LEQ GREAT LESS EQ NOT ASSIGN ASSIGN_CONST
%token <tokInfo> ERROR

%type <nodeInfo> program

%%

program   : NUMBER {}

%%

//#include "main.cpp"
