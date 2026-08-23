import type { TextStyle } from 'react-native';

export const displayLg: TextStyle = {
  fontFamily: 'LibreCaslonText_700Bold',
  fontSize: 48,
  fontWeight: '700',
  lineHeight: 56,
  letterSpacing: -0.96,
};

export const displayLgMobile: TextStyle = {
  fontFamily: 'LibreCaslonText_700Bold',
  fontSize: 36,
  fontWeight: '700',
  lineHeight: 42,
  letterSpacing: -0.72,
};

// docs/04 §5.1 specifies weight 600, but Libre Caslon Text only ships 400/700 —
// loads the 700 Bold file (closer to 600 than Regular) while keeping fontWeight
// at the spec's declared 600 for metadata purposes.
export const headlineMd: TextStyle = {
  fontFamily: 'LibreCaslonText_700Bold',
  fontSize: 32,
  fontWeight: '600',
  lineHeight: 40,
  letterSpacing: 0,
};

export const headlineSm: TextStyle = {
  fontFamily: 'LibreCaslonText_700Bold',
  fontSize: 24,
  fontWeight: '600',
  lineHeight: 32,
  letterSpacing: 0,
};

export const bodyLg: TextStyle = {
  fontFamily: 'Inter_400Regular',
  fontSize: 18,
  fontWeight: '400',
  lineHeight: 28,
  letterSpacing: 0,
};

export const bodyMd: TextStyle = {
  fontFamily: 'Inter_400Regular',
  fontSize: 16,
  fontWeight: '400',
  lineHeight: 24,
  letterSpacing: 0,
};

export const caption: TextStyle = {
  fontFamily: 'Inter_500Medium',
  fontSize: 12,
  fontWeight: '500',
  lineHeight: 16,
  letterSpacing: 0,
};

export const dataLabel: TextStyle = {
  fontFamily: 'JetBrainsMono_500Medium',
  fontSize: 14,
  fontWeight: '500',
  lineHeight: 20,
  letterSpacing: 0.28,
};

export const typography = {
  displayLg,
  displayLgMobile,
  headlineMd,
  headlineSm,
  bodyLg,
  bodyMd,
  caption,
  dataLabel,
} satisfies Record<string, TextStyle>;
