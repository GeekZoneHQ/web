/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    /**
     * Stylesheet generation mode.
     *
     * Set mode to "jit" if you want to generate your styles on-demand as you author your templates;
     * Set mode to "aot" if you want to generate the stylesheet in advance and purge later (aka legacy mode).
     */
    mode: "aot",

    purge: {
        content: [
            /**
             * HTML. Paths to Django template files that will contain Tailwind CSS classes.
             */
            /*  Templates within theme app (e.g. base.html) */
            '../templates/**/*.html',

            /* Templates in other apps. Adjust the following line so that it matches
            * your project structure.
            */
            '../../memberships/templates/**/*.html',

            /**
             * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
             * patterns match your project structure.
             */
            /* JS 1: Ignore any JavaScript in node_modules folder. */
            '!../../**/node_modules',
            /* JS 2: Process all JavaScript files in the project. */
            '../../**/*.js',

            /**
             * Python: If you use Tailwind CSS classes in Python, uncomment the following line
             * and make sure the pattern below matches your project structure.
             */
            // '../../**/*.py'
        ],
        safelist: [
            'dark',
            'animate-fade-in',
            'animate-fade-out',
            ...(new Array(21)).fill('-translate-x-')
                .map((str, i) => str + (i * 4).toString()),
            /* keeping the following until 'jit' mode works with regular expressions */
            // /^animate-fade-/,
            // /^-translate-x-/,
        ],
    },
    darkMode: 'class', // can be 'media', 'class' or false [sic]
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
                impact: [
                    'Impact',
                    'Haettenschweiler',
                    'Franklin Gothic Bold',
                    'Charcoal',
                    'Helvetica Inserat',
                    'Bitstream Vera Sans Bold',
                    'Arial Black',
                    'sans serif',
                ],
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
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
