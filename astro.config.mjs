// @ts-check

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
	site: 'https://jangkunblog.github.io',
	// GitHub Pages 배포 시 주석 해제
	// base: '/a11y-news',
	integrations: [mdx(), sitemap()],
});
