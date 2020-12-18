grammar day18_2;

/** PARSER **/

prog: line* ;
line: expr NEWLINE;

/** Addition has more precedence over multiplication, now **/
expr:	expr op='+' expr        # addition
    |	expr op='*' expr        # multiplication
    |	INT                     # integer
    |	'(' expr ')'            # parentheses
    ;

/** LEXER **/

NEWLINE : [\r\n]+ ;
INT     : [0-9]+ ;
WS      : [ ] -> skip ;
