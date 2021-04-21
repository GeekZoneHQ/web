// This is a minimal config.
// If you need the full config, get it from here:
// https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
module.exports = {
    purge: [
        // Templates within theme app (e.g. base.html)
        '../templates/**/*.html',
        // Templates in other apps. Uncomment the following line if it matches
        // your project structure or change it to match.
        '../../memberships/templates/**/*.html',
    ],
    darkMode: 'class',
    theme: {
        extend: {
            animation: {
                'fade-in': 'fadeIn 0.5s',
                'fade-out': 'fadeOut 0.5s',
            },
            colors: {
                'red-true': '#ff0000',
                'yellow-true': '#ffff00',
            },
            fontFamily: {
                impact: ['Impact', 'Haettenschweiler', 'Franklin Gothic Bold', 'Charcoal', 'Helvetica Inserat', 'Bitstream Vera Sans Bold', 'Arial Black', 'sans serif'],
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                fadeOut: {
                    '0%': { opacity: '1' },
                    '100%': { opacity: '0' },
                }
            },
            maxWidth: {
                '2xs': '18rem',
            },
            scale: {
                flip: '-1',
            },
            spacing: {
                '-68': '-17rem',
                '-76': '-19rem',
            },
        },
    },
    variants: {
        extend: {
            boxShadow: ['active'],
            display: ['dark'],
            inset: ['active'],
            margin: ['last'],
            position: ['active'],
        }
    },
    plugins: [],
}
