# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).
 
## [Proto-1.0-Alpha] - 2024-08-19

### Add
- New logic with SBERT
- HRIS models example

### Reports
- Similiarity scoring with SBERT:Models
    - Searcing sase:
        - Report types
        - Employees
    - Method
        - Searching by text:vector coordinates
        - Similiarity score >= 0.2%
    - Result
        - As expected with some issues
    - Issue
        - Data model needs to keep adjusting with human behavior
        - Need to fix typos or mix-language
        - it can't search for words 'leaves', I think some words cannot to be use similiarity algorithm, maybe I can use fuzzy-search
    - Solutions
        - Considering to combine with FuzzySearch
        - or Ruled base algorithm

## [Proto-1.0.1-Alpha] - 2024-08-19

### Change
- Lower similiarity score for employees
    - From 0.6 -> 0.3

### Reports
- With make user input clean .lower() .strip() it increase scores of similiarity
- Assumed range of similiarity around 0.3 to 0.6 for all models

## [Proto-1.0.2-Alpha] - 2024-08-29

### Add
- Spellchecking for typo (still got some issues)
- Companies data models

### Change
- Vector checking
    - Split sentence into single word to increase similiarity score

### Reports
- I need to know how to generate knowledge based for each transactional datas
- Also how to detect type of dates user inputted, such like:
    - `this week`
    - `this month`
    - `august to/until december`
    - specific date like: `YYYY-MM-DD` to `YYYY-MM-DD`
    - etc.

## [Proto-1.0.3-Alpha] - 2024-08-29

### Add
- Algorithm for typo handling
    - Some tricky logic added combined with existing library

- Algorithm for extracting date
    - Still lot of static validation, needs more improvments

### Reports
- Solved for issue date so far, but there will be lot of possibilities of date issue
- Need to change or improve algorithm to handle date extraction

## [Proto-1.0.4-Alpha] - 2024-08-30

### Add
- Translate language
    - Check possibility for translating to english as standard language for data model

### Reports
- I think the project size kinda big because of data models
- Also need to test it in real case
- But first, I need to make it as a service so user can access it from frontend

## [Proto-1.0.4-1-Alpha] - 2024-08-30

### Add
- REST APi
    - Now the service can access from outside

### Reports
- It's actually released as a service, just need to test it out!

## [Proto-1.0.4-2-Alpha] - 2024-08-31

### Add
- More filter logic for extracting date