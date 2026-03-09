# pages

Auto-generated file index, served via GitHub Pages.

→ **[idangiblykeyzar.github.io/pages](https://idangiblykeyzar.github.io/pages/)**

---

## Usage

Drop files into `public/` and push. The index updates itself.

```
public/
  md/
    your-file.md
  ...
```

## How it works

| Step | What happens |
|------|--------------|
| Push to `main` | GitHub Actions runs `scripts/generate_index.py` |
| Script scans `public/` | Builds a linked file tree |
| `index.html` is committed | Site reflects the new content automatically |
