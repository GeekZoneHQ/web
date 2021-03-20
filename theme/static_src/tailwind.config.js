// This is a minimal config.
// If you need the full config, get it from here:
// https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
module.exports = {
    purge: [
        // Templates within theme app (e.g. base.html)
        '../templates/**/*.html',
        // Templates in other apps. Uncomment the following line if it matches
        // your project structure or change it to match.
        '../../memberships/templates/**/*.html'
    ],
    darkMode: 'class',
    theme: {
        extend: {
            animation: {
                'fade-in': 'fadeIn 0.5s',
                'fade-out': 'fadeOut 0.5s'
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' }
                },
                fadeOut: {
                    '0%': { opacity: '1' },
                    '100%': { opacity: '0' }
                }
            },
            // transform: {
            //     'reflect-y': 'rotateY(180deg)'
            // }
        }
    },
    variants: {
        extend: {
            boxShadow: ['active'],
            inset: ['active'],
            margin: ['last'],
            position: ['active']
        }
    },
    plugins: []
}
