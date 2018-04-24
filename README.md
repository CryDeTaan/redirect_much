# Redirect Much

I wanted to solve a problem where I had a list of fully qualified domain names (FQDNs) that had certificate errors when 
browsing to them.
The FQDNs were no longer in use, however was still the property of an entity, so they had to be redirected 
to a main homepage.

Because the browser present the original FQDN in the HTTP request and the response is coming from a different domain
due to the redirect a cert error occurs.

I wanted to see from the list of FQDNs, how many of the cert errors I am getting are because of redirects.

## Installation
```commandline,
» git clone https://github.com/CryDeTaan/redirect_much.git
» pip install -r requirements.txt
```

Note: Consider using python virtualenv or similar to maintain and manage projects dependencies.  

## Usage

```
  _____          _ _               _     __  __            _
 |  __ \        | (_)             | |   |  \/  |          | |
 | |__) |___  __| |_ _ __ ___  ___| |_  | \  / |_   _  ___| |__
 |  _  // _ \/ _` | | '__/ _ \/ __| __| | |\/| | | | |/ __| '_  \
 | | \ \  __/ (_| | | | |  __/ (__| |_  | |  | | |_| | (__| | | |
 |_|  \_\___|\__,_|_|_|  \___|\___|\__| |_|  |_|\__,_|\___|_| |_|
                                            v0.1 - @CryDeTaan

usage: redirect_much.py [-h] --input <file name> [--output <file name>]

optional arguments:
  -h, --help            show this help message and exit
  --input <file name>   Input file, one host per line
  --output <file name>  Output file name (Optional)

```
The default output will retrun the results in JSON format to stdout.
The optional `--output <file name>` will output JSON format to the specified file name

## Example

```json,
» python redirect_much.py --input hosts

  _____          _ _               _     __  __            _
 |  __ \        | (_)             | |   |  \/  |          | |
 | |__) |___  __| |_ _ __ ___  ___| |_  | \  / |_   _  ___| |__
 |  _  // _ \/ _` | | '__/ _ \/ __| __| | |\/| | | | |/ __| '_  \
 | | \ \  __/ (_| | | | |  __/ (__| |_  | |  | | |_| | (__| | | |
 |_|  \_\___|\__,_|_|_|  \___|\___|\__| |_|  |_|\__,_|\___|_| |_|
                                            v0.1 - @CryDeTaan

{
    "www.google.com": {
        "http": {
            "http_redirect": "No Redirect",
            "state": "Up"
        },
        "https": {
            "cert": "Cert valid",
            "https_redirect": "No Redirect",
            "state": "Up"
        }
    }
}
```

TODO:

- Proper error logging
- Output to csv
- Input single host as argument

## License

See the [LICENSE](https://github.com/CryDeTaan/redirect_much/blob/master/LICENSE) 
file for license rights and limitations (MIT).