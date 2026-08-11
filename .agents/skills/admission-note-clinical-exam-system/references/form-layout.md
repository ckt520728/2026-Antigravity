# Hospital admission-note form — field inventory and mapping

Concrete reference for implementing Part 3 of the skill. Derived from a Taiwanese
regional hospital's pre-printed ADMISSION NOTE form. No patient data reproduced.

---

## Letterhead block

A single-row, three-column bordered table placed in the **document's page header
section** so it repeats on every page.

| Column | Width (pt) | Content |
|---|---|---|
| 1 | ~215 | `<醫院名稱>` (16 pt bold, centered) over `ADMISSION  NOTE` (12 pt bold, centered; two spaces between words) |
| 2 | ~190 | `病歷號：` / `姓　　名：` / `身分證號碼：` / `住院日期：` |
| 3 | ~105 | `床號：` / `生日：` / `性別：` |

Body text ~9 pt in the header cells, zero paragraph spacing, small cell padding.
Footer on the paper form is a centered `n/N` page number.

### ROC calendar helper

The admission date prints as `115 年 02 月 18 日` (ROC year = Gregorian − 1911).

```js
function toRocDate_(iso) {
  if (!iso) return '';
  var d = new Date(String(iso) + 'T00:00:00');
  if (isNaN(d.getTime())) return String(iso);
  var pad = function (n) { return (n < 10 ? '0' : '') + n; };
  return (d.getFullYear() - 1911) + ' 年 ' + pad(d.getMonth() + 1) + ' 月 ' + pad(d.getDate()) + ' 日';
}
```

Birth date on these forms is often already ROC-encoded (`0420221` = 民國 42/02/21).
Accept it as free text rather than trying to parse it.

---

## Section order and field mapping

| Form heading | Source field(s) | Notes |
|---|---|---|
| `主訴(Chief Complaints)：` | chiefComplaint | |
| `現在病歷(Present Illness)：` | presentIllness | includes ED course |
| `過去病史(Past History)：` | — | prints literal `Past history :` then four numbered subheadings |
| ⤷ `1. Disease :` | pastHistory | |
| ⤷ `2. History of trauma or surgery :` | surgicalHistory | |
| ⤷ `3. History of hospitalization :` | hospitalizationHistory | date range + hospital + problems |
| ⤷ `4. Home medication reviews :` | medications | grouped by date + issuing hospital |
| `藥物過敏(Drug Allergy)：` | allergies | default: *The patient is not allergic to any type of food or medicine.* |
| `家族史(Family History)：` | familyHistory (+ socialHistory as `Personal and social history :`) | the paper form has no separate social-history heading |
| `系統回顧(Review of Systems)：` | reviewOfSystems | prints literal `Review of systems` then the numbered systems |
| `理學檢查(Physical Examination)：` | vitalSigns, physicalExam | `Vital sign:` line first |
| `檢驗報告：` | labs only | **no English gloss on this heading** |
| `檢查報告：` | imaging/studies | **separate section from 檢驗報告** |
| `初步診斷(Impression)：` | problemList[].problem | flat numbered list |
| `治療及計劃(Management and Plan)：` | problemList[].plan | flat numbered list, renumbered continuously across problems |
| `主治醫師：` | doctorName | right-aligned signature line |

---

## Review of systems — the form's nine systems

Serialised as `<system>：<symptom>(-)；<symptom>(-)`.

1. systemic — fever, BW loss, change of appetite, night sweat
2. skin — petechiae, purpura, skin rash, itching
3. HEENT — blurred vision, ocular pain, hearing loss, tinnitus, vertigo, nasal stuffiness, nasal discharge, nasal bleeding, gum bleeding, sore throat, headache, oral ulcer
4. Cardiovascular — exertional chest tightness, PND, orthopnea, palpitation
5. Respiratory — dyspnea, cough, chest pain, hemoptysis
6. GI — anorexia, nausea, vomiting, dysphagia, heart burn, hunger pain, constipation, diarrhea, melena, change of bowel habit, small caliber stool
7. Urogenital — flank pain, hematuria, urinary frequency, urgency, dysuria, nocturia, polyuria, oliguria
8. Musculoskeletal — bone pain, arthralgia, myalgia, weakness
9. Neurological — numbness, paresis/paralysis

---

## Physical examination — the form's structure

```
Vital sign: T: __ ℃  P: __/min  R: __/min  BP: __/__ mmHg  SpO2: __%
General appearance: __
Conscious: E_V_M_
HEENT:      1.Conjunctivae pale(-) .icteric sclerae(-)
            2.Tonsil enlargement(-)
            3.Pupil: 3.0/3.0, Light reflex: +/+
Neck:       1.supple(+) 2.JVE(-) 3.Carotid bruit(-)
            4.Lymphadenopathy(-) 5.Thyroid enlargement(-)
Chest/lung: 1.Deformity(-) 2.Symmetric expansion(+)
            3.Tenderness of ribs(-) 4.Breathing sound: __
Heart:      1.Heart beat: RHB 2.Heart murmur(-) 3.PMI at 4th intercostal space
            4.Palpable: Thrill(-), Heave(-) 5.Gallop(-), Friction rub(-)
Abdomen:    1.soft(+) 2.Bowel sound: __ 3.Hepatomegaly(-) 4.Tympanic percussion(-)
            5.Tenderness(-) 6.Rebounding pain(-) 7.Muscle guarding(-)
            8.Flank knocking pain tenderness(-) 9.Murphy sign(-)
            10.Shifting dullness(-) 11.Scar(-)
Extremities:1.Freely movable 2.Pitting edema(-) 3.Clubbing finger(-) 4.Cyanosis(-)
```

Every item uses `(+)` / `(-)`. Offer the normal string per system and let the
physician flip individual items rather than retyping the block.

---

## Laboratory block conventions

The form writes labs as panel + date + space-separated values, not prose:

```
CBC  2/18  WBC:__  Hgb:__  PLT:__  MCV:__
BCS  2/18  BUN:__  Cr:__  Na:__  K:__  Cl:__  Sugar:__  CRP:__
SMA  11/14 GOT:__  GPT:__  TG:__  Chol:__  Alb:__
CxR  2/18  __
KUB  2/18  __
```

Match this rather than emitting `• Chest radiograph: ...` bullets — the format is
what makes it scannable on a ward round.

---

## Medication review conventions

Grouped by **date + issuing hospital**, then numbered:

```
<ROC date>-<hospital name>
  1.<Drug>(<strength>)  <qty> tab  <frequency>  <route> x <n> days
```

Discharge medications are flagged inline, e.g. `(出院帶藥)`.
