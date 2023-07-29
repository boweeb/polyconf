from polyconf.core.model import Context, Status
from polyconf.core.model.plugin import Plugin


class IpsumPlugin(Plugin):
    name = "ipsum"
    is_flat = True

    def hydrate(self, context: Context) -> Context:
        """Result value hydrator."""
        self.logger.info(f'{self.name} says, "hello"')

        fixed_name = "rubber"

        self.add_result(name="tunnel", value="grass", context=context, source=fixed_name)
        self.add_result(name="toaster", value="BALL", context=context, source=fixed_name)

        context.status = Status.OK
        return context


def factory(*args, **kwargs):
    return IpsumPlugin(*args, **kwargs)
