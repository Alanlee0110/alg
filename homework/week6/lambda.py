#!/usr/bin/env python3
import sys
import re

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


class Term:
    pass


class Var(Term):
    __slots__ = ("name",)

    def __init__(self, name):
        self.name = name


class Abs(Term):
    __slots__ = ("param", "body")

    def __init__(self, param, body):
        self.param = param
        self.body = body


class App(Term):
    __slots__ = ("fn", "arg")

    def __init__(self, fn, arg):
        self.fn = fn
        self.arg = arg


def tokenize(s):
    tokens = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
            continue
        if c in "\\λ":
            tokens.append("\\")
            i += 1
            continue
        if c == ".":
            tokens.append(".")
            i += 1
            continue
        if c in "()":
            tokens.append(c)
            i += 1
            continue
        if c == "=":
            tokens.append("=")
            i += 1
            continue
        if s.startswith("->", i):
            tokens.append(".")
            i += 2
            continue
        m = re.match(r"[A-Za-z_][A-Za-z0-9_']*", s[i:])
        if m:
            tokens.append(m.group(0))
            i += len(m.group(0))
            continue
        raise SyntaxError(f"無法識別的符號: {c!r}")
    return tokens


class Parser:
    def __init__(self, tokens):
        self.toks = tokens
        self.i = 0

    def peek(self):
        return self.toks[self.i] if self.i < len(self.toks) else None

    def advance(self):
        t = self.peek()
        self.i += 1
        return t

    def parse(self):
        t = self.parse_expr()
        if self.peek() is not None:
            raise SyntaxError(f"多餘的符號: {self.peek()!r}")
        return t

    def parse_expr(self):
        if self.peek() == "\\":
            self.advance()
            params = []
            while self.peek() is not None and self.peek() != ".":
                params.append(self.advance())
            if self.peek() != ".":
                raise SyntaxError("lambda 缺少 '.'")
            self.advance()
            body = self.parse_expr()
            for p in reversed(params):
                body = Abs(p, body)
            return body
        return self.parse_app()

    def parse_app(self):
        t = self.parse_atom()
        while self.peek() is not None and self.peek() not in (")", "="):
            t = App(t, self.parse_atom())
        return t

    def parse_atom(self):
        t = self.peek()
        if t is None:
            raise SyntaxError("表示式不完整")
        if t == "(":
            self.advance()
            e = self.parse_expr()
            if self.advance() != ")":
                raise SyntaxError("缺少 ')'")
            return e
        if t in ("\\", ")", ".", "="):
            raise SyntaxError(f"意外的符號: {t!r}")
        self.advance()
        return Var(t)


def parse(text):
    return Parser(tokenize(text)).parse()


def free_vars(t):
    if isinstance(t, Var):
        return {t.name}
    if isinstance(t, Abs):
        return free_vars(t.body) - {t.param}
    return free_vars(t.fn) | free_vars(t.arg)


_fresh = [0]


def fresh(name):
    _fresh[0] += 1
    return f"{name}{_fresh[0]}"


def subst(t, var, repl):
    if isinstance(t, Var):
        return repl if t.name == var else t
    if isinstance(t, Abs):
        if t.param == var:
            return t
        if t.param in free_vars(repl):
            newp = fresh(t.param)
            body = subst(t.body, t.param, Var(newp))
            return Abs(newp, subst(body, var, repl))
        return Abs(t.param, subst(t.body, var, repl))
    return App(subst(t.fn, var, repl), subst(t.arg, var, repl))


def show(t, prec=0):
    if isinstance(t, Var):
        return t.name
    if isinstance(t, Abs):
        s = "\\" + t.param + "." + show(t.body, 0)
        return "(" + s + ")" if prec > 0 else s
    s = show(t.fn, 1) + " " + show(t.arg, 2)
    return "(" + s + ")" if prec > 1 else s


def reduce_once(t):
    if isinstance(t, App):
        if isinstance(t.fn, Abs):
            return subst(t.fn.body, t.fn.param, t.arg)
        nxt = reduce_once(t.fn)
        if nxt is not None:
            return App(nxt, t.arg)
        nxt = reduce_once(t.arg)
        if nxt is not None:
            return App(t.fn, nxt)
        return None
    if isinstance(t, Abs):
        nxt = reduce_once(t.body)
        if nxt is not None:
            return Abs(t.param, nxt)
    return None


