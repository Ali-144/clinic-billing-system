Clinic_Config = {
    "currency": "PKR",
    "tax_rate": 0.05,  # 5% tax, use only if you want to apply it
    "senior_discount": 0.10,  # 10% senior citizen discount
    "insurance_consultation_coverage": 0.20,  # 20%
    "insurance_test_coverage": 0.50,  # 50%
}

patients = {
    "P001": {"name": "Ali Khan", "age": 32, "city": "Lahore", "insurance": True},
    "P002": {"name": "Ahmed Raza", "age": 45, "city": "Multan", "insurance": False},
    "P003": {"name": "Sara Ahmed", "age": 28, "city": "Lahore", "insurance": True},
    "P004": {"name": "Usman Ali", "age": 67, "city": "Islamabad", "insurance": False},
}

doctors = {
    "D001": {
        "name": "Dr. Hassan",
        "specialization": "Cardiology",
        "fee": 5000,
        "available": True,
    },
    "D002": {
        "name": "Dr. Sara",
        "specialization": "Dermatology",
        "fee": 3000,
        "available": True,
    },
    "D003": {
        "name": "Dr. Ahmed",
        "specialization": "General",
        "fee": 2000,
        "available": True,
    },
}
appointments = [
    {
        "appointment_id": "A001",
        "patient_id": "P001",
        "doctor_id": "D001",
        "status": "completed",
        "tests": ["ECG", "Blood Test"],
    },
    {
        "appointment_id": "A002",
        "patient_id": "P002",
        "doctor_id": "D003",
        "status": "completed",
        "tests": [],
    },
    {
        "appointment_id": "A003",
        "patient_id": "P003",
        "doctor_id": "D002",
        "status": "cancelled",
        "tests": [],
    },
    {
        "appointment_id": "A004",
        "patient_id": "P004",
        "doctor_id": "D001",
        "status": "completed",
        "tests": ["ECG"],
    },
]
test_prices = {"ECG": 1500, "Blood Test": 1000, "X-Ray": 2500, "MRI": 8000}
# Appointment Processing


def patient_status(Patient_id):
    if Patient_id in patients:
        return "available"
    else:
        return f"patient not available"


def doctor_status(doctor_id):
    if doctor_id in doctors:
        return "available"
    else:
        return f"doctor not available"


def doctor_available(doctor_id):
    if doctor_id in doctors:
        if doctors[doctor_id]["available"]:
            return "available"
        else:
            return f"{doctors[doctor_id]['name']} is not available"
    else:
        return f"doctor not available"


def find_appointment(appointment_id):
    for appointment in appointments:
        if appointment_id == appointment["appointment_id"]:
            return appointment
    return None

def appointment_status(appointment_id):
    for appointment in appointments:
        if appointment_id == appointment["appointment_id"]:
            return appointment["status"]
    return f"Patient {appointment_id} does not exist"


def test_status(tests):
    for test in tests:
        if test not in test_prices:
            return "invalid test"

    return "valid test"


# bill calculation


def calculate_test_charges(tests):
    total_charge = 0
    for test in tests:
        total_charge += test_prices[test]
    return total_charge


def calculate_total(*charges):
    total = 0
    for charge in charges:
        total += charge
    return total


def calculate_insurance_coverage(fee, test_charges, insurance):
    if insurance == False:
        return 0
    else:
        consultation_covered = fee * Clinic_Config["insurance_consultation_coverage"]
        test_coverage = test_charges * Clinic_Config["insurance_test_coverage"]
        return consultation_covered + test_coverage


def senior_citizen_discount(amount, age):
    if age >= 60:
        discount = amount * Clinic_Config["senior_discount"]
        return amount - discount
    else:
        return amount


def calculate_bill(fee, test_charges, insurance, age):validate_age
    subtotal = fee + test_charges
    insurance_coverage = calculate_insurance_coverage(fee, test_charges, insurance)
    after_insurance_total = subtotal - insurance_coverage
    final = senior_citizen_discount(after_insurance_total, age)
    return final


def calculate_bill_flexible(fee, **options):
    test_charges = 0
    if options.get("include_tests", False):
        test_charges = options.get("test_charges", 0)

    coverage = 0
    if options.get("insurance", False):
        coverage = calculate_insurance_coverage(fee, test_charges, True)

    amount = calculate_total(fee, test_charges) - coverage

    if options.get("senior_discount", False):
        amount -= amount * Clinic_Config["senior_discount"]

    return amount


