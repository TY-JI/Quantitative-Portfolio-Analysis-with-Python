import argparse
from datetime import datetime
import re

def parse_args():
    parser = argparse.ArgumentParser(
        description='Quantitative portfolio analysis using Ledoit-Wolf, '
                    'Black-Litterman, and mean-variance optimization.'
    )

    parser.add_argument(
        '--tickers', '-T',
        nargs='+',
        default=[
            'AAPL',
            'MSFT',
            'GOOGL',
            'JPM',
            'XOM'
        ],
        help='Space-separated list of stock tickers.'
    )

    parser.add_argument(
        '--interval', '-I',
        default='1d',
        choices=['1m', '5m', '15m', '60m', '1h', '1d'],
        help='Data sampling interval.'
    )

    parser.add_argument(
        '--period', '-P',
        default=None,
        help='Lookback period (e.g., 60d, 1y, 2y). Cannot be used with --start and --end.'
    )

    parser.add_argument(
        '--start', '-S',  
        default=None,
        help='Start date in YYYY-MM-DD format.'
    )

    parser.add_argument(
        '--end', '-E',
        default=None,
        help='End date in YYYY-MM-DD format.'
    )

    parser.add_argument(
        '--view', '-V',
        action='append',
        nargs='+',
        help='Add a view: relative ASSET1 ASSET2 VALUE or absolute ASSET VALUE.'
    )

    parser.add_argument(
        '--benchmark',
        action='store_true',
        help='Measures program runtime.'
    )

    args = parser.parse_args()
    args.tickers = [ticker.upper() for ticker in args.tickers]
    validate_args(args)
    return args

def validate_args(args):
    if args.period is None and args.start is None:
        args.period = '2y'

    check_duplicate_tickers(args.tickers)
    check_start_end_pair(args.start, args.end)
    check_period_with_dates(args.period, args.start)

    validate_dates(args.start, args.end)
    validate_period(args.period)

def check_duplicate_tickers(tickers):
    if len(tickers) != len(set(tickers)):
        duplicates = [
            ticker for ticker in set(tickers)
            if tickers.count(ticker) > 1
        ]

        raise ValueError(
            f'Duplicate tickers detected: {duplicates}'
        )

def check_start_end_pair(start, end):
    if (start is None) != (end is None):
        raise ValueError(
            '--start and --end must be provided together.'
        )

def check_period_with_dates(period, start):
    if period is not None and start is not None:
        raise ValueError(
            '--period cannot be used with --start or --end.'
        )

def validate_dates(start, end):
    if start is not None and end is not None:
        try:
            start = datetime.strptime(start, '%Y-%m-%d')
            end = datetime.strptime(end, '%Y-%m-%d')
        except ValueError:
            raise ValueError(
                'Dates must use YYYY-MM-DD format.'
            ) from None

        if start > end:
            raise ValueError(
                '--start cannot be later than --end.'
            )

def validate_period(period):
    if period is None:
        return
    
    if not re.fullmatch(r'\d+(d|mo|y)', period):
        raise ValueError(
            'Invalid period format. Use formats such as 30d, 1mo, 6mo, or 2y.'
        )