import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

import mdx from '@astrojs/mdx';

export default defineConfig({
  integrations: [sitemap(), mdx({
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
  })],
  site: 'https://ifsdb.github.io',
  server: { host: '127.0.0.1' },
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
  },
  vite: {
    define: {
      __IFSLIB_VERSION__: JSON.stringify('4.1.3'),
    },
  },
});
