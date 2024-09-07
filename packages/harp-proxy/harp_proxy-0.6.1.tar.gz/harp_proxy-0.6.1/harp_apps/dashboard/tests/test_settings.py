import pytest

from harp.config import asdict
from harp.errors import ConfigurationError

from ..settings import DashboardAuthSetting, DashboardSettings


def test_no_auth():
    assert DashboardAuthSetting() is None
    assert DashboardAuthSetting(type="") is None
    assert DashboardAuthSetting(type=None) is None


def test_invalid_auth():
    with pytest.raises(ConfigurationError):
        DashboardAuthSetting(type=None, value="no chance")

    with pytest.raises(ConfigurationError):
        DashboardAuthSetting(type="invalid")


def test_basic_auth():
    settings = DashboardAuthSetting(
        type="basic",
        algorithm="plain",
        users={"foo": "bar"},
    )
    assert asdict(settings) == {
        "type": "basic",
        "algorithm": "plain",
        "users": {"foo": "bar"},
    }


def test_no_devserver():
    settings = DashboardSettings()

    assert settings.devserver.enabled is True


def test_devserver_disable():
    settings = DashboardSettings(devserver={"enabled": False})

    assert settings.devserver.enabled is False
