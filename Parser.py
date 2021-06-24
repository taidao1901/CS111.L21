import ply.yacc as yacc
import Lexer
tokens= Lexer.tokens

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
)
names= { }
def p_statements(p):
    '''statements : statement
            | statement NEWLINE statements
            | statement statements'''
    if len(p)==4:
        p[0]=(p[1],p[3])
    elif len(p)==2:
        p[0]=p[1]
    else: 
        p[0]=(p[1],p[2])
def p_statement(p):
    '''statement : assign
            | expr
            | input_stmt
            | print_stmt
            | if_stmt
            | for_stmt
            | while_stmt'''
    p[0]=p[1]
def p_assign(p):
    '''assign : ID EQUALS expr'''
    p[0]=('ASSIGN',p[1],p[3])
def p_expr(p):
    '''expr : expr PLUS term
            | expr MINUS term
            | term
            | LPAREN expr RPAREN'''
    if (len(p)==4):
        if p[2]=='+':
            p[0]=('+',p[1],p[3])
        elif p[2]=='-':
            p[0]=('-',p[1],p[3])
        elif p[1]=='(':
            p[0]=p[2]
    elif (len(p)==2):
        p[0]=(p[1])
def p_term(p):
    '''term : term TIMES factor
           | term DIVIDE factor
           | factor'''
    if (len(p)==4):
        if p[2]=='*':
            p[0]=('*',p[1],p[3])
        elif p[2]=='/':
            p[0]=('/',p[1],p[3])
    elif (len(p)==2):
        p[0]=(p[1])
def p_factor(p):
    '''factor : INTEGER
              | ID
              | STRING
              | FLOAT'''
    p[0]= p[1]
def p_input_stmt(p):
    '''input_stmt : ID EQUALS input LPAREN RPAREN'''
    p[0]=('input',p[1])   
def p_print(p):
    '''print_stmt : print LPAREN expr RPAREN'''
    p[0]=('print',p[3])
def p_comp_op(p):
    '''comp_op : expr GREATER expr
            | expr LESS expr
            | expr EQUALTO expr
            | expr NOTEQUALTO expr'''
    if p[2]== '>':
        p[0]=('GREAT',p[1],p[3])
    elif p[2]== '<':
        p[0]=('LESS',p[1],p[3])
    elif p[2]== '==':
        p[0]=('EQUALTO',p[1],p[3])
    elif p[2]=='!=':
        p[0]=('NOTEQUALTO',p[1],p[3])
def p_if_stmt(p):
    '''if_stmt : if comp_op COLON block
            | if comp_op COLON block elif_stmt
            | if comp_op COLON block else_block '''
    if len(p)==5:
        p[0]=('if',p[2],p[4])
    elif len(p)==6:
        p[0]=('if',p[2],p[4],p[5])
def p_elif_stmt(p):
    '''elif_stmt : elif comp_op COLON block
            | elif comp_op COLON block elif_stmt
            | elif comp_op COLON block else_block '''
    if len(p)==5:
        p[0]=('elif',p[2],p[4])
    elif len(p)==6:
        p[0]=('elif',p[2],p[4],p[5])        
def p_else_block(p):
    '''else_block : else COLON block'''
    p[0]=('else',p[3])
def p_block(p):
    '''block : INDENT statements
            | INDENT statements DEDENT'''
    p[0]=('block',p[2])
def p_for_stmt(p):
    '''for_stmt : for ID in range in_range COLON block '''
    p[0]=('for',p[2],p[5],p[7])
def p_in_range(p):
    '''in_range : expr
            | LPAREN expr COMMA expr RPAREN'''
    if len(p)==2:
        p[0]=('in_range',p[1])
    elif len(p)==6:
        p[0]=('in_range',p[2],p[4])
def p_while_stmt(p):
    '''while_stmt : while comp_op COLON block'''
    p[0]=('while',p[2],p[4])
def p_error(p):
    print("Syntax error")
    exit()
yacc.yacc()
lines = []
while True:
    line = input()
    if line:
        lines.append(line)
    else:
        break
text = '\n'.join(lines)
result = yacc.parse(text)
print(result)