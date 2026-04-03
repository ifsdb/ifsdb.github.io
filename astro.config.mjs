import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

export default defineConfig({
  integrations: [sitemap()],
  site: 'https://ifsdb.github.io',
  server: { host: '127.0.0.1' },
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
  },
  vite: {
    define: {
      __IFSLIB_VERSION__: JSON.stringify('1.0.0'),
    },
  },
});
