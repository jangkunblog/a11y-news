// @ts-check

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
	site: 'https://yourusername.github.io',
	// 로컬 개발시에는 base를 사용하지 않고, GitHub Pages 배포시에만 사용
	// GitHub에 배포할 때는 아래 주석을 해제하세요
	// base: '/kakao-a11y-news',
	integrations: [mdx(), sitemap()],
});
