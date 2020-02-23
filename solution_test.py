from solution import parse_log_line, log_statics, get_n_key_with_max_values
from functools import partial
from io import StringIO


VALID_IPS = ["168.41.191.40", "72.44.32.10", "50.112.00.11"]

FULL_URL_PATHS = [
    "http://example.net/faq",  # http protocol without end slash
    "http://example.net/faq/",  # http protocol
    "https://example.net/faq",  # https protocol
    "https://example.net/faq/",  # http protocol with end slash
]

RELATIVE_PATHS = [
    "/docs/manage-users",  # relative path which does not have end slash
    "/docs/manage-users/",  # relative path which has end slash
]

EDGE_PATHS = ["/"]

ASSET_PATHS = [
    "/asset.js",  # js script
    "/asset.css",  # css assets
]

VALID_URLS = FULL_URL_PATHS + RELATIVE_PATHS + EDGE_PATHS + ASSET_PATHS

log_format = (
    '{ip} - - [{time}] "{request_info}" {status_code} '
    '{size} "-" "{client_info}"'
)

# for this project we only care about ip addresses and request URLs in request
# info other parts are not important for for now
build_test_log = partial(
    log_format.format,
    time="09/Jul/2018:10:11:30 +0200",
    status_code="200",
    size="31232",
    client_info="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7)",
)


request_info_format = "GET {url} HTTP/1.1 "


def test_can_extract_ip():
    # request_info is not what we focus for this testcase
    request_info = request_info_format.format(url="/")

    for ip in VALID_IPS:
        log_line = build_test_log(ip=ip, request_info=request_info)
        assert ip == parse_log_line(log_line)["ip"]


def test_can_extract_url():
    # ip is not what we focus for this testcase
    ip = "192.168.1.12"

    for url in VALID_URLS:
        request_info = request_info_format.format(url=url)
        log_line = build_test_log(ip=ip, request_info=request_info)
        assert url == parse_log_line(log_line)["request_path"]


def test_get_correct_statistics():
    # as we know ip and url can be extracted correctly we only need to use
    # one of them to test whether the statistics are correct
    # in this case we use ip for testing purpose
    request_info = request_info_format.format(url="/")

    sample_ips = VALID_IPS[0:1] * 10 + VALID_IPS[1:2] * 5 + VALID_IPS[2:] * 1
    sample_log = "\n".join(
        [build_test_log(ip=ip, request_info=request_info) for ip in sample_ips]
    )
    statistics = log_statics(StringIO(sample_log), parse_log_line, ["ip"])
    assert len(statistics["ip"]) == 3, "unique ip addresses is should be 3"

    warning = 'ip address number was not recorded correctly'
    assert statistics["ip"][VALID_IPS[0]] == 10, warning
    assert statistics["ip"][VALID_IPS[1]] == 5, warning
    assert statistics["ip"][VALID_IPS[2]] == 1, warning


def test_get_n_key_with_max_values():
    sample = {
        "top1": 1000,
        "top2": 100,
        "top3": 10,
        "least": 1,
    }

    assert get_n_key_with_max_values(sample, 2) == ['top1', 'top2']
