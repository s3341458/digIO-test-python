import argparse
import heapq
import operator
import re

from collections import defaultdict


# regex based on the my understanding about programming-task-example-data.log
# in real world scenario, I should able to get this from the configurtion file
# of web server
LOG_REGEX = (
    r"(?P<ip>[(\d\.)]+) - (?P<user>.*) \[(?P<date>.*?) +(.*?)\] "
    r'"(?P<method>\w+) (?P<request_path>.*?) HTTP/(?P<http_version>.*?)" '
    r'(?P<status_code>\d+) (?P<response_size>\d+) "-" "(?P<user_agent>.*?)"'
)


class ParseFunction(object):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, line):
        return self.parser.match(line).groupdict()


def log_statics(log_file, parse_function, sections):
    statistics = {section: defaultdict(lambda: 0) for section in sections}
    # generate statistics dictionaries of both ip addresses
    # and URLs in one iterative run in order to reduce IO
    # opearations and memory usage in case the log file is big
    for line in log_file:
        parsed_data = parse_function(line)
        for section in sections:
            statistics[section][parsed_data[section]] += 1
    return statistics


def get_n_key_with_max_values(dictionary, n):
    top_items = heapq.nlargest(
        n, dictionary.items(), key=operator.itemgetter(1)
    )
    return [item[0] for item in top_items]


# precompile log parser so it do not need to be compiled every time
log_parser = re.compile(LOG_REGEX)
parse_log_line = ParseFunction(log_parser)

if __name__ == "__main__":
    # ensure log_path can be provided as an input
    arg_parser = argparse.ArgumentParser(description="Digio Test Solution.")
    arg_parser.add_argument("log_path", type=str, help="Log file location")
    args = arg_parser.parse_args()

    with open(args.log_path) as log_file:
        statistics = log_statics(
            log_file, parse_log_line, ["ip", "request_path"]
        )

        print("Unique IP addresses: ", len(statistics["ip"]))

        top_3_visited_urls = get_n_key_with_max_values(
            statistics["request_path"], 3
        )
        print("The top 3 visited URLs: ", top_3_visited_urls)

        top_3_visited_ips = get_n_key_with_max_values(statistics["ip"], 3)
        print("The top 3 most active IP addresses: ", top_3_visited_ips)
