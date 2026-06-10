// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://mvpe-lab.github.io',
  // Old URL kept alive after the People -> Team rename
  redirects: {
    '/people/': '/team/',
  },
});
