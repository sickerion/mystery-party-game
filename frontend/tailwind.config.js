/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Dark mode colors (default)
        navy: '#1a1a2e',        // Fond principal dark
        darkNavy: '#16213e',    // Sections dark
        teal: '#0f3460',        // Accents dark

        // Light mode colors
        lightBg: '#f5f5f5',     // Fond principal light
        lightCard: '#ffffff',   // Cartes light
        lightBorder: '#e0e0e0', // Bordures light

        // Couleurs d'accentuation (identiques en dark/light)
        gold: '#d4af37',        // CTA, éléments importants
        crimson: '#8b0000',     // Alertes, mystère
        purple: '#9b59b6',      // Liens, hover

        // Couleurs neutres
        offWhite: '#e8e8e8',    // Texte principal dark mode
        lightGray: '#a8a8a8',   // Texte secondaire
        darkGray: '#2d2d2d',    // Cartes dark mode
        darkText: '#1a1a1a',    // Texte principal light mode

        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
