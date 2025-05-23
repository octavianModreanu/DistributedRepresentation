first_names = [
    "John", "Maria", "Liam", "Emma", "Noah", "Olivia", "William", "Ava", "James", "Isabella",
    "Logan", "Sophia", "Benjamin", "Mia", "Mason", "Charlotte", "Elijah", "Smith", "Johnson", "Williams",
    "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen",
    "King", "Wright", "Bob", "Alice", "Charlie", "David", "Eve", "Frank", "Grace", "Hank", "Ivy",
    "Jack", "Kathy", "Leo", "Mona", "Nina", "Oscar", "Paul", "Quinn", "Ray", "Sara",
    "Tom", "Uma", "Vic", "Wendy", "Xander", "Yara", "Zane", "Aaron", "Bella", "Cathy",
    "Derek", "Ella", "Fred", "Gina", "Hugo", "Iris", "Jake", "Kara", "Maya", "Nate",
    "Olive", "Pete", "Quincy", "Rita", "Sam", "Tina", "Ulysses", "Vera", "Will", "Xena"
]
ages = [
    str(age) for age in list(range(1, 100)) + ["100"]
]
educations = [
    "High School Diploma", "BSc in Chemistry", "MSc in Economics", "PhD in Computer Science",
    "Associate Degree in Nursing", "Bachelor of Arts in History", "Master of Business Administration",
    "Doctorate in Philosophy", "Certificate in Project Management", "Diploma in Graphic Design",
    "BA in English Literature", "MS in Physics", "Bachelor of Engineering", "MA in Political Science",
    "BS in Mathematics", "MFA in Fine Arts", "Doctor of Medicine", "High school", "Junior high school",
    "Elementary school", "Vocational training", "College", "University degree", "Postgraduate degree",
    "Online course", "Professional certification", "Trade school", "GED", "Home schooling",
    "JS", "HS", "Col", "PhD", "BA", "MA", "MSc", "MBA", "MD", "JD"
]
occupations = [
    "Software Engineer", "Teacher", "Nurse", "Accountant", "Police Officer",
    "Data Scientist", "Mechanical Engineer", "Sales Representative", "Graphic Designer",
    "Marketing Manager", "Civil Engineer", "Chef", "Doctor", "Lawyer", "Electrician",
    "Pharmacist", "Actor", "Burglar", "Bookie", "Pusher", "Dealer", "Mule", "Runner",
    "Enforcer", "Hustler", "Pimp", "Thief", "Gang Leader", "Bodyguard", "Hitman",
    "Smuggler", "Con Artist", "Forger", "Scammer", "Cybercriminal", "Kidnapper",
    "Extortionist", "Assassin", "Drug Lord", "Money Launderer", "Arms Dealer",
    "Psychologist", "Social Worker", "Financial Analyst", "Web Developer",
    "Project Manager", "Research Scientist", "Human Resources Manager",
    "Private Investigator", "Security Consultant", "Insurance Adjuster",
    "Real Estate Agent", "Construction Worker", "Bartender", "Waiter",
    "Customer Service Representative", "Administrative Assistant", "Warehouse Worker", "Delivery Driver"
]
gangs = [
    "Bloods", "Crips", "Latin Kings", "MS-13", "Hells Angels", "Aryan Brotherhood",
    "Black Guerrilla Family", "Gangster Disciples", "18th Street", "Nortenos",
    "Sureños", "Vice Lords", "Mara Salvatrucha", "Yakuza", "Triads", "Camorra",
    "Jets", "Sharks", "Sicilian Mafia", "Russian Mafia", "Colombian Cartel", "Mexican Cartel",
    "Bandidos", "Outlaws", "Pagans", "Sons of Silence", "Cossacks", "Black Disciples",
    "Gangster Disciples", "Crips", "Bloods", "Latin Kings", "MS-13", "Nortenos", "Sureños",
    "Hells Angels", "Aryan Brotherhood", "Black Guerrilla Family", "Vagos", "Rebels",
    "Nomads", "Mongols", "Coffin Cheaters", "Gypsy Jokers", "Comancheros", "Finks",
    "Satudarah", "Brothers for Life", "Notorious", "Rock Machine", "Black Pistons", "Black Mafia Family"
]
maritals = [
    "Single", "Married", "Engaged", "In a relationship", "It's complicated", 
    "Domestic partnership", "Cohabiting", "Civil union", "Common-law marriage",
    "Dating", "Long-distance relationship", "Open relationship", "Polyamorous",
    "Committed relationship", "Remarried", "Divorced", "Widowed", "Separated",
    "Annulled", "Partnered", "Unmarried", "Spouse deceased", "Broken up",
    "On a break", "Engagement ended", "Re-married", "Multiple partners",
    "Fiance", "Girlfriend", "Boyfriend", "Life partner", "Significant other",
    "Marital bliss", "Just married", "Never married", "Spinster", "Bachelor",
    "Bachelorette", "Living together", "Roommates", "Family arrangement",
    "Parents married", "Parents divorced", "Married again", "Engaged again",
    "Single again", "On and off", "Secret relationship", "Non-monogamous",
    "Trial separation", "Happy couple", "Complicated status"
    
]

CATEGORIES = ["Name", "Age", "Education", "Occupation", "Gang", "Marital Status"]

TRAIN_DATA = []


for fn in first_names:
    text = f"{fn}"
    TRAIN_DATA.append((text, {"categories": {cat: 1 if cat == "Name" else 0 for cat in CATEGORIES}}))


for age in ages:
    TRAIN_DATA.append((age, {"categories": {cat: 1 if cat == "Age" else 0 for cat in CATEGORIES}}))


for edu in educations:
    TRAIN_DATA.append((edu, {"categories": {cat: 1 if cat == "Education" else 0 for cat in CATEGORIES}}))


for occ in occupations:
    TRAIN_DATA.append((occ, {"categories": {cat: 1 if cat == "Occupation" else 0 for cat in CATEGORIES}}))


for gang in gangs:
    TRAIN_DATA.append((gang, {"categories": {cat: 1 if cat == "Gang" else 0 for cat in CATEGORIES}}))


for ms in maritals:
    TRAIN_DATA.append((ms, {"categories": {cat: 1 if cat == "Marital Status" else 0 for cat in CATEGORIES}}))

