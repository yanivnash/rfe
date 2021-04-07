"""
    1. Runs arp-scan to scan the network
    2. Writes the resulting names and ip addrs to the /etc/hosts file
"""
from collections import OrderedDict
import re
from typing import Dict, Optional
import delegator
from python_hosts import Hosts, HostsEntry
from validators.slug import slug as is_hostname_valid

DASH = "-"
TAB = "\t"
NL = "\n"
HOSTSFILE = "/etc/hosts"
HostsDict = Dict[str, str]


def main() -> None:
    """ Gets the dict of IPs to names, writes it to the hostsfile
    """
    write_hosts(discover_hosts())


def write_hosts(hostmap: HostsDict) -> None:
    """ Writes the passed-in hostmap to the hostsfile
    """
    hosts = Hosts(path=HOSTSFILE)
    for ip_addr, hostname in hostmap.items():
        sanitized_name = sanitize_hostname(hostname)
        new_entry = HostsEntry(
            entry_type="ipv4", address=ip_addr, names=[sanitized_name]
        )
        response = hosts.add([new_entry], force=True)

    try:
        response = hosts.write()
        print(
            f"Success! {response['ipv4_entries_written']} entries written to {HOSTSFILE}"
        )
    except:  # noqa  # pylint: disable=bare-except
        print(f"ERROR: Cannot write to {HOSTSFILE}. Run with sudo?")


def discover_hosts() -> HostsDict:
    """ Runs arp-scan to return a dict of IP addrs to names
    """
    response = delegator.run("arp-scan -l --plain --ignoredups")
    if response.return_code:
        print(response.out)
        print(response.err)
        raise OSError("Error running arp-scan")

    ret = {}
    for line in response.out.split(NL):
        if not line:
            continue

        fields = line.split(TAB)
        ip_addr = fields[0]
        name = fields[2]

        sanitized_name = sanitize_hostname(name)
        if not sanitized_name:
            print(f"WARNING: Invalid hostname found: {name}: {ip_addr}. Skipping.")
            continue

        ret[ip_addr] = sanitized_name

    # replace strings in the dict values?
    ret = {k: v.replace("KNOWN-", "") for k, v in ret.items()}
    ret = OrderedDict(sorted(ret.items()))
    return ret


def sanitize_hostname(name: str) -> Optional[str]:
    """ Sanitizes a hostname according to RFC: https://tools.ietf.org/html/rfc1123#page-13
        Returns None if it couldn't fix it
    """
    ret = re.sub("[^0-9a-zA-Z]+", DASH, name)
    ret = ret.strip()
    ret = ret.strip("-")
    ret = ret[:255]

    if not is_hostname_valid(ret):
        return None

    return ret


if __name__ == "__main__":
    main()
