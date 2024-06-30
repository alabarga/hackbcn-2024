# SQL Script

```sql


CREATE SCHEMA cdm;



CREATE SCHEMA vocabularies;



CREATE TABLE cdm.care_site (
    care_site_id bigint NOT NULL,
    location_id bigint,
    place_of_service_concept_id integer,
    care_site_name text,
    care_site_source_value text,
    place_of_service_source_value text,
    CONSTRAINT chk_care_site_care_site_name CHECK ((length(care_site_name) <= 255))
);


ALTER TABLE cdm.care_site OWNER TO postgres;


COMMENT ON TABLE cdm.care_site IS 'The CARE_SITE table contains a list of uniquely identified institutional (physical or organizational) units where healthcare delivery is practiced (offices, wards, hospitals, clinics, etc.).';



COMMENT ON COLUMN cdm.care_site.care_site_id IS 'A unique identifier for each Care Site.';



COMMENT ON COLUMN cdm.care_site.location_id IS 'A foreign key to the geographic Location in the LOCATION table, where the detailed address information is stored.';



COMMENT ON COLUMN cdm.care_site.place_of_service_concept_id IS 'A foreign key that refers to a Place of Service Concept ID in the Standardized Vocabularies.';



COMMENT ON COLUMN cdm.care_site.care_site_name IS 'The verbatim description or name of the Care Site as in data source';



COMMENT ON COLUMN cdm.care_site.care_site_source_value IS 'The identifier for the Care Site in the source data, stored here for reference.';



COMMENT ON COLUMN cdm.care_site.place_of_service_source_value IS 'The source code for the Place of Service as it appears in the source data, stored here for reference.';


CREATE TABLE cdm.cdm_source (
    cdm_version_concept_id integer,
    source_release_date date NOT NULL,
    cdm_release_date date,
    cdm_source_name text NOT NULL,
    cdm_source_abbreviation text NOT NULL,
    cdm_holder text NOT NULL,
    source_description text,
    source_documentation_reference text,
    cdm_etl_reference text,
    cdm_version text,
    vocabulary_version text,
    CONSTRAINT chk_cdm_source_cdm_etl_reference CHECK ((COALESCE(length(cdm_etl_reference), 0) <= 255)),
    CONSTRAINT chk_cdm_source_cdm_holder CHECK ((length(cdm_holder) <= 255)),
    CONSTRAINT chk_cdm_source_cdm_source_abbreviation CHECK ((length(cdm_source_abbreviation) <= 25)),
    CONSTRAINT chk_cdm_source_cdm_source_name CHECK ((length(cdm_source_name) <= 255)),
    CONSTRAINT chk_cdm_source_cdm_version CHECK ((COALESCE(length(cdm_version), 0) <= 10)),
    CONSTRAINT chk_cdm_source_source_documentation_reference CHECK ((COALESCE(length(source_documentation_reference), 0) <= 255)),
    CONSTRAINT chk_cdm_source_vocabulary_version CHECK ((COALESCE(length(vocabulary_version), 0) <= 20))
);


ALTER TABLE cdm.cdm_source OWNER TO postgres;


COMMENT ON TABLE cdm.cdm_source IS 'The CDM_SOURCE table contains detail about the source database and the process used to transform the data into the OMOP Common Data Model.';



COMMENT ON COLUMN cdm.cdm_source.source_release_date IS 'The date for which the source data are most current, such as the last day of data capture';



COMMENT ON COLUMN cdm.cdm_source.cdm_release_date IS 'The date when the CDM was instantiated';



COMMENT ON COLUMN cdm.cdm_source.cdm_source_name IS 'The full name of the source';



COMMENT ON COLUMN cdm.cdm_source.cdm_source_abbreviation IS 'An abbreviation of the name';



COMMENT ON COLUMN cdm.cdm_source.cdm_holder IS 'The name of the organization responsible for the development of the CDM instance';



COMMENT ON COLUMN cdm.cdm_source.source_description IS 'A description of the source data origin and purpose for collection. The description may contain a summary of the period of time that is expected to be covered by this dataset.';



COMMENT ON COLUMN cdm.cdm_source.source_documentation_reference IS 'URL or other external reference to location of source documentation';



COMMENT ON COLUMN cdm.cdm_source.cdm_etl_reference IS 'URL or other external reference to location of ETL specification documentation and ETL source code';



COMMENT ON COLUMN cdm.cdm_source.cdm_version IS 'The version of CDM used';



COMMENT ON COLUMN cdm.cdm_source.vocabulary_version IS 'The version of the vocabulary used';



CREATE TABLE cdm.cohort (
    cohort_definition_id bigint NOT NULL,
    subject_id bigint NOT NULL,
    cohort_start_date date NOT NULL,
    cohort_end_date date NOT NULL
);


ALTER TABLE cdm.cohort OWNER TO postgres;


COMMENT ON TABLE cdm.cohort IS 'The COHORT table contains records of subjects that satisfy a given set of criteria for a duration of time. The definition of the cohort is contained within the COHORT_DEFINITION table. Cohorts can be constructed of patients (Persons), Providers or Visits.';



COMMENT ON COLUMN cdm.cohort.cohort_definition_id IS 'A foreign key to a record in the COHORT_DEFINITION table containing relevant Cohort Definition information.';



COMMENT ON COLUMN cdm.cohort.subject_id IS 'A foreign key to the subject in the cohort. These could be referring to records in the PERSON, PROVIDER, VISIT_OCCURRENCE table.';



COMMENT ON COLUMN cdm.cohort.cohort_start_date IS 'The date when the Cohort Definition criteria for the Person, Provider or Visit first match.';



COMMENT ON COLUMN cdm.cohort.cohort_end_date IS 'The date when the Cohort Definition criteria for the Person, Provider or Visit no longer match or the Cohort membership was terminated.';



CREATE TABLE cdm.cohort_definition (
    cohort_definition_id integer NOT NULL,
    definition_type_concept_id integer NOT NULL,
    subject_concept_id integer NOT NULL,
    cohort_initiation_date date,
    cohort_definition_name text NOT NULL,
    cohort_definition_description text,
    cohort_definition_syntax text,
    CONSTRAINT chk_cohort_definition_cohort_definition_name CHECK ((length(cohort_definition_name) <= 255))
);


ALTER TABLE cdm.cohort_definition OWNER TO postgres;


COMMENT ON TABLE cdm.cohort_definition IS 'The COHORT_DEFINITION table contains records defining a Cohort derived from the data through the associated description and syntax and upon instantiation (execution of the algorithm) placed into the COHORT table.';



COMMENT ON COLUMN cdm.cohort_definition.cohort_definition_id IS 'This is the identifier given to the cohort, usually by the ATLAS application.';



COMMENT ON COLUMN cdm.cohort_definition.definition_type_concept_id IS 'Type defining what kind of Cohort Definition the record represents and how the syntax may be executed.';



COMMENT ON COLUMN cdm.cohort_definition.subject_concept_id IS 'This field contains a Concept that represents the domain of the subjects that are members of the cohort (e.g., Person, Provider, Visit).';



COMMENT ON COLUMN cdm.cohort_definition.cohort_initiation_date IS 'A date to indicate when the Cohort was initiated in the COHORT table.';



COMMENT ON COLUMN cdm.cohort_definition.cohort_definition_name IS 'A short description of the cohort.';



COMMENT ON COLUMN cdm.cohort_definition.cohort_definition_description IS 'A complete description of the cohort.';



COMMENT ON COLUMN cdm.cohort_definition.cohort_definition_syntax IS 'Syntax or code to operationalize the Cohort Definition.';



CREATE TABLE cdm.condition_era (
    condition_era_id bigint NOT NULL,
    person_id bigint NOT NULL,
    condition_concept_id integer NOT NULL,
    condition_occurrence_count integer,
    condition_era_start_date date,
    condition_era_end_date date
);


ALTER TABLE cdm.condition_era OWNER TO postgres;


COMMENT ON TABLE cdm.condition_era IS 'A Condition Era is defined as a span of time when the Person is assumed to have a given condition. Similar to Drug Eras, Condition Eras are chronological periods of Condition Occurrence. Combining individual Condition Occurrences into a single Condition Era serves two purposes:  * It allows aggregation of chronic conditions that require frequent ongoing care, instead of treating each Condition Occurrence as an independent event. * It allows aggregation of multiple, closely timed doctor visits for the same Condition to avoid double-counting the Condition Occurrences.  For example, consider a Person who visits her Primary Care Physician (PCP) and who is referred to a specialist. At a later time, the Person visits the specialist, who confirms the PCP''s original diagnosis and provides the appropriate treatment to resolve the condition. These two independent doctor visits should be aggregated into one Condition Era.';



COMMENT ON COLUMN cdm.condition_era.condition_era_id IS 'A unique identifier for each Condition Era.';



COMMENT ON COLUMN cdm.condition_era.person_id IS 'A foreign key identifier to the Person who is experiencing the Condition during the Condition Era. The demographic details of that Person are stored in the PERSON table.';



COMMENT ON COLUMN cdm.condition_era.condition_concept_id IS 'A foreign key that refers to a standard Condition Concept identifier in the Standardized Vocabularies.';



COMMENT ON COLUMN cdm.condition_era.condition_occurrence_count IS 'The number of individual Condition Occurrences used to construct the condition era.';



COMMENT ON COLUMN cdm.condition_era.condition_era_start_date IS 'The start date for the Condition Era constructed from the individual instances of Condition Occurrences.';



COMMENT ON COLUMN cdm.condition_era.condition_era_end_date IS 'The end date for the Condition Era constructed from the individual instances of Condition Occurrences.';



CREATE TABLE cdm.condition_occurrence (
    condition_occurrence_id bigint NOT NULL,
    person_id bigint,
    provider_id bigint,
    visit_occurrence_id bigint,
    visit_detail_id bigint,
    condition_start_datetime timestamp without time zone,
    condition_end_datetime timestamp without time zone,
    condition_concept_id integer,
    condition_type_concept_id integer,
    condition_status_concept_id integer,
    condition_source_concept_id integer,
    condition_start_date date,
    condition_end_date date,
    stop_reason text,
    condition_source_value text,
    condition_status_source_value text,
    CONSTRAINT chk_condition_occurrence_stop_reason CHECK ((COALESCE(length(stop_reason), 0) <= 20))
);


ALTER TABLE cdm.condition_occurrence OWNER TO postgres;


COMMENT ON TABLE cdm.condition_occurrence IS 'Conditions are records of a Person suggesting the presence of a disease or medical condition stated as a diagnosis, a sign, or a symptom, which is either observed by a Provider or reported by the patient. Conditions are recorded in different sources and levels of standardization, for example:  * Medical claims data include diagnoses coded in Source Vocabularies such as ICD-9-CM that are submitted as part of a reimbursement claim for health services * EHRs may capture Person conditions in the form of diagnosis codes or symptoms';



COMMENT ON COLUMN cdm.condition_occurrence.condition_occurrence_id IS 'A unique identifier for each Condition Occurrence event.';



COMMENT ON COLUMN cdm.condition_occurrence.person_id IS 'A foreign key identifier to the Person who is experiencing the condition. The demographic details of that Person are stored in the PERSON table.';



COMMENT ON COLUMN cdm.condition_occurrence.provider_id IS 'A foreign key to the Provider in the PROVIDER table who was responsible for capturing (diagnosing) the Condition.';



COMMENT ON COLUMN cdm.condition_occurrence.visit_occurrence_id IS 'A foreign key to the visit in the VISIT_OCCURRENCE table during which the Condition was determined (diagnosed).';



COMMENT ON COLUMN cdm.condition_occurrence.visit_detail_id IS 'A foreign key to the visit in the VISIT_DETAIL table during which the Condition was determined (diagnosed).';



COMMENT ON COLUMN cdm.condition_occurrence.condition_start_datetime IS 'The date and time when the instance of the Condition is recorded.';



COMMENT ON COLUMN cdm.condition_occurrence.condition_end_datetime IS 'The date when the instance of the Condition is considered to have ended.';



COMMENT ON COLUMN cdm.condition_occurrence.condition_concept_id IS 'A foreign key that refers to a Standard Concept identifier in the Standardized Vocabularies belonging to the ''Condition'' domain.';



COMMENT ON COLUMN cdm.condition_occurrence.condition_type_concept_id IS 'A foreign key to the predefined Concept identifier in the Standardized Vocabularies reflecting the source data from which the Condition was recorded, the level of standardization, and the type of occurrence. These belong to the ''Condition Type'' vocabulary';



COMMENT ON COLUMN cdm.condition_occurrence.condition_status_concept_id IS 'A foreign key that refers to a Standard Concept identifier in the Standardized Vocabularies reflecting the point of care at which the Condition was diagnosed.';



COMMENT ON COLUMN cdm.condition_occurrence.condition_source_concept_id IS 'A foreign key to a Condition Concept that refers to the code used in the source.';



COMMENT ON COLUMN cdm.condition_occurrence.condition_start_date IS 'The date when the instance of the Condition is recorded.';



COMMENT ON COLUMN cdm.condition_occurrence.condition_end_date IS 'The date when the instance of the Condition is considered to have ended.';



COMMENT ON COLUMN cdm.condition_occurrence.stop_reason IS 'The reason that the Condition was no longer present, as indicated in the source data.';



COMMENT ON COLUMN cdm.condition_occurrence.condition_source_value IS 'The source code for the Condition as it appears in the source data. This code is mapped to a Standard Condition Concept in the Standardized Vocabularies and the original code is stored here for reference.';



COMMENT ON COLUMN cdm.condition_occurrence.condition_status_source_value IS 'The source code for the condition status as it appears in the source data.  This code is mapped to a Standard Concept in the Standardized Vocabularies and the original code is stored here for reference.';



CREATE TABLE cdm.cost (
    cost_id bigint NOT NULL,
    cost_event_id bigint NOT NULL,
    cost_domain_id text NOT NULL,
    payer_plan_period_id bigint,
    cost_type_concept_id integer NOT NULL,
    currency_concept_id integer,
    revenue_code_concept_id integer,
    drg_concept_id integer,
    total_charge double precision,
    total_cost double precision,
    total_paid double precision,
    paid_by_payer double precision,
    paid_by_patient double precision,
    paid_patient_copay double precision,
    paid_patient_coinsurance double precision,
    paid_patient_deductible double precision,
    paid_by_primary double precision,
    paid_ingredient_cost double precision,
    paid_dispensing_fee double precision,
    amount_allowed double precision,
    revenue_code_source_value text,
    drg_source_value text
);


ALTER TABLE cdm.cost OWNER TO postgres;


CREATE TABLE cdm.death (
    person_id bigint NOT NULL,
    death_datetime timestamp without time zone,
    death_date date NOT NULL,
    death_type_concept_id integer NOT NULL,
    cause_concept_id integer,
    cause_source_concept_id integer,
    cause_source_value text,
    CONSTRAINT chk_death_cause_source_value CHECK ((COALESCE(length(cause_source_value), 0) <= 256))
);


ALTER TABLE cdm.death OWNER TO postgres;


COMMENT ON TABLE cdm.death IS 'The death domain contains the clinical event for how and when a Person dies (OMOP CDM v5).';



COMMENT ON COLUMN cdm.death.person_id IS 'A foreign key identifier to the deceased person. The demographic details of that person are stored in the person table.';



COMMENT ON COLUMN cdm.death.death_datetime IS 'The date and time the person was deceased.';



COMMENT ON COLUMN cdm.death.death_date IS 'The date the person was deceased.';



COMMENT ON COLUMN cdm.death.death_type_concept_id IS 'A foreign key referring to the predefined concept identifier in the Standardized Vocabularies reflecting how the death was represented in the source data.';



COMMENT ON COLUMN cdm.death.cause_concept_id IS 'A foreign key referring to a standard concept identifier in the Standardized Vocabularies for conditions.';



COMMENT ON COLUMN cdm.death.cause_source_concept_id IS 'A foreign key to the concept that refers to the code used in the source.';



CREATE TABLE cdm.device_exposure (
    device_exposure_id bigint NOT NULL,
    person_id bigint NOT NULL,
    provider_id bigint,
    visit_occurrence_id bigint,
    visit_detail_id bigint,
    device_exposure_start_datetime timestamp without time zone NOT NULL,
    device_exposure_end_datetime timestamp without time zone,
    device_concept_id integer NOT NULL,
    device_type_concept_id integer NOT NULL,
    quantity integer,
    device_source_concept_id integer NOT NULL,
    unit_concept_id integer,
    unit_source_concept_id integer,
    device_exposure_start_date date,
    device_exposure_end_date date,
    unique_device_id text,
    device_source_value text,
    production_id text,
    unit_source_value text
);


ALTER TABLE cdm.device_exposure OWNER TO postgres;


COMMENT ON TABLE cdm.device_exposure IS 'The ''Device'' domain captures information about a person''s exposure to a foreign physical object or instrument which is used for diagnostic or therapeutic purposes through a mechanism beyond chemical action. Devices include implantable objects (e.g. pacemakers, stents, artificial joints), medical equipment and supplies (e.g. bandages, crutches, syringes), other instruments used in medical procedures (e.g. sutures, defibrillators) and material used in clinical care (e.g. adhesives, body material, dental material, surgical material).';



COMMENT ON COLUMN cdm.device_exposure.device_exposure_id IS 'A system-generated unique identifier for each Device Exposure.';



COMMENT ON COLUMN cdm.device_exposure.person_id IS 'A foreign key identifier to the Person who is subjected to the Device. The demographic details of that Person are stored in the PERSON table.';



COMMENT ON COLUMN cdm.device_exposure.provider_id IS 'A foreign key to the provider in the PROVIDER table who initiated or administered the Device.';



COMMENT ON COLUMN cdm.device_exposure.visit_occurrence_id IS 'A foreign key to the visit in the VISIT_OCCURRENCE table during which the Device was used.';



COMMENT ON COLUMN cdm.device_exposure.visit_detail_id IS 'A foreign key to the visit detail record in the VISIT_DETAIL table during which the Device was used.';



COMMENT ON COLUMN cdm.device_exposure.device_exposure_start_datetime IS 'The date and time the Device or supply was applied or used.';



COMMENT ON COLUMN cdm.device_exposure.device_exposure_end_datetime IS 'The date and time use of the Device or supply was ceased.';



COMMENT ON COLUMN cdm.device_exposure.device_concept_id IS 'A foreign key that refers to a Standard Concept identifier in the Standardized Vocabularies belonging to the ''Device'' domain.';



COMMENT ON COLUMN cdm.device_exposure.device_type_concept_id IS 'A foreign key to the predefined Concept identifier in the Standardized Vocabularies reflecting the type of Device Exposure recorded. It indicates how the Device Exposure was represented in the source data and belongs to the ''Device Type'' domain.';



COMMENT ON COLUMN cdm.device_exposure.quantity IS 'The number of individual Devices used in the exposure.';



COMMENT ON COLUMN cdm.device_exposure.device_source_concept_id IS 'A foreign key to a Device Concept that refers to the code used in the source.';



COMMENT ON COLUMN cdm.device_exposure.device_exposure_start_date IS 'The date the Device or supply was applied or used.';



COMMENT ON COLUMN cdm.device_exposure.device_exposure_end_date IS 'The date use of the Device or supply was ceased.';



COMMENT ON COLUMN cdm.device_exposure.unique_device_id IS 'A UDI or equivalent identifying the instance of the Device used in the Person.';



COMMENT ON COLUMN cdm.device_exposure.device_source_value IS 'The source code for the Device as it appears in the source data. This code is mapped to a Standard Device Concept in the Standardized Vocabularies and the original code is stored here for reference.';



CREATE TABLE cdm.dose_era (
    dose_era_id bigint NOT NULL,
    person_id bigint NOT NULL,
    dose_era_start_datetime timestamp without time zone NOT NULL,
    dose_era_end_datetime timestamp without time zone NOT NULL,
    drug_concept_id integer NOT NULL,
    unit_concept_id integer NOT NULL,
    dose_value numeric NOT NULL
);


ALTER TABLE cdm.dose_era OWNER TO postgres;


COMMENT ON TABLE cdm.dose_era IS 'A Dose Era is defined as a span of time when the Person is assumed to be exposed to a constant dose of a specific active ingredient.';



COMMENT ON COLUMN cdm.dose_era.dose_era_id IS 'A unique identifier for each Dose Era.';



COMMENT ON COLUMN cdm.dose_era.person_id IS 'A foreign key identifier to the Person who is subjected to the drug during the drug era. The demographic details of that Person are stored in the PERSON table.';



COMMENT ON COLUMN cdm.dose_era.dose_era_start_datetime IS 'The start date for the drug era constructed from the individual instances of drug exposures. It is the start date of the very first chronologically recorded instance of utilization of a drug.';



COMMENT ON COLUMN cdm.dose_era.dose_era_end_datetime IS 'The end date for the drug era constructed from the individual instance of drug exposures. It is the end date of the final continuously recorded instance of utilization of a drug.';



COMMENT ON COLUMN cdm.dose_era.drug_concept_id IS 'A foreign key that refers to a Standard Concept identifier in the Standardized Vocabularies for the active Ingredient Concept.';



COMMENT ON COLUMN cdm.dose_era.unit_concept_id IS 'A foreign key that refers to a Standard Concept identifier in the Standardized Vocabularies for the unit concept.';



COMMENT ON COLUMN cdm.dose_era.dose_value IS 'The numeric value of the dose.';



CREATE TABLE cdm.drug_era (
    drug_era_id bigint NOT NULL,
    person_id bigint NOT NULL,
    drug_concept_id integer NOT NULL,
    drug_exposure_count integer,
    gap_days integer,
    drug_era_start_date date,
    drug_era_end_date date
);


ALTER TABLE cdm.drug_era OWNER TO postgres;


COMMENT ON TABLE cdm.drug_era IS 'A Drug Era is defined as a span of time when the Person is assumed to be exposed to a particular active ingredient. A Drug Era is not the same as a Drug Exposure: Exposures are individual records corresponding to the source when Drug was delivered to the Person, while successive periods of Drug Exposures are combined under certain rules to produce continuous Drug Eras.';



COMMENT ON COLUMN cdm.drug_era.drug_era_id IS 'A unique identifier for each Drug Era.';



COMMENT ON COLUMN cdm.drug_era.person_id IS 'A foreign key identifier to the Person who is subjected to the Drug during the fDrug Era. The demographic details of that Person are stored in the PERSON table.';



COMMENT ON COLUMN cdm.drug_era.drug_concept_id IS 'A foreign key that refers to a Standard Concept identifier in the Standardized Vocabularies for the Ingredient Concept.';



COMMENT ON COLUMN cdm.drug_era.drug_exposure_count IS 'The number of individual Drug Exposure occurrences used to construct the Drug Era.';



COMMENT ON COLUMN cdm.drug_era.gap_days IS 'The number of days that are not covered by DRUG_EXPOSURE records that were used to make up the era record.';



COMMENT ON COLUMN cdm.drug_era.drug_era_start_date IS 'The start date for the Drug Era constructed from the individual instances of Drug Exposures.';



COMMENT ON COLUMN cdm.drug_era.drug_era_end_date IS 'The end date for the drug era constructed from the individual instance of drug exposures.';



CREATE TABLE cdm.drug_exposure (
    drug_exposure_id bigint NOT NULL,
    person_id bigint NOT NULL,
    provider_id bigint,
    visit_occurrence_id bigint,
    visit_detail_id bigint,
    drug_exposure_start_datetime timestamp without time zone,
    drug_exposure_end_datetime timestamp without time zone,
    drug_concept_id integer NOT NULL,
    drug_type_concept_id integer NOT NULL,
    drug_source_concept_id integer NOT NULL,
    route_concept_id integer NOT NULL,
    refills integer,
    days_supply integer,
    drug_exposure_start_date date,
    drug_exposure_end_date date,
    verbatim_end_date date,
    quantity numeric,
    sig text,
    lot_number text,
    drug_source_value text,
    route_source_value text,
    dose_unit_source_value text,
    stop_reason text,
    CONSTRAINT chk_drug_exposure_lot_number CHECK ((COALESCE(length(lot_number), 0) <= 50)),
    CONSTRAINT chk_drug_exposure_stop_reason CHECK ((COALESCE(length(stop_reason), 0) <= 256))
);


ALTER TABLE cdm.drug_exposure OWNER TO postgres;


COMMENT ON TABLE cdm.drug_exposure IS 'The ''Drug'' domain captures records about the utilization of a Drug when ingested or otherwise introduced into the body. A Drug is a biochemical substance formulated in such a way that when administered to a Person it will exert a certain physiological effect. Drugs include prescription and over-the-counter medicines, vaccines, and large-molecule biologic therapies. Radiological devices ingested or applied locally do not count as Drugs.  Drug Exposure is inferred from clinical events associated with orders, prescriptions written, pharmacy dispensings, procedural administrations, and other patient-reported information, for example:  * The ''Prescription'' section of an EHR captures prescriptions written by physicians or from electronic ordering systems * The ''Medication list'' section of an EHR for both non-prescription products and medications prescribed by other providers * Prescriptions filled at dispensing providers such as pharmacies, and then captured in reimbursement claim systems * Drugs administered as part of a Procedure, such as chemotherapy or vaccines.';



COMMENT ON COLUMN cdm.drug_exposure.drug_exposure_id IS 'A system-generated unique identifier for each Drug utilization event.';



COMMENT ON COLUMN cdm.drug_exposure.person_id IS 'A foreign key identifier to the Person who is subjected to the Drug. The demographic details of that Person are stored in the PERSON table.';



COMMENT ON COLUMN cdm.drug_exposure.provider_id IS 'A foreign key to the provider in the PROVIDER table who initiated (prescribed or administered) the Drug Exposure.';



COMMENT ON COLUMN cdm.drug_exposure.visit_occurrence_id IS 'A foreign key to the Visit in the VISIT_OCCURRENCE table during which the Drug Exposure was initiated.';



COMMENT ON COLUMN cdm.drug_exposure.visit_detail_id IS 'A foreign key to the Visit Detail in the VISIT_DETAIL table during which the Drug Exposure was initiated.';



COMMENT ON COLUMN cdm.drug_exposure.drug_exposure_start_datetime IS 'The start date and time for the current instance of Drug utilization. Valid entries include a start datetime of a prescription, the date and time a prescription was filled, or the date and time on which a Drug administration procedure was recorded.';



COMMENT ON COLUMN cdm.drug_exposure.drug_exposure_end_datetime IS 'The end date and time for the current instance of Drug utilization. Depending on different sources, it could be a known or an inferred date and time and denotes the last day at which the patient was still exposed to Drug.';



COMMENT ON COLUMN cdm.drug_exposure.drug_concept_id IS 'A foreign key that refers to a Standard Concept identifier in the Standardized Vocabularies belonging to the ''Drug'' domain.';



COMMENT ON COLUMN cdm.drug_exposure.drug_type_concept_id IS 'A foreign key to the predefined Concept identifier in the Standardized Vocabularies reflecting the type of Drug Exposure recorded. It indicates how the Drug Exposure was represented in the source data and belongs to the ''Drug Type'' vocabulary.';



COMMENT ON COLUMN cdm.drug_exposure.drug_source_concept_id IS 'A foreign key to a Drug Concept that refers to the code used in the source.';



COMMENT ON COLUMN cdm.drug_exposure.route_concept_id IS 'A foreign key that refers to a Standard Concept identifier in the Standardized Vocabularies reflecting the route of administration and belonging to the ''Route'' domain.';



COMMENT ON COLUMN cdm.drug_exposure.refills IS 'The number of refills after the initial prescription. The initial prescription is not counted, values start with null.';



COMMENT ON COLUMN cdm.drug_exposure.days_supply IS 'The number of days of supply of the medication as prescribed. This reflects the intention of the provider for the length of exposure.';



COMMENT ON COLUMN cdm.drug_exposure.drug_exposure_start_date IS 'The start date for the current instance of Drug utilization. Valid entries include a start date of a prescription, the date a prescription was filled, or the date on which a Drug administration procedure was recorded.';



COMMENT ON COLUMN cdm.drug_exposure.drug_exposure_end_date IS 'The end date for the current instance of Drug utilization. Depending on different sources, it could be a known or an inferred date and denotes the last day at which the patient was still exposed to Drug.';



COMMENT ON COLUMN cdm.drug_exposure.verbatim_end_date IS 'The known end date of a drug_exposure as provided by the source.';



COMMENT ON COLUMN cdm.drug_exposure.quantity IS 'The quantity of drug as recorded in the original prescription or dispensing record.';



COMMENT ON COLUMN cdm.drug_exposure.sig IS 'The directions (''signetur'') on the Drug prescription as recorded in the original prescription (and printed on the container) or dispensing record.';



COMMENT ON COLUMN cdm.drug_exposure.lot_number IS 'An identifier assigned to a particular quantity or lot of Drug product from the manufacturer.';



COMMENT ON COLUMN cdm.drug_exposure.drug_source_value IS 'The source code for the Drug as it appears in the source data. This code is mapped to a Standard Drug concept in the Standardized Vocabularies and the original code is, stored here for reference.';



COMMENT ON COLUMN cdm.drug_exposure.route_source_value IS 'The information about the route of administration as detailed in the source.';



COMMENT ON COLUMN cdm.drug_exposure.dose_unit_source_value IS 'The information about the dose unit as detailed in the source.';



CREATE TABLE cdm.episode (
    episode_id bigint NOT NULL,
    person_id bigint NOT NULL,
    episode_parent_id bigint,
    episode_start_datetime timestamp without time zone,
    episode_end_datetime timestamp without time zone,
    episode_start_date date NOT NULL,
    episode_end_date date,
    episode_concept_id integer NOT NULL,
    episode_number integer,
    episode_object_concept_id integer NOT NULL,
    episode_type_concept_id integer NOT NULL,
    episode_source_concept_id integer,
    episode_source_value text,
    CONSTRAINT chk_episode_episode_source_value CHECK ((COALESCE(length(episode_source_value), 0) <= 50))
);


ALTER TABLE cdm.episode OWNER TO postgres;


CREATE TABLE cdm.episode_event (
    episode_id bigint NOT NULL,
    event_id bigint NOT NULL,
    episode_event_field_concept_id integer NOT NULL
);


ALTER TABLE cdm.episode_event OWNER TO postgres;


CREATE TABLE cdm.fact_relationship (
    fact_id_1 bigint NOT NULL,
    fact_id_2 bigint NOT NULL,
    domain_concept_id_1 integer NOT NULL,
    domain_concept_id_2 integer NOT NULL,
    relationship_concept_id integer NOT NULL
);


ALTER TABLE cdm.fact_relationship OWNER TO postgres;


COMMENT ON TABLE cdm.fact_relationship IS 'The FACT_RELATIONSHIP table contains records about the relationships between facts stored as records in any table of the CDM. Relationships can be defined between facts from the same domain, or different domains. Examples of Fact Relationships include: Person relationships (parent-child), care site relationships (hierarchical organizational structure of facilities within a health system), indication relationship (between drug exposures and associated conditions), usage relationships (of devices during the course of an associated procedure), or facts derived from one another (measurements derived from an associated specimen).';



COMMENT ON COLUMN cdm.fact_relationship.fact_id_1 IS 'The unique identifier in the table corresponding to the domain of fact one.';



COMMENT ON COLUMN cdm.fact_relationship.fact_id_2 IS 'The unique identifier in the table corresponding to the domain of fact two.';



COMMENT ON COLUMN cdm.fact_relationship.domain_concept_id_1 IS 'The concept representing the domain of fact one, from which the corresponding table can be inferred.';



COMMENT ON COLUMN cdm.fact_relationship.domain_concept_id_2 IS 'The concept representing the domain of fact two, from which the corresponding table can be inferred.';



COMMENT ON COLUMN cdm.fact_relationship.relationship_concept_id IS 'A foreign key to a Standard Concept ID of relationship in the Standardized Vocabularies.';



CREATE TABLE cdm.location (
    location_id bigint NOT NULL,
    country_concept_id integer,
    latitude numeric,
    longitude numeric,
    address_1 character varying(50),
    address_2 character varying(50),
    city character varying(50),
    state character varying(2),
    zip character varying(9),
    county character varying(20),
    location_source_value text,
    country_source_value character varying(100)
);


ALTER TABLE cdm.location OWNER TO postgres;


COMMENT ON TABLE cdm.location IS 'The LOCATION table represents a generic way to capture physical location or address information of Persons and Care Sites.';



COMMENT ON COLUMN cdm.location.location_id IS 'A unique identifier for each geographic location.';



COMMENT ON COLUMN cdm.location.latitude IS 'The geocoded latitude';



COMMENT ON COLUMN cdm.location.longitude IS 'The geocoded longitude';



COMMENT ON COLUMN cdm.location.address_1 IS 'The address field 1, typically used for the street address, as it appears in the source data.';



COMMENT ON COLUMN cdm.location.address_2 IS 'The address field 2, typically used for additional detail such as buildings, suites, floors, as it appears in the source data.';



COMMENT ON COLUMN cdm.location.city IS 'The city field as it appears in the source data.';



COMMENT ON COLUMN cdm.location.state IS 'The state field as it appears in the source data.';



COMMENT ON COLUMN cdm.location.zip IS 'The zip or postal code.';



COMMENT ON COLUMN cdm.location.county IS 'The county.';



COMMENT ON COLUMN cdm.location.location_source_value IS 'The verbatim information that is used to uniquely identify the location as it appears in the source data.';



COMMENT ON COLUMN cdm.location.country_source_value IS 'The country';



CREATE TABLE cdm.location_history (
    location_history_id bigint NOT NULL,
    location_id bigint NOT NULL,
    entity_id bigint NOT NULL,
    relationship_type_concept_id integer NOT NULL,
    start_date date NOT NULL,
    end_date date,
    domain_id text NOT NULL,
    CONSTRAINT chk_location_history_domain_id CHECK ((length(domain_id) <= 50))
);


ALTER TABLE cdm.location_history OWNER TO postgres;


COMMENT ON TABLE cdm.location_history IS 'The LOCATION HISTORY table stores relationships between Persons or Care Sites and geographic locations over time.';



COMMENT ON COLUMN cdm.location_history.location_history_id IS 'A unique identifier for each location history record (PK).';



COMMENT ON COLUMN cdm.location_history.location_id IS 'A foreign key to the location table.';



COMMENT ON COLUMN cdm.location_history.entity_id IS 'The unique identifier for the entity. References either person_id, provider_id, or care_site_id, depending on domain_id.';



COMMENT ON COLUMN cdm.location_history.relationship_type_concept_id IS 'The type of relationship between location and entity.';



COMMENT ON COLUMN cdm.location_history.start_date IS 'The date the relationship started.';



COMMENT ON COLUMN cdm.location_history.end_date IS 'The date the relationship ended.';



COMMENT ON COLUMN cdm.location_history.domain_id IS 'The domain of the entity that is related to the location. Either PERSON, PROVIDER, or CARE_SITE.';



CREATE TABLE cdm.measurement (
    measurement_id bigint NOT NULL,
    person_id bigint NOT NULL,
    provider_id bigint,
    visit_occurrence_id bigint,
    visit_detail_id bigint,
    measurement_event_id bigint,
    measurement_datetime timestamp without time zone NOT NULL,
    measurement_concept_id integer NOT NULL,
    measurement_type_concept_id integer NOT NULL,
    measurement_source_concept_id integer NOT NULL,
    measurement_date date,
    operator_concept_id integer,
    value_as_concept_id integer,
    unit_concept_id integer,
    unit_source_concept_id integer,
    meas_event_field_concept_id integer,
    value_as_number numeric,
    range_low numeric,
    range_high numeric,
    measurement_time text,
    measurement_source_value text,
    unit_source_value text,
    value_source_value text,
    CONSTRAINT chk_measurement_measurement_time CHECK ((COALESCE(length(measurement_time), 0) <= 10))
);


ALTER TABLE cdm.measurement OWNER TO postgres;


COMMENT ON TABLE cdm.measurement IS 'The MEASUREMENT table contains records of Measurement, i.e. structured values (numerical or categorical) obtained through systematic and standardized examination or testing of a Person or Person''s sample. The MEASUREMENT table contains both orders and results of such Measurements as laboratory tests, vital signs, quantitative findings from pathology reports, etc.';



COMMENT ON COLUMN cdm.measurement.measurement_id IS 'A unique identifier for each Measurement.';



COMMENT ON COLUMN cdm.measurement.person_id IS 'A foreign key identifier to the Person about whom the measurement was recorded. The demographic details of that Person are stored in the PERSON table.';



COMMENT ON COLUMN cdm.measurement.provider_id IS 'A foreign key to the provider in the PROVIDER table who was responsible for initiating or obtaining the measurement.';



COMMENT ON COLUMN cdm.measurement.visit_occurrence_id IS 'A foreign key to the Visit in the VISIT_OCCURRENCE table during which the Measurement was recorded.';



COMMENT ON COLUMN cdm.measurement.visit_detail_id IS 'A foreign key to the Visit Detail in the VISIT_DETAIL table during which the Measurement was recorded.';



COMMENT ON COLUMN cdm.measurement.measurement_datetime IS 'The date and time of the Measurement. Some database systems don''t have a datatype of time. To accommodate all temporal analyses, datatype datetime can be used (combining measurement_date and measurement_time [forum discussion](http://forums.ohdsi.org/t/date-time-and-datetime-problem-and-the-world-of-hours-and-1day/314))';



COMMENT ON COLUMN cdm.measurement.measurement_concept_id IS 'A foreign key to the standard measurement concept identifier in the Standardized Vocabularies. These belong to the ''Measurement'' domain, but could overlap with the ''Observation'' domain (see #3 below).';



COMMENT ON COLUMN cdm.measurement.measurement_type_concept_id IS 'A foreign key to the predefined Concept in the Standardized Vocabularies reflecting the provenance from where the Measurement record was recorded. These belong to the ''Meas Type'' vocabulary';



COMMENT ON COLUMN cdm.measurement.measurement_source_concept_id IS 'A foreign key to a Concept in the Standard Vocabularies that refers to the code used in the source.';



COMMENT ON COLUMN cdm.measurement.measurement_date IS 'The date of the Measurement.';



COMMENT ON COLUMN cdm.measurement.operator_concept_id IS 'A foreign key identifier to the predefined Concept in the Standardized Vocabularies reflecting the mathematical operator that is applied to the value_as_number. Operators are <, <=, =, >=, > and these concepts belong to the ''Meas Value Operator'' domain.';



COMMENT ON COLUMN cdm.measurement.value_as_concept_id IS 'A foreign key to a Measurement result represented as a Concept from the Standardized Vocabularies (e.g., positive/negative, present/absent, low/high, etc.). These belong to the ''Meas Value'' domain';



COMMENT ON COLUMN cdm.measurement.unit_concept_id IS 'A foreign key to a Standard Concept ID of Measurement Units in the Standardized Vocabularies that belong to the ''Unit'' domain.';



COMMENT ON COLUMN cdm.measurement.value_as_number IS 'A Measurement result where the result is expressed as a numeric value.';



COMMENT ON COLUMN cdm.measurement.range_low IS 'The lower limit of the normal range of the Measurement result. The lower range is assumed to be of the same unit of measure as the Measurement value.';



COMMENT ON COLUMN cdm.measurement.range_high IS 'The upper limit of the normal range of the Measurement. The upper range is assumed to be of the same unit of measure as the Measurement value.';



COMMENT ON COLUMN cdm.measurement.measurement_time IS 'The time of the Measurement. This is present for backwards compatibility and will be deprecated in an upcoming version';



COMMENT ON COLUMN cdm.measurement.measurement_source_value IS 'The Measurement name as it appears in the source data. This code is mapped to a Standard Concept in the Standardized Vocabularies and the original code is stored here for reference.';



COMMENT ON COLUMN cdm.measurement.unit_source_value IS 'The source code for the unit as it appears in the source data. This code is mapped to a standard unit concept in the Standardized Vocabularies and the original code is stored here for reference.';



COMMENT ON COLUMN cdm.measurement.value_source_value IS 'The source value associated with the content of the value_as_number or value_as_concept_id as stored in the source data.';



CREATE TABLE cdm.metadata (
    metadata_datetime timestamp without time zone,
    metadata_concept_id integer NOT NULL,
    metadata_type_concept_id integer NOT NULL,
    value_as_concept_id integer,
    metadata_date date,
    name text NOT NULL,
    value_as_string text,
    CONSTRAINT chk_metadata_name CHECK ((length(name) <= 250))
);




COMMENT ON TABLE cdm.metadata IS 'The METADATA table contains metadata information about a dataset that has been transformed to the OMOP Common Data Model.';



COMMENT ON COLUMN cdm.metadata.metadata_datetime IS 'The date and time associated with the metadata';



COMMENT ON COLUMN cdm.metadata.metadata_concept_id IS 'A foreign key that refers to a Standard Metadata Concept identifier in the Standardized Vocabularies.';



COMMENT ON COLUMN cdm.metadata.metadata_type_concept_id IS 'A foreign key that refers to a Standard Type Concept identifier in the Standardized Vocabularies.';



COMMENT ON COLUMN cdm.metadata.value_as_concept_id IS 'A foreign key to a metadata value stored as a Concept ID.';



COMMENT ON COLUMN cdm.metadata.metadata_date IS 'The date associated with the metadata';



COMMENT ON COLUMN cdm.metadata.name IS 'The name of the Concept stored in metadata_concept_id or a description of the data being stored.';



COMMENT ON COLUMN cdm.metadata.value_as_string IS 'The metadata value stored as a string.';



CREATE TABLE cdm.note (
    note_id bigint NOT NULL,
    person_id bigint NOT NULL,
    note_event_id bigint,
    provider_id bigint,
    visit_occurrence_id bigint,
    visit_detail_id bigint,
    note_datetime timestamp without time zone NOT NULL,
    note_event_field_concept_id integer NOT NULL,
    note_type_concept_id integer NOT NULL,
    note_class_concept_id integer NOT NULL,
    encoding_concept_id integer NOT NULL,
    language_concept_id integer NOT NULL,
    note_date date,
    note_title text,
    note_text text,
    note_source_value text,
    CONSTRAINT chk_note_note_title CHECK ((COALESCE(length(note_title), 0) <= 250))
);



COMMENT ON TABLE cdm.note IS 'The NOTE table captures unstructured information that was recorded by a provider about a patient in free text notes on a given date.';



COMMENT ON COLUMN cdm.note.note_id IS 'A unique identifier for each note.';



COMMENT ON COLUMN cdm.note.person_id IS 'A foreign key identifier to the Person about whom the Note was recorded. The demographic details of that Person are stored in the PERSON table.';



COMMENT ON COLUMN cdm.note.note_event_id IS 'A foreign key identifier to the event (e.g. Measurement, Procedure, Visit, Drug Exposure, etc) record during which the note was recorded.';



COMMENT ON COLUMN cdm.note.provider_id IS 'A foreign key to the Provider in the PROVIDER table who took the Note.';



COMMENT ON COLUMN cdm.note.visit_occurrence_id IS 'A foreign key to the Visit in the VISIT_OCCURRENCE table when the Note was taken.';



COMMENT ON COLUMN cdm.note.visit_detail_id IS 'A foreign key to the Visit in the VISIT_DETAIL table when the Note was taken.';



COMMENT ON COLUMN cdm.note.note_datetime IS 'The date and time the note was recorded.';



COMMENT ON COLUMN cdm.note.note_event_field_concept_id IS 'A foreign key to the predefined Concept in the Standardized Vocabularies reflecting the field to which the note_event_id is referring.';



COMMENT ON COLUMN cdm.note.note_type_concept_id IS 'A foreign key to the predefined Concept in the Standardized Vocabularies reflecting the type, origin or provenance of the Note. These belong to the ''Note Type'' vocabulary';



COMMENT ON COLUMN cdm.note.note_class_concept_id IS 'A foreign key to the predefined Concept in the Standardized Vocabularies reflecting the HL7 LOINC Document Type Vocabulary classification of the note.';



COMMENT ON COLUMN cdm.note.encoding_concept_id IS 'A foreign key to the predefined Concept in the Standardized Vocabularies reflecting the note character encoding type';



COMMENT ON COLUMN cdm.note.language_concept_id IS 'A foreign key to the predefined Concept in the Standardized Vocabularies reflecting the language of the note';



COMMENT ON COLUMN cdm.note.note_date IS 'The date the note was recorded.';



COMMENT ON COLUMN cdm.note.note_title IS 'The title of the Note as it appears in the source.';



COMMENT ON COLUMN cdm.note.note_text IS 'The content of the Note.';



COMMENT ON COLUMN cdm.note.note_source_value IS 'The source value associated with the origin of the Note';



CREATE TABLE cdm.note_nlp (
    note_nlp_id bigint NOT NULL,
    note_id bigint NOT NULL,
    section_concept_id integer NOT NULL,
    snippet text,
    "offset" text,
    lexical_variant text NOT NULL,
    note_nlp_concept_id integer NOT NULL,
    nlp_system text,
    nlp_date date NOT NULL,
    nlp_datetime timestamp without time zone,
    term_exists text,
    term_temporal text,
    term_modifiers text,
    note_nlp_source_concept_id integer NOT NULL
);




COMMENT ON TABLE cdm.note_nlp IS 'The NOTE_NLP table will encode all output of NLP on clinical notes. Each row represents a single extracted term from a note.';



COMMENT ON COLUMN cdm.note_nlp.note_nlp_id IS 'A unique identifier for each term extracted from a note.';



COMMENT ON COLUMN cdm.note_nlp.note_id IS 'A foreign key to the Note table note the term was';



COMMENT ON COLUMN cdm.note_nlp.section_concept_id IS 'A foreign key to the predefined Concept in the Standardized Vocabularies representing the section of the extracted term.';



COMMENT ON COLUMN cdm.note_nlp.snippet IS 'A small window of text surrounding the term.';



COMMENT ON COLUMN cdm.note_nlp."offset" IS 'Character offset of the extracted term in the input note.';



COMMENT ON COLUMN cdm.note_nlp.lexical_variant IS 'Raw text extracted from the NLP tool.';



COMMENT ON COLUMN cdm.note_nlp.note_nlp_concept_id IS 'A foreign key to the predefined Concept in the Standardized Vocabularies reflecting the normalized concept for the extracted term. Domain of the term is represented as part of the Concept table.';



COMMENT ON COLUMN cdm.note_nlp.nlp_system IS 'Name and version of the NLP system that extracted the term.Useful for data provenance.';



COMMENT ON COLUMN cdm.note_nlp.nlp_date IS 'The date of the note processing.Useful for data provenance.';



COMMENT ON COLUMN cdm.note_nlp.nlp_datetime IS 'The date and time of the note processing. Useful for data provenance.';



COMMENT ON COLUMN cdm.note_nlp.term_exists IS 'A summary modifier that signifies presence or absence of the term for a given patient. Useful for quick querying.';



COMMENT ON COLUMN cdm.note_nlp.term_temporal IS 'An optional time modifier associated with the extracted term. (for now “past” or “present” only). Standardize it later.';



COMMENT ON COLUMN cdm.note_nlp.term_modifiers IS 'A compact description of all the modifiers of the specific term extracted by the NLP system. (e.g. “son has rash” ? “negated=no,subject=family, certainty=undef,conditional=false,general=false”).';



COMMENT ON COLUMN cdm.note_nlp.note_nlp_source_concept_id IS 'A foreign key to a Concept that refers to the code in the source vocabulary used by the NLP system';



CREATE TABLE cdm.observation (
    observation_id bigint NOT NULL,
    person_id bigint NOT NULL,
    observation_datetime timestamp without time zone NOT NULL,
    provider_id bigint,
    visit_occurrence_id bigint,
    visit_detail_id bigint,
    observation_event_id bigint,
    observation_date date,
    observation_concept_id integer NOT NULL,
    observation_type_concept_id integer NOT NULL,
    qualifier_concept_id integer NOT NULL,
    observation_source_concept_id integer NOT NULL,
    obs_event_field_concept_id integer,
    value_as_concept_id integer,
    unit_concept_id integer,
    value_as_number numeric,
    value_as_string text,
    observation_source_value text,
    unit_source_value text,
    qualifier_source_value text,
    value_source_value text
);




COMMENT ON TABLE cdm.observation IS 'The OBSERVATION table captures clinical facts about a Person obtained in the context of examination, questioning or a procedure. Any data that cannot be represented by any other domains, such as social and lifestyle facts, medical history, family history, etc. are recorded here.';



COMMENT ON COLUMN cdm.observation.observation_id IS 'A unique identifier for each observation.';



COMMENT ON COLUMN cdm.observation.person_id IS 'A foreign key identifier to the Person about whom the observation was recorded. The demographic details of that Person are stored in the PERSON table.';



COMMENT ON COLUMN cdm.observation.observation_datetime IS 'The date and time of the observation.';



COMMENT ON COLUMN cdm.observation.provider_id IS 'A foreign key to the provider in the PROVIDER table who was responsible for making the observation.';



COMMENT ON COLUMN cdm.observation.visit_occurrence_id IS 'A foreign key to the visit in the VISIT_OCCURRENCE table during which the observation was recorded.';



COMMENT ON COLUMN cdm.observation.visit_detail_id IS 'A foreign key to the visit in the VISIT_DETAIL table during which the observation was recorded.';



COMMENT ON COLUMN cdm.observation.observation_event_id IS 'A foreign key to an event table (e.g., PROCEDURE_OCCURRENCE_ID).';



COMMENT ON COLUMN cdm.observation.observation_date IS 'The date of the observation.';



COMMENT ON COLUMN cdm.observation.observation_concept_id IS 'A foreign key to the standard observation concept identifier in the Standardized Vocabularies.';



COMMENT ON COLUMN cdm.observation.observation_type_concept_id IS 'A foreign key to the predefined concept identifier in the Standardized Vocabularies reflecting the type of the observation.';



COMMENT ON COLUMN cdm.observation.qualifier_concept_id IS 'A foreign key to a Standard Concept ID for a qualifier (e.g., severity of drug-drug interaction alert)';



COMMENT ON COLUMN cdm.observation.observation_source_concept_id IS 'A foreign key to a Concept that refers to the code used in the source.';



COMMENT ON COLUMN cdm.observation.obs_event_field_concept_id IS 'A foreign key that refers to a Standard Concept identifier in the Standardized Vocabularies referring to the field represented in the OBSERVATION_EVENT_ID.';



COMMENT ON COLUMN cdm.observation.value_as_concept_id IS 'A foreign key to an observation result stored as a Concept ID. This is applicable to observations where the result can be expressed as a Standard Concept from the Standardized Vocabularies (e.g., positive/negative, present/absent, low/high, etc.).';



COMMENT ON COLUMN cdm.observation.unit_concept_id IS 'A foreign key to a Standard Concept ID of measurement units in the Standardized Vocabularies.';



COMMENT ON COLUMN cdm.observation.value_as_number IS 'The observation result stored as a number. This is applicable to observations where the result is expressed as a numeric value.';



COMMENT ON COLUMN cdm.observation.value_as_string IS 'The observation result stored as a string. This is applicable to observations where the result is expressed as verbatim text.';



COMMENT ON COLUMN cdm.observation.observation_source_value IS 'The observation code as it appears in the source data. This code is mapped to a Standard Concept in the Standardized Vocabularies and the original code is, stored here for reference.';



COMMENT ON COLUMN cdm.observation.unit_source_value IS 'The source code for the unit as it appears in the source data. This code is mapped to a standard unit concept in the Standardized Vocabularies and the original code is, stored here for reference.';



COMMENT ON COLUMN cdm.observation.qualifier_source_value IS 'The source value associated with a qualifier to characterize the observation';



CREATE TABLE cdm.observation_period (
    observation_period_id bigint NOT NULL,
    person_id bigint NOT NULL,
    observation_period_start_date date NOT NULL,
    observation_period_end_date date NOT NULL,
    period_type_concept_id integer NOT NULL
);



COMMENT ON TABLE cdm.observation_period IS 'The OBSERVATION_PERIOD table contains records which uniquely define the spans of time for which a Person is at-risk to have clinical events recorded within the source systems, even if no events in fact are recorded (healthy patient with no healthcare interactions).';



COMMENT ON COLUMN cdm.observation_period.observation_period_id IS 'A unique identifier for each observation period.';



COMMENT ON COLUMN cdm.observation_period.person_id IS 'A foreign key identifier to the person for whom the observation period is defined. The demographic details of that person are stored in the person table.';



COMMENT ON COLUMN cdm.observation_period.observation_period_start_date IS 'The start date of the observation period for which data are available from the data source.';



COMMENT ON COLUMN cdm.observation_period.observation_period_end_date IS 'The end date of the observation period for which data are available from the data source.';



COMMENT ON COLUMN cdm.observation_period.period_type_concept_id IS 'A foreign key identifier to the predefined concept in the Standardized Vocabularies reflecting the source of the observation period information, belonging to the ''Obs Period Type'' vocabulary';



CREATE TABLE cdm.payer_plan_period (
    payer_plan_period_id bigint NOT NULL,
    person_id bigint NOT NULL,
    contract_person_id bigint,
    payer_plan_period_start_date date NOT NULL,
    payer_plan_period_end_date date NOT NULL,
    payer_concept_id integer NOT NULL,
    plan_concept_id integer NOT NULL,
    contract_concept_id integer,
    sponsor_concept_id integer,
    stop_reason_concept_id integer NOT NULL,
    payer_source_concept_id integer NOT NULL,
    plan_source_concept_id integer NOT NULL,
    contract_source_concept_id integer,
    sponsor_source_concept_id integer NOT NULL,
    stop_reason_source_concept_id integer NOT NULL,
    payer_source_value text,
    plan_source_value text,
    contract_source_value text,
    sponsor_source_value text,
    family_source_value text,
    stop_reason_source_value text
);




COMMENT ON TABLE cdm.payer_plan_period IS 'The PAYER_PLAN_PERIOD table captures details of the period of time that a Person is continuously enrolled under a specific health Plan benefit structure from a given Payer. Each Person receiving healthcare is typically covered by a health benefit plan, which pays for (fully or partially), or directly provides, the care. These benefit plans are provided by payers, such as health insurances or state or government agencies. In each plan the details of the health benefits are defined for the Person or her family, and the health benefit Plan might change over time typically with increasing utilization (reaching certain cost thresholds such as deductibles), plan availability and purchasing choices of the Person. The unique combinations of Payer organizations, health benefit Plans and time periods in which they are valid for a Person are recorded in this table.';



COMMENT ON COLUMN cdm.payer_plan_period.payer_plan_period_id IS 'A identifier for each unique combination of payer, plan, family code and time span.';



COMMENT ON COLUMN cdm.payer_plan_period.person_id IS 'A foreign key identifier to the Person covered by the payer. The demographic details of that Person are stored in the PERSON table.';



COMMENT ON COLUMN cdm.payer_plan_period.contract_person_id IS 'A foreign key identifier to the person_id in person table, for the person who is the primary subscriber/contract owner for the record in the payer_plan_period table. Maybe the same person or different person, depending on who is the primary subscriber/contract owner.';



COMMENT ON COLUMN cdm.payer_plan_period.payer_plan_period_start_date IS 'The start date of the payer plan period.';



COMMENT ON COLUMN cdm.payer_plan_period.payer_plan_period_end_date IS 'The end date of the payer plan period.';



COMMENT ON COLUMN cdm.payer_plan_period.payer_concept_id IS 'A foreign key that refers to a standard Payer concept identifier in the Standarized Vocabularies';



COMMENT ON COLUMN cdm.payer_plan_period.plan_concept_id IS 'A foreign key that refers to a standard plan concept identifier that represents the health benefit plan in the Standardized Vocabularies.';



COMMENT ON COLUMN cdm.payer_plan_period.contract_concept_id IS 'A foreign key to a standard concept representing the reason justifying the contract between person_id and contract_person_id.';



COMMENT ON COLUMN cdm.payer_plan_period.sponsor_concept_id IS 'A foreign key that refers to a concept identifier that represents the sponsor in the Standardized Vocabularies.';



COMMENT ON COLUMN cdm.payer_plan_period.stop_reason_concept_id IS 'A foreign key that refers to a standard termination reason that represents the reason for the termination in the Standardized Vocabularies.';



COMMENT ON COLUMN cdm.payer_plan_period.payer_source_concept_id IS 'A foreign key to a payer concept that refers to the code used in the source.';



COMMENT ON COLUMN cdm.payer_plan_period.plan_source_concept_id IS 'A foreign key to a plan concept that refers to the plan code used in the source data.';



COMMENT ON COLUMN cdm.payer_plan_period.contract_source_concept_id IS 'A foreign key to a concept that refers to the code used in the source as the reason justifying the contract.';



COMMENT ON COLUMN cdm.payer_plan_period.sponsor_source_concept_id IS 'A foreign key to a sponsor concept that refers to the sponsor code used in the source data.';



COMMENT ON COLUMN cdm.payer_plan_period.stop_reason_source_concept_id IS 'A foreign key to a stop-coverage concept that refers to the code used in the source.';



COMMENT ON COLUMN cdm.payer_plan_period.payer_source_value IS 'The source code for the payer as it appears in the source data.';



COMMENT ON COLUMN cdm.payer_plan_period.plan_source_value IS 'The source code for the Person''s health benefit plan as it appears in the source data.';



COMMENT ON COLUMN cdm.payer_plan_period.contract_source_value IS 'The source code representing the reason justifying the contract. Usually it is family relationship like a spouse, domestic partner, child etc.';



COMMENT ON COLUMN cdm.payer_plan_period.sponsor_source_value IS 'The source code for the Person''s sponsor of the health plan as it appears in the source data.';



COMMENT ON COLUMN cdm.payer_plan_period.family_source_value IS 'The source code for the Person''s family as it appears in the source data.';



COMMENT ON COLUMN cdm.payer_plan_period.stop_reason_source_value IS 'The reason for stop-coverage as it appears in the source data.';



CREATE TABLE cdm.person (
    person_id bigint NOT NULL,
    location_id bigint,
    provider_id bigint,
    care_site_id bigint,
    birth_datetime timestamp without time zone,
    year_of_birth integer NOT NULL,
    gender_source_concept_id integer NOT NULL,
    gender_concept_id integer NOT NULL,
    ethnicity_concept_id integer NOT NULL,
    ethnicity_source_concept_id integer NOT NULL,
    race_concept_id integer NOT NULL,
    race_source_concept_id integer NOT NULL,
    month_of_birth integer,
    day_of_birth integer,
    person_source_value text,
    gender_source_value text,
    race_source_value text,
    ethnicity_source_value text
);


COMMENT ON TABLE cdm.person IS 'The Person Domain contains records that uniquely identify each patient in the source data who is time at-risk to have clinical observations recorded within the source systems.';



COMMENT ON COLUMN cdm.person.person_id IS 'A unique identifier for each person.';



COMMENT ON COLUMN cdm.person.location_id IS 'A foreign key to the place of residency for the person in the location table, where the detailed address information is stored.';



COMMENT ON COLUMN cdm.person.provider_id IS 'A foreign key to the primary care provider the person is seeing in the provider table.';



COMMENT ON COLUMN cdm.person.care_site_id IS 'A foreign key to the site of primary care in the care_site table, where the details of the care site are stored.';



COMMENT ON COLUMN cdm.person.birth_datetime IS 'The date and time of birth of the person.';



COMMENT ON COLUMN cdm.person.year_of_birth IS 'The year of birth of the person. For data sources with date of birth, the year is extracted. For data sources where the year of birth is not available, the approximate year of birth is derived based on any age group categorization available.';



COMMENT ON COLUMN cdm.person.gender_source_concept_id IS 'A foreign key to the gender concept that refers to the code used in the source.';



COMMENT ON COLUMN cdm.person.gender_concept_id IS 'A foreign key that refers to an identifier in the CONCEPT table for the unique gender of the person.';



COMMENT ON COLUMN cdm.person.ethnicity_concept_id IS 'A foreign key that refers to the standard concept identifier in the Standardized Vocabularies for the ethnicity of the person, belonging to the ''Ethnicity'' vocabulary.';



COMMENT ON COLUMN cdm.person.ethnicity_source_concept_id IS 'A foreign key to the ethnicity concept that refers to the code used in the source.';



COMMENT ON COLUMN cdm.person.race_concept_id IS 'A foreign key that refers to an identifier in the CONCEPT table for the unique race of the person, belonging to the ''Race'' vocabulary.';



COMMENT ON COLUMN cdm.person.race_source_concept_id IS 'A foreign key to the race concept that refers to the code used in the source.';



COMMENT ON COLUMN cdm.person.month_of_birth IS 'The month of birth of the person. For data sources that provide the precise date of birth, the month is extracted and stored in this field.';



COMMENT ON COLUMN cdm.person.day_of_birth IS 'The day of the month of birth of the person. For data sources that provide the precise date of birth, the day is extracted and stored in this field.';



COMMENT ON COLUMN cdm.person.person_source_value IS 'An (encrypted) key derived from the person identifier in the source data. This is necessary when a use case requires a link back to the person data at the source dataset.';



COMMENT ON COLUMN cdm.person.gender_source_value IS 'The source code for the gender of the person as it appears in the source data. The person’s gender is mapped to a standard gender concept in the Standardized Vocabularies; the original value is stored here for reference.';



COMMENT ON COLUMN cdm.person.race_source_value IS 'The source code for the race of the person as it appears in the source data. The person race is mapped to a standard race concept in the Standardized Vocabularies and the original value is stored here for reference.';



COMMENT ON COLUMN cdm.person.ethnicity_source_value IS 'The source code for the ethnicity of the person as it appears in the source data. The person ethnicity is mapped to a standard ethnicity concept in the Standardized Vocabularies and the original code is, stored here for reference.';



CREATE TABLE cdm.procedure_occurrence (
    procedure_occurrence_id bigint NOT NULL,
    person_id bigint NOT NULL,
    procedure_datetime timestamp without time zone NOT NULL,
    provider_id bigint,
    visit_occurrence_id bigint,
    visit_detail_id bigint,
    procedure_end_datetime timestamp without time zone,
    procedure_concept_id integer NOT NULL,
    procedure_source_concept_id integer NOT NULL,
    procedure_type_concept_id integer NOT NULL,
    modifier_concept_id integer NOT NULL,
    quantity integer,
    procedure_date date,
    procedure_end_date date,
    procedure_source_value text,
    modifier_source_value text
);



COMMENT ON TABLE cdm.procedure_occurrence IS 'The PROCEDURE_OCCURRENCE table contains records of activities or processes ordered by, or carried out by, a healthcare provider on the patient to have a diagnostic or therapeutic purpose. Procedures are present in various data sources in different forms with varying levels of standardization. For example:  * Medical Claims include procedure codes that are submitted as part of a claim for health services rendered, including procedures performed. * Electronic Health Records that capture procedures as orders.';



COMMENT ON COLUMN cdm.procedure_occurrence.procedure_occurrence_id IS 'A system-generated unique identifier for each Procedure Occurrence.';



COMMENT ON COLUMN cdm.procedure_occurrence.person_id IS 'A foreign key identifier to the Person who is subjected to the Procedure. The demographic details of that Person are stored in the PERSON table.';



COMMENT ON COLUMN cdm.procedure_occurrence.procedure_datetime IS 'The date and time on which the Procedure was performed.';



COMMENT ON COLUMN cdm.procedure_occurrence.provider_id IS 'A foreign key to the provider in the PROVIDER table who was responsible for carrying out the procedure.';



COMMENT ON COLUMN cdm.procedure_occurrence.visit_occurrence_id IS 'A foreign key to the Visit in the VISIT_OCCURRENCE table during which the Procedure was carried out.';



COMMENT ON COLUMN cdm.procedure_occurrence.visit_detail_id IS 'A foreign key to the Visit Detail in the VISIT_DETAIL table during which the Procedure was carried out.';



COMMENT ON COLUMN cdm.procedure_occurrence.procedure_concept_id IS 'A foreign key that refers to a standard procedure Concept identifier in the Standardized Vocabularies.';



COMMENT ON COLUMN cdm.procedure_occurrence.procedure_source_concept_id IS 'A foreign key to a Procedure Concept that refers to the code used in the source.';



COMMENT ON COLUMN cdm.procedure_occurrence.procedure_type_concept_id IS 'A foreign key to the predefined Concept identifier in the Standardized Vocabularies reflecting the type of source data from which the procedure record is derived, belonging to the ''Procedure Type'' vocabulary.';



COMMENT ON COLUMN cdm.procedure_occurrence.modifier_concept_id IS 'A foreign key to a Standard Concept identifier for a modifier to the Procedure (e.g. bilateral). These concepts are typically distinguished by ''Modifier'' concept classes (e.g., ''CPT4 Modifier'' as part of the ''CPT4'' vocabulary).';



COMMENT ON COLUMN cdm.procedure_occurrence.quantity IS 'The quantity of procedures ordered or administered.';



COMMENT ON COLUMN cdm.procedure_occurrence.procedure_date IS 'The date on which the Procedure was performed.';



COMMENT ON COLUMN cdm.procedure_occurrence.procedure_source_value IS 'The source code for the Procedure as it appears in the source data. This code is mapped to a standard procedure Concept in the Standardized Vocabularies and the original code is, stored here for reference. Procedure source codes are typically ICD-9-Proc, CPT-4, HCPCS or OPCS-4 codes.';



COMMENT ON COLUMN cdm.procedure_occurrence.modifier_source_value IS 'The source code for the qualifier as it appears in the source data.';



CREATE TABLE cdm.provider (
    provider_id bigint NOT NULL,
    care_site_id bigint,
    specialty_concept_id integer NOT NULL,
    gender_concept_id integer NOT NULL,
    specialty_source_concept_id integer DEFAULT 0 NOT NULL,
    gender_source_concept_id integer NOT NULL,
    year_of_birth integer,
    gender_source_value text,
    provider_source_value text,
    specialty_source_value text,
    provider_name text,
    npi text,
    dea text,
    CONSTRAINT chk_provider_dea CHECK ((COALESCE(length(dea), 0) <= 20)),
    CONSTRAINT chk_provider_npi CHECK ((COALESCE(length(npi), 0) <= 20)),
    CONSTRAINT chk_provider_provider_name CHECK ((COALESCE(length(provider_name), 0) <= 255))
);



COMMENT ON TABLE cdm.provider IS 'The PROVIDER table contains a list of uniquely identified healthcare providers. These are individuals providing hands-on healthcare to patients, such as physicians, nurses, midwives, physical therapists etc.';



COMMENT ON COLUMN cdm.provider.provider_id IS 'A unique identifier for each Provider.';



COMMENT ON COLUMN cdm.provider.care_site_id IS 'A foreign key to the main Care Site where the provider is practicing.';



COMMENT ON COLUMN cdm.provider.specialty_concept_id IS 'A foreign key to a Standard Specialty Concept ID in the Standardized Vocabularies.';



COMMENT ON COLUMN cdm.provider.gender_concept_id IS 'The gender of the Provider.';



COMMENT ON COLUMN cdm.provider.specialty_source_concept_id IS 'A foreign key to a Concept that refers to the code used in the source.';



COMMENT ON COLUMN cdm.provider.gender_source_concept_id IS 'A foreign key to a Concept that refers to the code used in the source.';



COMMENT ON COLUMN cdm.provider.year_of_birth IS 'The year of birth of the Provider.';



COMMENT ON COLUMN cdm.provider.gender_source_value IS 'The gender code for the Provider as it appears in the source data, stored here for reference.';



COMMENT ON COLUMN cdm.provider.provider_source_value IS 'The identifier used for the Provider in the source data, stored here for reference.';



COMMENT ON COLUMN cdm.provider.specialty_source_value IS 'The source code for the Provider specialty as it appears in the source data, stored here for reference.';



COMMENT ON COLUMN cdm.provider.provider_name IS 'A description of the Provider.';



COMMENT ON COLUMN cdm.provider.npi IS 'The National Provider Identifier (NPI) of the provider.';



COMMENT ON COLUMN cdm.provider.dea IS 'The Drug Enforcement Administration (DEA) number of the provider.';



CREATE TABLE cdm.source_to_source_vocab_map (
    source_code text,
    source_concept_id integer,
    source_code_description text,
    source_vocabulary_id text,
    source_domain_id text,
    source_concept_class_id text,
    source_valid_start_date date,
    source_valid_end_date date,
    source_invalid_reason text,
    target_concept_id integer,
    target_concept_name text,
    target_vocabulary_id text,
    target_domain_id text,
    target_concept_class_id text,
    target_invalid_reason text,
    target_standard_concept text
);



CREATE TABLE cdm.source_to_standard_vocab_map (
    source_code text,
    source_concept_id integer,
    source_code_description text,
    source_vocabulary_id text,
    source_domain_id text,
    source_concept_class_id text,
    source_valid_start_date date,
    source_valid_end_date date,
    source_invalid_reason text,
    target_concept_id integer,
    target_concept_name text,
    target_vocabulary_id text,
    target_domain_id text,
    target_concept_class_id text,
    target_invalid_reason text,
    target_standard_concept text
);


ALTER TABLE cdm.source_to_standard_vocab_map OWNER TO postgres;


CREATE TABLE cdm.specimen (
    specimen_id bigint NOT NULL,
    person_id bigint NOT NULL,
    specimen_datetime timestamp without time zone NOT NULL,
    specimen_concept_id integer NOT NULL,
    specimen_type_concept_id integer NOT NULL,
    anatomic_site_concept_id integer NOT NULL,
    disease_status_concept_id integer NOT NULL,
    unit_concept_id integer,
    specimen_date date,
    quantity numeric,
    specimen_source_id text,
    specimen_source_value text,
    unit_source_value text,
    anatomic_site_source_value text,
    disease_status_source_value text,
    CONSTRAINT chk_specimen_specimen_source_id CHECK ((COALESCE(length(specimen_source_id), 0) <= 50))
);


ALTER TABLE cdm.specimen OWNER TO postgres;


COMMENT ON TABLE cdm.specimen IS 'The specimen domain contains the records identifying biological samples from a person.';



COMMENT ON COLUMN cdm.specimen.specimen_id IS 'A unique identifier for each specimen.';



COMMENT ON COLUMN cdm.specimen.person_id IS 'A foreign key identifier to the Person for whom the Specimen is recorded.';



COMMENT ON COLUMN cdm.specimen.specimen_datetime IS 'The date and time on the date when the Specimen was obtained from the person.';



COMMENT ON COLUMN cdm.specimen.specimen_concept_id IS 'A foreign key referring to a Standard Concept identifier in the Standardized Vocabularies for the Specimen.';



COMMENT ON COLUMN cdm.specimen.specimen_type_concept_id IS 'A foreign key referring to the Concept identifier in the Standardized Vocabularies reflecting the system of record from which the Specimen was represented in the source data.';



COMMENT ON COLUMN cdm.specimen.anatomic_site_concept_id IS 'A foreign key to a Standard Concept identifier for the anatomic location of specimen collection.';



COMMENT ON COLUMN cdm.specimen.disease_status_concept_id IS 'A foreign key to a Standard Concept identifier for the Disease Status of specimen collection.';



COMMENT ON COLUMN cdm.specimen.unit_concept_id IS 'A foreign key to a Standard Concept identifier for the Unit associated with the numeric quantity of the Specimen collection.';



COMMENT ON COLUMN cdm.specimen.specimen_date IS 'The date the specimen was obtained from the Person.';



COMMENT ON COLUMN cdm.specimen.quantity IS 'The amount of specimen collection from the person during the sampling procedure.';



COMMENT ON COLUMN cdm.specimen.specimen_source_id IS 'The Specimen identifier as it appears in the source data.';



COMMENT ON COLUMN cdm.specimen.specimen_source_value IS 'The Specimen value as it appears in the source data. This value is mapped to a Standard Concept in the Standardized Vocabularies and the original code is, stored here for reference.';



COMMENT ON COLUMN cdm.specimen.unit_source_value IS 'The information about the Unit as detailed in the source.';



COMMENT ON COLUMN cdm.specimen.anatomic_site_source_value IS 'The information about the anatomic site as detailed in the source.';



COMMENT ON COLUMN cdm.specimen.disease_status_source_value IS 'The information about the disease status as detailed in the source.';



CREATE TABLE cdm.survey_conduct (
    survey_conduct_id bigint NOT NULL,
    person_id bigint NOT NULL,
    survey_end_datetime timestamp without time zone NOT NULL,
    survey_start_datetime timestamp without time zone,
    visit_occurrence_id bigint,
    visit_detail_id bigint,
    response_visit_occurrence_id bigint,
    provider_id bigint,
    survey_concept_id integer NOT NULL,
    assisted_concept_id integer NOT NULL,
    respondent_type_concept_id integer NOT NULL,
    timing_concept_id integer NOT NULL,
    collection_method_concept_id integer NOT NULL,
    survey_source_concept_id integer NOT NULL,
    validated_survey_concept_id integer NOT NULL,
    survey_start_date date,
    survey_end_date date,
    assisted_source_value text,
    respondent_type_source_value text,
    timing_source_value text,
    collection_method_source_value text,
    survey_source_value text,
    survey_source_identifier text,
    validated_survey_source_value text,
    survey_version_number text,
    CONSTRAINT survey_source_identifier_length CHECK ((COALESCE(length(survey_source_identifier), 0) <= 100)),
    CONSTRAINT survey_version_number_length CHECK ((COALESCE(length(survey_version_number), 0) <= 20))
);




COMMENT ON TABLE cdm.survey_conduct IS 'The SURVEY_CONDUCT table is used to store an instance of a completed survey or questionnaire. It captures details of the individual questionnaire such as who completed it, when it was completed and to which patient treatment or visit it relates to (if any). Each SURVEY has a SURVEY_CONCEPT_ID, a concept in the CONCEPT table identifying the questionnaire e.g. EQ5D, VR12, SF12. Each questionnaire should exist in the CONCEPT table. Each SURVEY can be optionally related to a specific patient visit in order to link it both to the visit during which it was completed and any subsequent visit where treatment was assigned based on the patient''s responses.';



COMMENT ON COLUMN cdm.survey_conduct.survey_conduct_id IS 'Unique identifier for each completed survey.';



COMMENT ON COLUMN cdm.survey_conduct.person_id IS 'A foreign key identifier to the Person in the PERSON table about whom the survey was completed.';



COMMENT ON COLUMN cdm.survey_conduct.survey_end_datetime IS 'Date and time the survey was completed.';



COMMENT ON COLUMN cdm.survey_conduct.survey_start_datetime IS 'Date and time the survey was started.';



COMMENT ON COLUMN cdm.survey_conduct.visit_occurrence_id IS 'A foreign key to the VISIT_OCCURRENCE table during which the survey was completed';



COMMENT ON COLUMN cdm.survey_conduct.visit_detail_id IS 'A foreign key to the Visit in the VISIT_DETAIL table when the Note was taken.';



COMMENT ON COLUMN cdm.survey_conduct.response_visit_occurrence_id IS 'A foreign key to the visit in the VISIT_OCCURRENCE table during which treatment was carried out that relates to this survey.';



COMMENT ON COLUMN cdm.survey_conduct.provider_id IS 'A foreign key to the provider in the provider table who was associated with the survey completion.';



COMMENT ON COLUMN cdm.survey_conduct.survey_concept_id IS 'A foreign key to the predefined Concept identifier in the Standardized Vocabularies reflecting the name and identity of the survey.';



COMMENT ON COLUMN cdm.survey_conduct.assisted_concept_id IS 'A foreign key to the predefined Concept identifier in the Standardized Vocabularies indicating whether the survey was completed with assistance.';



COMMENT ON COLUMN cdm.survey_conduct.respondent_type_concept_id IS 'A foreign key to the predefined Concept identifier in the Standardized Vocabularies reflecting the respondent type. Example: Research Associate, Patient.';



COMMENT ON COLUMN cdm.survey_conduct.timing_concept_id IS 'A foreign key to the predefined Concept identifier in the Standardized Vocabularies that refers to a certain timing. Example: 3 month follow-up, 6 month follow-up.';



COMMENT ON COLUMN cdm.survey_conduct.collection_method_concept_id IS 'A foreign key to the predefined Concept identifier in the Standardized Vocabularies reflecting the data collection method (e.g. Paper, Telephone, Electronic Questionnaire).';



COMMENT ON COLUMN cdm.survey_conduct.survey_source_concept_id IS 'A foreign key to a predefined Concept that refers to the code for the survey name/title used in the source.';



COMMENT ON COLUMN cdm.survey_conduct.validated_survey_concept_id IS 'A foreign key to the predefined Concept identifier in the Standardized Vocabularies reflecting the validation status of the survey.';



COMMENT ON COLUMN cdm.survey_conduct.survey_start_date IS 'Date on which the survey was started.';



COMMENT ON COLUMN cdm.survey_conduct.survey_end_date IS 'Date on which the survey was completed.';



COMMENT ON COLUMN cdm.survey_conduct.assisted_source_value IS 'Source value representing whether patient required assistance to complete the survey. Example: “Completed without assistance”, ”Completed with assistance”.';



COMMENT ON COLUMN cdm.survey_conduct.respondent_type_source_value IS 'Source code representing role of person who completed the survey.';



COMMENT ON COLUMN cdm.survey_conduct.timing_source_value IS 'Text string representing the timing of the survey. Example: Baseline, 6-month follow-up.';



COMMENT ON COLUMN cdm.survey_conduct.collection_method_source_value IS 'The collection method as it appears in the source data.';



COMMENT ON COLUMN cdm.survey_conduct.survey_source_value IS 'The survey name/title as it appears in the source data.';



COMMENT ON COLUMN cdm.survey_conduct.survey_source_identifier IS 'Unique identifier for each completed survey in source system.';



COMMENT ON COLUMN cdm.survey_conduct.validated_survey_source_value IS 'Source value representing the validation status of the survey.';



COMMENT ON COLUMN cdm.survey_conduct.survey_version_number IS 'Version number of the questionnaire or survey used.';



CREATE TABLE cdm.visit_detail (
    visit_detail_id bigint NOT NULL,
    visit_detail_start_datetime timestamp without time zone,
    visit_detail_end_datetime timestamp without time zone,
    person_id bigint NOT NULL,
    visit_occurrence_id bigint NOT NULL,
    provider_id bigint,
    care_site_id bigint,
    preceding_visit_detail_id bigint,
    parent_visit_detail_id bigint,
    visit_detail_concept_id integer NOT NULL,
    visit_detail_type_concept_id integer NOT NULL,
    discharged_to_concept_id integer,
    admitted_from_concept_id integer,
    visit_detail_source_concept_id integer,
    visit_detail_start_date date,
    visit_detail_end_date date,
    admitted_from_source_value text,
    visit_detail_source_value text,
    discharged_to_source_value text
);



COMMENT ON TABLE cdm.visit_detail IS 'The VISIT_DETAIL table is an optional table used to represents details of each record in the parent visit_occurrence table. For every record in visit_occurrence table there may be 0 or more records in the visit_detail table with a 1:n relationship where n may be 0. The visit_detail table is structurally very similar to visit_occurrence table and belongs to the similar domain as the visit.';



COMMENT ON COLUMN cdm.visit_detail.visit_detail_id IS 'A unique identifier for each Person''s visit or encounter at a healthcare provider.';



COMMENT ON COLUMN cdm.visit_detail.visit_detail_start_datetime IS 'The date and time of the visit started.';



COMMENT ON COLUMN cdm.visit_detail.visit_detail_end_datetime IS 'The date and time of the visit end.';



COMMENT ON COLUMN cdm.visit_detail.person_id IS 'A foreign key identifier to the Person for whom the visit is recorded. The demographic details of that Person are stored in the PERSON table.';



COMMENT ON COLUMN cdm.visit_detail.visit_occurrence_id IS 'A foreign key that refers to the record in the VISIT_OCCURRENCE table. This is a required field, because for every visit_detail is a child of visit_occurrence and cannot exist without a corresponding parent record in visit_occurrence.';



COMMENT ON COLUMN cdm.visit_detail.provider_id IS 'A foreign key to the provider in the provider table who was associated with the visit.';



COMMENT ON COLUMN cdm.visit_detail.care_site_id IS 'A foreign key to the care site in the care site table that was visited.';



COMMENT ON COLUMN cdm.visit_detail.preceding_visit_detail_id IS 'A foreign key to the VISIT_DETAIL table of the visit immediately preceding this visit';



COMMENT ON COLUMN cdm.visit_detail.parent_visit_detail_id IS 'A foreign key to the VISIT_DETAIL table record to represent the immediate parent visit-detail record.';



COMMENT ON COLUMN cdm.visit_detail.visit_detail_concept_id IS 'A foreign key that refers to a visit Concept identifier in the Standardized Vocabularies belonging to the ''Visit'' Vocabulary.';



COMMENT ON COLUMN cdm.visit_detail.visit_detail_type_concept_id IS 'A foreign key to the predefined Concept identifier in the Standardized Vocabularies reflecting the type of source data from which the visit record is derived belonging to the ''Visit Type'' vocabulary.';



COMMENT ON COLUMN cdm.visit_detail.discharged_to_concept_id IS 'A foreign key to the predefined concept in the ''Place of Service'' Vocabulary reflecting the discharge disposition for a visit.';



COMMENT ON COLUMN cdm.visit_detail.admitted_from_concept_id IS 'A foreign key to the predefined concept in the ''Place of Service'' Vocabulary reflecting the admitting source for a visit.';



COMMENT ON COLUMN cdm.visit_detail.visit_detail_source_concept_id IS 'A foreign key to a Concept that refers to the code used in the source.';



COMMENT ON COLUMN cdm.visit_detail.visit_detail_start_date IS 'The start date of the visit.';



COMMENT ON COLUMN cdm.visit_detail.visit_detail_end_date IS 'The end date of the visit. If this is a one-day visit the end date should match the start date.';



COMMENT ON COLUMN cdm.visit_detail.admitted_from_source_value IS 'The source code for the admitting source as it appears in the source data.';



COMMENT ON COLUMN cdm.visit_detail.visit_detail_source_value IS 'The source code for the visit as it appears in the source data.';



COMMENT ON COLUMN cdm.visit_detail.discharged_to_source_value IS 'The source code for the discharge disposition as it appears in the source data.';



CREATE TABLE cdm.visit_occurrence (
    visit_occurrence_id bigint NOT NULL,
    person_id bigint NOT NULL,
    visit_start_datetime timestamp without time zone NOT NULL,
    visit_end_datetime timestamp without time zone NOT NULL,
    provider_id bigint,
    care_site_id bigint,
    preceding_visit_occurrence_id bigint,
    visit_concept_id integer NOT NULL,
    visit_type_concept_id integer NOT NULL,
    visit_source_concept_id integer NOT NULL,
    admitted_from_concept_id integer NOT NULL,
    discharged_to_concept_id integer NOT NULL,
    visit_start_date date,
    visit_end_date date,
    visit_source_value text,
    admitted_from_source_value text,
    discharged_to_source_value text
);



COMMENT ON TABLE cdm.visit_occurrence IS 'The VISIT_OCCURRENCE table contains the spans of time a Person continuously receives medical services from one or more providers at a Care Site in a given setting within the health care system. Visits are classified into 4 settings: outpatient care, inpatient confinement, emergency room, and long-term care. Persons may transition between these settings over the course of an episode of care (for example, treatment of a disease onset).';



COMMENT ON COLUMN cdm.visit_occurrence.visit_occurrence_id IS 'A unique identifier for each Person''s visit or encounter at a healthcare provider.';



COMMENT ON COLUMN cdm.visit_occurrence.person_id IS 'A foreign key identifier to the Person for whom the visit is recorded. The demographic details of that Person are stored in the PERSON table.';



COMMENT ON COLUMN cdm.visit_occurrence.visit_start_datetime IS 'The date and time of the visit started.';



COMMENT ON COLUMN cdm.visit_occurrence.visit_end_datetime IS 'The date and time of the visit end.';



COMMENT ON COLUMN cdm.visit_occurrence.provider_id IS 'A foreign key to the provider in the provider table who was associated with the visit.';



COMMENT ON COLUMN cdm.visit_occurrence.care_site_id IS 'A foreign key to the care site in the care site table that was visited.';



COMMENT ON COLUMN cdm.visit_occurrence.preceding_visit_occurrence_id IS 'A foreign key to the VISIT_OCCURRENCE table of the visit immediately preceding this visit';



COMMENT ON COLUMN cdm.visit_occurrence.visit_concept_id IS 'A foreign key that refers to a visit Concept identifier in the Standardized Vocabularies belonging to the ''Visit'' Vocabulary.';



COMMENT ON COLUMN cdm.visit_occurrence.visit_type_concept_id IS 'A foreign key to the predefined Concept identifier in the Standardized Vocabularies reflecting the type of source data from which the visit record is derived belonging to the ''Visit Type'' vocabulary.';



COMMENT ON COLUMN cdm.visit_occurrence.visit_source_concept_id IS 'A foreign key to a Concept that refers to the code used in the source.';



COMMENT ON COLUMN cdm.visit_occurrence.admitted_from_concept_id IS 'A foreign key to the predefined concept in the Place of Service Vocabulary reflecting where the patient was admitted from.';



COMMENT ON COLUMN cdm.visit_occurrence.discharged_to_concept_id IS 'A foreign key to the predefined concept in the Place of Service Vocabulary reflecting the discharge disposition for a visit.';



COMMENT ON COLUMN cdm.visit_occurrence.visit_start_date IS 'The start date of the visit.';



COMMENT ON COLUMN cdm.visit_occurrence.visit_end_date IS 'The end date of the visit. If this is a one-day visit the end date should match the start date.';



COMMENT ON COLUMN cdm.visit_occurrence.visit_source_value IS 'The source code for the visit as it appears in the source data.';



COMMENT ON COLUMN cdm.visit_occurrence.admitted_from_source_value IS 'The source code for where the patient was admitted from as it appears in the source data.';



COMMENT ON COLUMN cdm.visit_occurrence.discharged_to_source_value IS 'The source code for the discharge disposition as it appears in the source data.';




CREATE TABLE vocabularies.concept (
    concept_id integer NOT NULL,
    valid_start_date date NOT NULL,
    valid_end_date date NOT NULL,
    concept_name text NOT NULL,
    domain_id text NOT NULL,
    vocabulary_id text NOT NULL,
    concept_class_id text NOT NULL,
    concept_code text NOT NULL,
    standard_concept text,
    invalid_reason text,
    CONSTRAINT chk_concept_concept_code CHECK ((concept_code <> ''::text)),
    CONSTRAINT chk_concept_concept_name CHECK ((concept_name <> ''::text)),
    CONSTRAINT chk_concept_invalid_reason CHECK ((COALESCE(invalid_reason, ('D'::character varying)::text) = ANY (ARRAY[('D'::character varying)::text, ('U'::character varying)::text]))),
    CONSTRAINT chk_concept_standard_concept CHECK ((COALESCE(standard_concept, ('C'::character varying)::text) = ANY (ARRAY[('C'::character varying)::text, ('S'::character varying)::text])))
);



COMMENT ON TABLE vocabularies.concept IS 'The Standardized Vocabularies contains records, or Concepts, that uniquely identify each fundamental unit of meaning used to express clinical information in all domain tables of the CDM. Concepts are derived from vocabularies, which represent clinical information across a domain (e.g. conditions, drugs, procedures) through the use of codes and associated descriptions. Some Concepts are designated Standard Concepts, meaning these Concepts can be used as normative expressions of a clinical entity within the OMOP Common Data Model and within standardized analytics. Each Standard Concept belongs to one domain, which defines the location where the Concept would be expected to occur within data tables of the CDM.  Concepts can represent broad categories (like ''Cardiovascular disease''), detailed clinical elements (''Myocardial infarction of the anterolateral wall'') or modifying characteristics and attributes that define Concepts at various levels of detail (severity of a disease, associated morphology, etc.).  Records in the Standardized Vocabularies tables are derived from national or international vocabularies such as SNOMED-CT, RxNorm, and LOINC, or custom Concepts defined to cover various aspects of observational data analysis. For a detailed description of these vocabularies, their use in the OMOP CDM and their relationships to each other please refer to the [specifications](http://www.ohdsi.org/web/wiki/doku.php?id=documentation:vocabulary).';



COMMENT ON COLUMN vocabularies.concept.concept_id IS 'A unique identifier for each Concept across all domains.';



COMMENT ON COLUMN vocabularies.concept.valid_start_date IS 'The date when the Concept was first recorded. The default value is 1-Jan-1970, meaning, the Concept has no (known) date of inception.';



COMMENT ON COLUMN vocabularies.concept.valid_end_date IS 'The date when the Concept became invalid because it was deleted or superseded (updated) by a new concept. The default value is 31-Dec-2099, meaning, the Concept is valid until it becomes deprecated.';



COMMENT ON COLUMN vocabularies.concept.concept_name IS 'An unambiguous, meaningful and descriptive name for the Concept.';



COMMENT ON COLUMN vocabularies.concept.domain_id IS 'A foreign key to the [DOMAIN](https://github.com/OHDSI/CommonDataModel/wiki/DOMAIN) table the Concept belongs to.';



COMMENT ON COLUMN vocabularies.concept.vocabulary_id IS 'A foreign key to the [VOCABULARY](https://github.com/OHDSI/CommonDataModel/wiki/VOCABULARY) table indicating from which source the Concept has been adapted.';



COMMENT ON COLUMN vocabularies.concept.concept_class_id IS 'The attribute or concept class of the Concept. Examples are ''Clinical Drug'', ''Ingredient'', ''Clinical Finding'' etc.';



COMMENT ON COLUMN vocabularies.concept.concept_code IS 'The concept code represents the identifier of the Concept in the source vocabulary, such as SNOMED-CT concept IDs, RxNorm RXCUIs etc. Note that concept codes are not unique across vocabularies.';



COMMENT ON COLUMN vocabularies.concept.standard_concept IS 'This flag determines where a Concept is a Standard Concept, i.e. is used in the data, a Classification Concept, or a non-standard Source Concept. The allowables values are ''S'' (Standard Concept) and ''C'' (Classification Concept), otherwise the content is NULL.';



COMMENT ON COLUMN vocabularies.concept.invalid_reason IS 'Reason the Concept was invalidated. Possible values are D (deleted), U (replaced with an update) or NULL when valid_end_date has the default value.';



CREATE TABLE vocabularies.concept_ancestor (
    ancestor_concept_id integer NOT NULL,
    descendant_concept_id integer NOT NULL,
    min_levels_of_separation integer NOT NULL,
    max_levels_of_separation integer NOT NULL
);


COMMENT ON TABLE vocabularies.concept_ancestor IS 'The CONCEPT_ANCESTOR table is designed to simplify observational analysis by providing the complete hierarchical relationships between Concepts. Only direct parent-child relationships between Concepts are stored in the CONCEPT_RELATIONSHIP table. To determine higher level ancestry connections, all individual direct relationships would have to be navigated at analysis time. The CONCEPT_ANCESTOR table includes records for all parent-child relationships, as well as grandparent-grandchild relationships and those of any other level of lineage. Using the CONCEPT_ANCESTOR table allows for querying for all descendants of a hierarchical concept. For example, drug ingredients and drug products are all descendants of a drug class ancestor.  This table is entirely derived from the CONCEPT, CONCEPT_RELATIONSHIP and RELATIONSHIP tables.';



COMMENT ON COLUMN vocabularies.concept_ancestor.ancestor_concept_id IS 'A foreign key to the concept in the concept table for the higher-level concept that forms the ancestor in the relationship.';



COMMENT ON COLUMN vocabularies.concept_ancestor.descendant_concept_id IS 'A foreign key to the concept in the concept table for the lower-level concept that forms the descendant in the relationship.';



COMMENT ON COLUMN vocabularies.concept_ancestor.min_levels_of_separation IS 'The minimum separation in number of levels of hierarchy between ancestor and descendant concepts. This is an attribute that is used to simplify hierarchic analysis.';



COMMENT ON COLUMN vocabularies.concept_ancestor.max_levels_of_separation IS 'The maximum separation in number of levels of hierarchy between ancestor and descendant concepts. This is an attribute that is used to simplify hierarchic analysis.';



CREATE TABLE vocabularies.concept_class (
    concept_class_concept_id integer NOT NULL,
    concept_class_id text NOT NULL,
    concept_class_name text NOT NULL,
    CONSTRAINT chk_concept_class_concept_class_id CHECK ((length(concept_class_id) <= 20)),
    CONSTRAINT chk_concept_class_concept_class_name CHECK ((length(concept_class_name) <= 255))
);



COMMENT ON TABLE vocabularies.concept_class IS 'The CONCEPT_CLASS table is a reference table, which includes a list of the classifications used to differentiate Concepts within a given Vocabulary. This reference table is populated with a single record for each Concept Class:';



COMMENT ON COLUMN vocabularies.concept_class.concept_class_concept_id IS 'A foreign key that refers to an identifier in the [CONCEPT](https://github.com/OHDSI/CommonDataModel/wiki/CONCEPT) table for the unique Concept Class the record belongs to.';



COMMENT ON COLUMN vocabularies.concept_class.concept_class_id IS 'A unique key for each class.';



COMMENT ON COLUMN vocabularies.concept_class.concept_class_name IS 'The name describing the Concept Class, e.g. "Clinical Finding", "Ingredient", etc.';



CREATE TABLE vocabularies.concept_relationship (
    concept_id_1 integer NOT NULL,
    concept_id_2 integer NOT NULL,
    valid_start_date date NOT NULL,
    valid_end_date date NOT NULL,
    relationship_id text NOT NULL,
    invalid_reason text,
    CONSTRAINT chk_concept_relationship_relationship_id CHECK ((length(relationship_id) <= 20)),
    CONSTRAINT chk_invalid_reason CHECK ((COALESCE(invalid_reason, ('D'::character varying)::text) = 'D'::text))
);


ALTER TABLE vocabularies.concept_relationship OWNER TO postgres;


COMMENT ON TABLE vocabularies.concept_relationship IS 'The CONCEPT_RELATIONSHIP table contains records that define direct relationships between any two Concepts and the nature or type of the relationship. Each type of a relationship is defined in the [RELATIONSHIP](https://github.com/OHDSI/CommonDataModel/wiki/RELATIONSHIP) table.';



COMMENT ON COLUMN vocabularies.concept_relationship.concept_id_1 IS 'A foreign key to a Concept in the [CONCEPT](https://github.com/OHDSI/CommonDataModel/wiki/CONCEPT) table associated with the relationship. Relationships are directional, and this field represents the source concept designation.';



COMMENT ON COLUMN vocabularies.concept_relationship.concept_id_2 IS 'A foreign key to a Concept in the [CONCEPT](https://github.com/OHDSI/CommonDataModel/wiki/CONCEPT) table associated with the relationship. Relationships are directional, and this field represents the destination concept designation.';



COMMENT ON COLUMN vocabularies.concept_relationship.valid_start_date IS 'The date when the instance of the Concept Relationship is first recorded.';



COMMENT ON COLUMN vocabularies.concept_relationship.valid_end_date IS 'The date when the Concept Relationship became invalid because it was deleted or superseded (updated) by a new relationship. Default value is 31-Dec-2099.';



COMMENT ON COLUMN vocabularies.concept_relationship.relationship_id IS 'A unique identifier to the type or nature of the Relationship as defined in the [RELATIONSHIP](https://github.com/OHDSI/CommonDataModel/wiki/RELATIONSHIP) table.';



COMMENT ON COLUMN vocabularies.concept_relationship.invalid_reason IS 'Reason the relationship was invalidated. Possible values are ''D'' (deleted), ''U'' (replaced with an update) or NULL when valid_end_date has the default value.';



CREATE TABLE vocabularies.concept_synonym (
    concept_id integer NOT NULL,
    language_concept_id integer NOT NULL,
    concept_synonym_name text NOT NULL,
    CONSTRAINT chk_csyn_concept_synonym_name CHECK ((concept_synonym_name <> ''::text))
);


ALTER TABLE vocabularies.concept_synonym OWNER TO postgres;


COMMENT ON TABLE vocabularies.concept_synonym IS 'The CONCEPT_SYNONYM table is used to store alternate names and descriptions for Concepts.';



COMMENT ON COLUMN vocabularies.concept_synonym.concept_id IS 'A foreign key to the Concept in the CONCEPT table.';



COMMENT ON COLUMN vocabularies.concept_synonym.language_concept_id IS 'A foreign key to a Concept representing the language.';



COMMENT ON COLUMN vocabularies.concept_synonym.concept_synonym_name IS 'The alternative name for the Concept.';



CREATE TABLE vocabularies.domain (
    domain_concept_id integer,
    domain_id text NOT NULL,
    domain_name text NOT NULL,
    CONSTRAINT chk_domain_domain_id CHECK ((length(domain_id) <= 20)),
    CONSTRAINT chk_domain_domain_name CHECK ((length(domain_name) <= 255))
);


ALTER TABLE vocabularies.domain OWNER TO postgres;


COMMENT ON TABLE vocabularies.domain IS 'The DOMAIN table includes a list of OMOP-defined Domains the Concepts of the Standardized Vocabularies can belong to. A Domain defines the set of allowable Concepts for the standardized fields in the CDM tables. For example, the "Condition" Domain contains Concepts that describe a condition of a patient, and these Concepts can only be stored in the condition_concept_id field of the [CONDITION_OCCURRENCE](https://github.com/OHDSI/CommonDataModel/wiki/CONDITION_OCCURRENCE) and [CONDITION_ERA](https://github.com/OHDSI/CommonDataModel/wiki/CONDITION_ERA) tables. This reference table is populated with a single record for each Domain and includes a descriptive name for the Domain.';



COMMENT ON COLUMN vocabularies.domain.domain_concept_id IS 'A foreign key that refers to an identifier in the [CONCEPT](https://github.com/OHDSI/CommonDataModel/wiki/CONCEPT) table for the unique Domain Concept the Domain record belongs to.';



COMMENT ON COLUMN vocabularies.domain.domain_id IS 'A unique key for each domain.';



COMMENT ON COLUMN vocabularies.domain.domain_name IS 'The name describing the Domain, e.g. "Condition", "Procedure", "Measurement" etc.';



CREATE TABLE vocabularies.drug_strength (
    drug_concept_id integer NOT NULL,
    ingredient_concept_id integer NOT NULL,
    valid_start_date date NOT NULL,
    valid_end_date date NOT NULL,
    amount_unit_concept_id integer,
    numerator_unit_concept_id integer,
    denominator_unit_concept_id integer,
    box_size integer,
    amount_value numeric,
    numerator_value numeric,
    denominator_value numeric,
    invalid_reason text,
    CONSTRAINT chk_drug_strength_invalid_reason CHECK ((COALESCE(length(invalid_reason), 0) <= 1))
);


ALTER TABLE vocabularies.drug_strength OWNER TO postgres;


COMMENT ON TABLE vocabularies.drug_strength IS 'The DRUG_STRENGTH table contains structured content about the amount or concentration and associated units of a specific ingredient contained within a particular drug product. This table is supplemental information to support standardized analysis of drug utilization.';



COMMENT ON COLUMN vocabularies.drug_strength.drug_concept_id IS 'A foreign key to the Concept in the CONCEPT table representing the identifier for Branded Drug or Clinical Drug Concept.';



COMMENT ON COLUMN vocabularies.drug_strength.ingredient_concept_id IS 'A foreign key to the Concept in the CONCEPT table, representing the identifier for drug Ingredient Concept contained within the drug product.';



COMMENT ON COLUMN vocabularies.drug_strength.valid_start_date IS 'The date when the Concept was first recorded. The default value is 1-Jan-1970.';



COMMENT ON COLUMN vocabularies.drug_strength.valid_end_date IS 'The date when the concept became invalid because it was deleted or superseded (updated) by a new Concept. The default value is 31-Dec-2099.';



COMMENT ON COLUMN vocabularies.drug_strength.amount_unit_concept_id IS 'A foreign key to the Concept in the CONCEPT table representing the identifier for the Unit for the absolute amount of active ingredient.';



COMMENT ON COLUMN vocabularies.drug_strength.numerator_unit_concept_id IS 'A foreign key to the Concept in the CONCEPT table representing the identifier for the numerator Unit for the concentration of active ingredient.';



COMMENT ON COLUMN vocabularies.drug_strength.denominator_unit_concept_id IS 'A foreign key to the Concept in the CONCEPT table representing the identifier for the denominator Unit for the concentration of active ingredient.';



COMMENT ON COLUMN vocabularies.drug_strength.box_size IS 'The number of units of Clinical of Branded Drug, or Quantified Clinical or Branded Drug contained in a box as dispensed to the patient';



COMMENT ON COLUMN vocabularies.drug_strength.amount_value IS 'The numeric value associated with the amount of active ingredient contained within the product.';



COMMENT ON COLUMN vocabularies.drug_strength.numerator_value IS 'The numeric value associated with the concentration of the active ingredient contained in the product';



COMMENT ON COLUMN vocabularies.drug_strength.denominator_value IS 'The amount of total liquid (or other divisible product, such as ointment, gel, spray, etc.).';



COMMENT ON COLUMN vocabularies.drug_strength.invalid_reason IS 'Reason the concept was invalidated. Possible values are ''D'' (deleted), ''U'' (replaced with an update) or NULL when valid_end_date has the default value.';



CREATE TABLE vocabularies.relationship (
    relationship_concept_id integer NOT NULL,
    relationship_id text NOT NULL,
    relationship_name text NOT NULL,
    is_hierarchical text NOT NULL,
    defines_ancestry text NOT NULL,
    reverse_relationship_id text NOT NULL,
    CONSTRAINT chk_relationship_defines_ancestry CHECK ((length(defines_ancestry) <= 1)),
    CONSTRAINT chk_relationship_is_hierachical CHECK ((length(is_hierarchical) <= 1)),
    CONSTRAINT chk_relationship_relationship_id CHECK ((length(relationship_id) <= 20)),
    CONSTRAINT chk_relationship_relationship_name CHECK ((length(relationship_name) <= 255)),
    CONSTRAINT chk_relationship_reverse_relationship_id CHECK ((length(reverse_relationship_id) <= 20))
);


ALTER TABLE vocabularies.relationship OWNER TO postgres;


COMMENT ON TABLE vocabularies.relationship IS 'The RELATIONSHIP table provides a reference list of all types of relationships that can be used to associate any two concepts in the CONCEPT_RELATIONSHP table.';



COMMENT ON COLUMN vocabularies.relationship.relationship_concept_id IS 'A foreign key that refers to an identifier in the CONCEPT table for the unique relationship concept.';



COMMENT ON COLUMN vocabularies.relationship.relationship_id IS 'The type of relationship captured by the relationship record.';



COMMENT ON COLUMN vocabularies.relationship.relationship_name IS 'The text that describes the relationship type.';



COMMENT ON COLUMN vocabularies.relationship.is_hierarchical IS 'Defines whether a relationship defines concepts into classes or hierarchies. Values are 1 for hierarchical relationship or 0 if not.';



COMMENT ON COLUMN vocabularies.relationship.defines_ancestry IS 'Defines whether a hierarchical relationship contributes to the concept_ancestor table. These are subsets of the hierarchical relationships. Valid values are 1 or 0.';



COMMENT ON COLUMN vocabularies.relationship.reverse_relationship_id IS 'The identifier for the relationship used to define the reverse relationship between two concepts.';



CREATE TABLE vocabularies.source_to_concept_map (
    source_concept_id integer NOT NULL,
    target_concept_id integer NOT NULL,
    valid_start_date date NOT NULL,
    valid_end_date date NOT NULL,
    source_code text NOT NULL,
    source_vocabulary_id text NOT NULL,
    target_vocabulary_id text NOT NULL,
    source_code_description text,
    invalid_reason text,
    CONSTRAINT chk_source_to_concept_map_invalid_reason CHECK ((COALESCE(length(invalid_reason), 0) <= 1)),
    CONSTRAINT chk_source_to_concept_map_source_code CHECK ((length(source_code) <= 50)),
    CONSTRAINT chk_source_to_concept_map_source_code_description CHECK ((COALESCE(length(source_code_description), 0) <= 255)),
    CONSTRAINT chk_source_to_concept_map_source_vocabulary_id CHECK ((length(source_vocabulary_id) <= 20)),
    CONSTRAINT chk_source_to_concept_map_target_vocabulary_id CHECK ((length(target_vocabulary_id) <= 20))
);


ALTER TABLE vocabularies.source_to_concept_map OWNER TO postgres;


COMMENT ON TABLE vocabularies.source_to_concept_map IS 'The source to concept map table is a legacy data structure within the OMOP Common Data Model, recommended for use in ETL processes to maintain local source codes which are not available as Concepts in the Standardized Vocabularies, and to establish mappings for each source code into a Standard Concept as target_concept_ids that can be used to populate the Common Data Model tables. The SOURCE_TO_CONCEPT_MAP table is no longer populated with content within the Standardized Vocabularies published to the OMOP community.';



COMMENT ON COLUMN vocabularies.source_to_concept_map.source_concept_id IS 'A foreign key to the Source Concept that is being translated into a Standard Concept.';



COMMENT ON COLUMN vocabularies.source_to_concept_map.target_concept_id IS 'A foreign key to the target Concept to which the source code is being mapped.';



COMMENT ON COLUMN vocabularies.source_to_concept_map.valid_start_date IS 'The date when the mapping instance was first recorded.';



COMMENT ON COLUMN vocabularies.source_to_concept_map.valid_end_date IS 'The date when the mapping instance became invalid because it was deleted or superseded (updated) by a new relationship. Default value is 31-Dec-2099.';



COMMENT ON COLUMN vocabularies.source_to_concept_map.source_code IS 'The source code being translated into a Standard Concept.';



COMMENT ON COLUMN vocabularies.source_to_concept_map.source_vocabulary_id IS 'A foreign key to the VOCABULARY table defining the vocabulary of the source code that is being translated to a Standard Concept.';



COMMENT ON COLUMN vocabularies.source_to_concept_map.target_vocabulary_id IS 'A foreign key to the VOCABULARY table defining the vocabulary of the target Concept.';



COMMENT ON COLUMN vocabularies.source_to_concept_map.source_code_description IS 'An optional description for the source code. This is included as a convenience to compare the description of the source code to the name of the concept.';



COMMENT ON COLUMN vocabularies.source_to_concept_map.invalid_reason IS 'Reason the mapping instance was invalidated. Possible values are D (deleted), U (replaced with an update) or NULL when valid_end_date has the default value.';



CREATE TABLE vocabularies.source_to_standard_vocab_map (
    source_concept_id integer,
    target_concept_id integer,
    source_valid_start_date date,
    source_valid_end_date date,
    source_code text,
    source_code_description text,
    source_vocabulary_id text,
    source_domain_id text,
    source_concept_class_id text,
    source_invalid_reason text,
    target_concept_name text,
    target_vocabulary_id text,
    target_domain_id text,
    target_concept_class_id text,
    target_invalid_reason text,
    target_standard_concept text
);


ALTER TABLE vocabularies.source_to_standard_vocab_map OWNER TO postgres;


CREATE TABLE vocabularies.vocabulary (
    vocabulary_concept_id integer NOT NULL,
    vocabulary_id text NOT NULL,
    vocabulary_name text NOT NULL,
    vocabulary_reference text,
    vocabulary_version text,
    CONSTRAINT chk_vocabulary_vocabulary_id CHECK ((length(vocabulary_id) <= 20)),
    CONSTRAINT chk_vocabulary_vocabulary_name CHECK ((length(vocabulary_name) <= 255)),
    CONSTRAINT chk_vocabulary_vocabulary_reference CHECK ((length(vocabulary_reference) <= 255)),
    CONSTRAINT chk_vocabulary_vocabulary_version CHECK ((length(vocabulary_version) <= 255))
);


ALTER TABLE vocabularies.vocabulary OWNER TO postgres;


COMMENT ON TABLE vocabularies.vocabulary IS 'The VOCABULARY table includes a list of the Vocabularies collected from various sources or created de novo by the OMOP community. This reference table is populated with a single record for each Vocabulary source and includes a descriptive name and other associated attributes for the Vocabulary.';



COMMENT ON COLUMN vocabularies.vocabulary.vocabulary_concept_id IS 'A foreign key that refers to a standard concept identifier in the CONCEPT table for the Vocabulary the VOCABULARY record belongs to.';



COMMENT ON COLUMN vocabularies.vocabulary.vocabulary_id IS 'A unique identifier for each Vocabulary, such as ICD9CM, SNOMED, Visit.';



COMMENT ON COLUMN vocabularies.vocabulary.vocabulary_name IS 'The name describing the vocabulary, for example "International Classification of Diseases, Ninth Revision, Clinical Modification, Volume 1 and 2 (NCHS)" etc.';



COMMENT ON COLUMN vocabularies.vocabulary.vocabulary_reference IS 'External reference to documentation or available download of the about the vocabulary.';



COMMENT ON COLUMN vocabularies.vocabulary.vocabulary_version IS 'Version of the Vocabulary as indicated in the source.';



ALTER TABLE ONLY cdm.note_nlp ALTER COLUMN note_nlp_id SET DEFAULT nextval('cdm.note_nlp_note_nlp_id_seq'::regclass);



ALTER TABLE ONLY cdm.artifactdeployment
    ADD CONSTRAINT artdefpk PRIMARY KEY (artifactpath, objectname);



ALTER TABLE ONLY cdm.artifactexecution
    ADD CONSTRAINT depl_exec_pk PRIMARY KEY (id);



ALTER TABLE ONLY cdm.care_site
    ADD CONSTRAINT xpk_care_site_id PRIMARY KEY (care_site_id);



ALTER TABLE ONLY cdm.care_site_specialty
    ADD CONSTRAINT xpk_care_site_specialty_id PRIMARY KEY (care_site_id);



ALTER TABLE ONLY cdm.cohort_definition
    ADD CONSTRAINT xpk_cohort_definition_id PRIMARY KEY (cohort_definition_id);



ALTER TABLE ONLY cdm.cohort
    ADD CONSTRAINT xpk_cohort_id PRIMARY KEY (cohort_definition_id, subject_id, cohort_start_date, cohort_end_date);



ALTER TABLE ONLY cdm.condition_era
    ADD CONSTRAINT xpk_condition_era_id PRIMARY KEY (condition_era_id);



ALTER TABLE ONLY cdm.condition_occurrence
    ADD CONSTRAINT xpk_condition_occurrence_id PRIMARY KEY (condition_occurrence_id);



ALTER TABLE ONLY cdm.cost
    ADD CONSTRAINT xpk_cost_id PRIMARY KEY (cost_id);



ALTER TABLE ONLY cdm.death
    ADD CONSTRAINT xpk_death_id PRIMARY KEY (person_id);



ALTER TABLE ONLY cdm.device_exposure
    ADD CONSTRAINT xpk_device_exposure_id PRIMARY KEY (device_exposure_id);



ALTER TABLE ONLY cdm.dose_era
    ADD CONSTRAINT xpk_dose_era_id PRIMARY KEY (dose_era_id);



ALTER TABLE ONLY cdm.drug_era
    ADD CONSTRAINT xpk_drug_era_id PRIMARY KEY (drug_era_id);



ALTER TABLE ONLY cdm.drug_exposure
    ADD CONSTRAINT xpk_drug_exposure_id PRIMARY KEY (drug_exposure_id);



ALTER TABLE ONLY cdm.location_history
    ADD CONSTRAINT xpk_location_history_id PRIMARY KEY (location_history_id);



ALTER TABLE ONLY cdm.location
    ADD CONSTRAINT xpk_location_id PRIMARY KEY (location_id);



ALTER TABLE ONLY cdm.measurement
    ADD CONSTRAINT xpk_measurement_id PRIMARY KEY (measurement_id);



ALTER TABLE ONLY cdm.note
    ADD CONSTRAINT xpk_note_id PRIMARY KEY (note_id);



ALTER TABLE ONLY cdm.note_nlp
    ADD CONSTRAINT xpk_note_nlp PRIMARY KEY (note_nlp_id);



ALTER TABLE ONLY cdm.observation
    ADD CONSTRAINT xpk_observation_id PRIMARY KEY (observation_id);



ALTER TABLE ONLY cdm.observation_period
    ADD CONSTRAINT xpk_observation_period_id PRIMARY KEY (observation_period_id);



ALTER TABLE ONLY cdm.payer_plan_period
    ADD CONSTRAINT xpk_payer_plan_period_id PRIMARY KEY (payer_plan_period_id);



ALTER TABLE ONLY cdm.person
    ADD CONSTRAINT xpk_person_id PRIMARY KEY (person_id);



ALTER TABLE ONLY cdm.procedure_occurrence
    ADD CONSTRAINT xpk_procedure_occurrence_id PRIMARY KEY (procedure_occurrence_id);



ALTER TABLE ONLY cdm.provider
    ADD CONSTRAINT xpk_provider_id PRIMARY KEY (provider_id);



ALTER TABLE ONLY cdm.specimen
    ADD CONSTRAINT xpk_specimen PRIMARY KEY (specimen_id);



ALTER TABLE ONLY cdm.survey_conduct
    ADD CONSTRAINT xpk_survey_conduct_id PRIMARY KEY (survey_conduct_id);



ALTER TABLE ONLY cdm.visit_detail
    ADD CONSTRAINT xpk_visit_detail_id PRIMARY KEY (visit_detail_id);



ALTER TABLE ONLY cdm.visit_occurrence
    ADD CONSTRAINT xpk_visit_occurrence_id PRIMARY KEY (visit_occurrence_id);



ALTER TABLE ONLY vocabularies.artifactdeployment
    ADD CONSTRAINT artdefpk PRIMARY KEY (artifactpath, objectname);



ALTER TABLE ONLY vocabularies.artifactexecution
    ADD CONSTRAINT depl_exec_pk PRIMARY KEY (id);



ALTER TABLE ONLY vocabularies.concept_synonym
    ADD CONSTRAINT uq_concept_synonym UNIQUE (concept_id, concept_synonym_name, language_concept_id);



ALTER TABLE ONLY vocabularies.concept_ancestor
    ADD CONSTRAINT xpk_concept_ancestor PRIMARY KEY (ancestor_concept_id, descendant_concept_id);



ALTER TABLE ONLY vocabularies.concept_class
    ADD CONSTRAINT xpk_concept_class PRIMARY KEY (concept_class_id);



ALTER TABLE ONLY vocabularies.concept
    ADD CONSTRAINT xpk_concept_id PRIMARY KEY (concept_id);



ALTER TABLE ONLY vocabularies.concept_relationship
    ADD CONSTRAINT xpk_concept_relationship_id PRIMARY KEY (concept_id_1, concept_id_2, relationship_id);



ALTER TABLE ONLY vocabularies.domain
    ADD CONSTRAINT xpk_domain_id PRIMARY KEY (domain_id);



ALTER TABLE ONLY vocabularies.drug_strength
    ADD CONSTRAINT xpk_drug_strength PRIMARY KEY (drug_concept_id, ingredient_concept_id);



ALTER TABLE ONLY vocabularies.relationship
    ADD CONSTRAINT xpk_relationship_id PRIMARY KEY (relationship_id);



ALTER TABLE ONLY vocabularies.source_to_concept_map
    ADD CONSTRAINT xpk_source_to_concept_map_id PRIMARY KEY (source_vocabulary_id, target_concept_id, source_code, valid_end_date);



ALTER TABLE ONLY vocabularies.vocabulary
    ADD CONSTRAINT xpk_vocabulary_id PRIMARY KEY (vocabulary_id);



CREATE INDEX idx_cohort_cohort_definition_id ON cdm.cohort USING btree (cohort_definition_id);



CREATE INDEX idx_cohort_subject_id ON cdm.cohort USING btree (subject_id);



CREATE INDEX idx_condition_era_condition_concept_id ON cdm.condition_era USING btree (condition_concept_id);



CREATE INDEX idx_condition_era_person_id ON cdm.condition_era USING btree (person_id);



CREATE INDEX idx_condition_occurrence_condition_concept_id ON cdm.condition_occurrence USING btree (condition_concept_id);



CREATE INDEX idx_condition_occurrence_condition_source_concept_id ON cdm.condition_occurrence USING btree (condition_source_concept_id);



CREATE INDEX idx_condition_occurrence_condition_start_datetime ON cdm.condition_occurrence USING btree (condition_start_datetime);



CREATE INDEX idx_condition_occurrence_condition_status_concept_id ON cdm.condition_occurrence USING btree (condition_status_concept_id);



CREATE INDEX idx_condition_occurrence_condition_type_concept_id ON cdm.condition_occurrence USING btree (condition_type_concept_id);



CREATE INDEX idx_condition_occurrence_person_id ON cdm.condition_occurrence USING btree (person_id);



CREATE INDEX idx_condition_occurrence_visit_detail_id ON cdm.condition_occurrence USING btree (visit_detail_id);



CREATE INDEX idx_condition_occurrence_visit_occurrence_id ON cdm.condition_occurrence USING btree (visit_occurrence_id);



CREATE INDEX idx_device_exposure_device_concept_id ON cdm.device_exposure USING btree (device_concept_id);



CREATE INDEX idx_device_exposure_device_exposure_start_datetime ON cdm.device_exposure USING btree (device_exposure_start_datetime);



CREATE INDEX idx_device_exposure_person_id ON cdm.device_exposure USING btree (person_id);



CREATE INDEX idx_device_exposure_visit_detail_id ON cdm.device_exposure USING btree (visit_detail_id);



CREATE INDEX idx_device_exposure_visit_occurrence_id ON cdm.device_exposure USING btree (visit_occurrence_id);



CREATE INDEX idx_dose_era_dose_era_start_datetime ON cdm.dose_era USING btree (dose_era_start_datetime);



CREATE INDEX idx_dose_era_drug_concept_id ON cdm.dose_era USING btree (drug_concept_id);



CREATE INDEX idx_dose_era_person_id ON cdm.dose_era USING btree (person_id);



CREATE INDEX idx_drug_era_drug_concept_id ON cdm.drug_era USING btree (drug_concept_id);



CREATE INDEX idx_drug_era_person_id ON cdm.drug_era USING btree (person_id);



CREATE INDEX idx_drug_exposure_drug_concept_id ON cdm.drug_exposure USING btree (drug_concept_id);



CREATE INDEX idx_drug_exposure_drug_exposure_start_datetime ON cdm.drug_exposure USING btree (drug_exposure_start_datetime);



CREATE INDEX idx_drug_exposure_drug_source_concept_id ON cdm.drug_exposure USING btree (drug_source_concept_id);



CREATE INDEX idx_drug_exposure_person_id ON cdm.drug_exposure USING btree (person_id);



CREATE INDEX idx_drug_exposure_route_concept_id ON cdm.drug_exposure USING btree (route_concept_id);



CREATE INDEX idx_drug_exposure_visit_occurrence_id ON cdm.drug_exposure USING btree (visit_occurrence_id);



CREATE INDEX idx_episode_episode_start_datetime ON cdm.episode USING btree (episode_start_datetime);



CREATE INDEX idx_fact_relationship_domain_concept_id_1 ON cdm.fact_relationship USING btree (domain_concept_id_1);



CREATE INDEX idx_fact_relationship_domain_concept_id_2 ON cdm.fact_relationship USING btree (domain_concept_id_2);



CREATE INDEX idx_fact_relationship_relationship_concept_id ON cdm.fact_relationship USING btree (relationship_concept_id);



CREATE INDEX idx_measurement_measurement_concept_id ON cdm.measurement USING btree (measurement_concept_id);



CREATE INDEX idx_measurement_measurement_date ON cdm.measurement USING btree (measurement_date);



CREATE INDEX idx_measurement_measurement_datetime ON cdm.measurement USING btree (measurement_datetime);



CREATE INDEX idx_measurement_measurement_source_concept_id ON cdm.measurement USING btree (measurement_source_concept_id);



CREATE INDEX idx_measurement_person_id ON cdm.measurement USING btree (person_id);



CREATE INDEX idx_measurement_unit_concept_id ON cdm.measurement USING btree (unit_concept_id);



CREATE INDEX idx_measurement_value_as_concept_id ON cdm.measurement USING btree (value_as_concept_id);



CREATE INDEX idx_measurement_visit_occurrence_id ON cdm.measurement USING btree (visit_occurrence_id);



CREATE INDEX idx_note_encoding_concept_id ON cdm.note USING btree (encoding_concept_id);



CREATE INDEX idx_note_language_concept_id ON cdm.note USING btree (language_concept_id);



CREATE INDEX idx_note_nlp_concept_id ON cdm.note_nlp USING btree (note_nlp_concept_id);



CREATE INDEX idx_note_nlp_note_id ON cdm.note_nlp USING btree (note_id);



CREATE INDEX idx_note_note_class_concept_id ON cdm.note USING btree (note_class_concept_id);



CREATE INDEX idx_note_note_datetime ON cdm.note USING btree (note_datetime);



CREATE INDEX idx_note_note_event_field_concept_id ON cdm.note USING btree (note_event_field_concept_id);



CREATE INDEX idx_note_note_event_id ON cdm.note USING btree (note_event_id);



CREATE INDEX idx_note_note_type_concept_id ON cdm.note USING btree (note_type_concept_id);



CREATE INDEX idx_note_person_id ON cdm.note USING btree (person_id);



CREATE INDEX idx_note_visit_detail_id ON cdm.note USING btree (visit_detail_id);



CREATE INDEX idx_note_visit_occurrence_id ON cdm.note USING btree (visit_occurrence_id);



CREATE INDEX idx_observation_obs_event_field_concept_id ON cdm.observation USING btree (obs_event_field_concept_id);



CREATE INDEX idx_observation_observation_concept_id ON cdm.observation USING btree (observation_concept_id);



CREATE INDEX idx_observation_observation_datetime ON cdm.observation USING btree (observation_datetime);



CREATE INDEX idx_observation_observation_type_concept_id ON cdm.observation USING btree (observation_type_concept_id);



CREATE INDEX idx_observation_period_person_id ON cdm.observation_period USING btree (person_id);



CREATE INDEX idx_observation_period_start_date_person_id ON cdm.observation_period USING btree (observation_period_start_date, person_id);



CREATE INDEX idx_observation_person_id ON cdm.observation USING btree (person_id);



CREATE INDEX idx_observation_qualifier_concept_id ON cdm.observation USING btree (qualifier_concept_id);



CREATE INDEX idx_observation_unit_concept_id ON cdm.observation USING btree (unit_concept_id);



CREATE INDEX idx_observation_value_as_concept_id ON cdm.observation USING btree (value_as_concept_id);



CREATE INDEX idx_observation_visit_detail_id ON cdm.observation USING btree (visit_detail_id);



CREATE INDEX idx_observation_visit_occurrence_id ON cdm.observation USING btree (visit_occurrence_id);



CREATE INDEX idx_person_birth_datetime ON cdm.person USING btree (birth_datetime);



CREATE INDEX idx_person_ethnicity_concept_id ON cdm.person USING btree (ethnicity_concept_id);



CREATE INDEX idx_person_ethnicity_source_concept_id ON cdm.person USING btree (ethnicity_source_concept_id);



CREATE INDEX idx_person_gender_concept_id ON cdm.person USING btree (gender_concept_id);



CREATE INDEX idx_person_gender_source_concept_id ON cdm.person USING btree (gender_source_concept_id);



CREATE INDEX idx_person_race_concept_id ON cdm.person USING btree (race_concept_id);



CREATE INDEX idx_person_race_source_concept_id ON cdm.person USING btree (race_source_concept_id);



CREATE INDEX idx_procedure_occurrence_modifier_concept_id ON cdm.procedure_occurrence USING btree (modifier_concept_id);



CREATE INDEX idx_procedure_occurrence_person_id ON cdm.procedure_occurrence USING btree (person_id);



CREATE INDEX idx_procedure_occurrence_procedure_concept_id ON cdm.procedure_occurrence USING btree (procedure_concept_id);



CREATE INDEX idx_procedure_occurrence_procedure_datetime ON cdm.procedure_occurrence USING btree (procedure_datetime);



CREATE INDEX idx_procedure_occurrence_procedure_source_concept_id ON cdm.procedure_occurrence USING btree (procedure_source_concept_id);



CREATE INDEX idx_procedure_occurrence_procedure_type_concept_id ON cdm.procedure_occurrence USING btree (procedure_type_concept_id);



CREATE INDEX idx_procedure_occurrence_visit_detail_id ON cdm.procedure_occurrence USING btree (visit_detail_id);



CREATE INDEX idx_procedure_occurrence_visit_occurrence_id ON cdm.procedure_occurrence USING btree (visit_occurrence_id);



CREATE INDEX idx_source_vocab_map_source_code ON cdm.source_to_source_vocab_map USING btree (source_code);



CREATE INDEX idx_source_vocab_map_source_vocab_id ON cdm.source_to_source_vocab_map USING btree (source_vocabulary_id);



CREATE INDEX idx_specimen_specimen_datetime ON cdm.specimen USING btree (specimen_datetime);



CREATE INDEX idx_visit_detail_care_site_id ON cdm.visit_detail USING btree (care_site_id);



CREATE INDEX idx_visit_detail_discharged_to_concept_id ON cdm.visit_detail USING btree (discharged_to_concept_id);



CREATE INDEX idx_visit_detail_parent_visit_detail_id ON cdm.visit_detail USING btree (parent_visit_detail_id);



CREATE INDEX idx_visit_detail_person_id ON cdm.visit_detail USING btree (person_id);



CREATE INDEX idx_visit_detail_preceding_visit_detail_id ON cdm.visit_detail USING btree (preceding_visit_detail_id);



CREATE INDEX idx_visit_detail_visit_detail_concept_id ON cdm.visit_detail USING btree (visit_detail_concept_id);



CREATE INDEX idx_visit_detail_visit_detail_source_concept_id ON cdm.visit_detail USING btree (visit_detail_source_concept_id);



CREATE INDEX idx_visit_detail_visit_detail_start_datetime ON cdm.visit_detail USING btree (visit_detail_start_datetime);



CREATE INDEX idx_visit_detail_visit_detail_type_concept_id ON cdm.visit_detail USING btree (visit_detail_type_concept_id);



CREATE INDEX idx_visit_detail_visit_occurrence_id ON cdm.visit_detail USING btree (visit_occurrence_id);



CREATE INDEX idx_visit_occurrence_care_site_id ON cdm.visit_occurrence USING btree (care_site_id);



CREATE INDEX idx_visit_occurrence_discharged_to_concept_id ON cdm.visit_occurrence USING btree (discharged_to_concept_id);



CREATE INDEX idx_visit_occurrence_person_id ON cdm.visit_occurrence USING btree (person_id);



CREATE INDEX idx_visit_occurrence_preceding_visit_occurrence_id ON cdm.visit_occurrence USING btree (preceding_visit_occurrence_id);



CREATE INDEX idx_visit_occurrence_visit_concept_id ON cdm.visit_occurrence USING btree (visit_concept_id);



CREATE INDEX idx_visit_occurrence_visit_source_concept_id ON cdm.visit_occurrence USING btree (visit_source_concept_id);



CREATE INDEX idx_visit_occurrence_visit_start_datetime ON cdm.visit_occurrence USING btree (visit_start_datetime);



CREATE INDEX idx_visit_occurrence_visit_type_concept_id ON cdm.visit_occurrence USING btree (visit_type_concept_id);



CREATE INDEX idx_vocab_map_source_code ON cdm.source_to_standard_vocab_map USING btree (source_code);



CREATE INDEX idx_vocab_map_source_vocab_id ON cdm.source_to_standard_vocab_map USING btree (source_vocabulary_id);



CREATE INDEX trgm_note_note_text ON cdm.note USING gin (note_text public.gin_trgm_ops);



CREATE INDEX idx_ar_aid ON results.achilles_results USING btree (analysis_id);



CREATE INDEX idx_ar_aid_s1 ON results.achilles_results USING btree (analysis_id, stratum_1);



CREATE INDEX idx_ar_aid_s1234 ON results.achilles_results USING btree (analysis_id, stratum_1, stratum_2, stratum_3, stratum_4);



CREATE INDEX idx_ar_s1 ON results.achilles_results USING btree (stratum_1);



CREATE INDEX idx_ar_s2 ON results.achilles_results USING btree (stratum_2);



CREATE INDEX idx_ard_aid ON results.achilles_results_dist USING btree (analysis_id);



CREATE INDEX idx_ard_s1 ON results.achilles_results_dist USING btree (stratum_1);



CREATE INDEX idx_ard_s2 ON results.achilles_results_dist USING btree (stratum_2);



CREATE INDEX idx_concept_ancestor_descendant_concept_id ON vocabularies.concept_ancestor USING btree (descendant_concept_id);



CREATE INDEX idx_concept_concept_code ON vocabularies.concept USING btree (concept_code);



CREATE INDEX idx_concept_concept_name ON vocabularies.concept USING btree (concept_name);



CREATE INDEX idx_concept_relationship_concept_id_2 ON vocabularies.concept_relationship USING btree (concept_id_2);



CREATE INDEX idx_concept_synonym_concept_id ON vocabularies.concept_synonym USING btree (concept_id);



CREATE INDEX idx_drug_strength_amount_unit_concept_id ON vocabularies.drug_strength USING btree (amount_unit_concept_id);



CREATE INDEX idx_drug_strength_denominator_unit_concept_id ON vocabularies.drug_strength USING btree (denominator_unit_concept_id);



CREATE INDEX idx_drug_strength_ingredient_concept_id ON vocabularies.drug_strength USING btree (ingredient_concept_id);



CREATE INDEX idx_drug_strength_numerator_unit_concept_id ON vocabularies.drug_strength USING btree (numerator_unit_concept_id);



CREATE INDEX source_to_standard_vocab_map_source_code_idx ON vocabularies.source_to_standard_vocab_map USING btree (source_code);



CREATE INDEX source_to_standard_vocab_map_target_concept_id_idx ON vocabularies.source_to_standard_vocab_map USING btree (target_concept_id);



CREATE INDEX trgm_concept_concept_name ON vocabularies.concept USING gin (concept_name public.gin_trgm_ops);



ALTER TABLE ONLY cdm.care_site_specialty
    ADD CONSTRAINT care_site_specialty_care_site_id_fkey FOREIGN KEY (care_site_id) REFERENCES cdm.care_site(care_site_id) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.care_site_specialty
    ADD CONSTRAINT care_site_specialty_specialty_concept_id_fkey FOREIGN KEY (specialty_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.drug_exposure
    ADD CONSTRAINT drug_exposure_visit_detail_id_fkey FOREIGN KEY (visit_detail_id) REFERENCES cdm.visit_detail(visit_detail_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.drug_exposure
    ADD CONSTRAINT drug_exposure_visit_occurrence_id_fkey FOREIGN KEY (visit_occurrence_id) REFERENCES cdm.visit_occurrence(visit_occurrence_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.cohort
    ADD CONSTRAINT fpk_cohort_cohort_definition_id FOREIGN KEY (cohort_definition_id) REFERENCES cdm.cohort_definition(cohort_definition_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.cohort_definition
    ADD CONSTRAINT fpk_cohort_definition_definition_type_concept_id FOREIGN KEY (definition_type_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.cohort_definition
    ADD CONSTRAINT fpk_cohort_definition_subject_concept_id FOREIGN KEY (subject_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.condition_era
    ADD CONSTRAINT fpk_condition_era_condition_concept_id FOREIGN KEY (condition_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.condition_era
    ADD CONSTRAINT fpk_condition_era_person_id FOREIGN KEY (person_id) REFERENCES cdm.person(person_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.condition_occurrence
    ADD CONSTRAINT fpk_condition_occurrence_condition_concept_id FOREIGN KEY (condition_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.condition_occurrence
    ADD CONSTRAINT fpk_condition_occurrence_condition_source_concept_id FOREIGN KEY (condition_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.condition_occurrence
    ADD CONSTRAINT fpk_condition_occurrence_condition_status_concept_id FOREIGN KEY (condition_status_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.condition_occurrence
    ADD CONSTRAINT fpk_condition_occurrence_condition_type_concept_id FOREIGN KEY (condition_type_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.condition_occurrence
    ADD CONSTRAINT fpk_condition_occurrence_person_id FOREIGN KEY (person_id) REFERENCES cdm.person(person_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.condition_occurrence
    ADD CONSTRAINT fpk_condition_occurrence_provider_id FOREIGN KEY (provider_id) REFERENCES cdm.provider(provider_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.condition_occurrence
    ADD CONSTRAINT fpk_condition_occurrence_visit_detail_id FOREIGN KEY (visit_detail_id) REFERENCES cdm.visit_detail(visit_detail_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.condition_occurrence
    ADD CONSTRAINT fpk_condition_occurrence_visit_occurrence_id FOREIGN KEY (visit_occurrence_id) REFERENCES cdm.visit_occurrence(visit_occurrence_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.cost
    ADD CONSTRAINT fpk_cost_cost_type_concept_id FOREIGN KEY (cost_type_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.cost
    ADD CONSTRAINT fpk_cost_currency_concept_id FOREIGN KEY (currency_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.cost
    ADD CONSTRAINT fpk_cost_drg_concept_id FOREIGN KEY (drg_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.cost
    ADD CONSTRAINT fpk_cost_payer_plan_period_id FOREIGN KEY (payer_plan_period_id) REFERENCES cdm.payer_plan_period(payer_plan_period_id) DEFERRABLE;



ALTER TABLE ONLY cdm.cost
    ADD CONSTRAINT fpk_cost_revenue_code_concept_id FOREIGN KEY (revenue_code_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.death
    ADD CONSTRAINT fpk_death_cause_concept_id FOREIGN KEY (cause_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.death
    ADD CONSTRAINT fpk_death_cause_source_concept_id FOREIGN KEY (cause_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.death
    ADD CONSTRAINT fpk_death_death_type_concept FOREIGN KEY (death_type_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.death
    ADD CONSTRAINT fpk_death_person_id FOREIGN KEY (person_id) REFERENCES cdm.person(person_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.device_exposure
    ADD CONSTRAINT fpk_device_exposure_device_concept_id FOREIGN KEY (device_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.device_exposure
    ADD CONSTRAINT fpk_device_exposure_device_source_concept_id FOREIGN KEY (device_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.device_exposure
    ADD CONSTRAINT fpk_device_exposure_device_type_concept_id FOREIGN KEY (device_type_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.device_exposure
    ADD CONSTRAINT fpk_device_exposure_person_id FOREIGN KEY (person_id) REFERENCES cdm.person(person_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.device_exposure
    ADD CONSTRAINT fpk_device_exposure_provider_id FOREIGN KEY (provider_id) REFERENCES cdm.provider(provider_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.device_exposure
    ADD CONSTRAINT fpk_device_exposure_visit_detail_id FOREIGN KEY (visit_detail_id) REFERENCES cdm.visit_detail(visit_detail_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.device_exposure
    ADD CONSTRAINT fpk_device_exposure_visit_occurrence_id FOREIGN KEY (visit_occurrence_id) REFERENCES cdm.visit_occurrence(visit_occurrence_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.dose_era
    ADD CONSTRAINT fpk_dose_era_drug_concept_id FOREIGN KEY (drug_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.dose_era
    ADD CONSTRAINT fpk_dose_era_person_id FOREIGN KEY (person_id) REFERENCES cdm.person(person_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.dose_era
    ADD CONSTRAINT fpk_dose_era_unit_concept_id FOREIGN KEY (unit_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.drug_era
    ADD CONSTRAINT fpk_drug_era_drug_concept_id FOREIGN KEY (drug_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.drug_era
    ADD CONSTRAINT fpk_drug_era_person_id FOREIGN KEY (person_id) REFERENCES cdm.person(person_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.drug_exposure
    ADD CONSTRAINT fpk_drug_exposure_drug_concept_id FOREIGN KEY (drug_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.drug_exposure
    ADD CONSTRAINT fpk_drug_exposure_drug_source_concept_id FOREIGN KEY (drug_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.drug_exposure
    ADD CONSTRAINT fpk_drug_exposure_drug_type_concept_id FOREIGN KEY (drug_type_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.drug_exposure
    ADD CONSTRAINT fpk_drug_exposure_person_id FOREIGN KEY (person_id) REFERENCES cdm.person(person_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.drug_exposure
    ADD CONSTRAINT fpk_drug_exposure_provider_id FOREIGN KEY (provider_id) REFERENCES cdm.provider(provider_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.drug_exposure
    ADD CONSTRAINT fpk_drug_exposure_route_concept_id FOREIGN KEY (route_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.fact_relationship
    ADD CONSTRAINT fpk_fact_relationship_domain_concept_id_1 FOREIGN KEY (domain_concept_id_1) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.fact_relationship
    ADD CONSTRAINT fpk_fact_relationship_domain_concept_id_2 FOREIGN KEY (domain_concept_id_2) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.fact_relationship
    ADD CONSTRAINT fpk_fact_relationship_relationship_concept_id FOREIGN KEY (relationship_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.location_history
    ADD CONSTRAINT fpk_location_history_relationship_type_concept_id FOREIGN KEY (relationship_type_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.care_site
    ADD CONSTRAINT fpk_location_id FOREIGN KEY (location_id) REFERENCES cdm.location(location_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.measurement
    ADD CONSTRAINT fpk_measurement_measurement_concept_id FOREIGN KEY (measurement_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.measurement
    ADD CONSTRAINT fpk_measurement_measurement_source_concept_id FOREIGN KEY (measurement_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.measurement
    ADD CONSTRAINT fpk_measurement_measurement_type_concept_id FOREIGN KEY (measurement_type_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.measurement
    ADD CONSTRAINT fpk_measurement_operator_concept_id FOREIGN KEY (operator_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.measurement
    ADD CONSTRAINT fpk_measurement_person_id FOREIGN KEY (person_id) REFERENCES cdm.person(person_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.measurement
    ADD CONSTRAINT fpk_measurement_provider_id FOREIGN KEY (provider_id) REFERENCES cdm.provider(provider_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.measurement
    ADD CONSTRAINT fpk_measurement_unit_concept_id FOREIGN KEY (unit_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.measurement
    ADD CONSTRAINT fpk_measurement_value_as_concept_id FOREIGN KEY (value_as_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.metadata
    ADD CONSTRAINT fpk_metadata_metadata_concept_id FOREIGN KEY (metadata_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.metadata
    ADD CONSTRAINT fpk_metadata_metadata_type_concept FOREIGN KEY (metadata_type_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.note
    ADD CONSTRAINT fpk_note_encoding_concept_id FOREIGN KEY (encoding_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.note
    ADD CONSTRAINT fpk_note_language_concept_id FOREIGN KEY (language_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.note_nlp
    ADD CONSTRAINT fpk_note_nlp_concept FOREIGN KEY (note_nlp_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.note_nlp
    ADD CONSTRAINT fpk_note_nlp_concept_s FOREIGN KEY (note_nlp_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.note_nlp
    ADD CONSTRAINT fpk_note_nlp_note FOREIGN KEY (note_id) REFERENCES cdm.note(note_id) DEFERRABLE;



ALTER TABLE ONLY cdm.note_nlp
    ADD CONSTRAINT fpk_note_nlp_section_concept FOREIGN KEY (section_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.note
    ADD CONSTRAINT fpk_note_note_class_concept_id FOREIGN KEY (note_class_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.note
    ADD CONSTRAINT fpk_note_note_event_field_concept_id FOREIGN KEY (note_event_field_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.note
    ADD CONSTRAINT fpk_note_note_type_concept_id FOREIGN KEY (note_type_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.note
    ADD CONSTRAINT fpk_note_person_id FOREIGN KEY (person_id) REFERENCES cdm.person(person_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.note
    ADD CONSTRAINT fpk_note_provider_id FOREIGN KEY (provider_id) REFERENCES cdm.provider(provider_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.observation
    ADD CONSTRAINT fpk_observation_obs_event_field_concept_id FOREIGN KEY (obs_event_field_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.observation
    ADD CONSTRAINT fpk_observation_observation_concept_id FOREIGN KEY (observation_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.observation
    ADD CONSTRAINT fpk_observation_observation_source_concept_id FOREIGN KEY (observation_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.observation
    ADD CONSTRAINT fpk_observation_observation_type_concept_id FOREIGN KEY (observation_type_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.observation_period
    ADD CONSTRAINT fpk_observation_period_period_type_concept_id FOREIGN KEY (period_type_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.observation_period
    ADD CONSTRAINT fpk_observation_period_person_id FOREIGN KEY (person_id) REFERENCES cdm.person(person_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.observation
    ADD CONSTRAINT fpk_observation_person_id FOREIGN KEY (person_id) REFERENCES cdm.person(person_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.observation
    ADD CONSTRAINT fpk_observation_provider_id FOREIGN KEY (provider_id) REFERENCES cdm.provider(provider_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.observation
    ADD CONSTRAINT fpk_observation_qualifier_concept_id FOREIGN KEY (qualifier_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.observation
    ADD CONSTRAINT fpk_observation_unit_concept_id FOREIGN KEY (unit_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.observation
    ADD CONSTRAINT fpk_observation_value_as_concept_id FOREIGN KEY (value_as_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.observation
    ADD CONSTRAINT fpk_observation_visit_detail_id FOREIGN KEY (visit_detail_id) REFERENCES cdm.visit_detail(visit_detail_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.observation
    ADD CONSTRAINT fpk_observation_visit_occurrence_id FOREIGN KEY (visit_occurrence_id) REFERENCES cdm.visit_occurrence(visit_occurrence_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.payer_plan_period
    ADD CONSTRAINT fpk_payer_plan_period_contract_concept_id FOREIGN KEY (contract_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.payer_plan_period
    ADD CONSTRAINT fpk_payer_plan_period_contract_person_id FOREIGN KEY (contract_person_id) REFERENCES cdm.person(person_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.payer_plan_period
    ADD CONSTRAINT fpk_payer_plan_period_contract_source_concept_id FOREIGN KEY (contract_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.payer_plan_period
    ADD CONSTRAINT fpk_payer_plan_period_payer_concept_id FOREIGN KEY (payer_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.payer_plan_period
    ADD CONSTRAINT fpk_payer_plan_period_payer_source_concept_id FOREIGN KEY (payer_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.payer_plan_period
    ADD CONSTRAINT fpk_payer_plan_period_person_id FOREIGN KEY (person_id) REFERENCES cdm.person(person_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.payer_plan_period
    ADD CONSTRAINT fpk_payer_plan_period_plan_concept_id FOREIGN KEY (plan_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.payer_plan_period
    ADD CONSTRAINT fpk_payer_plan_period_plan_source_concept_id FOREIGN KEY (plan_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.payer_plan_period
    ADD CONSTRAINT fpk_payer_plan_period_sponsor_concept_id FOREIGN KEY (sponsor_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.payer_plan_period
    ADD CONSTRAINT fpk_payer_plan_period_sponsor_source_concept_id FOREIGN KEY (sponsor_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.payer_plan_period
    ADD CONSTRAINT fpk_payer_plan_period_stop_reason_concept_id FOREIGN KEY (stop_reason_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.payer_plan_period
    ADD CONSTRAINT fpk_payer_plan_period_stop_reason_source_concept_id FOREIGN KEY (stop_reason_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.person
    ADD CONSTRAINT fpk_person_care_site_id FOREIGN KEY (care_site_id) REFERENCES cdm.care_site(care_site_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.person
    ADD CONSTRAINT fpk_person_ethnicity_concept_id FOREIGN KEY (ethnicity_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.person
    ADD CONSTRAINT fpk_person_ethnicity_source_concept_id FOREIGN KEY (ethnicity_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.person
    ADD CONSTRAINT fpk_person_gender_concept_id FOREIGN KEY (gender_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.person
    ADD CONSTRAINT fpk_person_gender_source_concept_id FOREIGN KEY (gender_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.person
    ADD CONSTRAINT fpk_person_provider_id FOREIGN KEY (provider_id) REFERENCES cdm.provider(provider_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.person
    ADD CONSTRAINT fpk_person_race_concept_id FOREIGN KEY (race_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.person
    ADD CONSTRAINT fpk_person_race_source_concept_id FOREIGN KEY (race_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.procedure_occurrence
    ADD CONSTRAINT fpk_procedure_occurrence_modifier_concept_id FOREIGN KEY (modifier_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.procedure_occurrence
    ADD CONSTRAINT fpk_procedure_occurrence_person_id FOREIGN KEY (person_id) REFERENCES cdm.person(person_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.procedure_occurrence
    ADD CONSTRAINT fpk_procedure_occurrence_procedure_concept_id FOREIGN KEY (procedure_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.procedure_occurrence
    ADD CONSTRAINT fpk_procedure_occurrence_procedure_source_concept_id FOREIGN KEY (procedure_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.procedure_occurrence
    ADD CONSTRAINT fpk_procedure_occurrence_procedure_type_concept_id FOREIGN KEY (procedure_type_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.procedure_occurrence
    ADD CONSTRAINT fpk_procedure_occurrence_provider_id FOREIGN KEY (provider_id) REFERENCES cdm.provider(provider_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.procedure_occurrence
    ADD CONSTRAINT fpk_procedure_occurrence_visit_detail_id FOREIGN KEY (visit_detail_id) REFERENCES cdm.visit_detail(visit_detail_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.procedure_occurrence
    ADD CONSTRAINT fpk_procedure_occurrence_visit_occurrence_id FOREIGN KEY (visit_occurrence_id) REFERENCES cdm.visit_occurrence(visit_occurrence_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.provider
    ADD CONSTRAINT fpk_provider_care_site_id FOREIGN KEY (care_site_id) REFERENCES cdm.care_site(care_site_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.provider
    ADD CONSTRAINT fpk_provider_gender_concept_id FOREIGN KEY (gender_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.provider
    ADD CONSTRAINT fpk_provider_gender_source_concept_id FOREIGN KEY (gender_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.provider
    ADD CONSTRAINT fpk_provider_specialty_concept_id FOREIGN KEY (specialty_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.provider
    ADD CONSTRAINT fpk_provider_specialty_source_concept_id FOREIGN KEY (specialty_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.specimen
    ADD CONSTRAINT fpk_specimen_anatomic_site_concept_id FOREIGN KEY (anatomic_site_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.specimen
    ADD CONSTRAINT fpk_specimen_disease_status_concept_id FOREIGN KEY (disease_status_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.specimen
    ADD CONSTRAINT fpk_specimen_person_id FOREIGN KEY (person_id) REFERENCES cdm.person(person_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.specimen
    ADD CONSTRAINT fpk_specimen_specimen_concept_id FOREIGN KEY (specimen_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.specimen
    ADD CONSTRAINT fpk_specimen_specimen_type_concept_id FOREIGN KEY (specimen_type_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.specimen
    ADD CONSTRAINT fpk_specimen_unit_concept_id FOREIGN KEY (unit_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.survey_conduct
    ADD CONSTRAINT fpk_survey_conduct_assisted_concept_id FOREIGN KEY (assisted_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.survey_conduct
    ADD CONSTRAINT fpk_survey_conduct_collection_method_concept_id FOREIGN KEY (collection_method_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.survey_conduct
    ADD CONSTRAINT fpk_survey_conduct_person_id FOREIGN KEY (person_id) REFERENCES cdm.person(person_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.survey_conduct
    ADD CONSTRAINT fpk_survey_conduct_provider_id FOREIGN KEY (provider_id) REFERENCES cdm.provider(provider_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.survey_conduct
    ADD CONSTRAINT fpk_survey_conduct_respondent_type_concept_id FOREIGN KEY (respondent_type_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.survey_conduct
    ADD CONSTRAINT fpk_survey_conduct_survey_concept_id FOREIGN KEY (survey_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.survey_conduct
    ADD CONSTRAINT fpk_survey_conduct_survey_source_concept_id FOREIGN KEY (survey_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.survey_conduct
    ADD CONSTRAINT fpk_survey_conduct_timing_concept_id FOREIGN KEY (timing_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.survey_conduct
    ADD CONSTRAINT fpk_survey_conduct_validated_survey_concept_id FOREIGN KEY (validated_survey_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.visit_detail
    ADD CONSTRAINT fpk_visit_detail_care_site_id FOREIGN KEY (care_site_id) REFERENCES cdm.care_site(care_site_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.visit_detail
    ADD CONSTRAINT fpk_visit_detail_discharged_to_concept_id FOREIGN KEY (discharged_to_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.visit_detail
    ADD CONSTRAINT fpk_visit_detail_person_id FOREIGN KEY (person_id) REFERENCES cdm.person(person_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.visit_detail
    ADD CONSTRAINT fpk_visit_detail_preceding_visit_detail_id FOREIGN KEY (preceding_visit_detail_id) REFERENCES cdm.visit_detail(visit_detail_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.visit_detail
    ADD CONSTRAINT fpk_visit_detail_provider_id FOREIGN KEY (provider_id) REFERENCES cdm.provider(provider_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.visit_detail
    ADD CONSTRAINT fpk_visit_detail_visit_detail_concept_id FOREIGN KEY (visit_detail_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.visit_detail
    ADD CONSTRAINT fpk_visit_detail_visit_detail_parent_id FOREIGN KEY (parent_visit_detail_id) REFERENCES cdm.visit_detail(visit_detail_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.visit_detail
    ADD CONSTRAINT fpk_visit_detail_visit_detail_source_concept_id FOREIGN KEY (visit_detail_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.visit_detail
    ADD CONSTRAINT fpk_visit_detail_visit_detail_type_concept_id FOREIGN KEY (visit_detail_type_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.visit_detail
    ADD CONSTRAINT fpk_visit_detail_visit_occurrence_id FOREIGN KEY (visit_occurrence_id) REFERENCES cdm.visit_occurrence(visit_occurrence_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.visit_occurrence
    ADD CONSTRAINT fpk_visit_occurrence_care_site_id FOREIGN KEY (care_site_id) REFERENCES cdm.care_site(care_site_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.visit_occurrence
    ADD CONSTRAINT fpk_visit_occurrence_discharged_to_concept_id FOREIGN KEY (discharged_to_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.visit_occurrence
    ADD CONSTRAINT fpk_visit_occurrence_person_id FOREIGN KEY (person_id) REFERENCES cdm.person(person_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.visit_occurrence
    ADD CONSTRAINT fpk_visit_occurrence_preceding_visit_occurrence_id FOREIGN KEY (preceding_visit_occurrence_id) REFERENCES cdm.visit_occurrence(visit_occurrence_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.visit_occurrence
    ADD CONSTRAINT fpk_visit_occurrence_provider_id FOREIGN KEY (provider_id) REFERENCES cdm.provider(provider_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.visit_occurrence
    ADD CONSTRAINT fpk_visit_occurrence_visit_concept_id FOREIGN KEY (visit_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.visit_occurrence
    ADD CONSTRAINT fpk_visit_occurrence_visit_source_concept_id FOREIGN KEY (visit_source_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.visit_occurrence
    ADD CONSTRAINT fpk_visit_occurrence_visit_type_concept_id FOREIGN KEY (visit_type_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.measurement
    ADD CONSTRAINT measurement_visit_detail_id_fkey FOREIGN KEY (visit_detail_id) REFERENCES cdm.visit_detail(visit_detail_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.measurement
    ADD CONSTRAINT measurement_visit_occurrence_id_fkey FOREIGN KEY (visit_occurrence_id) REFERENCES cdm.visit_occurrence(visit_occurrence_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.note
    ADD CONSTRAINT note_visit_detail_id_fkey FOREIGN KEY (visit_detail_id) REFERENCES cdm.visit_detail(visit_detail_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY cdm.note
    ADD CONSTRAINT note_visit_occurrence_id_fkey FOREIGN KEY (visit_occurrence_id) REFERENCES cdm.visit_occurrence(visit_occurrence_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY vocabularies.concept_ancestor
    ADD CONSTRAINT fpk_concept_ancestor_ancestor_concept_id FOREIGN KEY (ancestor_concept_id) REFERENCES vocabularies.concept(concept_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.concept_ancestor
    ADD CONSTRAINT fpk_concept_ancestor_descendant_concept_id FOREIGN KEY (descendant_concept_id) REFERENCES vocabularies.concept(concept_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.concept_class
    ADD CONSTRAINT fpk_concept_class_concept_class_concept_id FOREIGN KEY (concept_class_concept_id) REFERENCES vocabularies.concept(concept_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.concept
    ADD CONSTRAINT fpk_concept_concept_class_id FOREIGN KEY (concept_class_id) REFERENCES vocabularies.concept_class(concept_class_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.concept
    ADD CONSTRAINT fpk_concept_domain_id FOREIGN KEY (domain_id) REFERENCES vocabularies.domain(domain_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.concept_relationship
    ADD CONSTRAINT fpk_concept_relationship_concept_id_1 FOREIGN KEY (concept_id_1) REFERENCES vocabularies.concept(concept_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.concept_relationship
    ADD CONSTRAINT fpk_concept_relationship_concept_id_2 FOREIGN KEY (concept_id_2) REFERENCES vocabularies.concept(concept_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.concept_relationship
    ADD CONSTRAINT fpk_concept_relationship_relationship_id FOREIGN KEY (relationship_id) REFERENCES vocabularies.relationship(relationship_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.concept_synonym
    ADD CONSTRAINT fpk_concept_synonym_concept FOREIGN KEY (concept_id) REFERENCES vocabularies.concept(concept_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.concept_synonym
    ADD CONSTRAINT fpk_concept_synonym_language_concept FOREIGN KEY (language_concept_id) REFERENCES vocabularies.concept(concept_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.concept
    ADD CONSTRAINT fpk_concept_vocabulary_id FOREIGN KEY (vocabulary_id) REFERENCES vocabularies.vocabulary(vocabulary_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.domain
    ADD CONSTRAINT fpk_domain_domain_concept_id FOREIGN KEY (domain_concept_id) REFERENCES vocabularies.concept(concept_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.drug_strength
    ADD CONSTRAINT fpk_drug_strength_amount_unit_concept_id FOREIGN KEY (amount_unit_concept_id) REFERENCES vocabularies.concept(concept_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.drug_strength
    ADD CONSTRAINT fpk_drug_strength_denominator_unit_concept_id FOREIGN KEY (denominator_unit_concept_id) REFERENCES vocabularies.concept(concept_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.drug_strength
    ADD CONSTRAINT fpk_drug_strength_drug_concept_id FOREIGN KEY (drug_concept_id) REFERENCES vocabularies.concept(concept_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.drug_strength
    ADD CONSTRAINT fpk_drug_strength_ingredient_concept_id FOREIGN KEY (ingredient_concept_id) REFERENCES vocabularies.concept(concept_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.drug_strength
    ADD CONSTRAINT fpk_drug_strength_numerator_unit_concept_id FOREIGN KEY (numerator_unit_concept_id) REFERENCES vocabularies.concept(concept_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.relationship
    ADD CONSTRAINT fpk_relationship_relationship_concept_id FOREIGN KEY (relationship_concept_id) REFERENCES vocabularies.concept(concept_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.relationship
    ADD CONSTRAINT fpk_relationship_reverse_relationship_id FOREIGN KEY (reverse_relationship_id) REFERENCES vocabularies.relationship(relationship_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.source_to_concept_map
    ADD CONSTRAINT fpk_source_to_concept_map_source_vocabulary_id FOREIGN KEY (source_vocabulary_id) REFERENCES vocabularies.vocabulary(vocabulary_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY vocabularies.source_to_concept_map
    ADD CONSTRAINT fpk_source_to_concept_map_target_concept_id FOREIGN KEY (target_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY vocabularies.source_to_concept_map
    ADD CONSTRAINT fpk_source_to_concept_map_target_vocabulary_id FOREIGN KEY (target_vocabulary_id) REFERENCES vocabularies.vocabulary(vocabulary_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY vocabularies.vocabulary
    ADD CONSTRAINT fpk_vocabulary_vocabulary_concept_id FOREIGN KEY (vocabulary_concept_id) REFERENCES vocabularies.concept(concept_id) DEFERRABLE;



ALTER TABLE ONLY vocabularies.source_to_standard_vocab_map
    ADD CONSTRAINT source_to_standard_vocab_map_source_concept_class_id_fkey FOREIGN KEY (source_concept_class_id) REFERENCES vocabularies.concept_class(concept_class_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY vocabularies.source_to_standard_vocab_map
    ADD CONSTRAINT source_to_standard_vocab_map_source_domain_id_fkey FOREIGN KEY (source_domain_id) REFERENCES vocabularies.domain(domain_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY vocabularies.source_to_standard_vocab_map
    ADD CONSTRAINT source_to_standard_vocab_map_target_concept_class_id_fkey FOREIGN KEY (target_concept_class_id) REFERENCES vocabularies.concept_class(concept_class_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY vocabularies.source_to_standard_vocab_map
    ADD CONSTRAINT source_to_standard_vocab_map_target_concept_id_fkey FOREIGN KEY (target_concept_id) REFERENCES vocabularies.concept(concept_id) ON UPDATE CASCADE DEFERRABLE;



ALTER TABLE ONLY vocabularies.source_to_standard_vocab_map
    ADD CONSTRAINT source_to_standard_vocab_map_target_vocabulary_id_fkey FOREIGN KEY (target_vocabulary_id) REFERENCES vocabularies.vocabulary(vocabulary_id) ON UPDATE CASCADE DEFERRABLE;
```
