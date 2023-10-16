class WorkerOdt:
    def __init__(self, person_id=None, person_number=None, correspondence_language=None, blood_type=None,
                 date_of_birth=None, date_of_death=None, country_of_birth=None, region_of_birth=None,
                 town_of_birth=None, applicant_number=None, created_by=None, creation_date=None,
                 last_updated_by=None, last_update_date=None, links=None, names=None, emails=None, addresses=None,
                 work_relationships=None):
        self.person_id = person_id
        self.person_number = person_number
        self.correspondence_language = correspondence_language
        self.blood_type = blood_type
        self.date_of_birth = date_of_birth
        self.date_of_death = date_of_death
        self.country_of_birth = country_of_birth
        self.region_of_birth = region_of_birth
        self.town_of_birth = town_of_birth
        self.applicant_number = applicant_number
        self.created_by = created_by
        self.creation_date = creation_date
        self.last_updated_by = last_updated_by
        self.last_update_date = last_update_date
        self.links = links
        self.names = names
        self.emails = emails
        self.addresses = addresses
        self.work_relationships = work_relationships