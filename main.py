from core.data_loader import load_data

def main():
    print("=== BizSight Decision Intelligence System ===")

    data = None

    while True:
        print("\n1. Load Data")
        print("2. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            try:
                data = load_data("data/sample_data.csv")
                print("Data loaded successfully.")
                print(data.head())
            except Exception as e:
                print("Error:", e)

        elif choice == "2":
            print("Exiting system.")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
