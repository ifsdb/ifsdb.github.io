import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const ifs = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/ifs' }),
  schema: z.object({
    name: z.string(),
    description: z.string(),
    cardDescription: z.string().optional(),
    dimension: z.string().optional(),
    transforms: z.number().int().positive(),
    tags: z.array(z.string()).default([]),
    aifs: z.string(),
    references: z.array(z.object({
      text: z.string(),
      url: z.string().url().optional(),
    })).optional(),
  }),
});

export const collections = { ifs };
