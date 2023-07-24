#!/usr/bin/env bash

# This is a quick-n-easy hack to demo the required scaffolding.
# I like the idea of this helper, but it will probably be migrated to polyconf-cli and native Python.

set -euo pipefail

_NAME="${1:-}"
PARENT_DIR="${2:-}"

PARENT_DIR="${PARENT_DIR%*/}"

[[ -n "${_NAME}" ]] || { echo "Usage: init-new-plugin.sh NAME PARENT_DIR" ; exit 1 ; }
[[ -n "${PARENT_DIR}" ]] || { echo "Usage: init-new-plugin.sh NAME PARENT_DIR" ; exit 1 ; }
[[ -d "${PARENT_DIR}" ]] || { echo "Not a directory! ${PARENT_DIR}" ; exit 1 ; }

NAME="${_NAME,,}"
TITLE="${NAME^}"

PLUGIN_DIR="polyconf-plugin-${NAME}"

cd "${PARENT_DIR}" || { echo "Could not cd to ${PARENT_DIR}" ; exit 1 ; }

[[ -e "${NAME}" ]] && { echo "\"${NAME}\" already exists in \"${PARENT_DIR}\"!" ; exit 1 ; }
mkdir "${PLUGIN_DIR}"
cd "${PLUGIN_DIR}"

git init

mkdir -p "src/polyconf/plugins/${NAME}"
touch "src/polyconf/plugins/${NAME}/__init__.py"

TEMPLATE="from polyconf.core.model import Context, Status
from polyconf.core.model.plugin import Plugin


class ${TITLE}Plugin(Plugin):
    name = \"${NAME}\"
    is_flat = True  # TODO: Review this value

    def hydrate(self, context: Context) -> Context:
        \"\"\"Result value hydrator.

        # TODO: Implement me!
        \"\"\"
        # Not necessary to \"say hi\" here, but it's useful for debugging
        self.logger.info(f'{self.name} says, \"hello\"')

        # [Do work here]
        # To contribute config values to the result, call this (often in a loop):
        self.add_result(name=..., value=..., context=context, source=...)

        # Update status and pass along the context
        context.status = Status.OK
        return context


def factory(*args, **kwargs):
    return ${TITLE}Plugin(*args, **kwargs)
"

echo "${TEMPLATE}" > "src/polyconf/plugins/${NAME}/plugin.py"
echo "Created project layout:"
find . -not -path '*/.*' -type f
