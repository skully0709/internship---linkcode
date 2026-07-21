# Sarthak Patani — Portfolio Website

A multi-page, animated portfolio built with plain HTML/CSS/JS — no build step, no dependencies. Just open `index.html` in a browser, or host the whole folder anywhere static (GitHub Pages, Netlify, Vercel, etc.).

## Pages
- `index.html` — Home / hero, with a cursor-reactive "design ↔ circuit" visual and typing animation
- `about.html` — Bio, education, working philosophy, contact form
- `projects.html` — Filterable project grid (Design / Technical / Game Dev / Research / Web)
- `skills.html` — Tabbed skill bars + hex badges across Design, Engineering, Research
- `achievements.html` — Timeline of academic and competition wins
- `certificates.html` — Certificate gallery
- `contact.html` — Contact form + interactive orbiting tech-stack sphere

## Adding your resume

Drop your resume PDF into the `resume/` folder and name it exactly:

    resume/Sarthak-Patani-Resume.pdf

That one file powers every resume link on the site — no HTML edits needed:
- **Nav bar** — a "Resume" link on every page (opens the PDF in a new tab)
- **Homepage hero** — a "Download Resume" button
- **About page** — a "Download Resume" button under the intro
- **Contact page** — a resume card with separate "View PDF" and "Download" links

Each spot is flagged in its `.html` file with an HTML comment
(`<!-- RESUME LINK -->` / `<!-- RESUME BUTTON -->` / `<!-- RESUME CARD -->`)
so they're easy to find with a search if you ever want to move, restyle,
or rename it. If you use a different filename, update those href/download
attributes to match.

Because the PDF lives at a fixed path on the site itself (rather than
behind a Google Drive/Dropbox login), once this is hosted anywhere,
`yoursite.com/resume/Sarthak-Patani-Resume.pdf` is a permanent, directly
shareable link — paste it into LinkedIn, an email, or a job application,
and it always opens the current file. Re-uploading a new PDF with the
same filename replaces it in place, no link updates needed anywhere.

## Adding your real photos & images

I couldn't pull images directly from your LinkedIn or Instagram — both block automated access. Instead, every image slot has a **placeholder with the exact filename it expects**, so the site works immediately and upgrades automatically once you drop files in.

Download your images manually (right-click → save on LinkedIn/Instagram, a few seconds each), then place them in the `img/` folder using these exact names:

| Filename | Where it's used | Suggested source |
|---|---|---|
| `img/headshot.jpg` | About page photo | LinkedIn profile photo or a clean headshot |
| `img/project-maid-app.jpg` | Maid-booking app case study | Figma export / screenshot |
| `img/project-assembly.jpg` | Assembly & UDP project | Code screenshot or terminal output |
| `img/project-platformer.jpg` | Platformer game | Gameplay screenshot |
| `img/project-research.jpg` | Decentralization research | Report cover or infographic |
| `img/project-bookstore.jpg` | Bookstore website | Site screenshot |
| `img/project-atm.jpg` | ATM simulator | Console screenshot |
| `img/project-tenure.jpg` | Tenure calculator | Console screenshot |
| `img/project-library.jpg` | Library management system | UI/DB screenshot |
| `img/project-chatbot.jpg` | Quantum AI chatbot UI | Figma export |
| `img/project-sbi.jpg` | SBI gamification project | Figma export / game screenshot |

That's it — no code changes needed. The `onerror` fallback in each `<img>` tag automatically swaps back to a styled placeholder if a file is missing, so nothing ever breaks.

### From Instagram (@sarthakpatani07)
Open the post/photo on desktop → right-click the image → "Save image as…" → rename to match the table above and drop into `img/`.

### From LinkedIn
Open your profile → click your profile photo → "..." menu or the download icon (if enabled) → save → rename to `headshot.jpg`.

## Customizing content
- Colors, fonts, spacing: `css/base.css` (`:root` variables at the top)
- Component styles (cards, timeline, orbit, form): `css/components.css`
- All interactivity (typing effect, scroll reveal, tabs, filters, orbit): `js/main.js`
- Text content: directly in each `.html` file — no templating, just edit and save

## Notes
- The contact form is front-end only (shows a success message on submit) — wire it to a real backend or a service like Formspree/EmailJS if you want actual emails delivered.
- Fully responsive down to small mobile widths.
- Respects `prefers-reduced-motion` for accessibility.
