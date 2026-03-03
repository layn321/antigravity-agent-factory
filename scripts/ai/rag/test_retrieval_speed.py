import time
import logging
import argparse
from scripts.ai.rag.rag_optimized import get_rag

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Test RAG retrieval speed")
    parser.add_argument(
        "--query", type=str, default="What is Streamlit?", help="Query to search"
    )
    parser.add_argument(
        "--k", type=int, default=5, help="Number of results to retrieve"
    )
    parser.add_argument(
        "--iterations", type=int, default=5, help="Number of iterations to average"
    )
    args = parser.parse_args()

    print("Initializing RAG system (Warmup=True)...")
    start_init = time.perf_counter()
    rag = get_rag(warmup=True)
    end_init = time.perf_counter()
    print(f"Initialization took: {end_init - start_init:.4f} seconds\n")

    print(
        f"Running speed test for query: '{args.query}' (k={args.k}, iterations={args.iterations})"
    )

    times = []
    for i in range(args.iterations):
        start = time.perf_counter()
        results = rag.search(args.query, k=args.k)
        end = time.perf_counter()
        duration = end - start
        times.append(duration)
        print(f"Iteration {i+1}: {duration:.4f} seconds (Found {len(results)} chunks)")

    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)

    print("\n--- Statistics ---")
    print(f"Average: {avg_time:.4f} seconds")
    print(f"Minimum: {min_time:.4f} seconds")
    print(f"Maximum: {max_time:.4f} seconds")


if __name__ == "__main__":
    main()
