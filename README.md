# EcoFeast-
#backend code:

import json
import os

DATA_FILE = "food_data.json"

# Initialize data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"users": [], "donors": [], "beneficiaries": [], "donations": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# Add a user
def add_user():
    if len(data["users"]) >= 100:
        print("User limit reached.")
        return
    user_id = len(data["users"]) + 1
    name = input("Enter user name: ")
    contact = input("Enter contact info: ")
    data["users"].append({"id": user_id, "name": name, "contact": contact})
    save_data(data)
    print("User added successfully.\n")

# Add a donor
def add_donor():
    if len(data["donors"]) >= 100:
        print("Donor limit reached.")
        return
    donor_id = len(data["donors"]) + 1
    name = input("Enter donor name: ")
    food_type = input("Enter food type: ")
    quantity = input("Enter quantity (kg): ")
    location = input("Enter location: ")
    data["donors"].append({
        "id": donor_id,
        "name": name,
        "food_type": food_type,
        "quantity": quantity,
        "location": location
    })
    save_data(data)
    print("Donor added successfully.\n")

# Add a beneficiary
def add_beneficiary():
    if len(data["beneficiaries"]) >= 100:
        print("Beneficiary limit reached.")
        return
    beneficiary_id = len(data["beneficiaries"]) + 1
    name = input("Enter beneficiary name: ")
    location = input("Enter location: ")
    data["beneficiaries"].append({"id": beneficiary_id, "name": name, "location": location})
    save_data(data)
    print("Beneficiary added successfully.\n")

# Add a donation
def add_donation():
    donor_id = int(input("Enter donor ID: "))
    beneficiary_id = int(input("Enter beneficiary ID: "))
    status = "Pending"
    data["donations"].append({
        "donor_id": donor_id,
        "beneficiary_id": beneficiary_id,
        "status": status
    })
    save_data(data)
    print("Donation added successfully.\n")

# View all data
def view_data():
    print(json.dumps(data, indent=4))

# Main loop
while True:
    print("\n--- Food Donation & Waste Management ---")
    print("1. Add User")
    print("2. Add Donor")
    print("3. Add Beneficiary")
    print("4. Add Donation")
    print("5. View All Data")
    print("6. Exit")

    try:
        choice = int(input("Enter choice: "))
    except EOFError:
        break

    if choice == 1:
        add_user()
    elif choice == 2:
        add_donor()
    elif choice == 3:
        add_beneficiary()
    elif choice == 4:
        add_donation()
    elif choice == 5:
        view_data()
    elif choice == 6:
        print("Exiting...")
        break
    else:
        print("Invalid choice.")


        

        #frontend code:
        
        <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>EcoFeast</title>
  <style>
    body {
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      background-color: #FFF5E1;
      color: #333;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      position: relative;
    }

    header {
      text-align: center;
      padding: 2rem 1rem;
      background-color: rgba(255, 255, 255, 0.8);
      border-bottom: 2px solid #ccc;
      width: 100%;
    }

    header h1 {
      font-size: 3rem;
      color: #3A6351;
      margin: 0;
    }

    header p {
      margin: 0.5rem 0 0;
    }

    nav {
      display: flex;
      justify-content: center;
      gap: 1rem;
      background: rgba(255, 255, 255, 0.7);
      padding: 1rem;
      border-bottom: 1px solid #ccc;
      width: 100%;
    }

    nav button {
      padding: 0.6rem 1.2rem;
      border: none;
      border-radius: 20px;
      background-color: #3A6351;
      color: white;
      font-size: 1rem;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }

    nav button:hover {
      background-color: #558b7f;
    }

    section {
      padding: 2rem;
      background-color: rgba(255, 255, 255, 0.85);
      margin: 2rem auto;
      max-width: 800px;
      border-radius: 15px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    }

    section h2 {
      color: #3A6351;
      border-bottom: 2px solid #3A6351;
      padding-bottom: 0.5rem;
      margin-bottom: 1rem;
    }

    label {
      display: block;
      margin: 1rem 0 0.3rem;
      font-weight: bold;
    }

    input, select {
      width: 100%;
      padding: 0.6rem;
      border-radius: 8px;
      border: 1px solid #ccc;
      font-size: 1rem;
    }

    button.submit {
      background-color: #3A6351;
      color: white;
      padding: 0.8rem 2rem;
      margin-top: 1rem;
      border: none;
      border-radius: 25px;
      font-size: 1.1rem;
      cursor: pointer;
      transition: all 0.3s ease;
    }

    button.submit:hover {
      background-color: #295243;
    }

    footer {
      text-align: center;
      padding: 1rem;
      background-color: rgba(255, 255, 255, 0.6);
      font-size: 0.9rem;
      color: #666;
      margin-top: 2rem;
    }

    .hidden {
      display: none;
    }

    .help-options button {
      margin-top: 1rem;
      padding: 1rem 2rem;
      background-color: #3A6351;
      color: white;
      border: none;
      border-radius: 25px;
      font-size: 1.2rem;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }

    .help-options button:hover {
      background-color: #558b7f;
    }

    .back-button {
      position: fixed;
      bottom: 20px;
      left: 20px;
      padding: 0.8rem 1.5rem;
      background-color: #28a745;
      color: white;
      font-size: 1rem;
      border: none;
      border-radius: 25px;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }

    .back-button:hover {
      background-color: #218838;
    }

    .hide-back-button {
      display: none;
    }
  </style>
