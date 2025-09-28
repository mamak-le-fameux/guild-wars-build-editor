export default [
    {
        files: ['backend/**/*.ts'],
        parser: '@typescript-eslint/parser',
        parserOptions: { project: './backend/tsconfig.json' },
        plugins: ['@typescript-eslint', 'prettier'],
        extends: ['eslint:recommended', 'plugin:@typescript-eslint/recommended', 'plugin:prettier/recommended'],
        env: { node: true },
    },
    {
        files: ['frontend/**/*.ts', 'frontend/**/*.tsx'],
        parser: '@typescript-eslint/parser',
        parserOptions: { project: './frontend/tsconfig.json' },
        plugins: ['@typescript-eslint', 'prettier', 'react'],
        extends: ['eslint:recommended', 'plugin:@typescript-eslint/recommended', 'plugin:prettier/recommended', 'plugin:react/recommended'],
        env: { browser: true },
    },
];
