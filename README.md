# Retro Styled Enosh Portfolio
<img width="959" height="434" alt="image" src="https://github.com/user-attachments/assets/90303fd8-4220-429c-ad4b-09cf8c0b4853" />

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Project Structure](#project-structure)
4. [Database Models](#database-models)
5. [Views and URL Routing](#views-and-url-routing)
6. [Frontend Implementation](#frontend-implementation)
7. [Language System](#language-system)

---

## Overview

This is a small project with Django. A portfolio project website with django that depicts a retro style aesthetics. <br>
Here I feature the following to acheive the retro style website:
- Pixelated, CRT-style (90s TV and Monitors) interface.
- We have a navigation menu on the left
- Each Project added can be mapped to the roles on the navigation menu
- The Skills accured from each projects and work experiences are consolidated in the Skills library
- Provided Multilingual support (Not with Machine translation but with my translation)
- Managed with Database content instead of static rendering
- Used icons for most part
- A CRT container with scan lines using `repeating-linear-gradient`
- Also added a command line terminal output for skill consolidation (using js to updat console after page navigation)

---

## Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────┐
│              Django Application                  │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Profiles │  │ Projects│  │  Skills │      │
│  │   App    │  │   App   │  │   App   │      │
│  └──────────┘  └──────────┘  └──────────┘      │
│       │              │              │           │
│       └──────────────┼──────────────┘           │
│                      │                          │
│              ┌───────▼───────┐                 │
│              │   SQLite DB   │                 │
│              │  (Multilingual │                 │
│              │    Content)   │                 │
│              └───────────────┘                 │
│                                                 │
│  ┌──────────────────────────────────────┐     │
│  │         Templates Layer              │     │
│  │  base.html → home.html               │     │
│  └──────────────────────────────────────┘     │
│                                                 │
│  ┌──────────────────────────────────────┐     │
│  │      Static Files (CSS/JS)           │     │
│  │  retro.css + console.js              │     │
│  └──────────────────────────────────────┘     │
└─────────────────────────────────────────────────┘
```

### Key Design Decisions

1. **Database-Based Translations**: Instead of using Django's frameworks I translate internally to show my language skills. Also, this allows for easier content management through the admin interface.

2. **Language Selection**: Language preference is stored in the session and can be changed via URL parameters (`?lang=en`).

3. **Category-Based Navigation**: Content is organized by categories (About Me, C++ Developer, Python Developer, ML Engineer, Projects, CI/CD, Skills), with the console automatically updating to show relevant skills.

4. **Retro Aesthetic**: CSS implements CRT monitor effects, pixel fonts, and a dark color scheme to achieve the 90s retro look.

---

## Project Structure

```
portfolio/
├── portfolio/              
│   ├── settings.py       
│   ├── urls.py            
│   └── wsgi.py            
│
├── profiles/              
│   ├── models.py         
│   ├── views.py           
│   ├── admin.py           
│   ├── utils.py           
│   └── migrations/        
│
├── projects/              
│   ├── models.py          
│   ├── admin.py           
│   └── migrations/        
│
├── skills/                
│   ├── models.py          
│   ├── views.py           
│   ├── admin.py           
│   └── migrations/        
│
├── templates/             
│   ├── base.html         
│   ├── home.html         
│   └── profiles/
│       └── detail.html    
│
└── static/                
    ├── css/
    │   └── retro.css      
    └── js/
        └── console.js    
```

---

## Database Models

### Profile Model

Stores user profile information with multilingual support.

**Fields:**
- `slug` (SlugField): Unique identifier
- `linkedin_url` (URLField): LinkedIn profile URL
- `github_url` (URLField): GitHub profile URL
- `cv_file` (FileField): Resume/CV file upload
- `title_en`, `title_de`, `title_ta` (CharField): Profile title in each language
- `description_en`, `description_de`, `description_ta` (TextField): Full description

**Methods:**
- `get_title(language)`: Returns title in specified language
- `get_description(language)`: Returns description in specified language

### Model

Stores "Profile" content for each language.

**Fields:**
- `language` (CharField): Language code ('en', 'de', 'ta')
- `content` (TextField): About me content
- `order` (IntegerField): Display order

### Skill Model

Individual skills within a category.

**Fields:**
- `category` (ForeignKey): Links to SkillCategory
- `order` (IntegerField): Display order within category
- `name_en`, `name_de`, `name_ta` (CharField): Skill name in each language
- `description_en`, `description_de`, `description_ta` (TextField): Optional description

**Methods:**
- `get_name(language)`: Returns name in specified language
- `get_description(language)`: Returns description in specified language

### Project Model

Portfolio projects with multilingual descriptions.

**Fields:**
- `title_en`, `title_de`, `title_ta` (CharField): Project title
- `description_en`, `description_de`, `description_ta` (TextField): Project description
- `tech_stack_en`, `tech_stack_de`, `tech_stack_ta` (CharField): Technology stack
- `github_url` (URLField): GitHub repository URL
- `profiles` (ManyToManyField): Related profiles

**Methods:**
- `get_title(language)`: Returns title in specified language
- `get_description(language)`: Returns description in specified language
- `get_tech_stack(language)`: Returns tech stack in specified language

---

## Views and URL Routing

### Home View (`profiles/views.py`)

The main view that handles:
- Language detection and switching
- Category selection
- Contents based on selected category

**Key Logic:**
1. Checks for language parameter in URL (`?lang=en`)
2. Stores language preference in session
3. Retrieves current language from request (URL param → session → default 'en')
4. Determines selected category from URL (`?category=about-me`)
5. Fetches appropriate content based on category:
   - `profile`: profile content for current language
   - `projects`: All projects that are mapped to the profile
   - Skill category slug: Skills for that category
6. Renders `home.html` template with context

### Console API View (`skills/views.py`)

API endpoint that returns formatted skill output for a category.

**Endpoint:** `/api/console/<category_slug>/`

**Query Parameters:**
- `lang`: Language code (optional, defaults to 'en')

**Response Format:**
```json
{
    "output": "C:\\>cat skills_cpp.txt\n\n  • Skill 1\n  • Skill 2\n\nC:\\>",
    "category": "C++ Developer",
    "language": "en"
}
```

**Implementation:**
- Formats output to mimic DOS command prompt
- Uses language-specific fields to display skills
- Returns 404 if category doesn't exist

### URL Patterns (`portfolio/urls.py`)

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("api/console/<str:category_slug>/", console_output, name="console_output"),
    path("profiles/<slug:slug>/", profile_detail, name="profile"),
]
```

---

## Frontend Implementation

### Base Template (`templates/base.html`)

The base template provides the overall layout structure:

1. **Top Bar**
   - Left: CV download, LinkedIn, GitHub links
   - Right: Language switcher (EN/DE/TA)

2. **Side Navigation**
   - Profiles
   - Skill Categories (dynamically loaded)
   - Projects

3. **Main Content Area**
   - Displays content based on selected category
   - Rendered by `home.html` template

4. **Console Area**
   - Fixed bottom section
   - Displays skills in command-line format
   - Auto-updates when category changes

### Retro CSS (`static/css/retro.css`)

**Key Features:**

1. **Color Scheme:**
   - Dark backgrounds: `#0a0a0f`, `#1a1a2e`, `#16213e`
   - Text colors: `#00ff41` (green), `#ffb000` (amber), `#e0e0e0` (white)

2. **CRT Effects:**
   - Scanlines overlay using `::before` pseudo-element
   - Radial gradient overlay using `::after` pseudo-element
   - Box shadows for depth

3. **Pixel Fonts:**
   - Primary: 'Press Start 2P' (Google Fonts)
   - Fallback: 'Courier New', monospace

4. **Grid Background:**
   - Subtle grid pattern using CSS gradients

5. **Button Styling:**
   - Pixelated buttons with `outset`/`inset` borders
   - Hover effects with border style changes

### Console JavaScript (`static/js/console.js`)

Its needed because I wanted the console to be dynamic in the browser.

**Functionality:**

1. **Category Detection:**
   - Reads category from URL parameters
   - Defaults to 'about-me' if not specified

2. **Console Updates:**
   - Automatically fetches skills when category changes
   - Shows welcome message for non-skill categories
   - Typewriter effect for retro feel (50ms delay per line)

3. **API Integration:**
   - Calls `/api/console/<category>/` endpoint
   - Passes current language as query parameter
   - Handles errors gracefully

4. **Event Handling:**
   - Listens to navigation item clicks
   - Updates console after page navigation
   - Handles browser back/forward buttons

---

## Language System

### Language Configuration (`portfolio/settings.py`)

```python
LANGUAGES = [
    ('en', 'English'),
    ('de', 'Deutsch'),
    ('ta', 'தமிழ்'),
]
```


---


## Future Enhancements

Potential improvements:
- Implement search functionality
- Add blog/news section
- Make it Mobile friendly

---
