# Ported from latex2sympy by @augustt198
# https://github.com/augustt198/latex2sympy
# See license in LICENSE.txt
import antlr4
from importlib.metadata import version

if not version('antlr4-python3-runtime').startswith('4.11'):
  raise ImportError("LaTeX parsing requires the antlr4 Python package,"
            " provided by pip (antlr4-python3-runtime) or"
            " conda (antlr-python-runtime), version 4.11")

from .errors import LaTeXParsingError
from .gen.LaTeXParser import LaTeXParser
from .gen.LaTeXLexer import LaTeXLexer
from .config import Config


def parse_latex_with_config(sympy, config: Config, strict=False):
  # ===========================================================================
  ErrorListener = antlr4.error.ErrorListener

  if ErrorListener:
    class MathErrorListener(ErrorListener.ErrorListener):  # type:ignore # noqa:F811
      def __init__(self, src):
        super(ErrorListener.ErrorListener, self).__init__()
        self.src = src

      def syntaxError(self, recog, symbol, line, col, msg, e):
        fmt = "%s\n%s\n%s"
        marker = "~" * col + "^"
        print(msg)

        if msg.startswith("missing"):
          err = fmt % (msg, self.src, marker)
        elif msg.startswith("no viable"):
          err = fmt % ("I expected something else here", self.src, marker)
        elif msg.startswith("mismatched"):
          names = LaTeXParser.literalNames
          expected = [
            names[i] for i in e.getExpectedTokens() if i < len(names)
          ]
          if len(expected) < 10:
            expected = " ".join(expected)
            err = (fmt % ("I expected one of these: " + expected, self.src,
                    marker))
          else:
            err = (fmt % ("I expected something else here", self.src,
                    marker))
        else:
          err = fmt % ("I don't understand this", self.src, marker)
        raise LaTeXParsingError(err)


  def parse_latex(sympy, strict=False):
    sympy = sympy.strip()
    matherror = MathErrorListener(sympy)

    stream = antlr4.InputStream(sympy)
    lex = LaTeXLexer(stream)
    lex.removeErrorListeners()
    lex.addErrorListener(matherror)

    tokens = antlr4.CommonTokenStream(lex)
    parser = LaTeXParser(tokens)

    # remove default console error listener
    parser.removeErrorListeners()
    parser.addErrorListener(matherror)

    relation = parser.math().relation()
    if strict and (relation.start.start != 0 or relation.stop.stop != len(sympy) - 1):
      raise LaTeXParsingError("Invalid LaTeX")

    expr = convert_relation(relation)

    return expr


  def convert_relation(rel):
    if rel.expr():
      return convert_expr(rel.expr())

    lh = convert_relation(rel.relation(0))
    rh = convert_relation(rel.relation(1))
    if rel.LT():
      return f"({lh} < {rh})"
    elif rel.LTE():
      return f"({lh} <= {rh})"
    elif rel.GT():
      return f"({lh} > {rh})"
    elif rel.GTE():
      return f"({lh} >= {rh})"
    elif rel.EQUAL():
      return f"({lh} == {rh})"
    elif rel.NEQ():
      return f"({lh} != {rh})"
    else:
      raise LaTeXParsingError("Unknown relation type")


  def convert_expr(expr):
    return convert_expr_relation(expr.expr_relation())
  

  def convert_expr_relation(rel):
    if rel is None:
      return None
    lh = convert_expr_relation(rel.expr_relation(0))
    rh = convert_expr_relation(rel.expr_relation(1))
    if lh is None and rh is None:
      return convert_add(rel.additive())
    elif rel.LT():
      return f"({lh} < {rh})"
    elif rel.LTE():
      return f"({lh} <= {rh})"
    elif rel.GT():
      return f"({lh} > {rh})"
    elif rel.GTE():
      return f"({lh} >= {rh})"
    elif rel.EQUAL():
      return f"({lh} == {rh})"
    elif rel.NEQ():
      return f"({lh} != {rh})"
    else:
      return convert_add(rel.additive())


  def convert_add(add):
    if add.ADD():
      lh = convert_add(add.additive(0))
      rh = convert_add(add.additive(1))
      return f"({lh} + {rh})"
    elif add.SUB():
      lh = convert_add(add.additive(0))
      rh = convert_add(add.additive(1))
      if hasattr(rh, "is_Atom") and rh.is_Atom:
        return f"({lh} - {rh})"
      return f"({lh} - {rh})"
    else:
      return convert_mp(add.mp())


  def convert_mp(mp):
    if hasattr(mp, 'mp'):
      mp_left = mp.mp(0)
      mp_right = mp.mp(1)
    else:
      mp_left = mp.mp_nofunc(0)
      mp_right = mp.mp_nofunc(1)

    if mp.MUL() or mp.CMD_TIMES() or mp.CMD_CDOT():
      lh = convert_mp(mp_left)
      rh = convert_mp(mp_right)
      return f"({lh} * {rh})"
    elif mp.DIV() or mp.CMD_DIV() or mp.COLON():
      lh = convert_mp(mp_left)
      rh = convert_mp(mp_right)
      return f"({lh} / {rh})"
    else:
      if hasattr(mp, 'unary'):
        return convert_unary(mp.unary())
      else:
        return convert_unary(mp.unary_nofunc())


  def convert_unary(unary):
    if hasattr(unary, 'unary'):
      nested_unary = unary.unary()
    else:
      nested_unary = unary.unary_nofunc()
    if hasattr(unary, 'postfix_nofunc'):
      first = unary.postfix()
      tail = unary.postfix_nofunc()
      postfix = [first] + tail
    else:
      postfix = unary.postfix()

    if unary.ADD():
      return convert_unary(nested_unary)
    elif unary.SUB():
      numabs = convert_unary(nested_unary)
      # Use Integer(-n) instead of Mul(-1, n)
      return f"-{numabs}"
    elif postfix:
      return convert_postfix_list(postfix)


  def convert_postfix_list(arr: list, i: int = 0):
    if i >= len(arr):
      raise LaTeXParsingError("Index out of bounds")

    res = convert_postfix(arr[i])

    if i == len(arr) - 1:
      return res  # nothing to multiply by
    else:
      if i > 0:
        left = convert_postfix(arr[i - 1])
        right = convert_postfix(arr[i + 1])

        if not (left or right) and str(res) == 'x':
          return convert_postfix_list(arr, i + 1)

      return f"({res} * {convert_postfix_list(arr, i + 1)})"


  def do_subs(expr, at):
    if at.expr():
      at_expr = convert_expr(at.expr())
      syms = at_expr.atoms()
      if len(syms) == 0:
        return expr
      elif len(syms) > 0:
        sym = next(iter(syms))
        return expr.subs(sym, at_expr)
    elif at.equality():
      lh = convert_expr(at.equality().expr(0))
      rh = convert_expr(at.equality().expr(1))
      return expr.subs(lh, rh)


  def convert_postfix(postfix):
    if hasattr(postfix, 'exp'):
      exp_nested = postfix.exp()
    else:
      exp_nested = postfix.exp_nofunc()

    exp = convert_exp(exp_nested)
    for op in postfix.postfix_op():
      if op.BANG():
        if isinstance(exp, list):
          raise LaTeXParsingError("Cannot apply postfix to derivative.")
        exp = f"{config.FACTORIAL}({exp})"
      elif op.eval_at():
        ev = op.eval_at()
        at_b = None
        at_a = None
        if ev.eval_at_sup():
          at_b = do_subs(exp, ev.eval_at_sup())
        if ev.eval_at_sub():
          at_a = do_subs(exp, ev.eval_at_sub())
        if at_b is not None and at_a is not None:
          exp = f"({at_b} - {at_a})"
        elif at_b is not None:
          exp = at_b
        elif at_a is not None:
          exp = at_a

    return exp


  def convert_exp(exp):
    if hasattr(exp, 'exp'):
      exp_nested = exp.exp()
    else:
      exp_nested = exp.exp_nofunc()

    if exp_nested:
      base = convert_exp(exp_nested)
      if isinstance(base, list):
        raise LaTeXParsingError("Cannot raise derivative to power")
      if exp.atom():
        exponent = convert_atom(exp.atom())
      elif exp.expr():
        exponent = convert_expr(exp.expr())
      return f"({base} ** {exponent})"
    else:
      if hasattr(exp, 'comp'):
        return convert_comp(exp.comp())
      else:
        return convert_comp(exp.comp_nofunc())


  def convert_comp(comp):
    if comp.group():
      return convert_expr(comp.group().expr())
    elif comp.abs_group():
      return f"{config.ABS}({convert_expr(comp.abs_group().expr())})"
    elif comp.atom():
      return convert_atom(comp.atom())
    elif comp.floor():
      return convert_floor(comp.floor())
    elif comp.ceil():
      return convert_ceil(comp.ceil())
    elif comp.func():
      return convert_func(comp.func())


  def convert_atom(atom):
    if atom.LETTER():
      sname = atom.LETTER().getText()
      if atom.subexpr():
        if atom.subexpr().expr():  # subscript is expr
          subscript = convert_expr(atom.subexpr().expr())
        else:  # subscript is atom
          subscript = convert_atom(atom.subexpr().atom())
        sname += '_{' + subscript + '}'
      if atom.SINGLE_QUOTES():
        sname += atom.SINGLE_QUOTES().getText()  # put after subscript for easy identify
      return sname
    elif atom.SYMBOL():
      s = atom.SYMBOL().getText()[1:]
      if s == "infty":
        return config.INFINITY
      else:
        if atom.subexpr():
          subscript = None
          if atom.subexpr().expr():  # subscript is expr
            subscript = convert_expr(atom.subexpr().expr())
          else:  # subscript is atom
            subscript = convert_atom(atom.subexpr().atom())
          subscriptName = subscript
          s += '_{' + subscriptName + '}'
        return s
    elif atom.number():
      s = atom.number().getText().replace(",", "")
      return s
    elif atom.DIFFERENTIAL():
      var = get_differential_var(atom.DIFFERENTIAL())
      return f"d{var}"
    elif atom.mathit():
      text = rule2text(atom.mathit().mathit_text())
      return text
    elif atom.frac():
      return convert_frac(atom.frac())
    elif atom.binom():
      return convert_binom(atom.binom())
    else:
      raise LaTeXParsingError("Unknown atom type")

  def rule2text(ctx):
    stream = ctx.start.getInputStream()
    # starting index of starting token
    startIdx = ctx.start.start
    # stopping index of stopping token
    stopIdx = ctx.stop.stop

    return stream.getText(startIdx, stopIdx)


  def convert_frac(frac):
    diff_op = False
    partial_op = False
    if frac.lower and frac.upper:
      lower_itv = frac.lower.getSourceInterval()
      lower_itv_len = lower_itv[1] - lower_itv[0] + 1
      if (frac.lower.start == frac.lower.stop
          and frac.lower.start.type == LaTeXLexer.DIFFERENTIAL):
        wrt = get_differential_var_str(frac.lower.start.text)
        diff_op = True
      elif (lower_itv_len == 2 and frac.lower.start.type == LaTeXLexer.SYMBOL
          and frac.lower.start.text == '\\partial'
          and (frac.lower.stop.type == LaTeXLexer.LETTER
            or frac.lower.stop.type == LaTeXLexer.SYMBOL)):
        partial_op = True
        wrt = frac.lower.stop.text
        if frac.lower.stop.type == LaTeXLexer.SYMBOL:
          wrt = wrt[1:]

      if diff_op or partial_op:
        if (diff_op and frac.upper.start == frac.upper.stop
            and frac.upper.start.type == LaTeXLexer.LETTER
            and frac.upper.start.text == 'd'):
          return [wrt]
        elif (partial_op and frac.upper.start == frac.upper.stop
            and frac.upper.start.type == LaTeXLexer.SYMBOL
            and frac.upper.start.text == '\\partial'):
          return [wrt]
        upper_text = rule2text(frac.upper)

        expr_top = None
        if diff_op and upper_text.startswith('d'):
          expr_top = parse_latex(upper_text[1:])
        elif partial_op and frac.upper.start.text == '\\partial':
          expr_top = parse_latex(upper_text[len('\\partial'):])
        if expr_top:
          return f"{config.DERIVATIVE}({expr_top}, {wrt})"
    if frac.upper:
      expr_top = convert_expr(frac.upper)
    else:
      expr_top = frac.upperd.text
    if frac.lower:
      expr_bot = convert_expr(frac.lower)
    else:
      expr_bot = frac.lowerd.text
    inverse_denom = f"(1 / {expr_bot})"
    if expr_top == 1:
      return inverse_denom
    else:
      return f"({expr_top} / {expr_bot})"

  def convert_binom(binom):
    expr_n = convert_expr(binom.n)
    expr_k = convert_expr(binom.k)
    return f"Binomial({expr_n}, {expr_k})"

  def convert_floor(floor):
    val = convert_expr(floor.val)
    return f"{config.FLOOR}({val})"

  def convert_ceil(ceil):
    val = convert_expr(ceil.val)
    return f"{config.CEIL}({val})"

  def convert_func(func):
    if func.func_normal():
      if func.L_PAREN():  # function called with parenthesis
        arg = convert_func_arg(func.func_arg())
      else:
        arg = convert_func_arg(func.func_arg_noparens())

      name = func.func_normal().start.text[1:]

      # change arc<trig> -> a<trig>
      if name in [
        "arcsin", "arccos", "arctan", "arccsc", "arcsec", "arccot"
      ]:
        name = "a" + name[3:]
        expr = f"{getattr(config, name.upper())}({arg})"
      if name in ["arsinh", "arcosh", "artanh"]:
        name = "a" + name[2:]
        expr = f"{getattr(config, name.upper())}({arg})"

      if name == "exp":
        expr = f"{config.EXP}({arg})"

      if name in ("log", "lg", "ln"):
        if func.subexpr():
          if func.subexpr().expr():
            base = convert_expr(func.subexpr().expr())
          else:
            base = convert_atom(func.subexpr().atom())
        elif name == "lg":  # ISO 80000-2:2019
          base = 10
        elif name in ("ln", "log"):  # SymPy's latex printer prints ln as log by default
          base = config.E
        expr = f"{config.LOG}({arg}, {base})"

      func_pow = None
      should_pow = True
      if func.supexpr():
        if func.supexpr().expr():
          func_pow = convert_expr(func.supexpr().expr())
        else:
          func_pow = convert_atom(func.supexpr().atom())

      if name in [
        "sin", "cos", "tan", "csc", "sec", "cot", "sinh", "cosh", "tanh"
      ]:
        if func_pow == -1:
          name = "a" + name
          should_pow = False
        
        expr = f"{getattr(config, name.upper())}({arg})"

      if func_pow and should_pow:
        expr = f"({expr} ** {func_pow})"

      return expr

    elif func.LETTER() or func.SYMBOL():
      if func.LETTER():
        fname = func.LETTER().getText()
      elif func.SYMBOL():
        fname = func.SYMBOL().getText()[1:]
      fname = str(fname)  # can't be unicode
      if func.subexpr():
        if func.subexpr().expr():  # subscript is expr
          subscript = convert_expr(func.subexpr().expr())
        else:  # subscript is atom
          subscript = convert_atom(func.subexpr().atom())
        subscriptName = subscript
        fname += '_{' + subscriptName + '}'
      if func.SINGLE_QUOTES():
        fname += func.SINGLE_QUOTES().getText()
      input_args = func.args()
      output_args = []
      while input_args.args():  # handle multiple arguments to function
        output_args.append(convert_expr(input_args.expr()))
        input_args = input_args.args()
      output_args.append(convert_expr(input_args.expr()))
      return f"{fname}({', '.join(output_args)})"
    elif func.FUNC_INT():
      raise NotImplementedError("Integral is not supported.")
    elif func.FUNC_SQRT():
      expr = convert_expr(func.base)
      if func.root:
        r = convert_expr(func.root)
        return f"({expr} ** (1 / {r}))"
      else:
        return f"{config.SQRT}({expr})"
    elif func.FUNC_OVERLINE():
      expr = convert_expr(func.base)
      return f"{config.CONJUGATE}({expr})"
    elif func.FUNC_SUM():
      return handle_sum_or_prod(func, "summation")
    elif func.FUNC_PROD():
      return handle_sum_or_prod(func, "product")
    elif func.FUNC_LIM():
      return handle_limit(func)


  def convert_func_arg(arg):
    if hasattr(arg, 'expr'):
      return convert_expr(arg.expr())
    else:
      return convert_mp(arg.mp_nofunc())


  # def handle_integral(func):
  #     if func.additive():
  #         integrand = convert_add(func.additive())
  #     elif func.frac():
  #         integrand = convert_frac(func.frac())
  #     else:
  #         integrand = 1

  #     int_var = None
  #     if func.DIFFERENTIAL():
  #         int_var = get_differential_var(func.DIFFERENTIAL())
  #     else:
  #         for sym in integrand.atoms(sympy.Symbol):
  #             s = str(sym)
  #             if len(s) > 1 and s[0] == 'd':
  #                 if s[1] == '\\':
  #                     int_var = sympy.Symbol(s[2:])
  #                 else:
  #                     int_var = sympy.Symbol(s[1:])
  #                 int_sym = sym
  #         if int_var:
  #             integrand = integrand.subs(int_sym, 1)
  #         else:
  #             # Assume dx by default
  #             int_var = sympy.Symbol('x')

  #     if func.subexpr():
  #         if func.subexpr().atom():
  #             lower = convert_atom(func.subexpr().atom())
  #         else:
  #             lower = convert_expr(func.subexpr().expr())
  #         if func.supexpr().atom():
  #             upper = convert_atom(func.supexpr().atom())
  #         else:
  #             upper = convert_expr(func.supexpr().expr())
  #         return sympy.Integral(integrand, (int_var, lower, upper))
  #     else:
  #         return sympy.Integral(integrand, int_var)


  def handle_sum_or_prod(func, name):
    val = convert_mp(func.mp())
    iter_var = convert_expr(func.subeq().equality().expr(0))
    start = convert_expr(func.subeq().equality().expr(1))
    if func.supexpr().expr():  # ^{expr}
      end = convert_expr(func.supexpr().expr())
    else:  # ^atom
      end = convert_atom(func.supexpr().atom())

    if name == "summation":
      return f"{config.SUM}({val}, ({iter_var}, {start}, {end}))"
    elif name == "product":
      return f"{config.PROD}({val}, ({iter_var}, {start}, {end}))"


  def handle_limit(func):
    sub = func.limit_sub()
    if sub.LETTER():
      var = sub.LETTER().getText()
    elif sub.SYMBOL():
      var = sub.SYMBOL().getText()[1:]
    else:
      var = "x"
    if sub.SUB():
      direction = "'-'"
    elif sub.ADD():
      direction = "'+'"
    else:
      direction = "'+-'"
    approaching = convert_expr(sub.expr())
    content = convert_mp(func.mp())

    return f"{config.LIMIT}({content}, {var}, {approaching}, {direction})"


  def get_differential_var(d):
    text = get_differential_var_str(d.getText())
    return text


  def get_differential_var_str(text):
    for i in range(1, len(text)):
      c = text[i]
      if not (c == " " or c == "\r" or c == "\n" or c == "\t"):
        idx = i
        break
    text = text[idx:]
    if text[0] == "\\":
      text = text[1:]
    return text

  # ===========================================================================
  return parse_latex(sympy, strict)