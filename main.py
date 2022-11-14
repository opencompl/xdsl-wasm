import sys
import ppci.wasm as parser

import dialect.wasm as wasm

from xdsl.ir import Region, MLContext
from xdsl.dialects.func import Func, FuncOp
from xdsl.printer import Printer

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <wasm file>")
    sys.exit(1)

infile = sys.argv[1]

with open(infile, "rb") as f:
    module = parser.Module(f)

print(module)

sections = module.get_definitions_per_section()

functions = sections["func"]

ctx = MLContext()
wasm.WASM(ctx)
Func(ctx)

printer = Printer(sys.stderr)


def build_instrs(instrs):
    mlir_instrs = []
    for instr in instrs:
        if type(instr) is parser.BlockInstruction:
            # Block Instructions
            raise NotImplementedError(instr.to_string())
        else:
            # Other Instructions
            op = instr[0]
            if op == "local.get":
                mlir_instrs += [wasm.LocalGet.get(instr[1][0].index)]
            elif op == "i32.add":
                mlir_instrs += [wasm.i32Add.get()]
            else:
                raise NotImplementedError(op)

    return mlir_instrs


for func in functions:
    instrs = build_instrs(func.instructions)
    fid = func.id

    region = Region.get(instrs)
    funcOp = FuncOp.from_region("func" + str(fid), [], [], region)
    printer.print_op(funcOp)
