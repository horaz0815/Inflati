// Militärisches Design-Theme
export const COLORS = {
  // Hauptfarben - Militärisches Grün und Grau
  primary: '#3C5233',      // Olivgrün
  primaryDark: '#2C3E2F',  // Dunkel Olivgrün
  primaryLight: '#4A6340', // Hell Olivgrün

  // Sekundärfarben
  secondary: '#5C6B5C',    // Militärgrau-Grün
  secondaryDark: '#3D4A3D', // Dunkel Militärgrau
  secondaryLight: '#7A8A7A', // Hell Militärgrau

  // Akzentfarben
  accent: '#8B7355',       // Sandbraun
  accentLight: '#A68A6A',  // Hell Sandbraun
  warning: '#B8860B',      // Dunkelgold (für Warnungen)
  danger: '#8B0000',       // Dunkelrot (für Fehler)
  success: '#556B2F',      // Olivgrün-Dunkel (für Erfolg)

  // UI Farben
  background: '#1A1F1A',   // Sehr dunkles Grün (fast schwarz)
  surface: '#242B24',      // Dunkle Oberfläche
  surfaceLight: '#2E362E', // Etwas hellere Oberfläche

  // Text Farben
  text: '#E8E8E8',         // Helles Grau (Haupttext)
  textSecondary: '#B8C0B8', // Mittelgrau (Sekundärtext)
  textDisabled: '#6B736B',  // Dunkelgrau (Deaktiviert)

  // Border/Divider
  border: '#3D4A3D',       // Dunkle Grenze
  divider: '#2E362E',      // Trennlinie

  // Spezielle Farben
  white: '#FFFFFF',
  black: '#000000',
  overlay: 'rgba(0, 0, 0, 0.7)',
  overlayLight: 'rgba(0, 0, 0, 0.4)',
};

export const SIZES = {
  // Schriftgrößen
  h1: 32,
  h2: 28,
  h3: 24,
  h4: 20,
  h5: 18,
  h6: 16,
  body: 16,
  bodySmall: 14,
  caption: 12,

  // Abstände
  paddingSmall: 8,
  padding: 16,
  paddingLarge: 24,
  paddingXL: 32,

  // Border Radius
  radiusSmall: 4,
  radius: 8,
  radiusLarge: 12,
  radiusXL: 16,

  // Icon Größen
  iconSmall: 16,
  icon: 24,
  iconLarge: 32,
  iconXL: 48,
};

export const FONTS = {
  // Schriftstile
  h1: {
    fontSize: SIZES.h1,
    fontWeight: '700',
    color: COLORS.text,
    letterSpacing: 0.5,
  },
  h2: {
    fontSize: SIZES.h2,
    fontWeight: '700',
    color: COLORS.text,
    letterSpacing: 0.5,
  },
  h3: {
    fontSize: SIZES.h3,
    fontWeight: '600',
    color: COLORS.text,
    letterSpacing: 0.3,
  },
  h4: {
    fontSize: SIZES.h4,
    fontWeight: '600',
    color: COLORS.text,
  },
  body: {
    fontSize: SIZES.body,
    fontWeight: '400',
    color: COLORS.text,
    lineHeight: 24,
  },
  bodyBold: {
    fontSize: SIZES.body,
    fontWeight: '600',
    color: COLORS.text,
    lineHeight: 24,
  },
  caption: {
    fontSize: SIZES.caption,
    fontWeight: '400',
    color: COLORS.textSecondary,
  },
  captionBold: {
    fontSize: SIZES.caption,
    fontWeight: '600',
    color: COLORS.textSecondary,
  },
};

export const SHADOWS = {
  small: {
    shadowColor: COLORS.black,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 2,
  },
  medium: {
    shadowColor: COLORS.black,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.30,
    shadowRadius: 4.65,
    elevation: 4,
  },
  large: {
    shadowColor: COLORS.black,
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.37,
    shadowRadius: 7.49,
    elevation: 8,
  },
};

const theme = {
  COLORS,
  SIZES,
  FONTS,
  SHADOWS,
};

export default theme;
