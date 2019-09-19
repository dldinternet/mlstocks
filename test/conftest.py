

def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "behavioural: distinguish behavioural tests"
    )
