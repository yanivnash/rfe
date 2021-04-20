"""
    Tests for arp-to-hosts
"""
from mock import MagicMock, patch  # create_autospec
import pytest
import arp_to_hosts.arp_to_hosts as test

TAB = test.TAB
NL = test.NL


def reset_mocks(*mocks):
    """ Resets all the mocks passed in
    """
    for mock in mocks:
        mock.reset_mock()


def test_sanitize_hostname():
    """ Tests sanitize_hostname
    """
    assertions = {
        "foo": "foo",
        " foo ": "foo",
        "foo / -- (bar)": "foo-bar",
        ")": None,
        "": None,
    }

    for hostname, result in assertions.items():
        assert test.sanitize_hostname(hostname) == result


@patch("delegator.run")
def test_discover_hosts(delegator_run):
    """ Tests discover_hosts
    """

    # Happy Path, single item
    arp_scan_output = "a" + TAB + "b" + TAB + "c"
    delegator_run.return_value = MagicMock(return_code=0, out=arp_scan_output)
    response = test.discover_hosts()
    assert delegator_run.call_count == 1
    assert len(response) == 1
    assert response["a"] == "c"
    reset_mocks(delegator_run)

    # Happy Path, multiple items, reversed order
    arp_scan_output = "d" + TAB + "e" + TAB + "f" + NL + "a" + TAB + "b" + TAB + "c"
    delegator_run.return_value = MagicMock(return_code=0, out=arp_scan_output)
    response = test.discover_hosts()
    assert len(response) == 2
    assert response["a"] == "c"
    assert response["d"] == "f"
    reset_mocks(delegator_run)

    # arp-scan no worky
    delegator_run.return_value = MagicMock(return_code=1)
    with pytest.raises(IOError):
        response = test.discover_hosts()
