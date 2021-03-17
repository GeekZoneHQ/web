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
                'fade-in': 'fadeIn 1s linear',
                'fade-out': 'fadeIn 1s linear reverse'
            },
            keyframes: {
                fadeIn: {
                    '0%': { visibility: 'hidden' },
                    '100%': { visibility: 'visible' }
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
