# Publish Inertia to a new GitHub repository

The prepared project includes scripts that create a **new, public** GitHub repository on the account `Ace-Alch`, push the clean source tree and try to enable GitHub Pages. The scripts refuse to overwrite an existing repository.

## Recommended: Windows

1. Install **Git for Windows** and **GitHub CLI** (`gh`) if you do not already have them.
2. Open PowerShell and run `gh auth login`. Choose your `Ace-Alch` account.
3. Extract this ZIP file to a local folder.
4. Double-click **`PUBLISH-WINDOWS.bat`**, or run `powershell -File publish-github.ps1` in that folder.
5. Open the newly created repository and its **Actions** tab. If prompted, enable Pages under **Settings → Pages → Build and deployment → GitHub Actions**.

## macOS / Linux

With Git and an authenticated GitHub CLI installed, extract the ZIP, open a terminal in the project directory, and run:

```bash
bash publish-github.sh
```

## Alternative: GitHub website

1. Create an empty **public** repository named `Inertia-Control-Studio` under your preferred account.
2. Upload the **extracted files and folders**, including hidden `.github` and `.gitignore`, to the `main` branch. A ZIP file uploaded as a single attachment does not expand into project files.
3. Open **Settings → Pages**, select **GitHub Actions**, then open **Actions** and run **Publish Inertia demo**.

## Expected output

- Source repository (after creation): `https://github.com/Ace-Alch/Inertia-Control-Studio`
- GitHub Pages demo (after successful deployment): usually `https://ace-alch.github.io/Inertia-Control-Studio/`

These are **intended addresses** until GitHub confirms creation and deployment. The workflow publishes only the rebuilt standalone `index.html`; it does not expose stored reports or private information from other local projects.

You can always run the application directly from `index.html` without GitHub Pages.
