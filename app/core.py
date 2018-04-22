#!/usr/bin/env python
import os
import requests
import json

json_output = {}


class Check_host:
    """
        Main class that prepares urls and performs all the checks.
    """

    # make some sub modules stfu
    requests.packages.urllib3.disable_warnings()

    def __init__(self):

        # The following variables needs to be populated for only an instance.
        self.http_state = ''
        self.http_redirect = ''

        self.https_state = ''
        self.https_cert = ''
        self.https_redirect = ''

    def prepare_url(self, host):
        """
        Take a line/host from the provided input file, and return a URL formatted string for both http and https.

        :param host: Hostname from the input file(sys.argv[1]).
        :return: array.url: An array of http(s)://<host>
        """

        http = f'http://{host}'
        https = f'https://{host}'

        return [http, https]

    def check_connection(self, url):
        """
        Check if the URL has an active host behind it as well as if the host is presenting a HTTP/(S) site.
        If the host is not responding to a http(s) request on port 80 or 443,
        it is considered down and execution will continue to the next host.

        This function will not return any data, it will only set some variables for the current instance of
        this class.

        :param url: Array containing both URLS returned by prepare_url()
        :return: None
        """

        # HTTP
        try:
            http_response = requests.get(url[0], timeout=3, allow_redirects=False)
            http_response.raise_for_status()

            self.http_state = 'Up'

            self.http_redirect = self.check_redirect(http_response)

        except requests.exceptions.RequestException as e:
            self.http_state = 'Down'

        # HTTPS
        try:
            https_response = requests.get(url[1], timeout=3, allow_redirects=False, verify=False)
            https_response.raise_for_status()

            self.https_state = 'Up'

            self.https_redirect = self.check_redirect(https_response)

            self.https_cert = self.check_cert(url[1])

        except requests.exceptions.RequestException as e:
            self.https_state = 'Down'

    def check_redirect(self, response):
        """
        Check if a redirect is in place and where the redirect points to. If no redirect has been implemented, continue
        to the next host.

        Again, this function will not return any data, it will only set some variables for the current instance of
        this class as part of the loop.
        These variables will be used in a final function call that will prepare a json payload of the data.

        :param response: Response to be checked for redirect.
        :return: None
        """

        if response.status_code == 301:
            return response.headers['Location']

        elif response.status_code == 200:
            return "No Redirect"

        else:
            return f'Unexpected return code {response.status_code}'

    def check_cert(self, url):
        """
        Check if a valid certificate is presented on a HTTPS request.

        :param url: https URL that should be checked for valid https cert
        :return: "Valid Cert"/"Cert Err"
        """

        try:
            r = requests.get(url)
            r.raise_for_status()
            return 'Cert valid'
        except requests.exceptions.SSLError:
            return 'Cert Err'

    def prepare_output(self, host):
        """
        Prepare the json output.
        This output will be used to write stdout, .json file, or csv file.

        :param host: Used as one of the parameters that will generate the json output.
        :return: json output
        """

        return ({
                    host: {
                        'http':
                            {
                                'state': self.http_state,
                                'http_redirect': self.http_redirect
                            },
                        'https':
                            {
                                'state': self.https_state,
                                'cert': self.https_cert,
                                'https_redirect': self.https_redirect
                            }
                    }
                })

    def start_check(self, host):
        """
        Initiates the redirector check on the host. This function will call the other functions in this class.
        This function will be called from outside the class.

        :param host:
        :return:
        """

        url = self.prepare_url(host)
        self.check_connection(url)


def progress(count, total, host):
    """
    Simple status bar that will show progress.
    Rewrite stdout with progress bar.

    :param count: Counter of current host/line being processed in from the input file(sys.argv[1]).
    :param total: Number of hosts/lines in from the input file(sys.argv[1]).
    :param host: Current hostname being processed.

    :return: None
    """

    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percent = round(100.0 * count / float(total), 0)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    os.sys.stdout.write(f'\033[K [{bar}] {percent}% -> {host}\r')
    os.sys.stdout.flush()


def run(input_file):
    with input_file as open_file:
        hosts = open_file.readlines()

        line_total = len(hosts)
        line_count = 0

        for host in hosts:
            host = host.rstrip()

            line_count += 1
            progress(line_count, line_total, host)

            check_host = Check_host()
            check_host.start_check(host)
            host_output = check_host.prepare_output(host)
            json_output.update(host_output)

        os.sys.stdout.write(f'\033[K')
        os.sys.stdout.flush()


def output(output_file):
    if output_file is not None:
        with output_file as outfile:
            json.dump(json_output, outfile, sort_keys=True, indent=4, ensure_ascii=False)

        print(f'Done - File written to {output_file.name}')

    else:
        print(json.dumps(json_output, sort_keys=True, indent=4, ensure_ascii=False))


