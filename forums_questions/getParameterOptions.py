from tableaudocumentapi import Workbook
import argparse
import logging
from lxml import etree
from pathlib import Path
import sys
import urllib
from xml.sax.saxutils import unescape, escape

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

def _parse_args():
    # Parse arguments from user
    parser = argparse.ArgumentParser(description='Parses workbook to find parameter options')
    parser.add_argument('--file', required=True, help='file to parse ')

    args = parser.parse_args()
    return args

def _get_options(parameter):
    name = parameter.name
    xml = parameter.xml
    # get list of options per parameter
    options = [member.get('value').strip('\"').lstrip('\\') for member in xml.findall('.//member')]
    if options:
        # if discrete list of options, print out parameter name and members
        print(f'Parameter {name} has the following options:')
        for option in options:
            print(f'\t- {option}')

def main():
    args = _parse_args()
    file = Path(args.file)
    # validate file type
    if file.suffix not in ['.twb', '.twbx']:
        _logger.error("%s is not a valid Workbook file type", file.name)
        sys.exit(1)
    workbook = Workbook(file)
    parameters = [datasource for datasource in workbook.datasources if datasource.name == 'Parameters']
    if not parameters:
        _logger.info("No parameters in workbook")
    else:
        parameters = parameters[0]
        for parameter in parameters.fields.values():
            _get_options(parameter)

if __name__ == '__main__':
    main()