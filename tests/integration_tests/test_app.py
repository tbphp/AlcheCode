from alchecode import Application


def test_app_simple_passthrough():
    app = Application("pwd 10", True)
    res = app.run()
    assert res is not None
