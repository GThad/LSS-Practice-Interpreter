import unittest as ut
from io import StringIO
from lexer.lisp_lexer import lex
from lexer.lisp_token import Token, TokenType

class TestParen(ut.TestCase):
    def setUp(self):
        self.prog = StringIO()
    
    def tearDown(self):
        self.prog.close()
        
    def test_lparen(self):
        self.prog.write("(")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        lParenToken = Token("(", "(", TokenType.LPAREN,
                                   1, 1)
        self.assertListEqual(tokens, [lParenToken])
        
    def test_rparen(self):
        self.prog.write(")")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        rParenToken = Token(")", ")", TokenType.RPAREN,
                                   1, 1)
        self.assertEqual(tokens, [rParenToken])
        
    def test_nested_paren_single_line(self):
        self.prog.write("((()))")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        lParenToken1 = Token("(", "(", TokenType.LPAREN,
                                   1, 1)
        lParenToken2 = Token("(", "(", TokenType.LPAREN,
                                   1, 2)
        lParenToken3 = Token("(", "(", TokenType.LPAREN,
                                   1, 3)
        rParenToken1 = Token(")", ")", TokenType.RPAREN,
                                   1, 4)
        rParenToken2 = Token(")", ")", TokenType.RPAREN,
                                   1, 5)
        rParenToken3 = Token(")", ")", TokenType.RPAREN,
                                   1, 6)
        expTokens = [lParenToken1, lParenToken2, lParenToken3,
                          rParenToken1, rParenToken2, rParenToken3]
        self.assertListEqual(tokens, expTokens)
                
    def test_nested_paren_multi_line(self):
        self.prog.write("((( \n )) \n )")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        lParenToken1 = Token("(", "(", TokenType.LPAREN,
                                   1, 1)
        lParenToken2 = Token("(", "(", TokenType.LPAREN,
                                   1, 2)
        lParenToken3 = Token("(", "(", TokenType.LPAREN,
                                   1, 3)
        rParenToken1 = Token(")", ")", TokenType.RPAREN,
                                   2, 2)
        rParenToken2 = Token(")", ")", TokenType.RPAREN,
                                   2, 3)
        rParenToken3 = Token(")", ")", TokenType.RPAREN,
                                   3, 2)
        expTokens = [lParenToken1, lParenToken2, lParenToken3,
                          rParenToken1, rParenToken2, rParenToken3]
        self.assertListEqual(tokens, expTokens)
                
    def test_parallel_paren_single_line(self):
        self.prog.write("() () ()")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        lParenToken1 = Token("(", "(", TokenType.LPAREN,
                                   1, 1)
        rParenToken1 = Token(")", ")", TokenType.RPAREN,
                                   1, 2)
        lParenToken2 = Token("(", "(", TokenType.LPAREN,
                                   1, 4)
        rParenToken2 = Token(")", ")", TokenType.RPAREN,
                                   1, 5)
        lParenToken3 = Token("(", "(", TokenType.LPAREN,
                                   1, 7)
        rParenToken3 = Token(")", ")", TokenType.RPAREN,
                                   1, 8)
        expTokens = [lParenToken1, rParenToken1, lParenToken2,
                          rParenToken2, lParenToken3, rParenToken3]
        self.assertListEqual(tokens, expTokens)
                
    def test_parallel_paren_multi_line(self):
        self.prog.write("()  \n ( \n ) ()")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        lParenToken1 = Token("(", "(", TokenType.LPAREN,
                                   1, 1)
        rParenToken1 = Token(")", ")", TokenType.RPAREN,
                                   1, 2)
        lParenToken2 = Token("(", "(", TokenType.LPAREN,
                                   2, 2)
        rParenToken2 = Token(")", ")", TokenType.RPAREN,
                                   3, 2)
        lParenToken3 = Token("(", "(", TokenType.LPAREN,
                                   3, 4)
        rParenToken3 = Token(")", ")", TokenType.RPAREN,
                                   3, 5)
        expTokens = [lParenToken1, rParenToken1, lParenToken2,
                          rParenToken2, lParenToken3, rParenToken3]
        self.assertListEqual(tokens, expTokens)
                
