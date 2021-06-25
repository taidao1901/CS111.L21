import ply.lex as lex
import ply.yacc as yacc


keywords = ('else','in','for','while','elif','if','range','print','input') 
operators=('EQUALS','PLUS','MINUS','TIMES','DIVIDE','GREATER','LESS','EQUALTO','NOTEQUALTO')
delimiters=('LPAREN','RPAREN','COLON','COMMA')
literal=('INTEGER','FLOAT','STRING')
# Danh sách các token cần định nghĩa
tokens =keywords+operators+delimiters+literal+('ID','INDENT','DEDENT','SPACE','NEWLINE','COMMENT') 

# Định nghĩa biến (Indentify)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in keywords:
        t.type=t.value
    return t
# Định nghĩa các operator
t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_GREATER = r'>'
t_LESS = r'<'
t_EQUALTO = r'=='
t_NOTEQUALTO = r'!='
# Định nghĩa các delimiter
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON=r'\:'
t_COMMA= r'\,'
#Định nghĩa các kiểu dữ liệu integer, float, string
t_INTEGER = r'\d+'
t_FLOAT= r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
def t_STRING(t):
    r'\'([^\\\n]|(\\.))*?\''
    return t
# Định nghĩa comment, bỏ qua token này
def t_COMMENT(t):
    r'\#.*'
    pass
 # Nếu kí hiệu không nằm trong danh sách token thì thông báo illegal character, và bỏ qua 
def t_error(t):
    print ("illegal character '%s" %t.value[0])
    t.lexer.skip(1)
# Định nghĩa newline, thụt lề, bỏ thụt lề
indents = [0]
def t_INDENT(t):
    r'\n[ ]*' 
    t.lexer.lineno += 1
    # Bỏ qua dòng trống
    if t.lexer.lexpos >= len(t.lexer.lexdata) or t.lexer.lexdata[t.lexer.lexpos] == "\n":
        return None  
    width = len(t.value) - 1
    last_pos = t.lexer.lexpos - width
    # Nếu width cùng cấp  với thụt lề cuối cùng thì trả về Newline
    if width == indents[-1]: 
        t.type= 'NEWLINE'
        t.value= '\n'
        return t
    # Nếu width cùng cấp  với thụt lề cuối cùng hơn cấp thì trả về là Indent
    elif width > indents[-1]: 
        t.type = 'INDENT'
        t.value = 1
        indents.append(width)
        return t
    # Xét xóa thụt lề (Dedent)
    else:
        ded = 0
        # Xét các thụt lề trước đó
        while len(indents) > 1:
            indents.pop()
            ded += 1
            # Nếu width cùng cấp với thụt lề cuối cùng thì trả về Dedent
            if width == indents[-1]:
                t.type = 'DEDENT'
                t.value = ded
                return t
        raise Exception("bad indent level at line %d: %s" % (t.lexer.lineno - 1,t.lexer.lines[t.lexer.lineno-1]))
# Định nghĩa khoảng trắng, bỏ qua
def t_SPACE(t):
    r'[ ]+'
    return None
# Kích hoạt lexer
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