def get_bill_details(appointment):
    patient_id = appointment["patient_id"]
    doctor_id = appointment["doctor_id"]
    tests = appointment["tests"]

    if appointment["status"] != "completed":
        return None
    if patient_status(patient_id) != "available":
        return None
    if doctor_available(doctor_id) != "available":
        return None
    if test_status(tests) != "valid test":
        return None

    fee = doctors[doctor_id]["fee"]
    test_charges = calculate_test_charges(tests)
    insurance = patients[patient_id]["insurance"]
    age = patients[patient_id]["age"]

    return {
        "appointment_id": appointment["appointment_id"],
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "fee": fee,
        "test_charges": test_charges,
        "coverage": calculate_insurance_coverage(fee, test_charges, insurance),
        "patient_paid": calculate_bill(fee, test_charges, insurance, age),
    }


def process_appointment(appointment_id):
    appointment = find_appointment(appointment_id)
    if appointment is None:
        return f"{appointment_id} appointment does not exist "

    patient_id = appointment["patient_id"]
    doctor_id = appointment["doctor_id"]
    status = appointment["status"]
    tests = appointment["tests"]

    if status == "cancelled":
        return f"{appointment_id}, Appointment already cancelled"

    patient_check = patient_status(patient_id)
    if patient_check != "available":
        return f"{patient_id} not available"

    doctor_check = doctor_status(doctor_id)
    if doctor_check != "available":
        return f"{doctor_id} not available"

    availability_check = doctor_available(doctor_id)
    if availability_check != "available":
        return "doctor not available"

    tests_check = test_status(tests)
    if tests_check != "valid test":
        return "invalid test"

    if status == "completed":
        fee = doctors[doctor_id]["fee"]
        test_charges = calculate_test_charges(tests)
        insurance = patients[patient_id]["insurance"]
        age = patients[patient_id]["age"]
        bill = calculate_bill(fee, test_charges, insurance, age)
        return f"{appointment_id} Accepted. | Bill: {bill}"

    else:
        return f"{appointment_id} is pending and  No bill yet"


def cancel_appointment(appointment_id):
    appointment = find_appointment(appointment_id)
    if appointment is None:
        return "Appointment does not exist"

    status = appointment["status"]

    if status == "completed":
        return "Completed appointment cannot be cancelled"

    if status == "cancelled":
        return "Appointment already cancelled"

    appointment["status"] = "cancelled"
    return "CANCELLED"


# ============================================================
# PASTE EVERYTHING BELOW AT THE END OF YOUR CURRENT CODE
# (these versions of test_status, get_bill_details and
#  process_appointment replace your old ones - Python uses the
#  last definition, so you can delete the old copies above)
# ==============================================================

VALID_STATUSES = {"pending", "completed", "cancelled"}
processed_appointments = set()


# ---------- extra validators ----------


def validate_status(status):
    if isinstance(status, str) and status in VALID_STATUSES:
        return "valid status"
    else:
        return f"invalid status: {status}"


def validate_age(age):
    if isinstance(age, int) and age >= 0:
        return "valid age"
    else:
        return f"invalid age: {age}"


def test_status(tests):
    seen = set()
    for test in tests:
        if test not in test_prices:
            return f"invalid test: {test}"
        if test in seen:
            return f"duplicate test: {test}"
        seen.add(test)

    return "valid test"


def validate_appointment(appointment):
    patient_id = appointment["patient_id"]
    doctor_id = appointment["doctor_id"]

    status_check = validate_status(appointment["status"])
    if status_check != "valid status":
        return status_check

    if patient_status(patient_id) != "available":
        return f"Patient {patient_id} does not exist"

    if doctor_status(doctor_id) != "available":
        return f"Doctor {doctor_id} does not exist"

    availability_check = doctor_available(doctor_id)
    if availability_check != "available":
        return availability_check

    age_check = validate_age(patients[patient_id]["age"])
    if age_check != "valid age":
        return age_check

    tests_check = test_status(appointment["tests"])
    if tests_check != "valid test":
        return tests_check

    return "valid appointment"


def format_money(amount):
    return f"{Clinic_Config['currency']} {amount:.2f}"


# ---------- billing details + processing (replace old versions) ----------


def get_bill_details(appointment):
    if appointment["status"] != "completed":
        return None
    if validate_appointment(appointment) != "valid appointment":
        return None

    patient_id = appointment["patient_id"]
    doctor_id = appointment["doctor_id"]
    tests = appointment["tests"]

    fee = doctors[doctor_id]["fee"]
    test_charges = calculate_test_charges(tests)
    insurance = patients[patient_id]["insurance"]
    age = patients[patient_id]["age"]

    return {
        "appointment_id": appointment["appointment_id"],
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "fee": fee,
        "test_charges": test_charges,
        "coverage": calculate_insurance_coverage(fee, test_charges, insurance),
        "patient_paid": calculate_bill(fee, test_charges, insurance, age),
    }


