## Kaggle API setup (local & CI)

This project uses the Kaggle CLI / API to download datasets. The Kaggle credentials file (kaggle.json) must be provided by each developer or by your CI system. Never commit `kaggle.json` to the repository.

Steps to create and use the token locally:

1. Go to your Kaggle account (https://www.kaggle.com/), Account tab, and click "Create API Token". This downloads a `kaggle.json` containing your username and key.
2. Place `kaggle.json` in `~/.kaggle/kaggle.json` (Linux/macOS) or `%USERPROFILE%\.kaggle\kaggle.json` (Windows). Ensure the file permissions are restricted (e.g., chmod 600 on POSIX).
3. Alternatively, set the environment variable `KAGGLE_CONFIG_DIR` to a directory that contains `kaggle.json`.

Example `kaggle.json` format:

```
{"username": "YOUR_USERNAME", "key": "YOUR_KEY"}
```

CI / Jenkins notes

- Do NOT store `kaggle.json` in the Git repository.
- In Jenkins, add the token as a "Secret file" credential (or secret text) and use `withCredentials` to copy it into `~/.kaggle/kaggle.json` at build time. See `Jenkinsfile` for an example.
- The code reads `KAGGLE_CONFIG_DIR` if set; otherwise it defaults to `~/.kaggle`.

Security

- Ensure `.gitignore` excludes `kaggle.json` (this repo already does).
- Rotate keys if a token is ever exposed.

If you want, I can add a small script to help developers create the correct folder/file locally and a Jenkinsfile snippet for Windows agents. 
