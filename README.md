# Fibo
This Django app includes the following main functionalities:

- Under fib/number: calculates and displays the exhaustive list of combinations of *number* as sums of Fibonacci numbers. Each sum is displayed as a dictionary where the key is a Fibonacci number, and the value is the number of occurrences of the Fibonacci number in the sum. Each dictionary is sorted by the smallest keys, and the list of dictionaries is sorted from the ones with the smallest keys (and largest occurrences (values) for the smallest elements), to those with the largest keys. A count of the duration it took to calculate or load the result is displayed at the top of the page.
- Database storage for the longest calculated Fibonacci sequence and for previously calculated results.
- Database storage for requests and responses so pages can be loaded faster.
- Caching of pages.
- Under /health: displays a list of health checks, namely disk usage, Cache availabiliy, DB availabiliy, File Storage availabiliy, and Memory usage.
