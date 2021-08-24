module.exports = {
  future: {
    // removeDeprecatedGapUtilities: true,
    // purgeLayersByDefault: true,
  },
  mode: 'jit',
  purge: [
    './src/**/*.html',
    './src/**/*.vue',
    './src/**/*.jsx',
  ],
  theme: {
    extend: {
      boxShadow: {
        blue: '0 4px 14px 0 rgba(19, 51, 81, 0.39)',
      },
    },
  },
  variants: {
    extend: {
      opacity: ['disabled', 'group-hover'],
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ]
}
