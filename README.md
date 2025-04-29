from matcher import match_donor_to_best_receiver

def get_donor_input():
    print("\nEnter Donor Details:")
    donor = {
        "Food_Category": input("Food Category: "),
        "Quantity": int(input("Quantity (in portions): ")),
        "latitude": float(input("Location Latitude: ")),
        "longitude": float(input("Location Longitude: ")),
        "Ingredients": input("Ingredients (comma-separated): ").split(",")
    }
    return donor

def get_receiver_input():
    receivers = []
    n = int(input("\nEnter number of food receivers: "))
    
    for i in range(n):
        print(f"\nReceiver #{i+1}")
        receiver = {
            "latitude": float(input("Location Latitude: ")),
            "longitude": float(input("Location Longitude: ")),
            "required_portions": int(input("Required Portions: ")),
            "allergies": input("Allergies (comma-separated): ").split(","),
            "people": {
                "children": int(input("Number of children: ")),
                "elderly": int(input("Number of elderly: "))
            }
        }
        receivers.append(receiver)
    
    return receivers

if __name__ == "__main__":
    donor = get_donor_input()
    receivers = get_receiver_input()

    best_receiver, score, distance = match_donor_to_best_receiver(donor, receivers)

    if best_receiver:
        print("\nBest Matched Receiver:")
        print(f"Location: ({best_receiver['latitude']}, {best_receiver['longitude']})")
        print(f"Required Portions: {best_receiver['required_portions']}")
        print(f"Children: {best_receiver['people']['children']}, Elderly: {best_receiver['people']['elderly']}")
        print(f"Score: {score:.2f}, Distance: {distance:.2f} km")
    else:
        print("No suitable receiver found.")
