class StockSpanner:

    def __init__(self):
        # maintain a monotonic stack for stock entry

        ## definition of stock entry:
        # first parameter is price quote
        # second parameter is price span
        self.stack = []

    def next(self, price: int) -> int:
        stack = self.stack

        cur_price_quote, cur_price_span = price, 1

        # Compute price span in stock data with monotonic stack
        while stack and stack[-1][0] <= cur_price_quote:
            prev_price_quote, prev_price_span = stack.pop()

            # update current price span with history data in stack
            cur_price_span += prev_price_span

        # Update latest price quote and price span
        stack.append((cur_price_quote, cur_price_span))

        return cur_price_span


if __name__ == '__main__':
    stockSpanner = StockSpanner()
    print(stockSpanner.next(100))
    print(stockSpanner.next(80))
    print(stockSpanner.next(60))
    print(stockSpanner.next(70))
    print(stockSpanner.next(60))
    print(stockSpanner.next(75))
    print(stockSpanner.next(85))
