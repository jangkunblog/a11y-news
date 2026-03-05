// @ts-check

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
	// Vercel 배포 시에는 base 경로 불필요
	site: 'https://a11y-news.vercel.app', // Vercel 배포 후 실제 URL로 변경
	integrations: [mdx(), sitemap()],
});
