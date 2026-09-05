import { DarkTheme, DefaultTheme, type Theme } from 'expo-router';

// Walris V1 is light-only (see app.json userInterfaceStyle); the design system
// doesn't define a dark palette, so the "dark" entry mirrors "light" for now.
const light = {
  background: 'hsl(231 100% 98.6%)',
  foreground: 'hsl(212 62.7% 11.6%)',
  card: 'hsl(0 0% 100%)',
  cardForeground: 'hsl(212 62.7% 11.6%)',
  popover: 'hsl(0 0% 100%)',
  popoverForeground: 'hsl(212 62.7% 11.6%)',
  primary: 'hsl(0 0% 0%)',
  primaryForeground: 'hsl(0 0% 100%)',
  secondary: 'hsl(161 100% 21.2%)',
  secondaryForeground: 'hsl(0 0% 100%)',
  muted: 'hsl(219 100% 94.9%)',
  mutedForeground: 'hsl(232 5.5% 28.6%)',
  accent: 'hsl(218 100% 93.1%)',
  accentForeground: 'hsl(212 62.7% 11.6%)',
  destructive: 'hsl(0 75.5% 41.6%)',
  border: 'hsl(216 95.6% 91.2%)',
  input: 'hsl(216 95.6% 91.2%)',
  ring: 'hsl(0 0% 0%)',
  radius: '0.75rem',
  chart1: 'hsl(12 76% 61%)',
  chart2: 'hsl(173 58% 39%)',
  chart3: 'hsl(197 37% 24%)',
  chart4: 'hsl(43 74% 66%)',
  chart5: 'hsl(27 87% 67%)',
} as const;

export const THEME = {
  light,
  dark: light,
};

export const NAV_THEME: Record<'light' | 'dark', Theme> = {
  light: {
    ...DefaultTheme,
    colors: {
      background: THEME.light.background,
      border: THEME.light.border,
      card: THEME.light.card,
      notification: THEME.light.destructive,
      primary: THEME.light.primary,
      text: THEME.light.foreground,
    },
  },
  dark: {
    ...DarkTheme,
    colors: {
      background: THEME.dark.background,
      border: THEME.dark.border,
      card: THEME.dark.card,
      notification: THEME.dark.destructive,
      primary: THEME.dark.primary,
      text: THEME.dark.foreground,
    },
  },
};
