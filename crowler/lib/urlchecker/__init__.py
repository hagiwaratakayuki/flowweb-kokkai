def process(url,checkers):
    for checker in checkers:
        if checker.check(url):
            return checker.process(url)