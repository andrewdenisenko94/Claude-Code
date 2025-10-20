# Medical Note Template System

A flexible and extensible Python-based template system for creating various types of medical notes including consultation notes, Epic handoff notes, and operative reports.

## Features

- **Multiple Template Types**: Pre-built templates for consult notes, handoff notes, and operative reports
- **Modifiable Fields**: Easy-to-use interface for setting and modifying note content
- **Validation**: Built-in validation to ensure required fields are completed
- **Structured Output**: Professional, well-formatted medical notes
- **Extensible Design**: Abstract base class allows for easy creation of custom templates
- **Field Management**: Support for both required and optional fields
- **List Support**: Automatic formatting of list-based fields (medications, recommendations, etc.)
- **Export Capability**: Export notes to dictionary format for integration with other systems

## Installation

This is a standalone Python module with no external dependencies. Simply clone or download the repository:

```bash
git clone <repository-url>
cd medical-note-templates
```

## Quick Start

```python
from medical_note_template import create_template

# Create a consult note
consult = create_template('consult')

# Set required fields
consult.set_multiple_fields({
    'patient_name': 'John Doe',
    'patient_mrn': '12345678',
    'date_of_consult': '2025-10-20',
    'consulting_service': 'Cardiology',
    'reason_for_consult': 'Evaluate for cardiac etiology of chest pain',
    'history_of_present_illness': 'Patient presents with...',
    'assessment': 'Likely angina...',
    'recommendations': ['Start aspirin', 'Cardiology follow-up']
})

# Generate the formatted note
print(consult.format_note())
```

## Template Types

### 1. Consultation Note (`ConsultNoteTemplate`)

Used when a specialist provides consultation on a patient.

**Required Fields:**
- `patient_name`
- `patient_mrn`
- `date_of_consult`
- `consulting_service`
- `reason_for_consult`
- `history_of_present_illness`
- `assessment`
- `recommendations`

**Optional Fields:**
- `patient_dob`, `age`, `sex`
- `referring_provider`
- `past_medical_history`, `past_surgical_history`
- `medications`, `allergies`
- `social_history`, `family_history`
- `review_of_systems`, `physical_exam`
- `labs`, `imaging`, `other_studies`
- `differential_diagnosis`, `plan`
- `follow_up`
- `attending_physician`, `consulting_physician`

### 2. Epic Handoff Note (`EpicHandoffTemplate`)

Used for patient handoffs between shifts or providers.

**Required Fields:**
- `patient_name`
- `patient_mrn`
- `patient_location`
- `primary_diagnosis`
- `active_issues`

**Optional Fields:**
- `age`, `sex`
- `admission_date`, `hospital_day`
- `brief_history`, `past_medical_history`
- `code_status`, `allergies`
- `vital_signs`, `key_labs`, `key_imaging`
- `current_medications`, `iv_fluids`
- `diet`, `activity`
- `lines_tubes_drains`
- `pending_studies`, `pending_consults`
- `to_do_list`, `if_then_scenarios`
- `anticipated_discharge_date`, `discharge_planning`
- `family_communication`
- `handoff_from`, `handoff_to`

### 3. Operative Report (`OperativeReportTemplate`)

Used to document surgical procedures.

**Required Fields:**
- `patient_name`
- `patient_mrn`
- `date_of_surgery`
- `preoperative_diagnosis`
- `postoperative_diagnosis`
- `procedure_performed`
- `surgeon`
- `anesthesia_type`
- `operative_findings`
- `description_of_procedure`
- `estimated_blood_loss`
- `specimens`
- `complications`
- `disposition`

**Optional Fields:**
- `patient_dob`, `age`, `sex`
- `indication`
- `assistant_surgeon`, `attending_surgeon`
- `anesthesiologist`, `nurses`
- `start_time`, `end_time`, `total_time`
- `ivf_given`, `urine_output`
- `drains`, `implants`
- `counts_correct`, `pathology`
- `condition`, `follow_up_plan`

## Usage Examples

### Creating a Template

There are two ways to create a template:

```python
# Method 1: Direct instantiation
from medical_note_template import ConsultNoteTemplate
consult = ConsultNoteTemplate()

# Method 2: Factory function (recommended)
from medical_note_template import create_template
consult = create_template('consult')
handoff = create_template('handoff')
operative = create_template('operative')
```

### Setting Field Values

```python
# Set a single field
note.set_field('patient_name', 'John Doe')

# Set multiple fields at once
note.set_multiple_fields({
    'patient_name': 'John Doe',
    'patient_mrn': '12345678',
    'age': '55'
})

# Get a field value
name = note.get_field('patient_name')
```

### Working with Lists

Many fields support both string and list formats:

```python
# Medications as a list (automatically formatted with bullets)
note.set_field('medications', [
    'Aspirin 81mg daily',
    'Lisinopril 10mg daily',
    'Metformin 1000mg twice daily'
])

# Or as a string
note.set_field('medications', 'Aspirin 81mg daily, Lisinopril 10mg daily')

# Recommendations as a list
note.set_field('recommendations', [
    'Start aspirin 325mg daily',
    'Admit to telemetry',
    'Cardiology to follow'
])
```