</head>
<body>

  <header>
    <h1>EcoFeast</h1>
    <p>Intelligent Food Redistribution & Bio-Waste Management</p>
  </header>

  <nav>
    <button onclick="showSection('user')">Add User</button>
    <button onclick="showSection('donor')">Add Donor</button>
    <button onclick="showSection('beneficiary')">Add Beneficiary</button>
    <button onclick="showSection('donation')">Add Donation</button>
  </nav>

  <main>
    <!-- User Form Section -->
    <section id="user" class="hidden">
      <h2>Add User</h2>
      <label>Name:</label>
      <input type="text" placeholder="Enter name" id="user-name"/>
      <label>Contact:</label>
      <input type="text" placeholder="Enter contact" id="user-contact"/>
      <button class="submit" onclick="submitUser()">Submit User</button>
    </section>

    <!-- Donor Form Section -->
    <section id="donor" class="hidden">
      <h2>Add Donor</h2>
      <label>Name:</label>
      <input type="text" placeholder="Enter donor name" id="donor-name"/>
      <label>Food Type:</label>
      <input type="text" placeholder="Enter food type" id="donor-food"/>
      <label>Quantity (kg):</label>
      <input type="number" placeholder="Enter quantity" id="donor-quantity"/>
      <label>Location:</label>
      <input type="text" placeholder="Enter location" id="donor-location"/>
      <button class="submit" onclick="submitDonor()">Submit Donor</button>
    </section>

    <!-- Beneficiary Form Section -->
    <section id="beneficiary" class="hidden">
      <h2>Add Beneficiary</h2>
      <label>Name:</label>
      <input type="text" placeholder="Enter beneficiary name" id="beneficiary-name"/>
      <label>Location:</label>
      <input type="text" placeholder="Enter location" id="beneficiary-location"/>
      <label>Required Quantity (kg):</label>
      <input type="number" placeholder="Enter required quantity" id="beneficiary-quantity"/>
      <button class="submit" onclick="submitBeneficiary()">Submit Beneficiary</button>
    </section>

    <!-- Donation Form Section -->
    <section id="donation" class="hidden">
      <h2>Add Donation</h2>
      <label>Donor ID:</label>
      <input type="number" placeholder="Enter donor ID" id="donor-id"/>
      <label>Beneficiary ID:</label>
      <input type="number" placeholder="Enter beneficiary ID" id="beneficiary-id"/>
      <button class="submit" onclick="submitDonation()">Submit Donation</button>
    </section>

    <!-- Thank You Section -->
    <section id="thank-you" class="hidden">
      <h2>Thank You for Joining EcoFeast!</h2>
      <p>Your contribution is making a positive impact.</p>
      <h3>How EcoFeast Works</h3>
      <p>EcoFeast connects food donors with beneficiaries to reduce food waste and support communities in need.</p>
      <p>After registering your donation, you will be able to contribute food or money!</p>
      <button class="submit" onclick="nextStep()">Next</button>
    </section>

    <!-- How Can We Help You Page -->
    <section id="how-can-we-help" class="hidden">
      <h2>How Can We Help You?</h2>
      <button class="submit" onclick="showHelpOption('Delivery')">Delivery</button>
      <button class="submit" onclick="showHelpOption('Make Donation')">Make Donation</button>
      <button class="submit" onclick="showHelpOption('Schedule a Food Drive')">Schedule a Food Drive</button>
    </section>

    <!-- Donation Options Page -->
    <section id="donation-options" class="hidden">
      <h2>Donation Options</h2>
      <button class="submit" onclick="showHelpOption('Donate Food')">Donate Food</button>
      <button class="submit" onclick="showHelpOption('Donate Money')">Donate Money</button>
    </section>

  </main>

  <footer>
    © 2025 EcoFeast. Designed with heart for a better tomorrow.
  </footer>

  <button class="back-button hide-back-button" id="backButton" onclick="goBack()">Back</button>

  <script>
    function showSection(id) {
      const sections = document.querySelectorAll('main section');
      sections.forEach(sec => sec.classList.add('hidden'));
      document.getElementById(id).classList.remove('hidden');
      sessionStorage.setItem('previousSection', id);
      showBackButton();
    }

    function showBackButton() {
      const backButton = document.getElementById('backButton');
      if (sessionStorage.getItem('previousSection') === 'thank-you' || sessionStorage.getItem('previousSection') === 'how-can-we-help') {
        backButton.classList.remove('hide-back-button');
      } else {
        backButton.classList.add('hide-back-button');
      }
    }

    function goBack() {
      const previousSection = sessionStorage.getItem('previousSection');
      if (previousSection) {
        showSection(previousSection);
      }
    }

    function submitUser() {
      // Add user logic
      showSection('thank-you');  // Redirect to thank you page
    }

    function nextStep() {
      showSection('how-can-we-help');  // Redirect to the "How can we help you" page
    }

    function showHelpOption(option) {
      alert(`You selected: ${option}. We will assist you shortly.`);
    }

    function submitDonation() {
      // Add donation logic
      showSection('donation-options');  // Redirect to donation options page
    }
  </script>

</body>
</html>




EcoFeast is a technology-driven platform designed to combat food waste and hunger in India by connecting surplus food donors, such as restaurants, hotels, and individuals, with NGOs and food banks. It leverages AI and ML for food categorization and demand prediction, while IoT sensors ensure food quality and safety. Route optimization minimizes transportation costs and improves efficiency, and real-time tracking enhances transparency. The user-friendly app makes food donation accessible to all demographics. EcoFeast also ensures compliance with food safety and legal regulations, preventing risks. By collaborating with NGOs, local governments, and businesses, it aims to create a scalable and sustainable food redistribution system that reduces waste and provides meals to the needy.
