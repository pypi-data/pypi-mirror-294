import time
import requests

def benchmark(url: str, time_limit: int = 1):
    start = time.time()
    inter_count = 0
    
    while True:
        requests.get(url)
        inter_count += 1
        if time.time() - start > time_limit:
            break
    return inter_count

if __name__ == "__main__":
    url = "http://127.0.0.1:8080/"
    print(benchmark(url))