### Validation

```python
# Check if all required fields are filled
is_valid, missing_fields = note.validate()

if not is_valid:
    print(f"Missing required fields: {missing_fields}")

# Get list of required and optional fields
required = note.get_required_fields()
optional = note.get_optional_fields()
```

### Generating the Note

```python
# Generate the formatted note
formatted_note = note.format_note()
print(formatted_note)

# Save to file
with open('consult_note.txt', 'w') as f:
    f.write(formatted_note)
```

### Exporting Data

```python
# Export note data to dictionary
data = note.export_to_dict()

# This returns:
# {
#     'template_type': 'ConsultNoteTemplate',
#     'created_date': '2025-10-20T12:00:00',
#     'last_modified': '2025-10-20T12:05:00',
#     'fields': { ... }
# }
```

### Clearing and Reusing

```python
# Clear all fields to reuse the template
note.clear()
```

## Complete Examples

See `examples.py` for complete, runnable examples of all template types:

```bash
python examples.py
```

This will generate sample notes demonstrating:
1. Consultation Note with full patient workup
2. Epic Handoff Note for ICU patient
3. Operative Report for appendectomy
4. Validation workflow
5. Export functionality

## Customization

### Creating Custom Templates

You can easily create custom templates by extending the base class:

```python
from medical_note_template import MedicalNoteTemplate

class DischargeNoteTemplate(MedicalNoteTemplate):
    def get_required_fields(self):
        return [
            'patient_name',
            'patient_mrn',
            'discharge_date',
            'admission_diagnosis',
            'discharge_diagnosis',
            'discharge_medications',
            'follow_up'
        ]

    def get_optional_fields(self):
        return [
            'hospital_course',
            'discharge_condition',
            'discharge_instructions'
        ]

    def format_note(self):
        # Implement your custom formatting logic
        note = "DISCHARGE SUMMARY\n\n"
        note += f"Patient: {self.get_field('patient_name')}\n"
        # ... add more formatting
        return note
```

### Modifying Existing Templates

The templates are designed to be easily modified. You can:

1. Fork the repository and modify the template classes directly
2. Extend existing templates with additional fields
3. Override the `format_note()` method to change the output format
4. Modify the `_format_section()` helper methods for different styling

## Architecture

### Class Hierarchy

```
MedicalNoteTemplate (Abstract Base Class)
├── ConsultNoteTemplate
├── EpicHandoffTemplate
└── OperativeReportTemplate
```

### Key Methods

- `set_field(name, value)`: Set a single field
- `set_multiple_fields(dict)`: Set multiple fields at once
- `get_field(name, default)`: Retrieve a field value
- `validate()`: Check if all required fields are filled
- `format_note()`: Generate the formatted note text
- `export_to_dict()`: Export note data as dictionary
- `clear()`: Clear all field values

### Design Principles

1. **Separation of Concerns**: Data storage, validation, and formatting are separated
2. **Extensibility**: Easy to add new template types or modify existing ones
3. **Type Safety**: Abstract base class ensures consistent interface
4. **Flexibility**: Support for both string and list field values
5. **Validation**: Built-in validation prevents incomplete notes

## Use Cases

### Clinical Scenarios

1. **Specialist Consultations**: Generate structured consult notes with recommendations
2. **Shift Changes**: Create comprehensive handoff notes for patient transfers
3. **Surgical Documentation**: Document operative procedures with all required details
4. **Quality Assurance**: Ensure consistent documentation across providers
5. **Training**: Teach proper note structure to medical students and residents

### Integration Scenarios

1. **EMR Integration**: Export notes to integrate with electronic medical records
2. **Voice Dictation**: Combine with speech-to-text for dictated notes
3. **Template Libraries**: Build institutional template libraries
4. **Automated Documentation**: Pre-fill fields from existing data sources
5. **Audit Trails**: Track note creation and modification times

## Best Practices

1. **Always Validate**: Call `validate()` before generating final notes
2. **Use Lists for Clarity**: Use list format for medications, recommendations, etc.
3. **Be Thorough**: Fill optional fields when relevant for complete documentation
4. **Review Output**: Always review generated notes before use in clinical settings
5. **Customize as Needed**: Adapt templates to your institution's requirements

## Important Notes

- **Not a Medical Device**: This is a documentation tool, not a medical device
- **Clinical Review Required**: All generated notes should be reviewed by qualified healthcare providers
- **Privacy**: Ensure HIPAA compliance when using with real patient data
- **Customization**: Adapt templates to meet your institution's documentation requirements
- **Validation**: Always validate notes before clinical use

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and examples
5. Submit a pull request

## License

This project is provided as-is for educational and documentation purposes.

## Support

For issues, questions, or feature requests, please open an issue on the repository.

## Changelog

### Version 1.0.0 (2025-10-20)
- Initial release
- Three template types: Consult, Handoff, Operative Report
- Full validation support
- Export functionality
- Comprehensive examples

## Future Enhancements

Potential future additions:
- Progress note template
- Discharge summary template
- Procedure note template
- H&P (History & Physical) template
- JSON/XML export options
- Template import/export
- Custom field validators
- Multi-language support
- Integration with common EMR systems