class TestNewLineEdgeCases(ut.TestCase):
    def setUp(self):
        self.prog = StringIO()
    
    def tearDown(self):
        self.prog.close()
        
    def test_first_newline(self):
        self.prog.write(" \n ()")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        lParenToken1 = Token("(", "(", TokenType.LPAREN,
                                   2, 2)
        rParenToken1 = Token(")", ")", TokenType.RPAREN,
                                   2, 3)
        expTokens = [lParenToken1, rParenToken1]
        self.assertListEqual(tokens, expTokens)
                
    def test_multi_first_newline(self):
        self.prog.write(" \n \n ()")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        lParenToken1 = Token("(", "(", TokenType.LPAREN,
                                   3, 2)
        rParenToken1 = Token(")", ")", TokenType.RPAREN,
                                   3, 3)
        expTokens = [lParenToken1, rParenToken1]
        self.assertListEqual(tokens, expTokens)
                
    def test_multi_between_newline(self):
        self.prog.write("( \n \n \n )")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        lParenToken1 = Token("(", "(", TokenType.LPAREN,
                                   1, 1)
        rParenToken1 = Token(")", ")", TokenType.RPAREN,
                                   4, 2)
        expTokens = [lParenToken1, rParenToken1]
        self.assertListEqual(tokens, expTokens)
                
    def test_last_newline(self):
        self.prog.write("() \n \n")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        lParenToken1 = Token("(", "(", TokenType.LPAREN,
                                   1, 1)
        rParenToken1 = Token(")", ")", TokenType.RPAREN,
                                   1, 2)
        expTokens = [lParenToken1, rParenToken1]
        self.assertListEqual(tokens, expTokens)
        
class TestInt(ut.TestCase):
    def setUp(self):
        self.prog = StringIO()
    
    def tearDown(self):
        self.prog.close()
    
    def test_digit_int(self):
        self.prog.write("2")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        intToken = Token("2", 2, TokenType.INT,
                               1, 1)
        self.assertListEqual(tokens, [intToken])
    
    def test_small_int(self):
        self.prog.write("2123")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        intToken = Token("2123", 2123, TokenType.INT,
                               1, 4)
        self.assertListEqual(tokens, [intToken])
    
    def test_large_int(self):
        self.prog.write("11223344556678899101011111212131314141515")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        intToken = Token("11223344556678899101011111212131314141515", 
                               11223344556678899101011111212131314141515, 
                               TokenType.INT, 1, 41)
        self.assertListEqual(tokens, [intToken])
    
    def test_neg_int(self):
        self.prog.write("-24")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        intToken = Token("-24", -24, 
                               TokenType.INT, 1, 3)
        self.assertListEqual(tokens, [intToken])
    
    def test_wrong_neg_int(self):
        self.prog.write("- 24")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        minusToken = Token("-", "-", TokenType.SYM, 1, 1)
        intToken = Token("24", 24, 
                               TokenType.INT, 1, 4)
        self.assertListEqual(tokens, [minusToken, intToken])
    
    def test_multiline_int(self):
        self.prog.write("24 \n 25")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        intToken = Token("24", 24, 
                               TokenType.INT, 1, 2)
        intToken2 = Token("25", 25, 
                               TokenType.INT, 2, 3)
        self.assertListEqual(tokens, [intToken, intToken2])
        
    def test_leading_zero(self):
        self.prog.write("0024")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        intToken = Token("0024", 24, 
                               TokenType.INT, 1, 4)
        self.assertListEqual(tokens, [intToken])
    
    def test_trailing_zero(self):
        self.prog.write("2400")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        intToken = Token("2400", 2400, 
                               TokenType.INT, 1, 4)
        self.assertListEqual(tokens, [intToken])
        
    def test_leading_trailing_zero(self):
        self.prog.write("002400")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        intToken = Token("002400", 2400, 
                               TokenType.INT, 1, 6)
        self.assertListEqual(tokens, [intToken])

