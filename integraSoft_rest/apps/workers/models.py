from django.db import models

# Clase que se encarga de comparar los trabajadores de peoplesoft con los trabajadores de wsdl
class WorkerFormatComparison:

    def __init__(self, 
                person_number: str, 
                name: str, 
                email: str,
                address1: str,
                address2: str,
                city: str,
                location_code: str,
                codigo_centro_costo: str,
            ):
        
        self.person_number: str = self.format_person_number( person_number)
        self.name: str = name
        self.email: str = email
        self.address1: str = address1
        self.address2: str = address2
        self.city: str = city
        self.location_code: str = location_code
        self.ccu_codigo_centro_costo: str = codigo_centro_costo


    @staticmethod
    def format_person_number(person_number: str):
        if person_number:
            person_number = person_number.strip()
        return person_number



class WorkerHcmNames(models.Model):
    legislation_code = models.CharField(max_length=10)
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    middle_names = models.CharField(max_length=20)
    display_name = models.CharField(max_length=20)
    order_name = models.CharField(max_length=20)
    list_name = models.CharField(max_length=20)
    full_name = models.CharField(max_length=20)
    name_language = models.CharField(max_length=20)
    created_by = models.CharField(max_length=20)
    creation_date = models.CharField(max_length=20)
    last_updated_by = models.CharField(max_length=20)
    last_update_date = models.CharField(max_length=20)
    link = models.CharField(max_length=500)

class WorkerHcmEmails(models.Model):
    email_address_id = models.CharField(max_length=30)
    email_type = models.CharField(max_length=5)
    email_address = models.CharField(max_length=20)
    from_date = models.CharField(max_length=20)
    to_date = models.CharField(max_length=20)
    created_by = models.CharField(max_length=20)
    creation_date = models.CharField(max_length=20)
    last_updated_by = models.CharField(max_length=20)
    last_update_date = models.CharField(max_length=20)
    primary_flag = models.CharField(max_length=20)
    link = models.CharField(max_length=500)

class WorkerHcmPhones(models.Model):
    phone_id = models.CharField(max_length=20)
    phone_type = models.CharField(max_length=20)
    legislation_code = models.CharField(max_length=20)
    country_code_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    from_date = models.CharField(max_length=20)
    created_by = models.CharField(max_length=20)
    creation_date = models.CharField(max_length=20)
    last_updated_by = models.CharField(max_length=20)
    last_update_date = models.CharField(max_length=20)
    primary_flag = models.CharField(max_length=20)
    link = models.CharField(max_length=500)

class WorkerHcmAddresses(models.Model):
    effective_start_date = models.CharField(max_length=20)
    effective_end_date = models.CharField(max_length=20)
    addressLine1 = models.CharField(max_length=30)
    addressLine2 = models.CharField(max_length=30)
    addressLine3 = models.CharField(max_length=30)
    addressLine4 = models.CharField(max_length=30)
    town_or_city = models.CharField(max_length=30)
    # region_1 = models.CharField(max_length=20)
    # region_2 = models.CharField(max_length=20)
    # region_3 = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)
    created_by = models.CharField(max_length=50)
    creation_date = models.CharField(max_length=50)
    last_updated_by = models.CharField(max_length=20)
    last_update_date = models.CharField(max_length=50)
    address_type = models.CharField(max_length=20)
    primary_flag = models.CharField(max_length=20)
    link = models.CharField(max_length=500)  # Assuming link is a string of max length 500

