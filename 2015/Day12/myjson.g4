grammar myjson;

// java -Xmx500M -cp "/usr/local/bin/antlr4.jar:$CLASSPATH" org.antlr.v4.Tool -Dlanguage=Python3 myjson.g4


elem : arr
     | obj
     | num
     | STRING
;

arr : '[' elem (',' elem)* ']'
      | '[' ']'
;

obj: '{' obj_param (',' obj_param)* '}'
      | '{' '}'
;

obj_param : STRING ':' elem
;

num: NUMBER;

//Must be before IDENT, because it 'defines' other keywords
WS     : [ \t\r] -> channel(1);
NUMBER : ('-')? ('0'..'9')+;
STRING : '"' ('a'..'z'|'A'..'Z')+ '"';
