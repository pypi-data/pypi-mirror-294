from __future__ import annotations
import typing as t

import kye.type.types as typ
from kye.vm.op import OP
from kye.compiled import Compiled, Model, Edge, Assertion, Expr, Cmd

def decompile(compiled: Compiled) -> typ.Types:
    types: typ.Types = {}
    
    for model in compiled.models.values():
        types[model.name] = decompile_model(model)
    
    for model in compiled.models.values():
        ir = types[model.name]
        for edge in model.edges.values():
            ir.define(decompile_edge(types, model.name, edge))
        for assertion in model.assertions:
            ir.assertions.append(decompile_assertion(assertion))

    return types

def decompile_model(model: Model) -> typ.Model:
    return typ.Model(
        name=model.name,
        source=model.name,
        indexes=typ.Indexes(model.indexes),
        loc=None,
    )

def decompile_edge(types: typ.Types, model: str, edge: Edge) -> typ.Edge:
    expr = None
    if edge.expr:
        expr = decompile_expr(edge.expr)
    
    returns = None
    if edge.type:
        returns = types[edge.type]
    
    return typ.Edge(
        name=edge.name,
        title=edge.title,
        indexes=typ.Indexes([]),
        allows_null=edge.null,
        allows_many=edge.many,
        model=types[model],
        returns=returns,
        expr=expr,
        loc=None,
    )

def decompile_assertion(assertion: Assertion) -> typ.Assertion:
    return typ.Assertion(
        expr=decompile_expr(assertion.expr),
        loc=None,
    )

def decompile_expr(expr: Expr) -> typ.Cmd:
    stack = list(expr)
    
    def pop() -> typ.Cmd:
        cmd = stack.pop()
        num_args = cmd.op.arity
        num_from_stack = num_args - len(cmd.args)
        assert len(stack) >= num_from_stack
        args = [pop() for _ in range(num_from_stack)]
        args += cmd.args
        return typ.Cmd(cmd.op, args)
    
    return pop()