class TestFloat(ut.TestCase):
    def setUp(self):
        self.prog = StringIO()
    
    def tearDown(self):
        self.prog.close()
    
    def test_small_float(self):
        self.prog.write("1.1")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        floatToken = Token("1.1", 1.1, TokenType.FLOAT,
                               1, 3)
        self.assertListEqual(tokens, [floatToken])
    
    def test_large_float(self):
        self.prog.write("112233445566.112233445566")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        floatToken = Token("112233445566.112233445566", 
                                 112233445566.112233445566, 
                                 TokenType.FLOAT, 1, 25)
        self.assertListEqual(tokens, [floatToken])
    
    def test_neg_float(self):
        self.prog.write("-2.45")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        floatToken = Token("-2.45", 
                                 -2.45, 
                                 TokenType.FLOAT, 1, 5)
        self.assertListEqual(tokens, [floatToken])
        
    def test_wrong_neg_float(self):
        self.prog.write("- 1.02")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        minusToken = Token("-", "-", TokenType.SYM, 1, 1)
        floatToken = Token("1.02", 1.02, 
                               TokenType.FLOAT, 1, 6)
        self.assertListEqual(tokens, [minusToken, floatToken])
    
    def test_multiline_float(self):
        self.prog.write("2.45 \n 2.46")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        floatToken1 = Token("2.45", 2.45, 
                                 TokenType.FLOAT, 1, 4)
        floatToken2 = Token("2.46", 2.46, 
                                 TokenType.FLOAT, 2, 5)
        self.assertListEqual(tokens, [floatToken1, floatToken2])
        
    def test_leading_zero(self):
        self.prog.write("0002.45")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        floatToken = Token("0002.45", 
                                 2.45, 
                                 TokenType.FLOAT, 1, 7)
        self.assertListEqual(tokens, [floatToken])
    
    def test_trailing_zero(self):
        self.prog.write("2.45000")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        floatToken = Token("2.45000", 
                                 2.45, 
                                 TokenType.FLOAT, 1, 7)
        self.assertListEqual(tokens, [floatToken])
        
    def test_leading_trailing_zero(self):
        self.prog.write("0002.45000")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        floatToken = Token("0002.45000", 
                                 2.45, 
                                 TokenType.FLOAT, 1, 10)
        self.assertListEqual(tokens, [floatToken])
        
    def test_no_front_float(self):
        self.prog.write(".45")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        floatToken = Token(".45", 
                                 0.45, 
                                 TokenType.FLOAT, 1, 3)
        self.assertListEqual(tokens, [floatToken])
        
    def test_no_back_float(self):
        self.prog.write("1.")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        floatToken = Token("1.", 
                                 1.0, 
                                 TokenType.FLOAT, 1, 2)
        self.assertListEqual(tokens, [floatToken])
        
