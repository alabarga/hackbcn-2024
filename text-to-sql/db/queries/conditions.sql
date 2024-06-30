-- name: conditions_by_person_id

SELECT condition_concept_id, condition_start_date, condition_end_date,concept_name
    FROM cdm.condition_occurrence co
    INNER JOIN vocabularies.concept c ON c.concept_code = cast(co.condition_concept_id as text)
    WHERE person_id = '%(person_id)s' 
    AND condition_start_date BETWEEN '%(start_date)s' AND '%(end_date)s'
    and domain_id ='Condition'
    and condition_concept_id not in ('423315002');
