// @ts-check

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
	// Netlify 배포 시에는 base 경로 불필요
	site: 'https://your-site-name.netlify.app', // Netlify 배포 후 실제 URL로 변경
	integrations: [mdx(), sitemap()],
});
