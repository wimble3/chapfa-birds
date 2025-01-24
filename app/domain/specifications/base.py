class Satisfaction:
    def is_satisfied_by(self, *args, **kwargs) -> bool:
        raise NotImplementedError()


class Specification(Satisfaction):
    def __and__(self, other: "Specification") -> "And":
        return And(self, other)

    def __or__(self, other: "Specification") -> "Or":
        return Or(self, other)

    def __invert__(self) -> "Not":
        return Not(self)


class And(Specification):
    def __init__(self, left: Specification, right: Specification) -> None:
        self.left = left
        self.right = right

    def is_satisfied_by(self, candidate: Satisfaction) -> bool:
        return bool(
            self.left.is_satisfied_by(candidate) and
            self.right.is_satisfied_by(candidate)
        )


class Or(Specification):
    def __init__(self, left: Specification, right: Specification) -> None:
        self.left = left
        self.right = right

    def is_satisfied_by(self, candidate: object) -> bool:
        return bool(
            self.left.is_satisfied_by(candidate) or
            self.right.is_satisfied_by(candidate)
        )


class Not(Specification):
    def __init__(self, spec: Specification):
        self.spec = spec

    def is_satisfied_by(self, candidate: object) -> bool:
        return not self.spec.is_satisfied_by(candidate)
