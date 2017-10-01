%option noyywrap
%option yylineno
%{
  #include <stdio.h>
  #include "j_token.h"
  #include "parser.tab.h"
  extern int lineNo;
%}

%%

"auto class"                      {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = strdup(yytext);
                                        s->line = yylineno;
                                        return AUTO_CLASS;
                                    }
[\(\)\[\]\},;]                      {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = strdup(yytext);
                                        s->line = yylineno;
                                        return yytext[0];
                                    }
[\{]                                {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = strdup(yytext);
                                        s->line = yylineno;
                                        return STARTCURLY;
                                    }

"if"                                {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "if";
                                        s->line = yylineno;
                                        return IF;
                                    }
"else"                              {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "else";
                                        s->line = yylineno;
                                        return ELSE;
                                    }
"var"                               {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "var";
                                        s->line = yylineno;
                                        return VAR;
                                    }
"int"                               {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "int";
                                        s->line = yylineno;
                                        return INT;
                                    }
"float"                             {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "float";
                                        s->line = yylineno;
                                        return FLOAT;
                                    }
"init"                             {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "init";
                                        s->line = yylineno;
                                        return INIT;
                                    }
"event"                             {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "event";
                                        s->line = yylineno;
                                        return EVENT;
                                    }
"preEvent"                          {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "preEvent";
                                        s->line = yylineno;
                                        return PRE_EVENT;
                                    }
"postEvent"                         {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "postEvent";
                                        s->line = yylineno;
                                        return POST_EVENT;
                                    }
"return"                            {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "Return";
                                        s->line = yylineno;
                                        return RETURN;
                                    }

"while"                             {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "While";
                                        s->line = yylineno;
                                        return WHILE;
                                    }
"break"                             {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "Break";
                                        s->line = yylineno;
                                        return BREAK;
                                    }

"false"                             {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "false";
                                        s->numericValue = 0;
                                        s->line = yylineno;
                                        return NUMBER;
                                    }
"true"                              {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->line = yylineno;
                                        s->stringValue = "true";
                                        s->numericValue = 1;
                                        s->line = yylineno;
                                        return NUMBER;
                                  }
"*"                               {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "*";
                                        s->line = yylineno;
                                        return MUL;
                                    }
"/"                                  {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "/";
                                        s->line = yylineno;
                                        return DIV;
                                    }
"%"                                  {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "%";
                                        s->line = yylineno;
                                        return MOD;
                                    }
"&&"                              {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "&&";
                                        s->line = yylineno;
                                        return AND;
                                    }
"+"                                  {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "+";
                                        s->line = yylineno;
                                        return ADD;
                                    }
"-"                                  {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "-";
                                        s->line = yylineno;
                                        return SUBT;
                                    }
"||"                              {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "||";
                                        s->line = yylineno;
                                        return OR;
                                    }
"!="                              {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "!=";
                                        s->line = yylineno;
                                        return NEQ;
                                    }
"<="                              {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "<=";
                                        s->line = yylineno;
                                        return LEQ;
                                    }
">="                              {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = ">=";
                                        s->line = yylineno;
                                        return GEQ;
                                    }
"=="                              {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "==";
                                        s->line = yylineno;
                                        return EQ;
                                    }

">"                                 {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = ">";
                                        s->line = yylineno;
                                        return GREAT;
                                    }
"<"                                 {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "<";
                                        s->line = yylineno;
                                        return LESS;
                                    }
[\=]                                {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "=";
                                        s->line = yylineno;
                                        return ASSIGN;
                                    }
[\!]                                {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = "!";
                                        s->line = yylineno;
                                        return NOT;
                                    }
[.]                                 {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = ".";
                                        s->line = yylineno;
                                        return DOT;
                                    }

[A-Za-z_][A-Za-z0-9_]*              {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = strdup(yytext);
                                        s->line = yylineno;
                                        return IDENT;
                                    }
[0-9]+                              {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                        s->stringValue = strdup(yytext);
                                        s->numericValue = atoi(yytext);
                                        s->line = yylineno;
                                        return NUMBER;
                                    }
"\r\n"            { lineNo++;}
"\n"              { lineNo++;}
"\r"              { lineNo++;}
"//".*\n          { lineNo++;}
" "               {}
\t                {}
.                                   {
                                        lineNo = yylineno;
                                        JToken * s = new JToken;
                                        yylval.tokInfo = s;
                                  s->stringValue = yytext;
                                  s->line = yylineno;
                                  return ERROR;
                                }

%%
