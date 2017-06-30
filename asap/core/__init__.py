import yaql

engine = yaql.factory.YaqlFactory().create()


def transform(data, expressions):
    assert type(expressions) == dict, \
        'expressions should be a dict'

    res = {}
    for key, value in expressions.items():
        exp = engine(value)
        res[key] = exp.evaluate(data)

    return res
