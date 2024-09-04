from typing import Final as Constant

TAG_ANCHOR: Constant[str] = 'a'
TAG_HREF: Constant[str] = 'href'
TAG_TABLE: Constant[str] = 'table' 
TAG_ROW: Constant[str] = 'tr'
TAG_COLUMN: Constant[str] = 'td'
TAG_ID: Constant[str] = 'id'
TAG_DIV: Constant[str] = 'div'

DEFAULT_DATE_FORMAT: Constant[str] = "%d/%m/%Y"
MONTH_FIRST_DATE_FORMAT: Constant[str] = "%m/%d/%Y"
DEFAULT_DATE_TIME_FORMAT: Constant[str] = "%d/%m/%Y %H:%M"

SLICE_REMOVE_HEADER: slice = slice(1, None)
SLICE_REMOVE_HEADER_FOOTER: slice = slice(1, -1)

SOUP_HTML_PARSER: Constant[str] = 'html.parser'

SHORT_TIMEOUT: Constant[int] = 10
DEFAULT_TIMEOUT: Constant[int] = 30
LONG_TIMEOUT: Constant[int] = 600
JUST_FUCKING_WAIT_TIMEOUT: Constant[int] = 6000
LOOP_LIMIT: Constant[int] = 3
