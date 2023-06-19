# Usage

```{caution}
This page is not yet accurate.  A _relevant_ snippet is below as a place-holder, but this does not reflect the intended usage pattern, yet.
```

PolyConf uses several primary objects:

Context
: Holds runtime information such as the application's name, prefix, etc.
  After the library is run, the `result` attribute will contain all the found data.
  (Note, the _name_ "result" is under review and may change.)
  The `Context` may be given initial data via the `given` attribute.

Plugin
: Is responsible for querying potential configuration data from a particular source.
  Ultimately, it contributes data to the `Context.result`.

Registry
: Is the container of plugins and external entrypoint for running PolyConf.
  The plugins may be statically defined or discovered automatically.

In summary, a `Registry` contains an ordered iterable of `Plugins`.
When `Registry.resolve` is given an initial `Context`,
each `Plugin` will contribute data to `Context.result`,
which is the object returned to the Library user.[^obj-returned]

[^obj-returned]: This is still under review because the _type_ of `Context.result` is PolyConf-specific (see notes on `Datum` under [Data Structure Design](#data-structure-design)).
We may return the cast `dict`, instead.


## Behind The Scenes

Although not directly related to usage, it is helpful to know a bit about how PolyConf works.

(data-structure-design)=
### Data Structure Design

Data collected `Plugins` is cast to `Datum` objects,
which store primitive types (aligned with JSON) with extra metadata to record where the data came from.
A `Datum` looks slightly different, depending on if the wrapped data is "scalar" or a "collection"
(see TBD for explicit definitions).

Of note:
* Scalar `Datums` use `value` and not `children`.
* Collection `Datums` use `children` and not `value`.
* `children` members are also `Datums`.
* `Datums` are cast into native types with `Datum.as_native_value` (property).
* Serialization produces a py-native datum representation.
* List collections use the index number as the `name`.
* Dictionary collections use the key as the `name`.

```{code} python
scalar_1 = Datum(
    name="a_string",
    value="foobar",
    sources={"mock_flat://action"},
)
scalar_2 = Datum(
    name="an_integer",
    value=99,
    sources={"mock_flat://action"},
)
collection_1 = Datum(
    name="a_list",
    children={
        Datum(name=0, value="one", sources={"mock_flat://significant"}),
        Datum(name=1, value="two", sources={"mock_flat://significant"}),
        Datum(name=2, value="three", sources={"mock_flat://significant"}),
    },
    sources={"mock_flat://significant"},
)
collection_2 = Datum(
    name="a_dictionary",
    children={
        Datum(name="foo", value="FOO", sources={"mock_flat://significant"}),
        Datum(name="bar", value="BAR", sources={"mock_flat://significant"}),
        Datum(name="baz", value="BAZ", sources={"mock_flat://significant"}),
    },
    sources={"mock_flat://significant"},
)

# Cast to native values
assert scalar_1.as_native_value == 'foobar'
assert scalar_2.as_native_value == 99
assert collection_1.as_native_value == ['three', 'one', 'two']
assert collection_2.as_native_value == {'foo': 'FOO', 'baz': 'BAZ', 'bar': 'BAR'}

# Serialized
assert scalar_1.serialize() =={
    'name': 'a_string',
    'value': 'foobar',
    'sources': ['mock_flat://action'],
}
assert scalar_2.serialize() =={
    'name': 'an_integer',
    'value': 99,
    'sources': ['mock_flat://action'],
}
assert collection_1.serialize() =={
    'name': 'a_list',
    'children': [
        {'name': 0, 'value': 'one', 'sources': ['mock_flat://significant']},
        {'name': 1, 'value': 'two', 'sources': ['mock_flat://significant']},
        {'name': 2, 'value': 'three', 'sources': ['mock_flat://significant']},
    ],
    'sources': ['mock_flat://significant'],
}
assert collection_2.serialize() =={
    'name': 'a_dictionary',
    'children': [
        {'name': 'bar', 'value': 'BAR', 'sources': ['mock_flat://significant']},
        {'name': 'baz', 'value': 'BAZ', 'sources': ['mock_flat://significant']},
        {'name': 'foo', 'value': 'FOO', 'sources': ['mock_flat://significant']},
    ],
    'sources': ['mock_flat://significant'],
}
```


## Code

```{code} python
from polyconf.core.registry import Registry
from polyconf.core import model


r = Registry(selected_plugins=["ALL"])
print(f"{r.available_plugins=}")

ctx_in = model.Context(app_name="foo")
ctx_out = r.resolve(ctx_in)
print(f"{ctx_out=}")
```
