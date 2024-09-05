class Config:
  INFINITY = "float('inf')"
  FACTORIAL = "math.factorial"
  DERIVATIVE = "Derivative"
  CONJUGATE = "Conjugate"
  SUM = "Sum"
  PROD = "Product"
  LIMIT = "Limit"

  FLOOR = "math.floor"
  CEIL = "math.ceil"

  SQRT = "math.sqrt"

  SIN = "math.sin"
  COS = "math.cos"
  TAN = "math.tan"
  SINH = "math.sinh"
  COSH = "math.cosh"
  TANH = "math.tanh"
  CSC = "1 / math.sin"
  SEC = "1 / math.cos"
  COT = "1 / math.tan"

  ASIN = "math.asin"
  ACOS = "math.acos"
  ATAN = "math.atan"
  ASINH = "math.asinh"
  ACOSH = "math.acosh"
  ATANH = "math.atanh"

  # These are not available in the math module, and will have to be implemented
  # by the calling code, e.g by defining python functions with those names in
  # the namespace of the calling code.
  ARCCSC = "arccsc"
  ARCSEC = "arcsec"
  ARCCOT = "arccot"

  LOG = "math.log"
  EXP = "math.exp"
  ABS = "abs"

  E = "math.e"
