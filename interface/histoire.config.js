import { defineConfig } from 'histoire'
import { HstSvelte } from '@histoire/plugin-svelte'

export default defineConfig({
  plugins: [
    HstSvelte(),
  ],
  storyMatch: [
    'src/story/**/*.story.svelte',
    'src/lib/**/*.story.svelte',
    'src/routes/**/*.story.svelte',

  ],
  tree: {
    file: function ({ path }) {
      return path
        .replace(/^src\//, '')
        .replace(/^story\//, '')
        .replace('.story.svelte', '')
        .split('/')
        .map(function (r) {

          return r[0].toUpperCase() + r.slice(1)

        })


    }
  },
})