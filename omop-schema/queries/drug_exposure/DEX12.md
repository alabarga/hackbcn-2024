<!---
Group:drug exposure
Name:DEX12 Distribution of forms used for a given ingredient
Author: Alberto Labarga
CDM Version: 5.4
-->

# DEX12: Distribution of forms used for a given ingredient

## Description
| This query determines the percent distribution of forms of drug products containing a given ingredient. See  vocabulary queries for obtaining valid drug_concept_id values.

## Query
The following is a sample run of the query. The input parameter is highlighted in  blue.

```sql
SELECT form_name,
       100.00 * cn / SUM(cn) OVER() AS percent_forms
  FROM (
SELECT drugform.concept_name AS form_name,
       COUNT(*)              AS cn
  FROM vocabularies.concept ingredient
  JOIN vocabularies.concept_ancestor a
    ON ingredient.concept_id = a.ancestor_concept_id
  JOIN vocabularies.concept drug
    ON a.descendant_concept_id = drug.concept_id
  JOIN vocabularies.concept_relationship r
    ON drug.concept_id = r.concept_id_1
  JOIN vocabularies.concept drugform
    ON r.concept_id_2 = drugform.concept_id
 WHERE ingredient.concept_id        = 1125315 --Acetaminophen
   AND ingredient.concept_class_id  = 'Ingredient'
   AND drug.standard_concept        = 'S'
   AND drugform.concept_class_id    = 'Dose Form'
 GROUP BY drugform.concept_name
HAVING COUNT(*) > 0
       ) TMP
 ORDER BY percent_forms desc;
```

## Input

|  Parameter |  Example |  Mandatory |  Notes |
| --- | --- | --- | --- |
|  ingredient.concept_id |  1125315 |  Yes |  Acetaminophen |

## Output

|  Field |  Description |
| --- | --- |
| form_name | The concept name of the dose form |
| percent_forms | The percent of forms drug products have containing the ingredient |

## Example output record

|  Field |  Description |
| --- | --- |
| form_name |  Oral Tablet |
| percent_forms |  95.69 |

## Documentation
https://ohdsi.github.io/CommonDataModel/cdm54.html#DRUG_EXPOSURE
