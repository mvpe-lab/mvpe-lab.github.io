import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Files starting with "_" (e.g. _TEMPLATE.md) are ignored and never published.

const news = defineCollection({
  loader: glob({ pattern: '[^_]*.md', base: './src/content/news' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    image: z.string().optional(),
  }),
});

const people = defineCollection({
  loader: glob({ pattern: '[^_]*.md', base: './src/content/people' }),
  schema: z.object({
    name: z.string(),
    role: z.enum([
      'Principal Investigator',
      'Postdoctoral Researcher',
      'PhD Student',
      'MSc Student',
      'Undergraduate Student',
      'Visiting Researcher',
      'Alumni',
    ]),
    photo: z.string().optional(),
    email: z.string().optional(),
    website: z.string().url().optional(),
    scholar: z.string().url().optional(),
    linkedin: z.string().url().optional(),
    start: z.string().optional(),
    // For alumni: degree earned and current position, e.g. "MSc 2027 — now at Tesla"
    note: z.string().optional(),
    order: z.number().default(99),
  }),
});

const research = defineCollection({
  loader: glob({ pattern: '[^_]*.md', base: './src/content/research' }),
  schema: z.object({
    title: z.string(),
    image: z.string().optional(),
    order: z.number().default(99),
  }),
});

export const collections = { news, people, research };
