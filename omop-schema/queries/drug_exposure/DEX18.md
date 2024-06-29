<!---
Group:drug exposure
Name:DEX18 What is the distribution of DRUG_TYPE_CONCEPT_ID (modes of distribution) for a given drug?
Author: Alberto Labarga
CDM Version: 5.4
-->

# DEX18: What is the distribution of DRUG_TYPE_CONCEPT_ID (modes of distribution) for a given drug?

## Description

## Query
The following is a sample run of the query. The input parameters are highlighted in blue.

```sql
SELECT c.concept_name AS drug_type, COUNT(*) AS drug_type_count
  FROM cdm.drug_exposure de
  JOIN vocabularies.concept c
    ON c.concept_id = de.drug_type_concept_id
 GROUP BY c.concept_name
 ORDER BY drug_type_count DESC;
```

## Input

 None

## Output

|  Field |  Description |
| --- | --- |
| drug_type | The type of drug. |
| drug_type_count | The number of exposures to the type of drug. |


## Example output record

|  Field |  Description |
| --- | --- |
| drug_type | Prescription dispensed in pharmacy |
| drug_type_count | 6294108 |

## Documentation
https://ohdsi.github.io/CommonDataModel/cdm54.html#DRUG_EXPOSURE
