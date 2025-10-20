"""
Example usage of the Medical Note Template system.
This file demonstrates how to create and use different types of medical notes.
"""

from medical_note_template import (
    ConsultNoteTemplate,
    EpicHandoffTemplate,
    OperativeReportTemplate,
    create_template
)


def example_consult_note():
    """Example: Creating a consultation note"""
    print("\n" + "="*80)
    print("EXAMPLE 1: CONSULT NOTE")
    print("="*80 + "\n")

    # Create a consult note template
    consult = ConsultNoteTemplate()

    # Set required fields
    consult.set_multiple_fields({
        'patient_name': 'John Doe',
        'patient_mrn': '12345678',
        'date_of_consult': '2025-10-20',
        'consulting_service': 'Cardiology',
        'reason_for_consult': 'Evaluate for cardiac etiology of chest pain',
        'history_of_present_illness': '''
        55-year-old male with history of hypertension and hyperlipidemia
        presenting with 3 days of intermittent chest pain. Pain is substernal,
        pressure-like, 6/10 intensity, radiates to left arm, associated with
        diaphoresis. No shortness of breath. Pain worse with exertion,
        improves with rest.
        '''.strip(),
        'assessment': '''
        Chest pain, likely angina
        - High pretest probability for coronary artery disease given risk factors
        - ECG shows ST depressions in lateral leads
        - Troponin mildly elevated at 0.08
        '''.strip(),
        'recommendations': [
            'Start aspirin 325mg daily',
            'Start atorvastatin 80mg daily',
            'Admit to telemetry',
            'NPO after midnight for cardiac catheterization in AM',
            'Cardiology to follow'
        ]
    })

    # Set optional fields
    consult.set_multiple_fields({
        'age': '55',
        'sex': 'Male',
        'past_medical_history': 'Hypertension, Hyperlipidemia, Type 2 Diabetes',
        'medications': [
            'Lisinopril 10mg daily',
            'Metformin 1000mg twice daily',
            'Aspirin 81mg daily'
        ],
        'allergies': 'NKDA',
        'physical_exam': '''
        Vital Signs: BP 145/92, HR 88, RR 16, O2 sat 98% on RA
        General: Alert, mild distress
        Cardiac: Regular rate and rhythm, no murmurs
        Lungs: Clear to auscultation bilaterally
        Extremities: No edema
        '''.strip(),
        'labs': 'Troponin 0.08, BNP 145, Creatinine 1.1',
        'consulting_physician': 'Dr. Jane Smith, Cardiology'
    })

    # Validate the note
    is_valid, missing = consult.validate()
    if not is_valid:
        print(f"Warning: Missing required fields: {missing}\n")

    # Generate and print the note
    print(consult.format_note())

    return consult


def example_handoff_note():
    """Example: Creating a handoff note"""
    print("\n" + "="*80)
    print("EXAMPLE 2: EPIC HANDOFF NOTE")
    print("="*80 + "\n")

    # Use factory function to create template
    handoff = create_template('handoff')

    # Set patient information
    handoff.set_multiple_fields({
        'patient_name': 'Jane Smith',
        'patient_mrn': '87654321',
        'patient_location': 'ICU Bed 12',
        'age': '68',
        'sex': 'Female',
        'admission_date': '2025-10-18',
        'hospital_day': '3',
        'code_status': 'Full Code',
        'primary_diagnosis': 'Septic shock secondary to pneumonia',
        'handoff_from': 'Dr. Williams (Day Team)',
        'handoff_to': 'Dr. Johnson (Night Team)'
    })

    # Set clinical information
    handoff.set_multiple_fields({
        'brief_history': '''
        68F admitted 3 days ago with fevers, hypotension, and altered mental status.
        Blood cultures grew E. coli. Started on broad-spectrum antibiotics.
        Required brief vasopressor support, now off pressors x 24 hours.
        '''.strip(),
        'active_issues': [
            '1. Septic shock - improving, off pressors x 24h, on cefepime day 3',
            '2. Acute kidney injury - Cr improved from 2.8 to 1.5',
            '3. Pneumonia - bilateral infiltrates on CXR',
            '4. Diabetes - holding home meds, on insulin sliding scale'
        ],
        'vital_signs': 'BP 110/65, HR 92, Temp 37.8C, RR 18, O2 sat 95% on 2L NC',
        'key_labs': 'WBC 12.5 (down from 18), Lactate 1.2, Cr 1.5',
        'current_medications': [
            'Cefepime 2g IV q8h',
            'Insulin sliding scale',
            'Heparin subcutaneous prophylaxis'
        ],
        'iv_fluids': 'NS at 75 mL/hr',
        'diet': 'Regular, diabetic',
        'lines_tubes_drains': [
            'Right IJ central line (placed 10/18)',
            'Foley catheter'
        ],
        'to_do_list': [
            'Repeat lactate in AM',
            'Follow-up blood cultures (pending)',
            'Consider stepping down to floor if stable overnight'
        ],
        'if_then_scenarios': [
            'If temp >38.5C: Pan-culture and notify MD',
            'If BP <90 systolic: 500mL bolus, then call MD',
            'If UOP <30mL/hr x 2hr: Call MD'
        ],
        'anticipated_discharge_date': '10/23/2025',
        'discharge_planning': 'Will need 7 more days of IV antibiotics, consider PICC and home health'
    })

    # Generate and print the note
    print(handoff.format_note())

    return handoff


