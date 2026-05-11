# Reaction–Diffusion Morphogenesis Lab

An interactive, forkable **Gray–Scott reaction–diffusion simulator** built with plain HTML, CSS and JavaScript.

This project shows how simple local chemical rules can generate complex biological-looking patterns such as:

- coral-like growth
- dividing spots
- maze structures
- zebra-like stripes
- worm-like trails
- self-organising fronts

It is designed to be useful from **student level to research level**: simple enough to understand in one file, but deep enough to extend into serious scientific-computing experiments.

---

## Live Demo

If hosted with GitHub Pages, the demo will run at:

```text
https://YOUR-USERNAME.github.io/reaction-diffusion-morphogenesis-lab/
```

---

## Why this project exists

Many scientific simulations on GitHub are either:

1. visually nice but scientifically shallow, or  
2. mathematically serious but difficult for beginners to run.

This repo tries to sit in the middle:

- no build tools
- no framework
- no package installation
- no hidden backend
- one readable `index.html`
- interactive sliders
- real-time plots
- scientifically meaningful equations

The aim is that a GCSE/A-level student can play with it, an undergraduate can read the code, and a PhD researcher can fork it into something more advanced.

---

## The Scientific Model

This project uses the **Gray–Scott reaction–diffusion model**.

Two chemical fields are simulated:

- `A` — the feed chemical
- `B` — the activator / morphogen-like chemical

The equations are:

```text
∂A/∂t = D_A ∇²A − A B² + F(1 − A)

∂B/∂t = D_B ∇²B + A B² − (k + F)B
```

Where:

| Symbol | Meaning |
|---|---|
| `A` | concentration of chemical A |
| `B` | concentration of chemical B |
| `D_A` | diffusion rate of A |
| `D_B` | diffusion rate of B |
| `F` | feed rate |
| `k` | kill rate |
| `∇²` | Laplacian / diffusion operator |

The model is simple, but it can produce surprisingly rich patterns.

---

## Features

- Interactive reaction–diffusion simulation
- Drag-to-seed morphogen injection
- Presets for coral, spots, worms, zebra and maze patterns
- Real-time telemetry:
  - mean activator level
  - variance
  - edge energy
  - active area
- Live morphology trace graph
- Multiple colour palettes
- Adjustable:
  - feed rate
  - kill rate
  - diffusion coefficients
  - simulation speed
  - brush size
  - contrast
  - glow
- Works directly in the browser
- Suitable for GitHub Pages

---

## How to Run Locally

Because this is a single HTML file, you can simply open:

```text
index.html
```

in a browser.

For a cleaner local server:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

---

## Suggested GitHub Repository Name

```text
reaction-diffusion-morphogenesis-lab
```

Alternative names:

```text
morphogenesis-lab
gray-scott-simulator
pattern-formation-lab
turing-pattern-explorer
```

---

## Step-by-Step: Create the Repo

### 1. Create a new GitHub repository

Repository name:

```text
reaction-diffusion-morphogenesis-lab
```

Description:

```text
Interactive Gray–Scott reaction–diffusion simulator for biological pattern formation, built with plain HTML, CSS and JavaScript.
```

Recommended topics:

```text
reaction-diffusion
gray-scott
morphogenesis
pattern-formation
simulation
scientific-computing
javascript
html5-canvas
education
```

---

### 2. Add files

Upload:

```text
index.html
README.md
LICENSE
```

---

### 3. Enable GitHub Pages

Go to:

```text
Settings → Pages
```

Then choose:

```text
Source: Deploy from a branch
Branch: main
Folder: /root
```

After a few minutes, GitHub Pages will give you a live URL.

---

## Roadmap

Possible future extensions:

- WebGL / GPU version
- export PNG snapshots
- parameter sweep mode
- side-by-side comparison mode
- automatic pattern classification
- Fourier spectrum panel
- anisotropic diffusion
- spatially varying feed and kill maps
- coupling to fluid flow
- Python notebook version for analysis

---

## Credits

Created by **Biswajit Jana** as part of an academic/scientific computing portfolio.

Website:

```text
https://biswajit1999.github.io/Biswajit_Jana.github.io/
```

---

## License

This project is released under the MIT License.

You may use, modify, and fork the code, but please credit the original author if you reuse the project publicly.