class TestString(ut.TestCase):
    def setUp(self):
        self.prog = StringIO()
    
    def tearDown(self):
        self.prog.close()
        
    def test_empty_string(self):
        self.prog.write("\"\"")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        strToken = Token("\"\"", "", TokenType.STR, 1, 2)
        self.assertListEqual(tokens, [strToken])
        
    def test_empty_with_ws(self):
        self.prog.write("\"  \"")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        strToken = Token("\"  \"", "  ", 
                               TokenType.STR, 1, 4)
        self.assertListEqual(tokens, [strToken])
        
    def test_only_newline(self):
        self.prog.write("\"\\n\"")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        strToken = Token("\"\\n\"", "\n", 
                               TokenType.STR, 1, 4)
        self.assertListEqual(tokens, [strToken])
        
    def test_char(self):
        self.prog.write("\"a\"")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        strToken = Token("\"a\"", "a", 
                               TokenType.STR, 1, 3)
        self.assertListEqual(tokens, [strToken])
        
    def test_word(self):
        self.prog.write("\"hello\"")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        strToken = Token("\"hello\"", "hello", 
                               TokenType.STR, 1, 7)
        self.assertListEqual(tokens, [strToken])
        
    def test_2char(self):
        self.prog.write("\"a b\"")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        strToken = Token("\"a b\"", "a b", 
                               TokenType.STR, 1, 5)
        self.assertListEqual(tokens, [strToken])
        
    def test_2word(self):
        self.prog.write("\"hello world\"")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        strToken = Token("\"hello world\"", "hello world", 
                               TokenType.STR, 1, 13)
        self.assertListEqual(tokens, [strToken])
        
    def test_2word_newline(self):
        self.prog.write("\"hello \\n world\"")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        strToken = Token("\"hello \\n world\"", 
                               "hello \n world",
                               TokenType.STR, 1, 16)
        self.assertListEqual(tokens, [strToken])
        
    def test_leading_ws(self):
        self.prog.write("\"    a\"")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        strToken = Token("\"    a\"", "    a", 
                               TokenType.STR, 1, 7)
        self.assertListEqual(tokens, [strToken])
        
    def test_trailing_ws(self):
        self.prog.write("\"a    \"")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        strToken = Token("\"a    \"", "a    ", 
                               TokenType.STR, 1, 7)
        self.assertListEqual(tokens, [strToken])
        
    def test_lead_trail_ws(self):
        self.prog.write("\"    a    \"")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        strToken = Token("\"    a    \"", "    a    ", 
                               TokenType.STR, 1, 11)
        self.assertListEqual(tokens, [strToken])

    def test_multiline(self):
        self.prog.write("\"abc \n def \n ghi\"")
        self.prog.seek(0)
        errors = lex(self.prog)[1]
        with self.assertRaises(SyntaxError):
            raise errors[0]

class TestSym(ut.TestCase):
    def setUp(self):
        self.prog = StringIO()
    
    def tearDown(self):
        self.prog.close()
        
    def test_char_sym(self):
        self.prog.write("+")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        symToken = Token("+", "+", TokenType.SYM, 1, 1)
        self.assertListEqual(tokens, [symToken])
        
    def test_word_sym(self):
        self.prog.write("append")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        symToken = Token("append", "append", 
                               TokenType.SYM, 1, 6)
        self.assertListEqual(tokens, [symToken])
        
    def test_multiword_sym(self):
        self.prog.write("append world hello")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        symToken1 = Token("append", "append", 
                               TokenType.SYM, 1, 6)
        symToken2 = Token("world", "world", 
                               TokenType.SYM, 1, 12)
        symToken3 = Token("hello", "hello", 
                               TokenType.SYM, 1, 18)
        self.assertListEqual(tokens, [symToken1, symToken2, symToken3])
        
    def test_odd_sym1(self):
        self.prog.write("..123")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        symToken = Token("..123", "..123", 
                               TokenType.SYM, 1, 5)
        self.assertListEqual(tokens, [symToken])
        
    def test_odd_sym2(self):
        self.prog.write("1.2.3")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        symToken = Token("1.2.3", "1.2.3", 
                               TokenType.SYM, 1, 5)
        self.assertListEqual(tokens, [symToken])
        
    def test_odd_sym3(self):
        self.prog.write("-_-")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        symToken = Token("-_-", "-_-", 
                               TokenType.SYM, 1, 3)
        self.assertListEqual(tokens, [symToken])
        
    def test_odd_sym4(self):
        self.prog.write("#%$")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        symToken = Token("#%$", "#%$", 
                               TokenType.SYM, 1, 3)
        self.assertListEqual(tokens, [symToken])
        
class TestBool(ut.TestCase):
    def setUp(self):
        self.prog = StringIO()
    
    def tearDown(self):
        self.prog.close()
        
    def test_bool_true(self):
        self.prog.write("true")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        symToken = Token("true", True, 
                               TokenType.BOOL, 1, 4)
        self.assertListEqual(tokens, [symToken])
        
    def test_bool_false(self):
        self.prog.write("false")
        self.prog.seek(0)
        tokens = lex(self.prog)[0]
        symToken = Token("false", False, 
                               TokenType.BOOL, 1, 5)
        self.assertListEqual(tokens, [symToken])
