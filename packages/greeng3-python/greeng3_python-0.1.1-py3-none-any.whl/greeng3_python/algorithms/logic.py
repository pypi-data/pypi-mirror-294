def distribute_cnf(p, q):
    if isinstance(p, And):
        return And(distribute_cnf(p.p, q), distribute_cnf(p.q, q))
    if isinstance(q, And):
        return And(distribute_cnf(p, q.p), distribute_cnf(p, q.q))
    return Or(p, q)


class Formula(object):
    def __init__(self, p=None, q=None):
        self.p = p
        self.q = q

    def evaluate(self):
        raise NotImplementedError

    def variables(self):
        raise NotImplementedError

    def to_nnf(self):
        raise NotImplementedError

    def to_cnf(self):
        raise NotImplementedError


class BinaryGate(Formula):
    def __init__(self, p, q):
        super().__init__(p, q)

    def evaluate(self):
        raise NotImplementedError

    def variables(self):
        return self.p.variables() + self.q.variables()


class And(BinaryGate):
    def __init__(self, p, q):
        super().__init__(p, q)

    def evaluate(self):
        return self.p.evaluate() and self.q.evaluate()

    def to_nnf(self):
        return And(p.to_nnf(), q.to_nnf())

    def to_cnf(self):
        return And(self.p.to_nnf(), self.q.to_nnf())


class Or(Formula):
    def __init__(self, p, q):
        super().__init__(p, q)

    def evaluate(self):
        return self.p.evaluate() or self.q.evaluate()

    def to_nnf(self):
        return Or(p.to_nnf(), q.to_nnf())

    def to_cnf(self):
        return distribute_cnf(self.p.to_cnf(), self.q.to_cnf())


class Not(Formula):
    def __init__(self, p):
        self.p = p

    def evaluate(self):
        return not self.p.evaluate()

    def variables(self):
        return self.p.variables()

    def to_nnf(self):
        if isinstance(self.p, And):
            return Or(Not(self.p.p), Not(self.p.q))
        if isinstance(self.p, Or):
            return And(Not(self.p.p), Not(self.p.q))
        if isinstance(self.p, Not):
            return self.p.p
        return self

    def to_cnf(self):
        return self


class Variable(Formula):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

    def variables(self):
        return [self]

    def to_nnf(self):
        return self

    def to_cnf(self):
        return self


class Clause(object):
    def __init__(self):
        self.literals = []

    def contains(self, literal):
        if not self.is_literal(literal):
            raise ValueError('formula is not a literal')
        for formula in self.literals:
            if self.literal_equals(formula, literal):
                return True
        return False

    def remove_literal(self, literal):
        if not self.is_literal(literal):
            raise ValueError('formula is not a literal')
        clause = Clause()
        clause.literals = [x for x in self.literals if not self.literal_equals(x, literal)]
        return clause

    def literal_equals(self, p, q):
        if isinstance(p, Variable) and isinstance(q, Variable):
            return p == q
        if isinstance(p, Not) and isinstance(q, Not):
            return self.literal_equals(p.p, q.p)
        return False

    def is_literal(self, literal):
        return isinstance(literal, Variable) or (isinstance(literal, Not) and isinstance(literal.p, Variable))


class Cnf(object):
    def __init__(self, conjunction=None):
        self.clauses = self.remove_parenthesis(conjunction) if conjunction else []

    def remove_parenthesis(self, conjunction):
        pass


def test1():
    p = Variable(False)
    q = Variable(False)
    formula = Or(Not(p), q)
    assert formula.evaluate()
    p.value = True
    assert not formula.evaluate()


if __name__ == '__main__':
    test1()
