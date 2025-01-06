<script>
  import BaseLink from "../BaseLink.svelte";
  import { getSpeechUrl } from "./speech.js";
  export let id;
  export let newWindow = true;
  let props;
  $: {
    if (newWindow == true) {
      props = { target: "_brank" };
    }
  }
</script>

<BaseLink href={getSpeechUrl(id)} {...props}>
  <slot />
</BaseLink>
