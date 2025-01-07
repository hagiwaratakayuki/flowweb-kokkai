<script>
  import BaseLink from "../BaseLink.svelte";
  import { getSpeakerUrl } from "./speaker";

  export let id;
  export let isNewWindow = false;
</script>

<BaseLink {isNewWindow} url={getSpeakerUrl(id)}><slot /></BaseLink>
