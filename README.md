# profiler-open-data-toronto
**What is this?**
This is a public repo for logic and documentation for Toronto's Open Data Profiler

**What is the Open Data Profiler**
Eventually, it will
1. Summarize each attribute in Toronto Open Data datastore resources
2. Assign classifications to each attribute
3. Present those on the Portal's API (and maybe frontend)

**How can I Contribute?**
- Reach out to opendata@toronto.ca
- Reach out on the Civic Tech Toronto Slack

## Version Control & Best Coding Practices
- Steps to be followed to download updated code/documentation before start of any new development
```
# Create a new branch (branch_name: follows a convention that you are comfortable with) for new development 
git checkout -b branch_name origin/develop

# Rebase to make sure that we have updated code locally on the branch_name 
git pull --rebase origin develop
```

- Steps to be followed to upload any new developments related to code/documentation
```
# Push your developments from branch_name into develop branch on github repo.
git push origin branch_name
```

- Comment & commit as per the need.  
- Any development (small or big) should be subjected to peer-review i.e., sending Pull Request (PR) 
- E.g: Developer/Reviewers:
  - E.x-1: Mac develops code related to Statistics of Strings ---> Reviewer: Hareesh or Denis
  - E.x-2: Hareesh develops code related to Statistics of Date/Datetimes ---> Reviewer: Mackenzie or Denis