def process_appointment(appointment_id):
    appointment = find_appointment(appointment_id)
    if appointment is None:
        return f"{appointment_id} -> REJECTED | Reason: Appointment does not exist"

    status = appointment["status"]

    if status == "cancelled":
        return f"{appointment_id} -> REJECTED | Reason: Appointment already cancelled"

    if appointment_id in processed_appointments:
        return f"{appointment_id} -> REJECTED | Reason: Appointment already processed"

    appointment_check = validate_appointment(appointment)
    if appointment_check != "valid appointment":
        return f"{appointment_id} -> REJECTED | Reason: {appointment_check}"

    if status == "completed":
        bill_details = get_bill_details(appointment)
        processed_appointments.add(appointment_id)
        return f"{appointment_id} -> ACCEPTED | Bill: {format_money(bill_details['patient_paid'])}"

    return f"{appointment_id} -> PENDING | No bill yet"


# ---------- report helpers ----------


def get_all_bills():
    details = [get_bill_details(appointment) for appointment in appointments]
    return [bill for bill in details if bill is not None]


def get_top_key(counts):
    if not counts:
        return None
    top_key = max(counts, key=lambda key: counts[key])
    if counts[top_key] == 0:
        return None
    return top_key


# ---------- doctor report ----------


def generate_doctor_report():
    bills = get_all_bills()
    per_doctor = {}

    for doctor_id in doctors:
        doctor_appointments = [a for a in appointments if a["doctor_id"] == doctor_id]
        doctor_bills = [b for b in bills if b["doctor_id"] == doctor_id]
        revenue = sum(b["patient_paid"] for b in doctor_bills)

        if doctor_bills:
            average_bill = revenue / len(doctor_bills)
        else:
            average_bill = 0

        per_doctor[doctor_id] = {
            "name": doctors[doctor_id]["name"],
            "specialization": doctors[doctor_id]["specialization"],
            "appointments": len(doctor_appointments),
            "completed": len(
                [a for a in doctor_appointments if a["status"] == "completed"]
            ),
            "cancelled": len(
                [a for a in doctor_appointments if a["status"] == "cancelled"]
            ),
            "revenue": revenue,
            "average_bill": average_bill,
        }

    appointment_counts = {
        doctor_id: per_doctor[doctor_id]["appointments"] for doctor_id in per_doctor
    }
    top_doctor_id = get_top_key(appointment_counts)

    specialization_counts = {}
    for doctor_id in per_doctor:
        specialization = per_doctor[doctor_id]["specialization"]
        specialization_counts[specialization] = (
            specialization_counts.get(specialization, 0)
            + per_doctor[doctor_id]["appointments"]
        )

    if top_doctor_id is None:
        most_requested_doctor = None
    else:
        most_requested_doctor = per_doctor[top_doctor_id]["name"]

    return {
        "per_doctor": per_doctor,
        "most_requested_doctor": most_requested_doctor,
        "most_requested_specialization": get_top_key(specialization_counts),
    }


def show_doctor_report():
    report = generate_doctor_report()
    print("=" * 40)
    print("DOCTOR REPORT")
    print("=" * 40)

    sorted_doctors = sorted(
        report["per_doctor"].items(),
        key=lambda item: item[1]["revenue"],
        reverse=True,
    )
    for doctor_id, stats in sorted_doctors:
        print(f"{doctor_id} | {stats['name']} ({stats['specialization']})")
        print(
            f"  Appointments: {stats['appointments']} | "
            f"Completed: {stats['completed']} | Cancelled: {stats['cancelled']}"
        )
        print(
            f"  Revenue: {format_money(stats['revenue'])} | "
            f"Average Bill: {format_money(stats['average_bill'])}"
        )

    print(f"Most Requested Doctor: {report['most_requested_doctor']}")
    print(f"Most Requested Specialization: {report['most_requested_specialization']}")
    print("=" * 40)


# ---------- patient report ----------


def generate_patient_report():
    bills = get_all_bills()
    per_patient = {}

    for patient_id in patients:
        patient_appointments = [
            a for a in appointments if a["patient_id"] == patient_id
        ]
        patient_bills = [b for b in bills if b["patient_id"] == patient_id]

        per_patient[patient_id] = {
            "name": patients[patient_id]["name"],
            "appointments": len(patient_appointments),
            "completed": len(
                [a for a in patient_appointments if a["status"] == "completed"]
            ),
            "cancelled": len(
                [a for a in patient_appointments if a["status"] == "cancelled"]
            ),
            "total_charges": sum(b["fee"] + b["test_charges"] for b in patient_bills),
            "coverage": sum(b["coverage"] for b in patient_bills),
            "patient_paid": sum(b["patient_paid"] for b in patient_bills),
        }

    spending = {
        patient_id: per_patient[patient_id]["patient_paid"]
        for patient_id in per_patient
    }
    appointment_counts = {
        patient_id: per_patient[patient_id]["appointments"]
        for patient_id in per_patient
    }
    top_spender_id = get_top_key(spending)
    top_visitor_id = get_top_key(appointment_counts)

    if top_spender_id is None:
        highest_spending_patient = None
    else:
        highest_spending_patient = per_patient[top_spender_id]["name"]

    if top_visitor_id is None:
        most_appointments_patient = None
    else:
        most_appointments_patient = per_patient[top_visitor_id]["name"]

    return {
        "per_patient": per_patient,
        "highest_spending_patient": highest_spending_patient,
        "most_appointments_patient": most_appointments_patient,
        "no_completed_patients": [
            per_patient[pid]["name"]
            for pid in per_patient
            if per_patient[pid]["completed"] == 0
        ],
        "insured_patients": [
            patient["name"] for patient in patients.values() if patient["insurance"]
        ],
        "senior_patients": [
            patient["name"]
            for patient in patients.values()
            if validate_age(patient["age"]) == "valid age" and patient["age"] >= 60
        ],
    }