def example_operative_report():
    """Example: Creating an operative report"""
    print("\n" + "="*80)
    print("EXAMPLE 3: OPERATIVE REPORT")
    print("="*80 + "\n")

    # Create operative report template
    op_report = OperativeReportTemplate()

    # Set all required fields
    op_report.set_multiple_fields({
        'patient_name': 'Robert Johnson',
        'patient_mrn': '11223344',
        'date_of_surgery': '2025-10-20',
        'preoperative_diagnosis': 'Acute appendicitis',
        'postoperative_diagnosis': 'Acute appendicitis with perforation',
        'procedure_performed': 'Laparoscopic appendectomy',
        'surgeon': 'Dr. Michael Chen',
        'anesthesia_type': 'General endotracheal anesthesia',
        'operative_findings': '''
        Upon entering the abdomen, there was purulent fluid in the right lower
        quadrant. The appendix was identified and found to be inflamed,
        gangrenous, and perforated at the tip. No other abnormalities noted.
        '''.strip(),
        'description_of_procedure': '''
        After informed consent was obtained, the patient was brought to the OR
        and placed in supine position. General anesthesia was induced. The
        abdomen was prepped and draped in sterile fashion.

        A 12mm umbilical incision was made and Veress needle inserted.
        Pneumoperitoneum established to 15mmHg. Laparoscope inserted and
        diagnostic laparoscopy performed. Two 5mm ports placed in left lower
        quadrant and suprapubic region under direct visualization.

        The appendix was identified and found to be perforated. The mesoappendix
        was divided using LigaSure device. The base of the appendix was divided
        using an endoscopic stapler with two firings. The appendix was placed in
        an endoscopic retrieval bag and removed through the umbilical port.

        The abdomen was copiously irrigated with warm saline until clear.
        Hemostasis confirmed. All port sites closed with absorbable suture.
        Skin closed with subcuticular sutures. Sterile dressing applied.

        Patient tolerated the procedure well and was transferred to PACU in
        stable condition.
        '''.strip(),
        'estimated_blood_loss': '25 mL',
        'specimens': 'Appendix sent to pathology',
        'complications': 'None',
        'disposition': 'To PACU, then floor'
    })

    # Set optional fields
    op_report.set_multiple_fields({
        'age': '42',
        'sex': 'Male',
        'indication': '''
        42-year-old male with 24 hours of right lower quadrant pain, fever,
        and leukocytosis. CT scan shows inflamed appendix with periappendiceal
        fat stranding.
        '''.strip(),
        'assistant_surgeon': 'Dr. Sarah Lee',
        'attending_surgeon': 'Dr. Michael Chen',
        'anesthesiologist': 'Dr. David Park',
        'start_time': '14:30',
        'end_time': '15:45',
        'total_time': '1 hour 15 minutes',
        'ivf_given': '1000 mL Lactated Ringers',
        'urine_output': '200 mL',
        'counts_correct': 'All sponge and instrument counts correct x2',
        'condition': 'Stable, extubated, to PACU',
        'follow_up_plan': '''
        - Advance diet as tolerated
        - IV antibiotics x 24 hours, then transition to PO
        - Anticipated discharge post-op day 1-2
        - Follow up in clinic in 2 weeks for wound check
        '''.strip()
    })

    # Validate and generate
    is_valid, missing = op_report.validate()
    if not is_valid:
        print(f"Warning: Missing required fields: {missing}\n")

    print(op_report.format_note())

    return op_report


def example_validation():
    """Example: Demonstrating validation"""
    print("\n" + "="*80)
    print("EXAMPLE 4: VALIDATION")
    print("="*80 + "\n")

    # Create a template with incomplete data
    consult = ConsultNoteTemplate()
    consult.set_field('patient_name', 'Test Patient')
    consult.set_field('patient_mrn', '99999999')

    # Validate
    is_valid, missing = consult.validate()

    print(f"Is valid: {is_valid}")
    print(f"Missing required fields: {missing}\n")

    print("Required fields for Consult Note:")
    for field in consult.get_required_fields():
        print(f"  - {field}")

    print("\nOptional fields for Consult Note:")
    for field in consult.get_optional_fields():
        print(f"  - {field}")


def example_export():
    """Example: Exporting note data"""
    print("\n" + "="*80)
    print("EXAMPLE 5: EXPORTING NOTE DATA")
    print("="*80 + "\n")

    # Create a simple note
    handoff = create_template('handoff')
    handoff.set_multiple_fields({
        'patient_name': 'Test Patient',
        'patient_mrn': '12345',
        'patient_location': 'Floor 3B',
        'primary_diagnosis': 'Pneumonia',
        'active_issues': ['Pneumonia', 'Hypertension']
    })

    # Export to dictionary
    data = handoff.export_to_dict()

    print("Exported note data:")
    import json
    print(json.dumps(data, indent=2, default=str))


if __name__ == '__main__':
    """Run all examples"""

    # Example 1: Consult Note
    example_consult_note()

    # Example 2: Handoff Note
    example_handoff_note()

    # Example 3: Operative Report
    example_operative_report()

    # Example 4: Validation
    example_validation()

    # Example 5: Export
    example_export()

    print("\n" + "="*80)
    print("All examples completed!")
    print("="*80 + "\n")
