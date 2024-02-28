import dataclasses


@dataclasses.dataclass(frozen=True, slots=True)
class ComplexityEvaluationNode:
    name: str

    def evaluate(
        self, fragments_definition: dict[str, list["ComplexityEvaluationNode"]]
    ) -> int:
        raise NotImplementedError


@dataclasses.dataclass(frozen=True, slots=True)
class LazyFragment(ComplexityEvaluationNode):

    def evaluate(
        self, fragments_definition: dict[str, list["ComplexityEvaluationNode"]]
    ):
        nodes = fragments_definition.get(self.name)
        if not nodes:
            return 0
        return sum(
            node.evaluate(fragments_definition=fragments_definition) for node in nodes
        )


@dataclasses.dataclass(frozen=True, slots=True)
class Field(ComplexityEvaluationNode):
    complexity: int
    multiplier: int

    def evaluate(self, *args, **kwargs) -> int:
        return self.complexity * self.multiplier
