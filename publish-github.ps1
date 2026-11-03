# Publish a NEW repository under the indicated GitHub account.
# Requires Git, GitHub CLI, and `gh auth login`. Refuses to overwrite existing repositories.
param(
  [string]$Owner = 'Ace-Alch',
  [string]$Repo = 'Inertia-Control-Studio'
)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$Full = "$Owner/$Repo"
foreach ($Cmd in @('git', 'gh')) {
  if (-not (Get-Command $Cmd -ErrorAction SilentlyContinue)) {
    throw "Missing $Cmd. Install it first, then open a new PowerShell window."
  }
}
gh auth status *> $null
if ($LASTEXITCODE -ne 0) { throw 'Run gh auth login first.' }
gh repo view $Full *> $null
if ($LASTEXITCODE -eq 0) { throw "Repository $Full already exists. Nothing was overwritten." }
if (-not (Test-Path '.git')) {
  git init -b main
  if ($LASTEXITCODE -ne 0) { throw 'git init failed.' }
}
git add --all
if ($LASTEXITCODE -ne 0) { throw 'git add failed.' }
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
  git commit -m 'Initial release: Inertia Control Studio 4.1'
  if ($LASTEXITCODE -ne 0) { throw 'git commit failed. Check your Git name and email settings.' }
}
git rev-parse HEAD *> $null
if ($LASTEXITCODE -ne 0) { throw 'No commit exists. Nothing was published.' }
git remote get-url origin *> $null
if ($LASTEXITCODE -eq 0) { throw 'An origin remote already exists. Refusing to continue.' }
gh repo create $Full --public --description 'Offline nonlinear pendulum dynamics, controller design and optimization laboratory' --source . --remote origin --push
if ($LASTEXITCODE -ne 0) { throw 'Repository creation or push failed. Check the CLI output.' }
'{"build_type":"workflow"}' | gh api -X POST "repos/$Full/pages" --input - *> $null
if ($LASTEXITCODE -ne 0) {
  Write-Warning 'Enable GitHub Pages in Settings > Pages > Build and deployment > GitHub Actions.'
}
gh workflow run pages.yml --repo $Full
if ($LASTEXITCODE -ne 0) {
  Write-Warning 'Open the Actions tab and run Publish Inertia demo manually.'
}
Write-Host "Repository: https://github.com/$Full"
Write-Host 'Check the Actions tab for the Pages deployment URL.'
