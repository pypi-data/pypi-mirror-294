lexer grammar GearLexer;






// Keywords
FN			: 'fn';
CLASS		: 'class';
EXTENDS		: 'extends';
ENUM		: 'enum';

PRIVATE		: 'pv';
PUBLIC		: 'pb';
SELF		: 'self';

RETURN		: 'return';

ANY			: 'any';

IF			: 'if';
ELSE		: 'else';
WHILE		: 'while';
DO			: 'do';
FOR			: 'for';
BREAK		: 'break';
CONTINUE	: 'continue';
SWITCH		: 'switch';
CASE		: 'case';

TRUE		: 'true';
FALSE		: 'false';

//
// == Operators ==
//

// Arithmetic operators
ADD			: '+';
SUB			: '-';
MUL			: '*';
DIV			: '/';
MOD			: '%';

BITAND		: '&';
BITOR		: '|';
BITXOR		: '^';
BITNOT		: '~';
LSHIFT		: '<<';
RSHIFT		: '>>';

// Assignment operators
ASSIGN		: '=';
ADD_ASSIGN	: '+=';
SUB_ASSIGN	: '-=';
MUL_ASSIGN	: '*=';
DIV_ASSIGN	: '/=';
MOD_ASSIGN	: '%=';

AND_ASSIGN	: '&=';
OR_ASSIGN	: '|=';
XOR_ASSIGN	: '^=';
LS_ASSIGN	: '<<=';
RS_ASSIGN	: '>>=';




// Increment/decrement operators
INC			: '++';
DEC			: '--';


// Boolean operators
AND			: '&&';
OR			: '||';
NOT			: '!';
XOR			: '^^';



// Relational operators
GT			: '>';
LT			: '<';
EQ			: '==';
NE			: '!=';
GE			: '>=';
LE			: '<=';




//
// == Punctuation ==
//
SEMI			: ';';
COMMA			: ',';
DOT				: '.';
ARROW			: '->';

TERNARY			: '?';
COLON			: ':';

LPAREN			: '(';
RPAREN			: ')';
LBRACE			: '{';
RBRACE			: '}';
LBRACKET		: '[';
RBRACKET		: ']';



HASH			: '#';
DOLLAR			: '$';
UNDERSCORE		: '_';

fragment COG	: '@';
fragment MAGIC	: '__';

// Literals
INTEGER_LITERAL	: [0-9]+;
FLOAT_LITERAL	: [0-9]+'.'[0-9]+;


// Identifiers
CogID			: COG[a-zA-Z_][a-zA-Z0-9_]*;
MagicID			: MAGIC[a-zA-Z_][a-zA-Z0-9_]*MAGIC;
ID				: [a-zA-Z_][a-zA-Z0-9_]*;


// built-in types
TYPE_VOID		: 'void';
TYPE_BOOL		: '@bool';
TYPE_INT		: '@int';
TYPE_FLOAT		: '@float';
TYPE_STRING		: '@str';


// Whitespace and comments

WS
	: [ \t\r\n]+ -> channel(HIDDEN)
	;

Newline
	: ('\r' '\n'? | '\n') -> channel(HIDDEN)
	;

BlockComment
	: '/*' .*? '*/' -> channel(HIDDEN)
	;

LineComment
	: '//' ~[\r\n]* -> channel(HIDDEN)
	;
