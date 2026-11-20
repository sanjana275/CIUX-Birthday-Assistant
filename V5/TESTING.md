# CIUX Birthday Assistant — V5 Testing Report

**GM University · School of Computer Science and Technology**  
**Course:** UE24CS3540 — Conversational Interfaces and UX  
**Version:** V5 — Browser-Based Voice Assistant

## 1. Testing Overview

Testing verifies the Birthday Assistant's intent recognition, entity extraction, dialogue context, clarification handling, factual responses and browser-based voice interaction.

The testing process includes:
- Automated unit testing using Pytest.
- Manual conversational testing.
- Context and clarification testing.
- Browser voice input and output testing.

## 2. Automated Test Results

**Command executed:**

```powershell
python -m pytest -v
```

**Actual result:**

| Metric | Result |
|---|---:|
| Total automated tests | 19 |
| Passed | 19 |
| Failed | 0 |
| Execution time | 13.10 seconds |
| Result | PASS |

### Test distribution

| Test file | Passed |
|---|---:|
| test_dialogue.py | 6 |
| test_nlu.py | 7 |
| test_rules.py | 6 |
| **Total** | **19** |

## 3. Manual Test Cases — 40 Utterances

The following test cases form the manual conversational testing plan. Record the actual result and status after executing each case.

### Category A: Direct Questions (10)

| ID | User utterance | Expected behaviour | Actual result / Status |
|---|---|---|---|
| T01 | Hello | Display greeting | Pending |
| T02 | When is Appa's birthday? | Retrieve Appa's birthday | Pending |
| T03 | When is Rahul's birthday? | Retrieve birthday or ask clarification if ambiguous | Pending |
| T04 | How many birthdays are in September? | Return September birthday count | Pending |
| T05 | Any nephew birthdays in September? | Return matching nephew birthday information | Pending |
| T06 | Where does Lakshmi live? | Retrieve place or ask clarification | Pending |
| T07 | How old is Raghavendra Gowda? | Retrieve age | Pending |
| T08 | Who has birthdays tomorrow? | Return matching upcoming birthdays | Pending |
| T09 | Help | Display supported question examples | Pending |
| T10 | How many birthdays are in October? | Return October birthday count | Pending |

### Category B: Paraphrased Questions (10)

| ID | User utterance | Expected behaviour | Actual result / Status |
|---|---|---|---|
| T11 | Tell me Appa's date of birth | Retrieve Appa's birthday | Pending |
| T12 | On which date was Rahul born? | Retrieve birthday or clarify ambiguity | Pending |
| T13 | Count the people born in September | Return September birthday count | Pending |
| T14 | Do any of my nephews celebrate birthdays in September? | Identify matching relationship and month | Pending |
| T15 | Which place does Lakshmi stay in? | Retrieve place or clarify ambiguity | Pending |
| T16 | Tell me Raghavendra Gowda's age | Retrieve age | Pending |
| T17 | Whose birthday is coming tomorrow? | Return upcoming birthday information | Pending |
| T18 | Show September birthdays | Return September birthday information | Pending |
| T19 | Give me the October birthday count | Return October birthday count | Pending |
| T20 | Can you tell me Appa's birthday date? | Retrieve Appa's birthday | Pending |

### Category C: Contextual and Multi-turn Questions (10)

| ID | Conversation / utterance | Expected behaviour | Actual result / Status |
|---|---|---|---|
| T21 | How many birthdays are in September? | Return September count | Pending |
| T22 | What about October? | Reuse previous count intent for October | Pending |
| T23 | Any nephew birthdays in September? | Return matching results | Pending |
| T24 | What about October? | Reuse nephew relationship for October | Pending |
| T25 | When is Appa's birthday? | Retrieve Appa's birthday | Pending |
| T26 | Where does he live? | Resolve follow-up if supported; otherwise ask for clarification | Pending |
| T27 | When is Rahul's birthday? | Retrieve birthday or ask clarification | Pending |
| T28 | Select one of the displayed clarification options | Resolve the selected person | Pending |
| T29 | Reset Conversation | Clear conversation context | Pending |
| T30 | What about October? (after reset) | Do not reuse previous context; ask for required information | Pending |

### Category D: Ambiguous and Unsupported Questions (10)

| ID | User utterance | Expected behaviour | Actual result / Status |
|---|---|---|---|
| T31 | When is Lakshmi's birthday? | Ask which Lakshmi is intended if multiple matches exist | Pending |
| T32 | When is Rahul's birthday? | Ask for clarification if multiple matches exist | Pending |
| T33 | When is an unknown person's birthday? | Avoid inventing information; report no match | Pending |
| T34 | Tell me the birthday of an unknown nickname | Ask for clarification or report no match | Pending |
| T35 | What is the weather today? | Handle unsupported request gracefully | Pending |
| T36 | Tell me a joke | Handle unsupported request gracefully | Pending |
| T37 | What is the birthday of a person not in the dataset? | Do not invent a birthday | Pending |
| T38 | Give me all personal details of an unknown person | Avoid fabricating records | Pending |
| T39 | What about that person? (without context) | Ask for clarification | Pending |
| T40 | Random unsupported words | Display a graceful fallback response | Pending |

**Note:** Some names may match multiple dataset records. The expected behaviour is to clarify when ambiguous rather than assume a person.

## 4. Voice Interaction Testing

| ID | Test | Expected behaviour | Status |
|---|---|---|---|
| V01 | Click Speak | Start microphone recognition | Manually tested |
| V02 | Allow microphone permission | Browser permits microphone use | Manually tested |
| V03 | Speak a birthday question | Convert speech into visible text | Manually tested |
| V04 | Submit a text question | Display chatbot response | Manually tested |
| V05 | Enable voice output | Read response aloud | Manually tested |
| V06 | Disable voice output | Keep text response without speech | Manually tested |
| V07 | Reset conversation | Clear conversation context | Manually tested |

## 5. Evaluation Metrics

The following metrics can be calculated after completing the manual tests:

- **Intent accuracy:** Correctly identified intents divided by evaluated utterances.
- **Entity accuracy:** Correctly extracted entities divided by evaluated entities.
- **Task success rate:** Successfully completed tasks divided by attempted tasks.
- **Clarification success:** Correctly resolved ambiguous requests divided by clarification attempts.
- **Grounded factuality:** Factual answers supported by the dataset.
- **Voice recognition success:** Correctly recognized spoken inputs divided by voice attempts.

Do not report numerical accuracy percentages until the corresponding tests have been executed and evaluated.

## 6. Conclusion

The V5 automated test suite completed successfully with 19 passed tests and zero failures.

Manual testing is used to evaluate the 40 conversational utterances and the browser voice interaction features. Final manual test outcomes and evaluation metrics should be added after execution.

**Project design principle:** Gemini understands the user's question, the deterministic rule engine retrieves factual information, and browser speech technologies provide voice interaction.