def show_patient_report():
    report = generate_patient_report()
    print("=" * 40)
    print("PATIENT REPORT")
    print("=" * 40)

    sorted_patients = sorted(
        report["per_patient"].items(),
        key=lambda item: item[1]["patient_paid"],
        reverse=True,
    )
    for patient_id, stats in sorted_patients:
        print(f"{patient_id} | {stats['name']}")
        print(
            f"  Appointments: {stats['appointments']} | "
            f"Completed: {stats['completed']} | Cancelled: {stats['cancelled']}"
        )
        print(
            f"  Total Charges: {format_money(stats['total_charges'])} | "
            f"Insurance Coverage: {format_money(stats['coverage'])} | "
            f"Patient Paid: {format_money(stats['patient_paid'])}"
        )

    print(f"Highest Spending Patient: {report['highest_spending_patient']}")
    print(f"Patient With Most Appointments: {report['most_appointments_patient']}")
    print(
        f"No Completed Appointment: {', '.join(report['no_completed_patients']) or 'None'}"
    )
    print(f"Insured Patients: {', '.join(report['insured_patients']) or 'None'}")
    print(f"Senior Patients: {', '.join(report['senior_patients']) or 'None'}")
    print("=" * 40)


# ---------- clinic dashboard ----------


def generate_clinic_report():
    bills = get_all_bills()
    doctor_report = generate_doctor_report()
    patient_report = generate_patient_report()

    return {
        "total_patients": len(patients),
        "total_doctors": len(doctors),
        "total_appointments": len(appointments),
        "completed": len([a for a in appointments if a["status"] == "completed"]),
        "cancelled": len([a for a in appointments if a["status"] == "cancelled"]),
        "pending": len([a for a in appointments if a["status"] == "pending"]),
        "consultation_revenue": sum(b["fee"] for b in bills),
        "test_revenue": sum(b["test_charges"] for b in bills),
        "insurance_coverage": sum(b["coverage"] for b in bills),
        "patient_revenue": sum(b["patient_paid"] for b in bills),
        "most_requested_specialization": doctor_report["most_requested_specialization"],
        "highest_spending_patient": patient_report["highest_spending_patient"],
    }


def show_clinic_report():
    report = generate_clinic_report()
    print("=" * 40)
    print("CLINIC DASHBOARD")
    print("=" * 40)
    print(f"Total Patients: {report['total_patients']}")
    print(f"Total Doctors: {report['total_doctors']}")
    print(f"Total Appointments: {report['total_appointments']}")
    print(f"Completed: {report['completed']}")
    print(f"Cancelled: {report['cancelled']}")
    print(f"Pending: {report['pending']}")
    print(f"Total Consultation Revenue: {format_money(report['consultation_revenue'])}")
    print(f"Total Test Revenue: {format_money(report['test_revenue'])}")
    print(f"Total Insurance Coverage: {format_money(report['insurance_coverage'])}")
    print(f"Total Patient Revenue: {format_money(report['patient_revenue'])}")
    print(f"Most Requested Specialization: {report['most_requested_specialization']}")
    print(f"Highest Spending Patient: {report['highest_spending_patient']}")
    print("=" * 40)


# ---------- CLI ----------


def show_menu():
    print("\n===== CLINIC MENU =====")
    print("1. Process appointment")
    print("2. Cancel appointment")
    print("3. Doctor report")
    print("4. Patient report")
    print("5. Clinic dashboard")
    print("6. Exit")


def main():
    while True:
        show_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            appointment_id = input("Appointment ID: ").strip().upper()
            print(process_appointment(appointment_id))
        elif choice == "2":
            appointment_id = input("Appointment ID: ").strip().upper()
            print(cancel_appointment(appointment_id))
        elif choice == "3":
            show_doctor_report()
        elif choice == "4":
            show_patient_report()
        elif choice == "5":
            show_clinic_report()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please enter 1-6")


if __name__ == "__main__":
    main()
