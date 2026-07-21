# Sarthak Patani — Portfolio Website

A multi-page, animated portfolio built with **plain HTML + CSS only — zero JavaScript**, no build step, no dependencies. Every interaction (mobile menu, tabs, filters, reveals, typing effect, orbiting tech stack) runs on pure CSS (keyframe animations, the `:checked` radio/checkbox trick, and — where supported — scroll-driven animations). Just open `index.html` in a browser, or host the whole folder anywhere static (GitHub Pages, Netlify, Vercel, etc.).

## Pages
- `index.html` — Home / hero, with an ambient auto-blending "design ↔ circuit" visual and a CSS crossfade typing animation
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
- All interactivity is CSS-only now: reveal animations and the loader live in `css/base.css`; the typing effect, bridge-scene blend, tabs, filters, and orbit are in `css/components.css`. Tabs/filters use hidden `<input type="radio">` elements + the `:checked` selector — search each `.html` file for `class="tab-radio"` to find them.
- Text content: directly in each `.html` file — no templating, just edit and save

## Notes
- **No JavaScript anywhere in this build.** The mobile nav menu, skill tabs, and project filters use the CSS `:checked` radio/checkbox technique instead of click handlers. Scroll-position effects (the top progress bar) use CSS scroll-driven animations (`animation-timeline: scroll(root)`), which is supported in current Chrome/Edge/Safari and degrades gracefully (simply stays hidden) elsewhere — it's a bonus effect, not something the page depends on.
- The contact form now submits via `mailto:` (`action="mailto:sarthak.patani@example.com"`), which opens the visitor's email app with the message pre-filled — there's no way to submit silently without a backend or JS, so this is the plain-HTML equivalent. Swap in a real backend or a service like Formspree if you want in-page delivery back.
- The animated stat counters and skill-bar "fill" are done via CSS: skill bars use the `@keyframes` implicit-from trick (`from { width: 0% }`, with the target width set inline per bar) so they always fill in on load; stat numbers use a staggered fade/scale-in instead of counting up, since counting requires either JS or fragile CSS `@property` tricks.
- Fully responsive down to small mobile widths.
- Respects `prefers-reduced-motion` for accessibility.
