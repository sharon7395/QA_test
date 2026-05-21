from src.testing.test_framework import AmmeterTestFramework

def main():
    framework = AmmeterTestFramework()

    ammeter_types = ["greenlee", "entes", "circutor"]
    results = {}

    for ammeter_type in ammeter_types:
        print(f"\nTesting {ammeter_type} ammeter...")
        results[ammeter_type] = framework.run_test(ammeter_type)

    for ammeter_type, result in results.items():
        print(f"\nResults for {ammeter_type}:")
        print(f"Mean: {result['statistics']['mean']}")
        print(f"Median: {result['statistics']['median']}")
        print(f"Std Dev: {result['statistics']['standard_deviation']}")
        print(f"Min: {result['statistics']['min']}")
        print(f"Max: {result['statistics']['max']}")

    most_stable = min(
        results,
        key=lambda ammeter: results[ammeter]["statistics"]["standard_deviation"]
    )


    print(f"\nMost stable ammeter: {most_stable}")
    print(
        f"Lowest standard deviation: "
        f"{results[most_stable]['statistics']['standard_deviation']}"
    )

if __name__ == "__main__":
    main()