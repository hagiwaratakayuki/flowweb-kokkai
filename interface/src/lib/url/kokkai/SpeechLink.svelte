<script>
  import BaseLink from "../BaseLink.svelte";
  import { getSpeechUrl } from "./speech.js";
  export let id;
  export let isNewWindow = true;
  let props;
</script>

<BaseLink url={getSpeechUrl(id)} {isNewWindow}>
  <slot />
</BaseLink>