def expand(t, defs, bound=frozenset()):
    if isinstance(t, Var):
        if t.name in defs and t.name not in bound:
            return defs[t.name]
        return t
    if isinstance(t, Abs):
        return Abs(t.param, expand(t.body, defs, bound | {t.param}))
    return App(expand(t.fn, defs, bound), expand(t.arg, defs, bound))


def _count_f(t, f, x):
    if isinstance(t, Var):
        return 0 if t.name == x else None
    if isinstance(t, App) and isinstance(t.fn, Var) and t.fn.name == f:
        inner = _count_f(t.arg, f, x)
        return None if inner is None else inner + 1
    return None


def church_numeral(t):
    if isinstance(t, Abs) and isinstance(t.body, Abs):
        return _count_f(t.body.body, t.param, t.body.param)
    return None


def is_true(t):
    return (isinstance(t, Abs) and isinstance(t.body, Abs)
            and isinstance(t.body.body, Var) and t.body.body.name == t.param)


def is_false(t):
    return (isinstance(t, Abs) and isinstance(t.body, Abs)
            and isinstance(t.body.body, Var)
            and t.body.body.name == t.body.param)


def describe(t):
    parts = []
    n = church_numeral(t)
    if n is not None:
        parts.append(f"Church 數字 {n}")
    if is_true(t):
        parts.append("布林值 TRUE")
    if is_false(t):
        parts.append("布林值 FALSE")
    return " / ".join(parts) if parts else None


def clip(s, limit):
    if len(s) <= limit:
        return s
    return s[:limit] + f" …(省略 {len(s) - limit} 字元)"


def evaluate(term, label, max_steps=500, max_len=600):
    print("=" * 64)
    print(f"程式: {label}")
    print("=" * 64)
    print("[起始項]")
    print("    " + clip(show(term), max_len))

    cur = term
    steps = 0
    print("[β 化簡]")
    while steps < max_steps:
        nxt = reduce_once(cur)
        if nxt is None:
            break
        cur = nxt
        steps += 1
        print(f"  {steps:>3}. {clip(show(cur), max_len)}")

    if steps >= max_steps:
        print(f"  (已達 {max_steps} 步上限，尚未化簡完畢)")
    print(f"[正規形式] (共 {steps} 步 β 化簡)")
    print("    " + clip(show(cur), max_len))
    d = describe(cur)
    if d:
        print(f"    => {d}")
    print()


def run_source(source, max_steps=500, max_len=600):
    defs = {}
    for raw in source.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_']*)\s*=\s*(.+)$", line)
        if m:
            name, rhs = m.group(1), m.group(2)
            term = expand(parse(rhs), defs)
            defs[name] = term
            continue
        term = expand(parse(line), defs)
        evaluate(term, line, max_steps=max_steps, max_len=max_len)


DEMO = r"""
TRUE  = \x.\y.x
FALSE = \x.\y.y
IF    = \p.\a.\b.p a b
NOT   = \p.p FALSE TRUE

ZERO  = \f.\x.x
ONE   = \f.\x.f x
TWO   = \f.\x.f (f x)
THREE = \f.\x.f (f (f x))
FIVE  = \f.\x.f (f (f (f (f x))))

SUCC  = \n.\f.\x.f (n f x)
PLUS  = \m.\n.\f.\x.m f (n f x)
MULT  = \m.\n.\f.m (n f)
POW   = \b.\e.e b
PRED  = \n.\f.\x.n (\g.\h.h (g f)) (\u.x) (\u.u)
SUB   = \m.\n.n PRED m
ISZERO = \n.n (\x.FALSE) TRUE

ISZERO ZERO
PLUS TWO THREE
MULT TWO THREE
POW TWO THREE
PRED THREE
SUB FIVE TWO
"""


def main():
    args = sys.argv[1:]
    if args:
        with open(args[0], encoding="utf-8") as f:
            run_source(f.read())
    else:
        run_source(DEMO)


if __name__ == "__main__":
    main()
