from contextvars import ContextVar, copy_context

from anysync import anysync


def syncify_with_context(func):
    @anysync
    async def inner_wrapper(*a, **kw):
        val = await func(*a, **kw)
        ctx = copy_context()
        return val, ctx

    def outer_wrapper(*a, **kw):
        val, ctx = inner_wrapper(*a, **kw).run()
        for var_obj, var_val in ctx.items():
            var_obj.set(var_val)
        return val

    return outer_wrapper


var = ContextVar("var", default=0)


@syncify_with_context
async def set_var():
    var.set(42)


set_var()

assert var.get() == 42
