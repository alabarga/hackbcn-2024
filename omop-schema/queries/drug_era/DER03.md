<!---
Group:drug era
Name:DER03 What is the number of distinct ingredients per patient?
Author: Alberto Labarga
CDM Version: 5.4
-->

# DER03: What is the number of distinct ingredients per patient?

## Description
Average number of distinct ingredients for all patients.

## Query
```sql
SELECT
        avg(cnt)
from
        (
                select
                        count(distinct r.drug_concept_id) cnt,
                        r.person_id
                FROM
                        cdm.drug_era r
                GROUP BY
                        r.person_id
        ) a
```

## Input

None

## Output

|  Field |  Description |
| --- | --- |
| avg |  Average count of distinct ingredient for all patients |

## Example output record

|  Field |  Value |
| --- | --- |
| avg |  10 |

## Documentation
https://ohdsi.github.io/CommonDataModel/cdm54.html#DRUG_ERA
