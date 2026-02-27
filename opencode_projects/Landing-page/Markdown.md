
# 🚀 Penpot Design-to-Code System (2026 Edition)

מדריך זה מציג ארכיטקטורה סקיילבילית לבניית מערכת דפי נחיתה באמצעות Penpot, עם דגש על אוטומציה ו-Code-First approach. המטרה: **Design once, deploy everywhere.**

## ⏱️ הערכת זמנים ו-ROI

ההשקעה הראשונית כבדה, אך היא מחזירה את עצמה אקספוננציאלית החל מהדף השני.

| שלב | משימה | זמן מוערך | ערך (Value) |
| :--- | :--- | :--- | :--- |
| **Day 1** | **System Setup** | 4–8 שעות | תשתית חד-פעמית. לא חוזרים לזה. |
| **Day 2** | **Base Templates** | 2–4 שעות | שלד מוכן לשימוש (Skeleton). |
| **Day 2.5** | **First Landing** | 3–6 שעות | דף פרודקשן ראשון מלא. |
| **Day 3+** | **Scaling** | **45-90 דק'** | ייצור דפים חדשים בשיטת "הרכבה". |

***

## 🏗️ שלב 0: הקמת סביבה (DevOps)

לפני שמתחילים לעצב, מכינים את הקרקע לאוטומציה.

### 1. Penpot Local Instance
ודא שאתה רץ על הגרסה היציבה האחרונה (v2.x+).
```bash
# בתיקיית ה-Docker שלך
git clone https://github.com/penpot/penpot.git
cd penpot/docker
docker compose up -d
```

### 2. Export Tooling
התקנת הכלים לייצוא אוטומטי של Tokens לקוד.
```bash
npm install -g penpot-export
# או בתוך הפרויקט
npm install --save-dev penpot-export
```

***

## 🧱 שלב 1: Design System & Tokens (הבסיס)
**זמן:** 4–8 שעות (חד פעמי)

במקום לעצב "דפים", אנחנו מעצבים "ערכים" ו"לוגיקה".

### 1.1 Global Tokens (Primitive Values)
הגדרת ערכים "טיפשים" שלא משתנים לפי Theme.
*   **Colors:** `blue-500 (#3B82F6)`, `gray-900 (#111827)`, `white (#FFFFFF)`.
*   **Spacing:** `spacing-4 (1rem)`, `spacing-8 (2rem)`.
*   **Typography:** `font-sans (Inter)`, `text-xl (1.25rem)`.

### 1.2 Semantic Tokens (The Magic Layer) 🌟
יצירת אליאסים שמצביעים על ה-Global Tokens. **זה המפתח ל-Dark Mode.**

| Semantic Name | Light Mode Value | Dark Mode Value | שימוש |
| :--- | :--- | :--- | :--- |
| `bg-primary` | `{white}` | `{gray-900}` | רקע ראשי של הדף |
| `text-primary` | `{gray-900}` | `{white}` | טקסט ראשי |
| `brand-main` | `{blue-600}` | `{blue-400}` | כפתורים ו-CTAs |
| `border-subtle` | `{gray-200}` | `{gray-800}` | קווים מפרידים |

> **Best Practice:** ב-Penpot 2.0+, השתמש בפיצ'ר ה-**Themes** המובנה כדי למפות את הערכים האלו. אל תשכפל קבצים.

### 1.3 Atomic Components (Wrappers)
יצירת קומפוננטות בסיסיות שמשתמשות *רק* ב-Semantic Tokens.
*   **Button:** משתמש ב-`brand-main` לרקע, `text-inverse` לטקסט.
*   **Input:** משתמש ב-`border-subtle`, `bg-surface`.
*   **Card:** משתמש ב-`bg-surface`, `shadow-md`.

***

## 🧩 שלב 2: Blocks & Templates Strategy
**זמן:** 2–4 שעות

בניית "לגו" שמאפשר הרכבה מהירה.

### 2.1 Section Blocks (Boards)
כל בלוק הוא Board נפרד בתוך ספריית ה-Blocks, עם Auto Layout (Flex/Grid).
1.  **Hero Block:** (H1 + Subtitle + 2 CTAs + Image Placeholder).
2.  **Features Grid:** (Grid של 3 Cards).
3.  **Pricing Table:** (Toggle חודשי/שנתי).
4.  **Footer:** (Links + Socials).

### 2.2 The Master Template
יצירת דף (Page) שמחבר את הבלוקים האלו ל-Layout שלם.
*   **מבנה:** Navbar -> Hero -> Social Proof -> Features -> CTA -> Footer.
*   **Constraint:** הכל מוגדר עם Responsive Constraints (Left/Right, Stretch) כדי שיתאים למובייל/דסקטופ אוטומטית.

***

## 🌐 שלב 3: Production Pipeline (Design-to-Code)
**זמן:** 3–6 שעות (Setup ראשוני + דף ראשון)

כאן אנחנו הופכים את Penpot ל-Single Source of Truth של הקוד.

### 3.1 Penpot Configuration
צור קובץ `penpot-export.config.js` בשורש הפרויקט (Astro/Next.js):

```javascript
module.exports = {
  accessToken: process.env.PENPOT_ACCESS_TOKEN,
  files: [
    {
      fileId: "YOUR_DESIGN_SYSTEM_FILE_ID",
      output: "src/styles",
      format: "css/variables", // מייצר variables.css
      options: {
        prefix: "theme-", // התוצאה: --theme-bg-primary
      }
    }
  ]
};
```

### 3.2 Tailwind Integration
הגדר את `tailwind.config.mjs` לקרוא את המשתנים שנוצרו אוטומטית:

```javascript
export default {
  theme: {
    extend: {
      colors: {
        // מיפוי דינמי למשתני ה-CSS של Penpot
        primary: "var(--theme-bg-primary)",
        surface: "var(--theme-bg-surface)",
        brand: "var(--theme-brand-main)",
      },
      // ... typography and spacing mappings
    }
  }
}
```

### 3.3 Automation Script (`package.json`)
```json
"scripts": {
  "sync:design": "penpot-export && echo '✅ Design Tokens Updated'",
  "dev": "npm run sync:design && astro dev"
}
```

***

## ⚡ שלב 4: Scaling (The 45-Minute Workflow)
**זמן:** 45–90 דקות לדף

איך מייצרים דף חדש ביום השלישי?

1.  **Duplicate:** משכפלים את ה-`Master Template` ב-Penpot.
2.  **Content:** מחליפים טקסטים ותמונות (דרך Data tab או ידנית).
3.  **Overrides:** משנים `Visible` לבלוקים שלא צריך (למשל, מסתירים Pricing).
4.  **Visuals:** מוסיפים SVG/Illustrations ספציפיים לדף הזה.
5.  **Export:** אם שיניתם Tokens או הוספתם צבעים, מריצים `npm run sync:design`.
6.  **Code:** מעתיקים את ה-Structure (או משתמשים ב-Components מוכנים ב-React/Astro שתואמים לבלוקים ב-Penpot).

***

## ⚠️ נקודות קריטיות ל-Developer
1.  **Sudo & Permissions:** ודא שמשתמש ה-Docker שלך יכול לכתוב לתיקיית ה-Assets המקומית כדי שהתמונות יישמרו.
2.  **Version Control:** שמור את קבצי ה-JSON/CSS שנוצרים מ-Penpot ב-Git. זה התיעוד של ה-System שלך ברגע נתון.
3.  **Naming Conventions:** השמות ב-Penpot **חייבים** להיות באנגלית וללא רווחים (kebab-case) כדי שיתאימו ל-CSS Variables (למשל: `hero-section` ולא `Hero Section`).
