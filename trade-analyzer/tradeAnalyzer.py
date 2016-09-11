from collections import defaultdict
from collections import OrderedDict


class AnalyzedShare(object):
    def __init__(self, symbol=None, latest_timestamp=None, max_time_gap=0, total_volume=0, max_trade_price=None):
        self.symbol = symbol
        self.latest_timestamp = latest_timestamp
        self.max_time_gap = max_time_gap
        self.total_volume = total_volume
        self.max_trade_price = max_trade_price
        self.share_price_profile = defaultdict(lambda: int(0))

    def add_to_share_price_profile(self, price, quantity):
        self.share_price_profile[price] += quantity

    def weighted_average_price(self):
        total_price = sum(p * q for p, q in self.share_price_profile.items())
        total_quantity = sum(q for _, q in self.share_price_profile.items())
        # Note: in python 3 exactly halfway cases are rounded to the nearest even instead of away from zero
        return int(total_price / total_quantity)

    def __str__(self):
        return ','.join(str(x) for x in
                        (self.symbol, self.max_time_gap, self.total_volume, self.weighted_average_price(),
                         self.max_trade_price))


def analyze(trades):
    analyzed_shares = defaultdict(AnalyzedShare)

    for trade in trades:
        timestamp, symbol, quantity, price = trade.split(',')
        timestamp = int(timestamp)
        quantity = int(quantity)
        price = int(price)

        if symbol not in analyzed_shares:
            analyzed_shares[symbol].symbol = symbol
            analyzed_shares[symbol].max_time_gap = 0
            analyzed_shares[symbol].total_volume = quantity
            analyzed_shares[symbol].max_trade_price = price
        else:
            current_time_gap = timestamp - analyzed_shares[symbol].latest_timestamp

            if analyzed_shares[symbol].max_time_gap < current_time_gap:
                analyzed_shares[symbol].max_time_gap = current_time_gap

            analyzed_shares[symbol].total_volume += quantity

            if analyzed_shares[symbol].max_trade_price < price:
                analyzed_shares[symbol].max_trade_price = price

        analyzed_shares[symbol].latest_timestamp = timestamp
        analyzed_shares[symbol].add_to_share_price_profile(price=price, quantity=quantity)

        # The reason why yield is placed inside the for loop instead of outside
        # is mainly for flexibility - it allows us to analyze up to any chosen parts of the trade file
        yield OrderedDict(sorted(analyzed_shares.items()))


def analyze_file(file, output_file):
    with open(file) as trades:
        # traversing through the whole file to analyze the whole file
        # (or we could traverse through only part of the file if needed)
        analyzed_shares = None
        for analyzed_shares in analyze(trades):
            pass

        # for _, analyzed_share in analyzed_shares.items():
        #     print(analyzed_share)
        write_output_file(output_file, (str(x) for _, x in analyzed_shares.items()))


def write_output_file(output_file, analyzed_shares):
    with open(output_file, mode='w') as file:
        file.write('\n'.join(analyzed_shares))


print("Analyzing sample input file, writing output to sample-output.csv")
analyze_file('sample-input.txt', 'sample-output.csv')

print()
print("Analyzing main input file, writing output to output.csv")
analyze_file('input.csv', 'output.csv')
