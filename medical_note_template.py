"""
Medical Note Template System
A modifiable template system for generating various types of medical notes.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Any


class MedicalNoteTemplate(ABC):
    """
    Base class for all medical note templates.
    Provides common functionality for creating, editing, and formatting medical notes.
    """

    def __init__(self):
        self.fields: Dict[str, Any] = {}
        self.created_date = datetime.now()
        self.last_modified = datetime.now()

    @abstractmethod
    def get_required_fields(self) -> List[str]:
        """Return list of required field names for this template."""
        pass

    @abstractmethod
    def get_optional_fields(self) -> List[str]:
        """Return list of optional field names for this template."""
        pass

    @abstractmethod
    def format_note(self) -> str:
        """Format and return the complete medical note."""
        pass

    def set_field(self, field_name: str, value: Any) -> None:
        """Set a field value in the template."""
        self.fields[field_name] = value
        self.last_modified = datetime.now()

    def get_field(self, field_name: str, default: Any = None) -> Any:
        """Get a field value from the template."""
        return self.fields.get(field_name, default)

    def set_multiple_fields(self, field_dict: Dict[str, Any]) -> None:
        """Set multiple fields at once."""
        self.fields.update(field_dict)
        self.last_modified = datetime.now()

    def validate(self) -> tuple[bool, List[str]]:
        """
        Validate that all required fields are filled.
        Returns (is_valid, list_of_missing_fields)
        """
        missing_fields = []
        for field in self.get_required_fields():
            if field not in self.fields or not self.fields[field]:
                missing_fields.append(field)
        return (len(missing_fields) == 0, missing_fields)

    def clear(self) -> None:
        """Clear all field values."""
        self.fields = {}
        self.last_modified = datetime.now()

    def export_to_dict(self) -> Dict[str, Any]:
        """Export the note as a dictionary."""
        return {
            'template_type': self.__class__.__name__,
            'created_date': self.created_date.isoformat(),
            'last_modified': self.last_modified.isoformat(),
            'fields': self.fields.copy()
        }

    def _format_section(self, title: str, content: str, indent: int = 0) -> str:
        """Helper method to format a section with title and content."""
        if not content:
            return ""
        indent_str = " " * indent
        return f"{indent_str}{title}:\n{indent_str}{content}\n\n"

    def _format_list_section(self, title: str, items: List[str], indent: int = 0) -> str:
        """Helper method to format a section with a list of items."""
        if not items:
            return ""
        indent_str = " " * indent
        formatted_items = "\n".join([f"{indent_str}- {item}" for item in items])
        return f"{indent_str}{title}:\n{formatted_items}\n\n"


class ConsultNoteTemplate(MedicalNoteTemplate):
    """
    Template for consultation notes.
    Used when a specialist provides consultation on a patient.
    """

    def get_required_fields(self) -> List[str]:
        return [
            'patient_name',
            'patient_mrn',
            'date_of_consult',
            'consulting_service',
            'reason_for_consult',
            'history_of_present_illness',
            'assessment',
            'recommendations'
        ]

    def get_optional_fields(self) -> List[str]:
        return [
            'patient_dob',
            'age',
            'sex',
            'referring_provider',
            'past_medical_history',
            'past_surgical_history',
            'medications',
            'allergies',
            'social_history',
            'family_history',
            'review_of_systems',
            'physical_exam',
            'labs',
            'imaging',
            'other_studies',
            'differential_diagnosis',
            'plan',
            'follow_up',
            'attending_physician',
            'consulting_physician'
        ]

    def format_note(self) -> str:
        """Format the consult note."""
        note = "=" * 80 + "\n"
        note += "CONSULTATION NOTE\n"
        note += "=" * 80 + "\n\n"

        # Patient Demographics
        note += "PATIENT INFORMATION:\n"
        note += f"Name: {self.get_field('patient_name', '[NOT PROVIDED]')}\n"
        note += f"MRN: {self.get_field('patient_mrn', '[NOT PROVIDED]')}\n"
        if self.get_field('patient_dob'):
            note += f"DOB: {self.get_field('patient_dob')}\n"
        if self.get_field('age'):
            note += f"Age: {self.get_field('age')}\n"
        if self.get_field('sex'):
            note += f"Sex: {self.get_field('sex')}\n"
        note += f"Date of Consult: {self.get_field('date_of_consult', '[NOT PROVIDED]')}\n"
        note += f"Consulting Service: {self.get_field('consulting_service', '[NOT PROVIDED]')}\n"
        if self.get_field('referring_provider'):
            note += f"Referring Provider: {self.get_field('referring_provider')}\n"
        note += "\n"

        # Reason for Consult
        note += self._format_section("REASON FOR CONSULT",
                                     self.get_field('reason_for_consult', '[NOT PROVIDED]'))

        # History of Present Illness
        note += self._format_section("HISTORY OF PRESENT ILLNESS",
                                     self.get_field('history_of_present_illness', '[NOT PROVIDED]'))

        # Past Medical History
        if self.get_field('past_medical_history'):
            note += self._format_section("PAST MEDICAL HISTORY",
                                        self.get_field('past_medical_history'))

        # Past Surgical History
        if self.get_field('past_surgical_history'):
            note += self._format_section("PAST SURGICAL HISTORY",
                                        self.get_field('past_surgical_history'))

        # Medications
        if self.get_field('medications'):
            if isinstance(self.get_field('medications'), list):
                note += self._format_list_section("MEDICATIONS",
                                                  self.get_field('medications'))
            else:
                note += self._format_section("MEDICATIONS",
                                            self.get_field('medications'))

        # Allergies
        if self.get_field('allergies'):
            note += self._format_section("ALLERGIES", self.get_field('allergies'))

        # Social History
        if self.get_field('social_history'):
            note += self._format_section("SOCIAL HISTORY",
                                        self.get_field('social_history'))

        # Family History
        if self.get_field('family_history'):
            note += self._format_section("FAMILY HISTORY",
                                        self.get_field('family_history'))

        # Review of Systems
        if self.get_field('review_of_systems'):
            note += self._format_section("REVIEW OF SYSTEMS",
                                        self.get_field('review_of_systems'))

        # Physical Exam
        if self.get_field('physical_exam'):
            note += self._format_section("PHYSICAL EXAMINATION",
                                        self.get_field('physical_exam'))

        # Labs
        if self.get_field('labs'):
            note += self._format_section("LABORATORY DATA", self.get_field('labs'))

        # Imaging
        if self.get_field('imaging'):
            note += self._format_section("IMAGING", self.get_field('imaging'))

        # Other Studies
        if self.get_field('other_studies'):
            note += self._format_section("OTHER STUDIES",
                                        self.get_field('other_studies'))

        # Assessment
        note += self._format_section("ASSESSMENT",
                                     self.get_field('assessment', '[NOT PROVIDED]'))

        # Differential Diagnosis
        if self.get_field('differential_diagnosis'):
            if isinstance(self.get_field('differential_diagnosis'), list):
                note += self._format_list_section("DIFFERENTIAL DIAGNOSIS",
                                                  self.get_field('differential_diagnosis'))
            else:
                note += self._format_section("DIFFERENTIAL DIAGNOSIS",
                                            self.get_field('differential_diagnosis'))

        # Recommendations
        if isinstance(self.get_field('recommendations'), list):
            note += self._format_list_section("RECOMMENDATIONS",
                                             self.get_field('recommendations', ['[NOT PROVIDED]']))
        else:
            note += self._format_section("RECOMMENDATIONS",
                                        self.get_field('recommendations', '[NOT PROVIDED]'))

        # Plan
        if self.get_field('plan'):
            if isinstance(self.get_field('plan'), list):
                note += self._format_list_section("PLAN", self.get_field('plan'))
            else:
                note += self._format_section("PLAN", self.get_field('plan'))

        # Follow-up
        if self.get_field('follow_up'):
            note += self._format_section("FOLLOW-UP", self.get_field('follow_up'))

        # Signature
        note += "\n" + "-" * 80 + "\n"
        if self.get_field('consulting_physician'):
            note += f"Consulting Physician: {self.get_field('consulting_physician')}\n"
        if self.get_field('attending_physician'):
            note += f"Attending Physician: {self.get_field('attending_physician')}\n"
        note += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"

        return note


class EpicHandoffTemplate(MedicalNoteTemplate):
    """
    Template for Epic handoff notes.
    Used for patient handoffs between shifts or providers.
    """

    def get_required_fields(self) -> List[str]:
        return [
            'patient_name',
            'patient_mrn',
            'patient_location',
            'primary_diagnosis',
            'active_issues'
        ]

    def get_optional_fields(self) -> List[str]:
        return [
            'age',
            'sex',
            'admission_date',
            'hospital_day',
            'brief_history',
            'past_medical_history',
            'code_status',
            'allergies',
            'vital_signs',
            'key_labs',
            'key_imaging',
            'current_medications',
            'iv_fluids',
            'diet',
            'activity',
            'lines_tubes_drains',
            'pending_studies',
            'pending_consults',
            'to_do_list',
            'if_then_scenarios',
            'anticipated_discharge_date',
            'discharge_planning',
            'family_communication',
            'handoff_from',
            'handoff_to'
        ]

    def format_note(self) -> str:
        """Format the Epic handoff note."""
        note = "=" * 80 + "\n"
        note += "HANDOFF NOTE\n"
        note += "=" * 80 + "\n\n"

        # Header
        note += f"Patient: {self.get_field('patient_name', '[NOT PROVIDED]')}\n"
        note += f"MRN: {self.get_field('patient_mrn', '[NOT PROVIDED]')}\n"
        note += f"Location: {self.get_field('patient_location', '[NOT PROVIDED]')}\n"
        if self.get_field('age'):
            note += f"Age: {self.get_field('age')}\n"
        if self.get_field('sex'):
            note += f"Sex: {self.get_field('sex')}\n"
        if self.get_field('admission_date'):
            note += f"Admission Date: {self.get_field('admission_date')}\n"
        if self.get_field('hospital_day'):
            note += f"Hospital Day: {self.get_field('hospital_day')}\n"
        if self.get_field('code_status'):
            note += f"Code Status: {self.get_field('code_status')}\n"
        note += f"Handoff Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        if self.get_field('handoff_from'):
            note += f"From: {self.get_field('handoff_from')}\n"
        if self.get_field('handoff_to'):
            note += f"To: {self.get_field('handoff_to')}\n"
        note += "\n"

        # Primary Diagnosis
        note += self._format_section("PRIMARY DIAGNOSIS",
                                     self.get_field('primary_diagnosis', '[NOT PROVIDED]'))

        # Brief History
        if self.get_field('brief_history'):
            note += self._format_section("BRIEF HISTORY",
                                        self.get_field('brief_history'))

        # Past Medical History
        if self.get_field('past_medical_history'):
            note += self._format_section("PAST MEDICAL HISTORY",
                                        self.get_field('past_medical_history'))

        # Allergies
        if self.get_field('allergies'):
            note += self._format_section("ALLERGIES", self.get_field('allergies'))

        # Active Issues
        if isinstance(self.get_field('active_issues'), list):
            note += self._format_list_section("ACTIVE ISSUES",
                                             self.get_field('active_issues', ['[NOT PROVIDED]']))
        else:
            note += self._format_section("ACTIVE ISSUES",
                                        self.get_field('active_issues', '[NOT PROVIDED]'))

        # Vital Signs
        if self.get_field('vital_signs'):
            note += self._format_section("VITAL SIGNS", self.get_field('vital_signs'))

        # Key Labs
        if self.get_field('key_labs'):
            note += self._format_section("KEY LABS", self.get_field('key_labs'))

        # Key Imaging
        if self.get_field('key_imaging'):
            note += self._format_section("KEY IMAGING", self.get_field('key_imaging'))

        # Current Medications
        if self.get_field('current_medications'):
            if isinstance(self.get_field('current_medications'), list):
                note += self._format_list_section("CURRENT MEDICATIONS",
                                                  self.get_field('current_medications'))
            else:
                note += self._format_section("CURRENT MEDICATIONS",
                                            self.get_field('current_medications'))

        # IV Fluids
        if self.get_field('iv_fluids'):
            note += self._format_section("IV FLUIDS", self.get_field('iv_fluids'))

        # Diet
        if self.get_field('diet'):
            note += self._format_section("DIET", self.get_field('diet'))

        # Activity
        if self.get_field('activity'):
            note += self._format_section("ACTIVITY", self.get_field('activity'))

        # Lines, Tubes, Drains
        if self.get_field('lines_tubes_drains'):
            if isinstance(self.get_field('lines_tubes_drains'), list):
                note += self._format_list_section("LINES/TUBES/DRAINS",
                                                  self.get_field('lines_tubes_drains'))
            else:
                note += self._format_section("LINES/TUBES/DRAINS",
                                            self.get_field('lines_tubes_drains'))

        # Pending Studies
        if self.get_field('pending_studies'):
            if isinstance(self.get_field('pending_studies'), list):
                note += self._format_list_section("PENDING STUDIES",
                                                  self.get_field('pending_studies'))
            else:
                note += self._format_section("PENDING STUDIES",
                                            self.get_field('pending_studies'))

        # Pending Consults
        if self.get_field('pending_consults'):
            if isinstance(self.get_field('pending_consults'), list):
                note += self._format_list_section("PENDING CONSULTS",
                                                  self.get_field('pending_consults'))
            else:
                note += self._format_section("PENDING CONSULTS",
                                            self.get_field('pending_consults'))

        # To-Do List
        if self.get_field('to_do_list'):
            if isinstance(self.get_field('to_do_list'), list):
                note += self._format_list_section("TO-DO LIST",
                                                  self.get_field('to_do_list'))
            else:
                note += self._format_section("TO-DO LIST",
                                            self.get_field('to_do_list'))

        # If-Then Scenarios
        if self.get_field('if_then_scenarios'):
            if isinstance(self.get_field('if_then_scenarios'), list):
                note += self._format_list_section("IF-THEN SCENARIOS",
                                                  self.get_field('if_then_scenarios'))
            else:
                note += self._format_section("IF-THEN SCENARIOS",
                                            self.get_field('if_then_scenarios'))

        # Discharge Planning
        if self.get_field('anticipated_discharge_date'):
            note += self._format_section("ANTICIPATED DISCHARGE DATE",
                                        self.get_field('anticipated_discharge_date'))

        if self.get_field('discharge_planning'):
            note += self._format_section("DISCHARGE PLANNING",
                                        self.get_field('discharge_planning'))

        # Family Communication
        if self.get_field('family_communication'):
            note += self._format_section("FAMILY COMMUNICATION",
                                        self.get_field('family_communication'))

        note += "=" * 80 + "\n"
        return note


class OperativeReportTemplate(MedicalNoteTemplate):
    """
    Template for operative reports.
    Used to document surgical procedures.
    """

    def get_required_fields(self) -> List[str]:
        return [
            'patient_name',
            'patient_mrn',
            'date_of_surgery',
            'preoperative_diagnosis',
            'postoperative_diagnosis',
            'procedure_performed',
            'surgeon',
            'anesthesia_type',
            'operative_findings',
            'description_of_procedure',
            'estimated_blood_loss',
            'specimens',
            'complications',
            'disposition'
        ]

    def get_optional_fields(self) -> List[str]:
        return [
            'patient_dob',
            'age',
            'sex',
            'indication',
            'assistant_surgeon',
            'attending_surgeon',
            'anesthesiologist',
            'nurses',
            'start_time',
            'end_time',
            'total_time',
            'ivf_given',
            'urine_output',
            'drains',
            'implants',
            'counts_correct',
            'pathology',
            'condition',
            'follow_up_plan'
        ]

    def format_note(self) -> str:
        """Format the operative report."""
        note = "=" * 80 + "\n"
        note += "OPERATIVE REPORT\n"
        note += "=" * 80 + "\n\n"

        # Patient Information
        note += "PATIENT INFORMATION:\n"
        note += f"Name: {self.get_field('patient_name', '[NOT PROVIDED]')}\n"
        note += f"MRN: {self.get_field('patient_mrn', '[NOT PROVIDED]')}\n"
        if self.get_field('patient_dob'):
            note += f"DOB: {self.get_field('patient_dob')}\n"
        if self.get_field('age'):
            note += f"Age: {self.get_field('age')}\n"
        if self.get_field('sex'):
            note += f"Sex: {self.get_field('sex')}\n"
        note += f"Date of Surgery: {self.get_field('date_of_surgery', '[NOT PROVIDED]')}\n"
        if self.get_field('start_time'):
            note += f"Start Time: {self.get_field('start_time')}\n"
        if self.get_field('end_time'):
            note += f"End Time: {self.get_field('end_time')}\n"
        if self.get_field('total_time'):
            note += f"Total Time: {self.get_field('total_time')}\n"
        note += "\n"

        # Surgical Team
        note += "SURGICAL TEAM:\n"
        note += f"Surgeon: {self.get_field('surgeon', '[NOT PROVIDED]')}\n"
        if self.get_field('assistant_surgeon'):
            note += f"Assistant Surgeon: {self.get_field('assistant_surgeon')}\n"
        if self.get_field('attending_surgeon'):
            note += f"Attending Surgeon: {self.get_field('attending_surgeon')}\n"
        if self.get_field('anesthesiologist'):
            note += f"Anesthesiologist: {self.get_field('anesthesiologist')}\n"
        note += f"Anesthesia Type: {self.get_field('anesthesia_type', '[NOT PROVIDED]')}\n"
        if self.get_field('nurses'):
            note += f"Nursing Staff: {self.get_field('nurses')}\n"
        note += "\n"

        # Diagnoses
        note += self._format_section("PREOPERATIVE DIAGNOSIS",
                                     self.get_field('preoperative_diagnosis', '[NOT PROVIDED]'))

        note += self._format_section("POSTOPERATIVE DIAGNOSIS",
                                     self.get_field('postoperative_diagnosis', '[NOT PROVIDED]'))

        # Procedure
        if isinstance(self.get_field('procedure_performed'), list):
            note += self._format_list_section("PROCEDURE(S) PERFORMED",
                                             self.get_field('procedure_performed', ['[NOT PROVIDED]']))
        else:
            note += self._format_section("PROCEDURE(S) PERFORMED",
                                        self.get_field('procedure_performed', '[NOT PROVIDED]'))

        # Indication
        if self.get_field('indication'):
            note += self._format_section("INDICATION", self.get_field('indication'))

        # Operative Findings
        note += self._format_section("OPERATIVE FINDINGS",
                                     self.get_field('operative_findings', '[NOT PROVIDED]'))

        # Description of Procedure
        note += self._format_section("DESCRIPTION OF PROCEDURE",
                                     self.get_field('description_of_procedure', '[NOT PROVIDED]'))

        # Intraoperative Details
        note += "INTRAOPERATIVE DETAILS:\n"
        note += f"Estimated Blood Loss: {self.get_field('estimated_blood_loss', '[NOT PROVIDED]')}\n"
        if self.get_field('ivf_given'):
            note += f"IV Fluids Given: {self.get_field('ivf_given')}\n"
        if self.get_field('urine_output'):
            note += f"Urine Output: {self.get_field('urine_output')}\n"
        note += "\n"

        # Specimens
        note += self._format_section("SPECIMENS",
                                     self.get_field('specimens', '[NOT PROVIDED]'))

        # Pathology
        if self.get_field('pathology'):
            note += self._format_section("PATHOLOGY", self.get_field('pathology'))

        # Drains/Implants
        if self.get_field('drains'):
            note += self._format_section("DRAINS", self.get_field('drains'))

        if self.get_field('implants'):
            note += self._format_section("IMPLANTS", self.get_field('implants'))

        # Counts
        if self.get_field('counts_correct'):
            note += self._format_section("COUNTS", self.get_field('counts_correct'))

        # Complications
        note += self._format_section("COMPLICATIONS",
                                     self.get_field('complications', '[NOT PROVIDED]'))

        # Disposition
        note += self._format_section("DISPOSITION",
                                     self.get_field('disposition', '[NOT PROVIDED]'))

        # Condition
        if self.get_field('condition'):
            note += self._format_section("CONDITION", self.get_field('condition'))

        # Follow-up
        if self.get_field('follow_up_plan'):
            note += self._format_section("FOLLOW-UP PLAN",
                                        self.get_field('follow_up_plan'))

        # Signature
        note += "\n" + "-" * 80 + "\n"
        note += f"Surgeon: {self.get_field('surgeon', '[NOT PROVIDED]')}\n"
        if self.get_field('attending_surgeon'):
            note += f"Attending: {self.get_field('attending_surgeon')}\n"
        note += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"

        return note


# Factory function for easy template creation
def create_template(template_type: str) -> MedicalNoteTemplate:
    """
    Factory function to create a medical note template.

    Args:
        template_type: Type of template ('consult', 'handoff', or 'operative')

    Returns:
        Instance of the requested template type

    Raises:
        ValueError: If template_type is not recognized
    """
    templates = {
        'consult': ConsultNoteTemplate,
        'handoff': EpicHandoffTemplate,
        'operative': OperativeReportTemplate
    }

    template_type = template_type.lower()
    if template_type not in templates:
        raise ValueError(f"Unknown template type: {template_type}. "
                        f"Valid types are: {', '.join(templates.keys())}")

    return templates[template_type]()
