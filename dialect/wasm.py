from dataclasses import dataclass

from typing import Type

from xdsl.ir import Operation, MLContext
from xdsl.irdl import irdl_op_definition, AttributeDef
from xdsl.dialects.builtin import IntegerAttr


@irdl_op_definition
class LocalGet(Operation):
    name: str = "wasm.local.get"

    ref = AttributeDef(IntegerAttr)

    @classmethod
    def get(cls, ref):
        return cls.build(attributes={"ref": ref})


@irdl_op_definition
class i32Add(Operation):
    name: str = "wasm.i32.add"

    @classmethod
    def get(cls):
        return cls.build()


@dataclass
class WASM:
    ctx: MLContext

    def __post_init__(self):
        self.ctx.register_op(LocalGet)
        self.ctx.register_op(i32Add)
