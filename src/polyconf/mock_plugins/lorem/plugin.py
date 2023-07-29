from polyconf.core.model import Context, Status
from polyconf.core.model.plugin import Plugin


class LoremPlugin(Plugin):
    name = "lorem"
    is_flat = True

    def hydrate(self, context: Context) -> Context:
        """Result value hydrator."""
        self.logger.info(f'{self.name} says, "hello"')

        fixed_name = "toy"

        self.add_result(name="brick", value="sky", context=context, source=fixed_name)
        self.add_result(name="toaster", value="ball", context=context, source=fixed_name)

        context.status = Status.OK
        return context


# TODO: Reconsider. As-is, this pattern seems unnecessary.
def factory(*args, **kwargs):
    return LoremPlugin(*args, **kwargs)