class WorkerHcmWorkRelationshipsAssignments(models.Model):
    assignment_id = models.CharField(max_length=20)
    assignment_number = models.CharField(max_length=20)
    assignment_name = models.CharField(max_length=20)
    action_code = models.CharField(max_length=20)
    # reason_code = models.CharField(max_length=20)
    effective_start_date = models.CharField(max_length=20)
    effective_end_date = models.CharField(max_length=20)
    # effective_sequence = models.CharField(max_length=20)
    # effective_latest_change = models.CharField(max_length=20)
    business_unit_id = models.CharField(max_length=20)
    business_unit_name = models.CharField(max_length=20)
    assignment_type = models.CharField(max_length=20)
    assignment_status_type_id = models.CharField(max_length=20)
    assignment_status_type_code = models.CharField(max_length=20)
    assignment_status_type = models.CharField(max_length=20)
    system_person_type = models.CharField(max_length=20)
    user_person_type_id = models.CharField(max_length=20)
    user_person_type = models.CharField(max_length=20)
    # primary_flag = models.CharField(max_length=20)
    # primary_assignment_flag = models.CharField(max_length=20)
    # synchronize_from_position_flag = models.CharField(max_length=20)
    job_id = models.CharField(max_length=20)
    job_code = models.CharField(max_length=20)
    department_id = models.CharField(max_length=20)
    department_name = models.CharField(max_length=100)
    # location_id = models.CharField(max_length=20)
    # location_code = models.CharField(max_length=20)
    # work_at_home_flag = models.CharField(max_length=20)
    # assignment_category = models.CharField(max_length=20)
    # worker_category = models.CharField(max_length=20)
    # permanent_temporary = models.CharField(max_length=20)
    # full_part_time = models.CharField(max_length=20)
    # manager_flag = models.CharField(max_length=20)
    # hourly_salaried_code = models.CharField(max_length=20)
    # normal_hours = models.CharField(max_length=20)
    # frequency = models.CharField(max_length=20)
    # labour_union_member_flag = models.CharField(max_length=20)
    # union_id = models.CharField(max_length=20)
    # union_name = models.CharField(max_length=20)
    # collective_agreement_id = models.CharField(max_length=20)
    # collective_agreement_name = models.CharField(max_length=20)
    standard_working_hours = models.CharField(max_length=20)
    # standard_frequency = models.CharField(max_length=20)
    created_by = models.CharField(max_length=20)
    creation_date = models.CharField(max_length=20)
    last_updated_by = models.CharField(max_length=20)
    last_update_date = models.CharField(max_length=20)
    link = models.CharField(max_length=500)

    def __str__(self):
        return self.assignment_name

class WorkerHcmWorkRelationships(models.Model):
    period_of_service_id = models.CharField(max_length=20)
    legislation_code = models.CharField(max_length=20)
    legal_entity_id = models.CharField(max_length=20)
    legal_employer_name = models.CharField(max_length=20)
    worker_type = models.CharField(max_length=20)
    primary_flag = models.CharField(max_length=20)
    start_date = models.CharField(max_length=20)
    # legal_employer_seniority_date = models.CharField(max_length=20, help_text='LegalEmployerSeniorityDate')
    # enterprise_seniority_date = models.CharField(max_length=20, help_text='EnterpriseSeniorityDate')
    # on_military_service_flag = models.CharField(max_length=20, help_text='OnMilitaryServiceFlag')
    worker_number = models.CharField(max_length=20)
    # recommended_for_rehire = models.CharField(max_length=20, help_text='RecommendedForRehire')
    # recommendation_reason = models.CharField(max_length=20, help_text='RecommendationReason')
    # recommendation_authorized_by_person_id = models.CharField(max_length=20, help_text='RecommendationAuthorizedByPersonId')
    created_by = models.CharField(max_length=20)
    creation_date = models.CharField(max_length=20)
    last_updated_by = models.CharField(max_length=20)
    last_update_date = models.CharField(max_length=20)
    projected_termination_date = models.CharField(max_length=20)
    link = models.CharField(max_length=500)
    assignments = models.ForeignKey(WorkerHcmWorkRelationshipsAssignments, on_delete=models.CASCADE)

class WorkerHcm(models.Model):
    person_id = models.CharField(max_length=20)
    person_number = models.CharField(max_length=20)
    date_of_birth = models.CharField(max_length=20)
    date_of_death = models.CharField(max_length=20)
    country_of_birth = models.CharField(max_length=20)
    region_of_birth = models.CharField(max_length=20)
    town_of_birth = models.CharField(max_length=20)
    created_by = models.CharField(max_length=20)
    creation_date = models.CharField(max_length=20)
    last_updated_by = models.CharField(max_length=20)
    last_update_date = models.CharField(max_length=20)
    link = models.CharField(max_length=500)
    names = models.OneToOneField(WorkerHcmNames, on_delete=models.CASCADE)
    emails = models.ForeignKey(WorkerHcmEmails, on_delete=models.CASCADE)
    phones = models.ForeignKey(WorkerHcmPhones, on_delete=models.CASCADE)
    addresses = models.ForeignKey(WorkerHcmAddresses, on_delete=models.CASCADE)
    work_relationships = models.ForeignKey(WorkerHcmWorkRelationships, on_delete=models.CASCADE)