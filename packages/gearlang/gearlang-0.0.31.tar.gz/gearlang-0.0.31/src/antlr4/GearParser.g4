parser grammar GearParser;

options {
    tokenVocab=GearLexer;
    language=Rust;
}


program
	: classDeclaration program
	| enumDeclaration program
	| EOF
	;


enumDeclaration
	: ENUM ID LBRACE enumBody RBRACE
	;

enumBody
	: ID (ASSIGN INTEGER_LITERAL)? (COMMA ID (ASSIGN INTEGER_LITERAL)?)*
	;

classDeclaration
	: CLASS (ID| CogID) (EXTENDS ID)? LBRACE classBody RBRACE
	;

classBody
	: attributeDeclaration classBody
	| methodDeclaration classBody
	| magicMethodDeclaration classBody
	| attributeDeclaration
	| methodDeclaration
	| magicMethodDeclaration
	;


methodDeclaration
	: FN ID LPAREN parameterList? RPAREN block
	;

magicMethodDeclaration
	: FN MagicID LPAREN parameterList? RPAREN block
	;


block
	: LBRACE statement* RBRACE
	;



statement
	: expressionInline
	| IF LBRACE booleanExpression RBRACE block elseStatement?
	| WHILE LBRACE booleanExpression RBRACE block
	| DO block WHILE LBRACE booleanExpression RBRACE SEMI
	| FOR LPAREN expression SEMI booleanExpression SEMI expression RPAREN block
	| BREAK SEMI
	| CONTINUE SEMI
	// | SWITCH LPAREN expression RPAREN LBRACE caseBlock* RBRACE
	| RETURN expressionInline SEMI
	;


elseStatement
	: ELSE block
	| ELSE IF LBRACE booleanExpression RBRACE block elseStatement?
	;


expressionInline
	: expression SEMI
	;

expression
	: assignmentExpression
	| functionCall
	| variableDeclaration
	;

assignmentExpression
	: ID operatorIncrement
	;

booleanExpression
	: LPAREN booleanExpression RPAREN
	| NOT booleanExpression
	| booleanExpression operatorBoolean booleanExpression
	| booleanExpression operatorRelational booleanExpression
	| booleanLiteral
	| ID
	| functionCall
	;

functionCall
	: ID LPAREN argumentList? RPAREN
	;

argumentList
	: typeList expressionInline (COMMA typeList expressionInline)*
	;


attributeDeclaration
	: visibility? variableDeclaration
	;


parameterList
	: parameter (COMMA parameter)*
	;

parameter
	: typeList ID
	;

typeList
	: type (BITOR type)*
	;

type
	: builtInType
	| ID
	;


variableDeclaration
	: type ID (ASSIGN expressionInline)? SEMI
	;

visibility
	: PRIVATE
	| PUBLIC
	;



operatorAssign
	: ASSIGN
	| ADD_ASSIGN
	| SUB_ASSIGN
	| MUL_ASSIGN
	| DIV_ASSIGN
	| MOD_ASSIGN
	| AND_ASSIGN
	| OR_ASSIGN
	| XOR_ASSIGN
	| LS_ASSIGN
	| RS_ASSIGN
	;


operatorIncrement
	: INC
	| DEC
	;


operatorBoolean
	: AND
	| OR
	| NOT
	| XOR
	;

operatorRelational
	: EQ
	| NE
	| GT
	| LT
	| GE
	| LE
	;

builtInType
	: ANY
	| TYPE_VOID
	| TYPE_BOOL
	| TYPE_INT
	| TYPE_FLOAT
	| TYPE_STRING
	;


booleanLiteral
	: TRUE
	| FALSE
	;

