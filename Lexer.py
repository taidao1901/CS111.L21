import ply.lex as lex
import ply.yacc as yacc


keywords = ('else','in','for','while','elif','if','range','print','input')
operators=('EQUALS','PLUS','MINUS','TIMES','DIVIDE','GREATER','LESS','EQUALTO','NOTEQUALTO')
delimiters=('LPAREN','RPAREN','COLON','COMMA')
literal=('INTEGER','FLOAT','STRING')
tokens =keywords+operators+delimiters+literal+('ID','INDENT','DEDENT','SPACE','NEWLINE')


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in keywords:
        t.type=t.value
    return t

t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_GREATER = r'>'
t_LESS = r'<'
t_EQUALTO = r'=='
t_NOTEQUALTO = r'!='

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON=r'\:'
t_COMMA= r'\,'

t_INTEGER = r'\d+'
t_FLOAT= r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
def t_STRING(t):
    r'\'([^\\\n]|(\\.))*?\''
    return t
 
def t_COMMENT(t):
    r'\#.*'
    pass
    
def t_error(t):
    print ("illegal character '%s" %t.value[0])
    t.lexer.skip(1)

indents = [0]
def t_INDENT(t):
    r'\n[ ]*' 
    t.lexer.lineno += 1
    if t.lexer.lexpos >= len(t.lexer.lexdata) or t.lexer.lexdata[t.lexer.lexpos] == "\n": # empty line
        return None
    width = len(t.value) - 1
    last_pos = t.lexer.lexpos - width
    if width == indents[-1]:
        t.type= 'NEWLINE'
        t.value= '\n'
        return t
        #return None
    elif width > indents[-1]:
        t.type = 'INDENT'
        t.value = 1
        indents.append(width)
        return t
    else:
        ded = 0
        while len(indents) > 1:
            indents.pop()
            ded += 1
            if width == indents[-1]:
                t.type = 'DEDENT'
                t.value = ded
                return t
        raise Exception("bad indent level at line %d: %s" % (t.lexer.lineno - 1,t.lexer.lines[t.lexer.lineno-1]))

def t_SPACE(t):
    r'[ ]+'
    return None
lexer=lex.lex()
"""lines = []
while True:
    line = input()
    if line:
        lines.append(line)
    else:
        break
text = '\n'.join(lines)
lexer.input(text)
 
 # Tokenize
while True:
     tok = lexer.token()
     if not tok: 
         break      # No more input
     print(tok.type,str(tok.value))"""
