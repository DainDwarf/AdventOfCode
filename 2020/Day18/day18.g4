grammar day18;

/** PARSER **/

prog: line* ;
line: expr NEWLINE;

expr:	expr op=('*'|'+') expr  # operation
    |	INT                     # integer
    |	'(' expr ')'            # parentheses
    ;

/** LEXER **/

NEWLINE : [\r\n]+ ;
INT     : [0-9]+ ;
WS      : [ ] -> skip ;
