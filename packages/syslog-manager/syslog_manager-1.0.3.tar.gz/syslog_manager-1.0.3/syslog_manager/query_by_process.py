import re


def parse_syslog_line(line):
    syslog_pattern = re.compile(
        r'^(?P<timestamp>[A-Za-z]{3} \d{2} \d{2}:\d{2}:\d{2}) '
        r'(?P<hostname>\S+) '
        r'(?P<process>\S+?)'
        r'(?:\[(?P<pid>\d+)\])?: '
        r'(?P<message>.*)$'
    )

    match = syslog_pattern.match(line)
    if match:
        return match.groupdict()
    return None


def query_by_process(syslog_file, process_name):

    log_entries = []
    process_name_pattern = re.escape(process_name)  # Escape special characters in process_name
    pattern = re.compile(rf'{process_name_pattern}')
    try:
        with open(syslog_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parsed_line = parse_syslog_line(line)
                if parsed_line and pattern.match(parsed_line['process']):
                    log_entries.append(line.strip())

    except FileNotFoundError:
        raise FileNotFoundError(f"The file {syslog_file} does not exist.")
    except IOError as e:
        raise IOError(f"Error reading the file {syslog_file}: {e}")

    # Output to stdout
    if log_entries:
        print("\n".join(log_entries))

    # Return the result
    return "\n".join(log_entries)
