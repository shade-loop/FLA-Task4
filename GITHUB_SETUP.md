# Publish this Task 4 repository

Suggested repository name: `FLA-Task4-Infinite-Loop-Detection`

1. Sign in to GitHub and create an **empty** repository with that name. Do not initialize it with a README.
2. Extract this ZIP. Open PowerShell **inside the extracted `FLA_Task4_Repo` folder**.
3. Run:

```powershell
git init
git add .
git commit -m "Add CLA-2 Task 4 infinite-loop detection project"
git branch -M main
git remote add origin https://github.com/shade-loop/FLA-Task4-Infinite-Loop-Detection.git
git push -u origin main
```

If `origin` already exists, use `git remote set-url origin https://github.com/shade-loop/FLA-Task4-Infinite-Loop-Detection.git` instead of `git remote add origin ...`.

After successful push, add your actual GitHub URL to the Task 4 Word report. For demonstration screenshots, run the program and tests yourself and capture the real terminal output.
