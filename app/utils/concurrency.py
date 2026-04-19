from concurrent.futures import ThreadPoolExecutor, as_completed

def run_parallel(func, items):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(func, item) for item in items]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print("❌ Error in thread:", e)