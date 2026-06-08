import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: '9006PA2 Base',
      favicon: '/favicon.svg',
      sidebar: [
        {
          label: 'Overview',
          items: ['index', 'architecture', 'inference-pipe'],
        },
        {
          label: 'Student Setup',
          items: ['getting-started'],
        },
      ],
    }),
  ],
});
