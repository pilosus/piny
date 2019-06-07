def pytest_make_parametrize_id(config, val, argname):
    """
    Prettify output for parametrized tests
    """
    if isinstance(val, dict):
        return "{}({})".format(
            argname, ", ".join("{}={}".format(k, v) for k, v in val.items())
        )
