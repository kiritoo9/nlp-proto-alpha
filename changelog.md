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